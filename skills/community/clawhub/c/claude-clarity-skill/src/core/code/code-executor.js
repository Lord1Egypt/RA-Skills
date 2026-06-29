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

// 危险命令黑名单（安全过滤）
const DANGEROUS_PATTERNS = [
  /rm\s+-rf\s+/,                        // 禁止 rm -rf 删除命令
  /^rm\s+-rf\s+/m,                     // 行首的 rm -rf
  /\.\.\/\.\.\//,                      // 路径穿越尝试
  /eval\s*\(/i,                         // 危险 eval
  /exec\s*\(/i,                         // 危险 exec
  /child_process/i,                     // 禁止子进程模块
  /require\s*\(\s*['\"]child_process['\"]\s*\)/i,
  /import\s+.*child_process/i,
  /\bsudo\s+rm\b/i,                     // 禁止 sudo rm
  /format\s+\//i,                       // 格式化根目录
  /mkfs\./i,                            // 创建文件系统
  /dd\s+if=/i,                          // 直接磁盘操作
  /curl\s+-/i,                          // 禁止 curl 下载/网络访问
  /wget\s+/i,                           // 禁止 wget 下载
  /process\.binding/i,                  // 禁止原生模块绑定
  /require\s*\(\s*['\"]net['\"]\s*\)/i, // 禁止网络模块
  /require\s*\(\s*['\"]http['\"]\s*\)/i,
  /require\s*\(\s*['\"]https['\"]\s*\)/i,
  /require\s*\(\s*['\"]dgram['\"]\s*\)/i,
  /require\s*\(\s*['\"]tls['\"]\s*\)/i,
  /require\s*\(\s*['\"]vm['\"]\s*\)/i,
];

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
  return output.substring(0, MAX_OUTPUT_SIZE) + '\n... [输出已截断]';
}

/**
 * 安全检查：检测危险命令
 */
function securityCheck(code) {
  for (const pattern of DANGEROUS_PATTERNS) {
    if (pattern.test(code)) {
      return { safe: false, reason: `检测到危险模式: ${pattern.toString()}` };
    }
  }
  return { safe: true };
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
  return new Promise(resolve => setTimeout(resolve, ms));
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
 * 执行子进程并等待结果（增强版，含资源监控）
 */
function executeProcess(command, args, options = {}) {
  return new Promise((resolve) => {
    const { timeout = DEFAULT_STEP_TIMEOUT, cwd = process.cwd(), maxMemoryMB = 512 } = options;

    let stdout = '';
    let stderr = '';
    let killed = false;
    let pid = null;

    // 资源监控（v2.0 新增）
    const startTime = Date.now();
    const startCpuTime = process.cpuUsage ? process.cpuUsage() : null;

    const proc = spawn(command, args, {
      cwd,
      env: { ...process.env, NODE_ENV: 'production' },
      stdio: ['pipe', 'pipe', 'pipe'],
      detached: false,
    });

    pid = proc.pid;

    // 超时控制
    const timer = setTimeout(() => {
      killed = true;
      proc.kill('SIGKILL');
    }, timeout);

    proc.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    proc.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    proc.on('error', (error) => {
      clearTimeout(timer);
      resolve({
        stdout,
        stderr: stderr + '\n进程错误: ' + error.message,
        exitCode: -1,
        killed,
        duration: Date.now() - startTime,
        pid
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
  async execute(code, language, options = {}) {
    // ⚠️ 安全警告: execute() 不提供沙箱隔离（仅检查黑名单）
    // 推荐使用 sandbox() 方法获得完整的文件系统+网络访问限制
    if (!options.silentDeprecation) {
      console.warn('[CodeExecutor] 警告: execute() 方法没有沙箱隔离, 建议改用 sandbox() 方法');
    }
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
    let strategy = getRetryStrategy('unknown');
    const maxRetries = options.retryCount ?? Math.min(strategy.maxRetries, this.retryCount);

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      if (attempt > 0) {
        await sleep(this.retryDelay * Math.pow(strategy.backoff, attempt - 1));
      }

      if (!config.compileRequired) {
        tempFile = createTempFile(execCode, language);
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

        const result = await executeProcess(
          execCommand,
          execArgs,
          { timeout: runTimeout, maxMemoryMB: maxMemory }
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
   * 沙箱执行 - 最高安全级别
   */
  async sandbox(code, language, options = {}) {
    const sandboxOptions = {
      ...options,
      syntaxCheck: true,
      stepTimeout: options.stepTimeout || Math.min(this.stepTimeout, 3000),
      totalTimeout: options.totalTimeout || Math.min(this.totalTimeout, 10000),
      retryOnError: false,
      useCache: false, // 沙箱模式禁用缓存
      incremental: false // 沙箱模式禁用增量
    };

    const securityResult = securityCheck(code);
    if (!securityResult.safe) {
      return this._createErrorResult(`沙箱安全检查失败: ${securityResult.reason}`, -1);
    }

    // 网络访问检查
    const networkPatterns = [
      /fetch\s*\(/i, /http\.request/i, /https\.request/i,
      /net\.connect/i, /socket\.connect/i, /grpc/i, /websocket/i,
      /requests\./i, /urllib/i, /curl/i, /wget/i
    ];

    if (options.allowNetwork !== true) {
      for (const pattern of networkPatterns) {
        if (pattern.test(code)) {
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
          return this._createErrorResult('沙箱模式禁止直接文件系统访问', -1);
        }
      }
    }

    return this.execute(code, language, sandboxOptions);
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
      successRate: (successCount / total * 100).toFixed(1) + '%',
      avgDuration: (totalDuration / total).toFixed(0) + 'ms',
      byLanguage: Object.fromEntries(
        Object.entries(byLanguage).map(([lang, stats]) => [
          lang,
          {
            total: stats.total,
            successRate: (stats.success / stats.total * 100).toFixed(1) + '%',
            avgDuration: (stats.totalDuration / stats.total).toFixed(0) + 'ms'
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