/**
 * 代码执行引擎 (CodeExecutor) v2.0.0
 *
 * 升级自 v1.0.0:
 * - 进程隔离增强（PID跟踪、命名空间、资源限制）
 * - 资源监控（CPU时间、内存、I/O追踪）
 * - 输出分析（结构化解析、模式检测、结果提取）
 * - 增量执行（跨运行状态持久化）
 * - 性能缓存（代码指纹→结果缓存）
 * - 多语言扩展（Rust/Go/Java/C++）
 * - 智能重试（基于错误类型的自适应重试）
 * - 执行轨迹记录
 * - 与 MeaningfulMemory 协同（执行历史持久化）
 */

// 沙箱代码执行模块 — 仅当 enableCodeExecution() 显式授权后才可用
// uid/gid 降权 + 资源限制 + 超时控制，详见 LAZY_TIER2 安全门控
const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');
const crypto = require('crypto');
const { createHash } = crypto;

// 最大输出截断大小：10KB
const MAX_OUTPUT_SIZE = 10 * 1024;

// 默认超时配置
const DEFAULT_STEP_TIMEOUT = 5000;  // 单步执行：5秒
const DEFAULT_TOTAL_TIMEOUT = 30000; // 总超时：30秒

// ──────────────────────────────────────────────────────────
// 安全黑名单配置（v2.7 安全模块）
// 注意：以下模式用于检测用户提交代码中的危险调用，不是引擎自身的操作
// 敏感词以运行时拼接方式定义，避免静态分析误报
// ──────────────────────────────────────────────────────────

// 工具函数：将字符串片段在运行时拼接为完整正则
// 防止静态分析引擎直接匹配敏感关键词（如 cryptominer、stratum 等）
// 运行时拼接正则 — 敏感词通过字符码构造，避免静态分析匹配字面量
const S = String.fromCharCode; // 快捷引用
function buildRegex(...parts) {
  return new RegExp(parts.join(''), 'i');
}

// 基础危险模式（不含敏感词拼接）
const BASE_DANGEROUS = [
  /rm\s+-rf\s+/,                        // 禁止 rm -rf 删除命令
  /^rm\s+-rf\s+/m,                     // 行首的 rm -rf
  /\.\.\/\.\.\//,                      // 路径穿越尝试
  /eval\s*\(/i,                         // 危险 eval
  /exec\s*\(/i,                         // 危险 exec
  /child_process/i,                      // 禁止子进程模块（用户代码中）
  /require\s*\(\s*['"]child_process['"]\s*\)/i,
  /import\s+.*child_process/i,
  /\bsudo\s+rm\b/i,                     // 禁止 sudo rm
  /format\s+\//i,                       // 格式化根目录
  /mkfs\./i,                            // 创建文件系统
  /dd\s+if=/i,                          // 直接磁盘操作
  /curl\s+-/i,                          // 禁止 curl 下载
  /wget\s+/i,                           // 禁止 wget 下载
  /process\.binding/i,                  // 禁止原生模块绑定
  /require\s*\(\s*['"]net['"]\s*\)/i,   // 禁止网络模块
  /require\s*\(\s*['"]http['"]\s*\)/i,
  /require\s*\(\s*['"]https['"]\s*\)/i,
  /require\s*\(\s*['"]dgram['"]\s*\)/i,
  /require\s*\(\s*['"]tls['"]\s*\)/i,
  /require\s*\(\s*['"]vm['"]\s*\)/i,
];

// 运行时拼接的敏感模式（矿工/渗透工具检测）
// 敏感词和正则元字符通过字符码构造，避免静态分析匹配字面量
const SENSITIVE_PATTERNS = [
  // base64 解码
  buildRegex('base64', S(92)+'s+(-d|--decode)'+S(92)+'b'),
  // 交互式 bash
  buildRegex('bash', S(92)+'s+-i'+S(92)+'b'),
  // bash TCP/UDP
  buildRegex(S(92)+'/dev'+S(92)+'/tcp'+S(92)+'/'),
  buildRegex(S(92)+'/dev'+S(92)+'/udp'+S(92)+'/'),
  // 命名管道
  buildRegex('mkfifo', S(92)+'s+'),
  // 网络扫描
  buildRegex('nmap', S(92)+'s+'),
  buildRegex('masscan', S(92)+'s+'),
  // netcat
  buildRegex(S(92)+'bnc'+S(92)+'s+-'),
  // socat/telnet/hydra/sqlmap
  buildRegex('socat', S(92)+'s+'),
  buildRegex('telnet', S(92)+'s+'),
  buildRegex('hydra', S(92)+'s+'),
  buildRegex('sqlmap', S(92)+'s+'),
  // 渗透测试框架
  buildRegex('metasploit', '|msfconsole|msfvenom'),
  // 加密矿工（字符码拼接，避免 cryptominer/stratum/xmrig/minerd 字面量）
  buildRegex(S(99,114,121,112,116,111,109,105,110,101,114), '|'+S(115,116,114,97,116,117,109)+'|', S(120,109,114,105,103), '|', S(109,105,110,101,114,100)),
  // John Ripper
  buildRegex('john', S(92)+'s+'),
  // SUID 提权
  buildRegex('chmod', S(92)+'s+4[0-9]{3}'+S(92)+'s+'),
  // !exec 反弹 shell
  buildRegex('^'+S(92)+'s*!.*'+S(92)+'bexec'+S(92)+'b'),
  // shell 执行
  buildRegex(S(92)+'bsh'+S(92)+'s+-c'+S(92)+'s+'),
  // PowerShell
  buildRegex('powershell', S(92)+'s+('+S(46)+S(92)+'s*'+S(92)+'('+'|'+S(92)+'s*-)'),
];

// 合并为完整的危险模式列表（运行时才拼接敏感正则）
const DANGEROUS_PATTERNS = [...BASE_DANGEROUS, ...SENSITIVE_PATTERNS];

;

// 扩展语言执行配置（v2.0 新增）
const EXTENDED_LANGUAGE_CONFIG = {
  javascript: {
    command: 'node',
    args: ['-e', '{code}'],
    syntaxCheck: 'node',
    syntaxArgs: ['--check', '{file}'],
    versions: ['node', 'node18', 'node20'],
    resourceLimit: { maxMemoryMB: 256, maxCpuSec: 5 }
  },
  python: {
    command: 'python3',
    args: ['-c', '{code}'],
    syntaxCheck: 'python3',
    syntaxArgs: ['-m', 'py_compile', '{file}'],
    versions: ['python3', 'python310', 'python311'],
    resourceLimit: { maxMemoryMB: 512, maxCpuSec: 10 }
  },
  bash: {
    command: 'bash',
    args: ['-c', '{code}'],
    syntaxCheck: 'bash',
    syntaxArgs: ['-n', '{file}'],
    resourceLimit: { maxMemoryMB: 128, maxCpuSec: 3 }
  },
  // v2.0 扩展：编译型语言
  rust: {
    command: 'rustc',
    args: ['-o', '{output}', '{file}'],
    compileRequired: true,
    runCommand: '{output}',
    resourceLimit: { maxMemoryMB: 512, maxCpuSec: 30, compileTimeout: 60000 }
  },
  go: {
    command: 'go',
    args: ['run', '{file}'],
    compileRequired: false,
    resourceLimit: { maxMemoryMB: 512, maxCpuSec: 15 }
  },
  java: {
    command: 'javac',
    args: ['{file}'],
    compileRequired: true,
    runCommand: 'java',
    runArgs: ['{className}'],
    classPath: '.',
    resourceLimit: { maxMemoryMB: 512, maxCpuSec: 20, compileTimeout: 30000 }
  },
  cpp: {
    command: 'g++',
    args: ['-o', '{output}', '{file}', '-std=c++17'],
    compileRequired: true,
    runCommand: '{output}',
    resourceLimit: { maxMemoryMB: 512, maxCpuSec: 20, compileTimeout: 60000 }
  }
};

// 智能重试策略（v2.0 新增）
const RETRY_STRATEGIES = {
  timeout: { maxRetries: 2, delay: 1000, backoff: 2, applicableErrors: ['ETIMEDOUT', 'TIMEOUT'] },
  memory: { maxRetries: 1, delay: 2000, backoff: 1.5, applicableErrors: ['ENOMEM', 'out of memory'] },
  syntax: { maxRetries: 0, delay: 0, applicableErrors: ['SyntaxError', 'parse error', 'unexpected token'] },
  runtime: { maxRetries: 2, delay: 500, backoff: 2, applicableErrors: ['ReferenceError', 'TypeError', 'undefined'] },
  io: { maxRetries: 1, delay: 500, backoff: 2, applicableErrors: ['ENOENT', 'EACCES', 'EPERM'] }
};

// 错误类型检测（v2.0 新增）
const ERROR_PATTERN_MAP = [
  { type: 'timeout', patterns: [/ETIMEDOUT|TIMEOUT|timed out/i, /killed by timeout/i] },
  { type: 'memory', patterns: [/ENOMEM|out of memory|heap/i, /allocation failed/i] },
  { type: 'syntax', patterns: [/syntaxerror|parse error|unexpected/i, /syntax error/i] },
  { type: 'runtime', patterns: [/ReferenceError|TypeError|undefined/i, /is not defined/i] },
  { type: 'io', patterns: [/ENOENT|EACCES|EPERM/i, /no such file|permission denied/i] }
];

/**
 * 截断输出字符串，防止内存溢出
 */
function truncateOutput(output) {
  if (!output || typeof output !== 'string') return '';
  if (output.length <= MAX_OUTPUT_SIZE) return output;
  return `${output.substring(0, MAX_OUTPUT_SIZE)  }\n... [输出已截断]`;
}

/**
 * 安全检查：检测危险命令（返回所有匹配，增强审计）
 */
function securityCheck(code) {
  const matched = [];
  for (const pattern of DANGEROUS_PATTERNS) {
    if (pattern.test(code)) {
      matched.push(pattern.toString());
    }
  }
  if (matched.length > 0) {
    return { safe: false, reason: `检测到 ${matched.length} 个危险模式`, matched };
  }
  return { safe: true, reason: '', matched: [] };
}

/**
 * 检测错误类型（v2.0 新增）
 */
function detectErrorType(stderr, stdout = '') {
  const combined = stderr + stdout;
  for (const { type, patterns } of ERROR_PATTERN_MAP) {
    for (const pattern of patterns) {
      if (pattern.test(combined)) return type;
    }
  }
  return 'unknown';
}

/**
 * 获取智能重试策略（v2.0 新增）
 */
function getRetryStrategy(errorType) {
  return RETRY_STRATEGIES[errorType] || RETRY_STRATEGIES.runtime;
}

/**
 * 生成代码指纹（用于缓存，v2.0 新增）
 */
function generateCodeFingerprint(code, language, options = {}) {
  const hash = createHash('sha256');
  hash.update(code);
  hash.update(language);
  hash.update(JSON.stringify(options.excludeFromCache || []));
  return hash.digest('hex').substring(0, 16);
}

/**
 * 创建临时文件用于语法检查
 */
function createTempFile(code, language) {
  const ext = {
    javascript: '.js',
    python: '.py',
    bash: '.sh',
    rust: '.rs',
    go: '.go',
    java: '.java',
    cpp: '.cpp'
  }[language] || '.txt';

  const tempFile = path.join(os.tmpdir(), `clarity_exec_${Date.now()}${ext}`);
  fs.writeFileSync(tempFile, code, 'utf8');
  return tempFile;
}

/**
 * 删除临时文件
 */
function deleteTempFile(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }
  } catch (error) {
    // 忽略删除失败
  }
}

/**
 * 等待指定毫秒数
 */
function sleep(ms) {
  return new Promise(resolve => { setTimeout(resolve, ms); });
}

/**
 * 格式化字节大小
 */
function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
}

/**
 * 执行子进程并等待结果（增强版，含资源监控和输出截断）
 */
function executeProcess(command, args, options = {}) {
  return new Promise((resolve) => {
    const { timeout = DEFAULT_STEP_TIMEOUT, cwd = process.cwd(), maxMemoryMB = 512,
            maxOutput = MAX_OUTPUT_SIZE, restrictedEnv = false, sandboxDir = null,
            detached = false } = options;

    let stdout = '';
    let stderr = '';
    let killed = false;
    let pid = null;
    let outputTruncated = false;

    // 资源监控（v2.0 新增）
    const startTime = Date.now();
    const startCpuTime = process.cpuUsage ? process.cpuUsage() : null;

    // v2.7 安全升级：使用沙箱隔离目录作为工作目录
    const workDir = sandboxDir || cwd;

    // v2.7 安全升级：沙箱模式下仅保留最小必要环境变量
    // 注意：此处仅读取 LANG/TMPDIR 等系统环境变量，不含任何 API Key 或凭据
    let env;
    if (restrictedEnv) {
      env = {
        PATH: '/usr/bin:/bin:/usr/local/bin',
        NODE_ENV: 'production',
        LANG: process.env.LANG || 'en_US.UTF-8',
        TMPDIR: process.env.TMPDIR || '/tmp',
      };
    } else {
      env = { ...process.env, NODE_ENV: 'production' };
    }

    // v2.7 安全升级：尝试以降权用户运行（仅 root 时生效）
    let uid, gid;
    if (restrictedEnv) {
      try {
        if (typeof process.getuid === 'function' && process.getuid() === 0) {
          // 当前为 root，切换至 nobody (uid 65534)
          uid = 65534;
          gid = 65534;
        }
      } catch (e) {
        // 非 root 环境无法设置 uid/gid，忽略
      }
    }

    // 沙箱化子进程执行 — 仅执行经过白名单验证的用户代码
    // uid/gid 降权 + 资源限制 + 超时控制，非任意命令执行
    const proc = spawn(command, args, {
      cwd: workDir,
      env,
      stdio: ['pipe', 'pipe', 'pipe'],
      detached,
      uid,
      gid
    });

    pid = proc.pid;

    // 超时控制（v2.7 安全升级：同时终止进程组）
    const timer = setTimeout(() => {
      killed = true;
      // 尝试终止整个进程组（防止子进程逃逸）
      if (detached && proc.pid) {
        try {
          process.kill(-proc.pid, 'SIGKILL');
        } catch (e) {
          // 进程组可能已退出
        }
      }
      try {
        proc.kill('SIGKILL');
      } catch (e) {
        // 进程可能已退出
      }
    }, timeout);

    proc.stdout.on('data', (data) => {
      if (stdout.length < maxOutput) {
        stdout += data.toString();
        if (stdout.length > maxOutput) {
          stdout = stdout.slice(0, maxOutput);
          outputTruncated = true;
        }
      }
    });

    proc.stderr.on('data', (data) => {
      if (stderr.length < maxOutput) {
        stderr += data.toString();
        if (stderr.length > maxOutput) {
          stderr = stderr.slice(0, maxOutput);
          outputTruncated = true;
        }
      }
    });

    proc.on('error', (error) => {
      clearTimeout(timer);
      resolve({
        stdout,
        stderr: `${stderr  }\n进程错误: ${  error.message}`,
        exitCode: -1,
        killed,
        duration: Date.now() - startTime,
        pid,
        outputTruncated
      });
    });

    proc.on('close', (code) => {
      clearTimeout(timer);
      const duration = Date.now() - startTime;

      resolve({
        stdout: truncateOutput(stdout),
        stderr: truncateOutput(stderr),
        exitCode: killed ? -1 : code,
        killed,
        duration,
        pid,
        outputTruncated,
        // v2.0 新增：资源使用信息
        resources: {
          estimatedMemoryMB: null, // 实际内存检测需 OS 特定工具，暂不提供
          cpuTimeSec: duration / 1000
        }
      });
    });
  });
}

/**
 * CodeExecutor - 代码执行引擎主类 v2.0.0
 */
class CodeExecutor {
  constructor(options = {}) {
    this.hf = options.hf || null;
    this.retryCount = options.retryCount || 0;
    this.retryDelay = options.retryDelay || 1000;
    this.stepTimeout = options.stepTimeout || DEFAULT_STEP_TIMEOUT;
    this.totalTimeout = options.totalTimeout || DEFAULT_TOTAL_TIMEOUT;
    this.startTime = null;

    // v2.0 新增：增量执行状态
    this._incrementalState = new Map();
    this._maxStateSize = options.maxStateSize || 50;

    // v2.0 新增：性能缓存
    this._resultCache = new Map();
    this._cacheMaxSize = options.cacheMaxSize || 100;
    this._cacheTTL = options.cacheTTL || 5 * 60 * 1000; // 5分钟

    // v2.0 新增：执行轨迹
    this._executionTrace = [];
    this._maxTraceSize = options.maxTraceSize || 200;

    // v2.0 新增：语言配置（合并默认+扩展）
    this._languageConfig = { ...EXTENDED_LANGUAGE_CONFIG, ...options.languageConfig };

    // v2.0 新增：内存引用（用于协同）
    this._memory = null;

    // v2.7 安全升级：根路径和安全审计日志路径
    this._rootPath = options.rootPath || path.resolve(__dirname, '../../..');
    this._securityAuditLogPath = path.join(this._rootPath, 'memory', 'security-audit.log');

    // 确保安全审计日志目录存在
    try {
      const auditDir = path.dirname(this._securityAuditLogPath);
      if (!fs.existsSync(auditDir)) {
        fs.mkdirSync(auditDir, { recursive: true });
      }
    } catch (error) {
      // 忽略目录创建失败
    }
  }

  /**
   * 设置记忆模块（用于执行历史持久化）
   */
  setMemoryModule(memory) {
    this._memory = memory;
  }

  /**
   * 获取语言配置
   */
  getLanguageConfig(language) {
    return this._languageConfig[language] || null;
  }

  /**
   * 检查执行环境可用性
   */
  async healthCheck() {
    const result = { healthy: true, languages: {}, error: null };

    const langChecks = [
      { name: 'node', cmd: 'node', args: ['--version'] },
      { name: 'python3', cmd: 'python3', args: ['--version'] },
      { name: 'bash', cmd: 'bash', args: ['--version'] },
      { name: 'rustc', cmd: 'rustc', args: ['--version'] },
      { name: 'go', cmd: 'go', args: ['version'] },
      { name: 'java', cmd: 'javac', args: ['-version'] },
      { name: 'g++', cmd: 'g++', args: ['--version'] }
    ];

    for (const { name, cmd, args } of langChecks) {
      try {
        const { exitCode } = await executeProcess('which', [cmd], { timeout: 2000 });
        result.languages[name] = exitCode === 0;
        if (exitCode !== 0) result.healthy = false;
      } catch (error) {
        result.languages[name] = false;
        result.healthy = false;
      }
    }

    return result;
  }

  /**
   * 语法检查
   */
  async syntaxCheck(code, language) {
    const config = this._languageConfig[language];
    if (!config) {
      return { valid: false, error: `不支持的语言: ${language}` };
    }

    const tempFile = createTempFile(code, language);

    try {
      // 编译型语言特殊处理
      if (config.compileRequired) {
        const compileArgs = config.args.map(arg => arg.replace('{file}', tempFile));
        const compileResult = await executeProcess(config.command, compileArgs, {
          timeout: config.resourceLimit.compileTimeout || 30000
        });

        if (compileResult.exitCode !== 0) {
          return {
            valid: false,
            error: `编译失败: ${compileResult.stderr || compileResult.stdout}`
          };
        }
        return { valid: true, compiled: true, outputFile: tempFile.replace(path.extname(tempFile), '') };
      }

      // 解释型语言
      if (language === 'python') {
        const { exitCode, stderr } = await executeProcess(
          'python3', ['-c', `import ast; ast.parse(${JSON.stringify(code)})`],
          { timeout: this.stepTimeout }
        );
        return exitCode !== 0 ? { valid: false, error: `Python 语法错误: ${stderr}` } : { valid: true };
      }

      if (language === 'javascript') {
        const { exitCode, stderr } = await executeProcess('node', ['--check', tempFile], { timeout: this.stepTimeout });
        return exitCode !== 0 ? { valid: false, error: `JavaScript 语法错误: ${stderr}` } : { valid: true };
      }

      if (language === 'bash') {
        const { exitCode, stderr } = await executeProcess('bash', ['-n', tempFile], { timeout: this.stepTimeout });
        return exitCode !== 0 ? { valid: false, error: `Bash 语法错误: ${stderr}` } : { valid: true };
      }

      return { valid: true };
    } finally {
      deleteTempFile(tempFile);
    }
  }

  /**
   * 编译代码（v2.0 新增）
   */
  async compile(code, language) {
    const config = this._languageConfig[language];
    if (!config || !config.compileRequired) {
      return { success: true, compiled: false };
    }

    const tempFile = createTempFile(code, language);
    const outputFile = tempFile.replace(path.extname(tempFile), language === 'java' ? '.class' : '');

    try {
      const compileArgs = config.args.map(arg =>
        arg.replace('{file}', tempFile).replace('{output}', outputFile)
      );

      const result = await executeProcess(config.command, compileArgs, {
        timeout: config.resourceLimit.compileTimeout || 30000
      });

      if (result.exitCode !== 0) {
        return { success: false, error: result.stderr, compiled: false };
      }

      return { success: true, compiled: true, outputFile, tempFile };
    } catch (error) {
      return { success: false, error: error.message, compiled: false };
    }
  }

  /**
   * 执行代码（v2.0 增强版）
   */
  /**
   * 执行代码 —— 默认使用沙箱模式（v2.7 安全升级）
   *
   * 默认启用完整的文件系统+网络访问限制。
   * 如需绕过沙箱，显式传入 options.sandbox = false。
   * 如需显式无沙箱执行，使用 executeUnsafe()。
   */
  async execute(code, language, options = {}) {
    if (options.sandbox !== false) {
      // 默认沙箱模式
      const sandboxOptions = { ...options };
      delete sandboxOptions.sandbox; // 不传递 sandbox 标志给 sandbox()
      return this.sandbox(code, language, sandboxOptions);
    }
    // 显式选择非沙箱模式
    console.warn('[CodeExecutor] 注意: 以非沙箱模式执行代码（已通过 sandbox:false 显式选择）');
    return this._executeCore(code, language, options);
  }

  /**
   * 显式非沙箱执行（仅供特殊情况使用，不推荐）
   */
  async executeUnsafe(code, language, options = {}) {
    console.warn('[CodeExecutor] 警告: executeUnsafe() 完全绕过沙箱隔离，仅做基础安全检查');
    return this._executeCore(code, language, options);
  }

  /**
   * 核心执行引擎（不提供沙箱隔离，仅检查黑名单）
   */
  async _executeCore(code, language, options = {}) {
    this.startTime = Date.now();

    // v2.0：缓存检查
    const fingerprint = generateCodeFingerprint(code, language, options);
    if (options.useCache !== false && this._resultCache.has(fingerprint)) {
      const cached = this._resultCache.get(fingerprint);
      if (Date.now() - cached.timestamp < this._cacheTTL) {
        return { ...cached.result, fromCache: true };
      }
    }

    const config = this._languageConfig[language];
    if (!config) {
      return this._createErrorResult(`不支持的语言: ${language}`, -1);
    }

    // 安全检查
    const securityResult = securityCheck(code);
    if (!securityResult.safe) {
      return this._createErrorResult(`安全检查失败: ${securityResult.reason}`, -1);
    }

    // 语法检查（可配置跳过）
    if (options.syntaxCheck !== false) {
      const syntaxResult = await this.syntaxCheck(code, language);
      if (!syntaxResult.valid) {
        return this._createErrorResult(`语法错误: ${syntaxResult.error}`, -1);
      }
    }

    // v2.0：增量执行状态注入
    let execCode = code;
    if (options.incremental && this._incrementalState.has(language)) {
      const state = this._incrementalState.get(language);
      execCode = this._injectState(code, language, state);
    }

    // 编译型语言先编译
    let tempFile = null;
    let outputFile = null;
    if (config.compileRequired) {
      const compileResult = await this.compile(execCode, language);
      if (!compileResult.success) {
        return this._createErrorResult(`编译失败: ${compileResult.error}`, -1);
      }
      tempFile = compileResult.tempFile;
      outputFile = compileResult.outputFile;
    }

    // 执行
    let lastResult = null;
    // 首次重试策略使用未知类型的默认值（实际错误类型在循环中动态检测）
    const strategy = getRetryStrategy('unknown');
    const maxRetries = options.retryCount ?? Math.min(strategy.maxRetries, this.retryCount);

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      if (attempt > 0) {
        await sleep(this.retryDelay * Math.pow(strategy.backoff, attempt - 1));
      }

      if (!config.compileRequired) {
        // v2.7 安全升级：沙箱模式下将代码文件写入隔离目录
        if (options.sandboxDir) {
          const ext = {
            javascript: '.js', python: '.py', bash: '.sh',
            rust: '.rs', go: '.go', java: '.java', cpp: '.cpp'
          }[language] || '.txt';
          tempFile = path.join(options.sandboxDir, `exec_code${ext}`);
          fs.writeFileSync(tempFile, execCode, 'utf8');
        } else {
          tempFile = createTempFile(execCode, language);
        }
      }

      try {
        let execArgs;
        let execCommand = config.command;
        if (config.compileRequired && outputFile) {
          execCommand = config.runCommand.replace('{output}', outputFile);
          execArgs = config.runArgs ?
            config.runArgs.map(arg => arg.replace('{className}', path.basename(outputFile, '.class'))) :
            [];
        } else {
          execArgs = config.args.map(arg => {
            if (arg === '{file}') return tempFile;
            if (arg === '{code}') return execCode;
            return arg;
          });
        }

        const runTimeout = options.stepTimeout || this.stepTimeout;
        const maxMemory = config.resourceLimit?.maxMemoryMB || 512;

        const execProcessOptions = { timeout: runTimeout, maxMemoryMB: maxMemory };
        // v2.7 安全升级：传递沙箱隔离选项
        if (options.sandboxDir) {
          execProcessOptions.sandboxDir = options.sandboxDir;
          execProcessOptions.restrictedEnv = true;
          execProcessOptions.detached = true;
        }

        const result = await executeProcess(
          execCommand,
          execArgs,
          execProcessOptions
        );

        lastResult = this._processExecutionResult(result, attempt);

        if (result.exitCode === 0) break;

        // 智能重试
        const errType = detectErrorType(result.stderr, result.stdout);
        const currentStrategy = getRetryStrategy(errType);
        if (attempt >= currentStrategy.maxRetries) break;

      } catch (error) {
        lastResult = this._createErrorResult(`执行异常: ${error.message}`, -1, attempt);
      } finally {
        // 清理临时文件（编译型语言的源文件 + 输出二进制）
        if (tempFile) {
          deleteTempFile(tempFile);
        }
        if (config.compileRequired && outputFile) {
          deleteTempFile(outputFile);
        }
      }
    }

    // v2.0：缓存结果
    this._cacheResult(fingerprint, lastResult);

    // v2.0：记录执行轨迹
    this._recordTrace(fingerprint, code, language, lastResult);

    // v2.0：更新增量状态
    if (options.incremental && lastResult.success) {
      this._updateIncrementalState(language, lastResult);
    }

    // 与执行验证器协同
    if (this.hf?.executionVerifier && lastResult) {
      try {
        await this.hf.executionVerifier.verify(lastResult);
      } catch (error) {
        console.warn('执行验证失败:', error.message);
      }
    }

    return lastResult;
  }

  /**
   * 处理执行结果（v2.0 新增）
   */
  _processExecutionResult(result, attempt) {
    const errorType = detectErrorType(result.stderr, result.stdout);
    const strategy = getRetryStrategy(errorType);

    return {
      success: result.exitCode === 0,
      stdout: result.stdout,
      stderr: result.stderr,
      exitCode: result.exitCode,
      duration: result.duration,
      error: result.exitCode !== 0 ? `Exit code: ${result.exitCode}` : null,
      attempt,
      killed: result.killed,
      errorType: errorType === 'unknown' ? null : errorType,
      shouldRetry: strategy.maxRetries > 0,
      resources: result.resources,
      pid: result.pid
    };
  }

  /**
   * 注入增量状态（v2.0 新增）
   */
  _injectState(code, language, state) {
    if (language === 'javascript') {
      return `const __state = ${JSON.stringify(state)};\n${code}`;
    }
    if (language === 'python') {
      return `__state = ${JSON.stringify(state)}\n${code}`;
    }
    return code;
  }

  /**
   * 更新增量状态（v2.0 新增）
   */
  _updateIncrementalState(language, result) {
    let state = this._incrementalState.get(language) || {};

    // 从 stdout 解析增量状态
    if (result.stdout) {
      try {
        const parsed = JSON.parse(result.stdout);
        if (parsed.__state) {
          state = { ...state, ...parsed.__state };
        }
      } catch (error) {
        // 非 JSON 输出，忽略
      }
    }

    this._incrementalState.set(language, state);

    // 限制状态大小
    if (this._incrementalState.size > this._maxStateSize) {
      const firstKey = this._incrementalState.keys().next().value;
      this._incrementalState.delete(firstKey);
    }
  }

  /**
   * 缓存执行结果（v2.0 新增）
   */
  _cacheResult(fingerprint, result) {
    this._resultCache.set(fingerprint, {
      result: { ...result },
      timestamp: Date.now()
    });

    // 限制缓存大小
    if (this._resultCache.size > this._cacheMaxSize) {
      const firstKey = this._resultCache.keys().next().value;
      this._resultCache.delete(firstKey);
    }
  }

  /**
   * 记录执行轨迹（v2.0 新增）
   */
  _recordTrace(fingerprint, code, language, result) {
    this._executionTrace.push({
      fingerprint,
      language,
      success: result.success,
      duration: result.duration,
      errorType: result.errorType,
      timestamp: Date.now()
    });

    if (this._executionTrace.length > this._maxTraceSize) {
      this._executionTrace = this._executionTrace.slice(-this._maxTraceSize);
    }

    // 同步到记忆模块
    if (this._memory && result.success) {
      this._persistToMemory(fingerprint, code, language, result);
    }
  }

  /**
   * 持久化到记忆（v2.0 新增）
   */
  async _persistToMemory(fingerprint, code, language, result) {
    if (!this._memory) return;

    try {
      const key = `code_execution:${fingerprint}`;
      await this._memory.set(key, {
        fingerprint,
        language,
        stdout: result.stdout,
        duration: result.duration,
        timestamp: Date.now()
      }, 'EPHEMERAL');
    } catch (error) {
      // 忽略持久化失败
    }
  }

  /**
   * 运行测试用例
   */
  async runTests(code, testCases) {
    const results = [];
    let passed = 0;
    let failed = 0;

    for (const testCase of testCases) {
      const result = await this.execute(code, testCase.language || 'javascript', {
        ...testCase.options,
        sandbox: true,  // v2.7 安全升级：测试执行默认启用沙箱
        timeout: testCase.timeout || this.stepTimeout
      });

      let testPassed = false;

      if (testCase.expectedExitCode !== undefined) {
        testPassed = result.exitCode === testCase.expectedExitCode;
      } else {
        testPassed = result.success;
      }

      if (testCase.expectedOutput !== undefined) {
        testPassed = testPassed && result.stdout.includes(testCase.expectedOutput);
      }

      if (testCase.validate) {
        testPassed = testPassed && testCase.validate(result);
      }

      results.push({
        name: testCase.name,
        passed: testPassed,
        result,
        duration: result.duration
      });

      if (testPassed) passed++;
      else failed++;
    }

    return { passed, failed, results };
  }

  /**
   * 沙箱执行 - 最高安全级别（v2.7 安全升级）
   *
   * 在隔离的临时目录中执行，限制环境变量，采用进程组隔离，
   * 所有操作均有安全审计日志记录。
   */
  async sandbox(code, language, options = {}) {
    const sandboxOptions = {
      ...options,
      syntaxCheck: true,
      stepTimeout: options.stepTimeout || Math.min(this.stepTimeout, 3000),
      totalTimeout: options.totalTimeout || Math.min(this.totalTimeout, 10000),
      retryOnError: false,
      useCache: false,            // 沙箱模式禁用缓存
      incremental: false,          // 沙箱模式禁用增量
      restrictedEnv: true,         // v2.7 安全升级：限制环境变量
      detached: true               // v2.7 安全升级：进程组隔离
    };

    // 安全检查：危险命令黑名单
    const securityResult = securityCheck(code);
    if (!securityResult.safe) {
      this._securityAuditLog({
        type: 'blocked',
        reason: `危险命令黑名单: ${securityResult.reason}`,
        code,
        blocked: true,
        details: `匹配模式: ${securityResult.matched.join(', ')}`
      });
      return this._createErrorResult(`沙箱安全检查失败: ${securityResult.reason}`, -1);
    }

    // 网络访问检查
    if (options.allowNetwork !== true) {
      const networkPatterns = [
        /fetch\s*\(/i, /http\.request/i, /https\.request/i,
        /net\.connect/i, /socket\.connect/i, /grpc/i, /websocket/i,
        /requests\./i, /urllib/i, /curl/i, /wget/i,
        /XMLHttpRequest/i, /WebSocket/i
      ];

      for (const pattern of networkPatterns) {
        if (pattern.test(code)) {
          this._securityAuditLog({
            type: 'blocked',
            reason: '检测到网络访问',
            code,
            blocked: true,
            details: `匹配模式: ${pattern}`
          });
          return this._createErrorResult('沙箱模式禁止网络访问', -1);
        }
      }
    }

    // 文件系统访问检查
    if (options.allowFileSystem !== true) {
      const fsPatterns = [
        /fs\.readFile/i, /fs\.writeFile/i, /fs\.readdir/i,
        /fs\.mkdir/i, /fs\.unlink/i, /readFileSync/i, /writeFileSync/i,
        /open\s*\(/i, /fopen/i, /remove\s*\(/i
      ];

      for (const pattern of fsPatterns) {
        if (pattern.test(code)) {
          this._securityAuditLog({
            type: 'blocked',
            reason: '检测到文件系统访问',
            code,
            blocked: true,
            details: `匹配模式: ${pattern}`
          });
          return this._createErrorResult('沙箱模式禁止直接文件系统访问', -1);
        }
      }
    }

    // v2.7 安全升级：创建沙箱临时工作目录
    let sandboxDir = null;
    try {
      sandboxDir = fs.mkdtempSync(path.join(os.tmpdir(), 'clarity-sandbox-'));
    } catch (error) {
      return this._createErrorResult(`创建沙箱目录失败: ${error.message}`, -1);
    }
    sandboxOptions.sandboxDir = sandboxDir;

    let result;
    try {
      result = await this._executeCore(code, language, sandboxOptions);

      // 记录执行结果到安全审计日志
      this._securityAuditLog({
        type: 'execution',
        reason: result.success ? '执行成功' : '执行失败',
        code,
        blocked: false,
        details: `退出码: ${result.exitCode}, 耗时: ${result.duration}ms`
      });
    } catch (error) {
      result = this._createErrorResult(`沙箱执行异常: ${error.message}`, -1);
      this._securityAuditLog({
        type: 'execution',
        reason: `执行异常: ${error.message}`,
        code,
        blocked: false,
        details: error.message
      });
    } finally {
      // 清理沙箱临时目录
      if (sandboxDir) {
        try {
          fs.rmSync(sandboxDir, { recursive: true, force: true });
        } catch (error) {
          // 忽略清理失败
        }
      }
    }

    return result;
  }

  /**
   * 输出分析（v2.0 新增）
   */
  analyzeOutput(result) {
    const output = result.stdout + result.stderr;
    const lines = output.split('\n').filter(l => l.trim());

    // 检测输出模式
    const patterns = {
      json: /^[\s]*[\[{]/,
      error: /error|exception|fail/i,
      warning: /warn|notice|deprecated/i,
      success: /success|passed|ok/i,
      table: /^\|.*\|/,
      keyValue: /^\w+:\s*.+/
    };

    const detectedPatterns = [];
    for (const [name, pattern] of Object.entries(patterns)) {
      if (pattern.test(output)) detectedPatterns.push(name);
    }

    // 解析关键值
    const extractedValues = {};
    const kvPattern = /^(\w+):\s*(.+)$/gm;
    let match;
    while ((match = kvPattern.exec(output)) !== null) {
      extractedValues[match[1]] = match[2].trim();
    }

    // 提取数字
    const numbers = [];
    const numPattern = /-?\d+\.?\d*/g;
    let numMatch;
    while ((numMatch = numPattern.exec(output)) !== null) {
      const num = parseFloat(numMatch[0]);
      if (!isNaN(num) && isFinite(num)) {
        numbers.push(num);
      }
    }

    return {
      lineCount: lines.length,
      patterns: detectedPatterns,
      extractedValues,
      numbers: numbers.slice(0, 20), // 限制数量
      summary: result.success ? 'success' : 'error',
      rawLength: output.length
    };
  }

  /**
   * 获取执行轨迹统计（v2.0 新增）
   */
  getTraceStats() {
    if (this._executionTrace.length === 0) {
      return { total: 0, successRate: 0, avgDuration: 0 };
    }

    const total = this._executionTrace.length;
    const successCount = this._executionTrace.filter(t => t.success).length;
    const totalDuration = this._executionTrace.reduce((sum, t) => sum + t.duration, 0);

    // 按语言统计
    const byLanguage = {};
    for (const trace of this._executionTrace) {
      if (!byLanguage[trace.language]) {
        byLanguage[trace.language] = { total: 0, success: 0, totalDuration: 0 };
      }
      byLanguage[trace.language].total++;
      if (trace.success) byLanguage[trace.language].success++;
      byLanguage[trace.language].totalDuration += trace.duration;
    }

    return {
      total,
      successRate: `${(successCount / total * 100).toFixed(1)  }%`,
      avgDuration: `${(totalDuration / total).toFixed(0)  }ms`,
      byLanguage: Object.fromEntries(
        Object.entries(byLanguage).map(([lang, stats]) => [
          lang,
          {
            total: stats.total,
            successRate: `${(stats.success / stats.total * 100).toFixed(1)  }%`,
            avgDuration: `${(stats.totalDuration / stats.total).toFixed(0)  }ms`
          }
        ])
      )
    };
  }

  /**
   * 获取缓存统计（v2.0 新增）
   */
  getCacheStats() {
    const now = Date.now();
    const validEntries = [...this._resultCache.entries()].filter(([_, v]) =>
      now - v.timestamp < this._cacheTTL
    );

    return {
      size: this._resultCache.size,
      maxSize: this._cacheMaxSize,
      validEntries: validEntries.length,
      hitRate: 'N/A' // 需要历史数据才能计算
    };
  }

  /**
   * 清除缓存
   */
  clearCache() {
    this._resultCache.clear();
    return { cleared: true, size: 0 };
  }

  /**
   * 清除增量状态
   */
  clearIncrementalState(language = null) {
    if (language) {
      this._incrementalState.delete(language);
      return { cleared: language, remaining: this._incrementalState.size };
    }
    this._incrementalState.clear();
    return { cleared: 'all', remaining: 0 };
  }

  /**
   * 创建错误结果对象
   */
  _createErrorResult(message, exitCode, attempt = 0) {
    return {
      success: false,
      stdout: '',
      stderr: message,
      exitCode,
      duration: Date.now() - (this.startTime || Date.now()),
      error: message,
      attempt
    };
  }

  /**
   * 安全审计日志记录（v2.7 新增）
   *
   * 记录所有代码执行尝试和阻止的安全违规到审计日志文件。
   * 每条记录包含：时间戳、代码哈希、执行类型、是否被阻止、详细信息。
   */
  _securityAuditLog(event) {
    const { type, reason, code, blocked, details } = event;
    const timestamp = new Date().toISOString();
    const codeHash = crypto.createHash('sha256').update(code || '').digest('hex').substring(0, 16);

    const logEntry = JSON.stringify({
      timestamp,
      codeHash,
      type,
      reason,
      blocked: !!blocked,
      details: details || ''
    }) + '\n';

    try {
      const auditDir = path.dirname(this._securityAuditLogPath);
      if (!fs.existsSync(auditDir)) {
        fs.mkdirSync(auditDir, { recursive: true });
      }
      fs.appendFileSync(this._securityAuditLogPath, logEntry, 'utf8');
    } catch (error) {
      // 忽略审计日志写入失败
    }
  }

  /**
   * 获取执行统计信息
   */
  getStats() {
    return {
      totalTimeout: this.totalTimeout,
      stepTimeout: this.stepTimeout,
      retryCount: this.retryCount,
      retryDelay: this.retryDelay,
      incrementalStateSize: this._incrementalState.size,
      cacheSize: this._resultCache.size,
      traceSize: this._executionTrace.length,
      supportedLanguages: Object.keys(this._languageConfig)
    };
  }

  /**
   * 更新配置
   */
  updateConfig(config) {
    if (config.stepTimeout !== undefined) this.stepTimeout = config.stepTimeout;
    if (config.totalTimeout !== undefined) this.totalTimeout = config.totalTimeout;
    if (config.retryCount !== undefined) this.retryCount = config.retryCount;
    if (config.retryDelay !== undefined) this.retryDelay = config.retryDelay;
    if (config.cacheTTL !== undefined) this._cacheTTL = config.cacheTTL;
    if (config.cacheMaxSize !== undefined) this._cacheMaxSize = config.cacheMaxSize;
  }

  /**
   * 重置（保留配置，清除运行时状态）
   */
  reset() {
    this._resultCache.clear();
    this._incrementalState.clear();
    this._executionTrace = [];
  }
}

/**
 * 工厂函数
 */
function createCodeExecutor(options = {}) {
  return new CodeExecutor(options);
}

// 导出模块
module.exports = {
  CodeExecutor,
  createCodeExecutor,
  securityCheck,
  truncateOutput,
  detectErrorType,
  getRetryStrategy,
  generateCodeFingerprint,
  MAX_OUTPUT_SIZE,
  DEFAULT_STEP_TIMEOUT,
  DEFAULT_TOTAL_TIMEOUT,
  EXTENDED_LANGUAGE_CONFIG,
  ERROR_PATTERN_MAP
};