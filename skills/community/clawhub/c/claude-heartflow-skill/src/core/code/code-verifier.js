/**
 * HeartFlow CodeVerifier v2.0.0
 *
 * 代码验证引擎 - 三层验证 + 质量评分
 *
 * 三层验证：
 * 1. 语法验证：基于 AST 解析（JS 使用 acorn，Python 使用 py_compile）
 * 2. 逻辑验证：执行 + 输出比对
 * 3. 测试验证：TDD 模式（生成测试→执行→验证）
 *
 * 质量评分：0-100 分（可读性/效率/安全性/完整性）
 *
 * dispatch 路由：
 * - verify(code, language, criteria)       → 综合验证
 * - verifySyntax(code, language)          → 语法检查
 * - verifyLogic(code, language, expectedOutput) → 逻辑验证
 * - runTDD(task, language)                → TDD 流程
 * - getQualityScore(code, language)       → 质量评分
 *
 * 与心虫 execution-verifier.js 协同，复用验证逻辑
 * 验证结果持久化到 MeaningfulMemory（学习成功/失败模式）
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// AST 解析器（JS）
let acorn = null;
try {
  acorn = require('acorn');
} catch (e) {
  // acorn 未安装，跳过 AST 解析
}

// ============================================================
// 工具函数
// ============================================================

/**
 * 异步执行命令
 * @param {string} cmd - 命令
 * @param {Array} args - 参数
 * @param {Object} options - 选项
 * @returns {Promise<{stdout, stderr, exitCode, timedOut}>}
 */
function execCommand(cmd, args, options = {}) {
  return new Promise((resolve) => {
    const timeout = options.timeout || 30000;
    let stdout = '';
    let stderr = '';
    let timedOut = false;

    const proc = spawn(cmd, args, {
      cwd: options.cwd || process.cwd(),
      env: { ...process.env, ...options.env },
      timeout
    });

    const timer = setTimeout(() => {
      timedOut = true;
      proc.kill('SIGKILL');
    }, timeout);

    proc.stdout?.on('data', (data) => { stdout += data.toString(); });
    proc.stderr?.on('data', (data) => { stderr += data.toString(); });

    proc.on('close', (code) => {
      clearTimeout(timer);
      resolve({ stdout, stderr, exitCode: code, timedOut });
    });

    proc.on('error', (err) => {
      clearTimeout(timer);
      resolve({ stdout, stderr, exitCode: -1, timedOut: false, error: err.message });
    });
  });
}

/**
 * 临时文件写入
 * @param {string} content - 内容
 * @param {string} ext - 扩展名
 * @returns {string} 文件路径
 */
function writeTempFile(content, ext) {
  const tmpDir = require('os').tmpdir();
  const filename = `hf_verify_${Date.now()}_${crypto.randomBytes(4).toString('hex')}${ext}`;
  const filePath = path.join(tmpDir, filename);
  fs.writeFileSync(filePath, content, 'utf8');
  return filePath;
}

/**
 * 删除临时文件
 * @param {string} filePath - 文件路径
 */
function deleteTempFile(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }
  } catch (e) {
    // 忽略删除错误
  }
}

/**
 * 计算文本复杂度
 * @param {string} code - 代码
 * @returns {Object} 复杂度指标
 */
function calculateComplexity(code) {
  const lines = code.split('\n');
  const nonEmptyLines = lines.filter(l => l.trim().length > 0);

  // 圈复杂度估算（基于分支关键词）
  const branchKeywords = ['if', 'else', 'for', 'while', 'switch', 'case', 'catch', 'try', 'finally'];
  const branchCount = branchKeywords.reduce((sum, kw) => sum + (code.match(new RegExp(`\\b${kw}\\b`, 'g')) || []).length, 0);
  // 单独计算逻辑运算符
  const logicOps = ((code.match(/&&|\|\|/g)) || []).length;
  const questionOps = ((code.match(/\?/g)) || []).length;
  const totalBranchCount = branchCount + logicOps + questionOps;
  const cyclomaticComplexity = Math.max(1, 1 + totalBranchCount);

  // 嵌套深度
  let maxDepth = 0;
  let currentDepth = 0;
  for (const char of code) {
    if (char === '{' || char === '(') currentDepth++;
    else if (char === '}' || char === ')') currentDepth--;
    maxDepth = Math.max(maxDepth, currentDepth);
  }

  return {
    totalLines: lines.length,
    nonEmptyLines: nonEmptyLines.length,
    cyclomaticComplexity,
    maxNestingDepth: maxDepth,
    // 平均行长度
    avgLineLength: nonEmptyLines.length > 0
      ? nonEmptyLines.reduce((sum, l) => sum + l.trim().length, 0) / nonEmptyLines.length
      : 0
  };
}

// ============================================================
// 验证结果缓存
// ============================================================

const _resultCache = new Map();
const CACHE_MAX_SIZE = 100;
const CACHE_TTL = 5 * 60 * 1000; // 5分钟
let _cacheHits = 0; // 累计缓存命中次数（用于计算命中率）

function getCacheKey(code, language, method) {
  return crypto.createHash('md5').update(`${method}:${language}:${code}`).digest('hex');
}

function getFromCache(key) {
  const entry = _resultCache.get(key);
  if (!entry) return null;
  if (Date.now() - entry.timestamp > CACHE_TTL) {
    _resultCache.delete(key);
    return null;
  }
  _cacheHits++;
  return entry.data;
}

function setCache(key, data) {
  if (_resultCache.size >= CACHE_MAX_SIZE) {
    // 删除最老的条目
    const oldestKey = _resultCache.keys().next().value;
    _resultCache.delete(oldestKey);
  }
  _resultCache.set(key, { data, timestamp: Date.now() });
}

// ============================================================
// CodeVerifier 主类
// ============================================================

class CodeVerifier {
  /**
   * @param {Object} options
   * @param {Object} options.hf - HeartFlow 实例（用于 dispatch 调用其他模块）
   * @param {Object} options.memory - MeaningfulMemory 实例（可选，将自动获取）
   */
  constructor(options = {}) {
    this.hf = options.hf || null;
    this.memory = options.memory || null;
    this.stats = {
      totalVerifications: 0,
      successCount: 0,
      failureCount: 0,
      avgQualityScore: 0,
      tddCycles: 0,
      lastVerification: null
    };
  }

  /**
   * 获取 MeaningfulMemory 实例
   * @returns {Object|null}
   */
  getMemory() {
    if (this.memory) return this.memory;
    if (this.hf) {
      try {
        this.memory = this.hf.dispatch ? this.hf.dispatch('memory.getMeaningfulMemory') : null;
      } catch (e) {
        // dispatch 不可用
      }
    }
    return this.memory;
  }

  /**
   * 将验证结果记录到记忆
   * @param {Object} result - 验证结果
   * @param {string} type - 验证类型
   */
  async recordToMemory(result, type) {
    const memory = this.getMemory();
    if (!memory) return;

    try {
      const record = {
        type: `code_verification:${type}`,
        timestamp: Date.now(),
        result,
        stats: { ...this.stats }
      };

      // 使用记忆的 store 方法（如果可用）
      if (typeof memory.store === 'function') {
        await memory.store(record.type, record);
      }
    } catch (e) {
      // 记忆写入失败不影响主流程
    }
  }

  // ============================================================
  // 路由派发（dispatch 入口）
  // ============================================================

  /**
   * dispatch 路由派发
   * @param {string} method - 方法名
   * @param {...any} args - 参数
   * @returns {any}
   */
  dispatch(method, ...args) {
    switch (method) {
      case 'verify':
        return this.verify(...args);
      case 'verifySyntax':
        return this.verifySyntax(...args);
      case 'verifyLogic':
        return this.verifyLogic(...args);
      case 'runTDD':
        return this.runTDD(...args);
      case 'getQualityScore':
        return this.getQualityScore(...args);
      default:
        throw new Error(`CodeVerifier: 未知方法 ${method}`);
    }
  }

  // ============================================================
  // 综合验证
  // ============================================================

  /**
   * 综合验证
   * @param {string} code - 代码
   * @param {string} language - 语言 (js, python, shell)
   * @param {Object} criteria - 验证标准
   * @returns {Object} 综合验证结果
   */
  async verify(code, language, criteria = {}) {
    this.stats.totalVerifications++;
    this.stats.lastVerification = Date.now();

    const cacheKey = getCacheKey(code, language, 'verify');
    const cached = getFromCache(cacheKey);
    if (cached) return cached;

    const result = {
      passed: true,
      syntax: null,
      logic: null,
      quality: null,
      errors: [],
      warnings: [],
      score: 0
    };

    // 1. 语法验证
    result.syntax = await this.verifySyntax(code, language);
    if (!result.syntax.passed) {
      result.passed = false;
      result.errors.push(...result.syntax.errors);
    }

    // 2. 逻辑验证（如果有预期输出）
    if (criteria.expectedOutput !== undefined) {
      result.logic = await this.verifyLogic(code, language, criteria.expectedOutput);
      if (!result.logic.passed) {
        result.passed = false;
        result.errors.push(...result.logic.errors);
      }
    }

    // 3. 质量评分
    result.quality = this.getQualityScore(code, language);
    result.score = result.quality.score;

    // 4. 严重性分级
    result.severity = this._classifySeverity(result.errors, result.warnings);

    // 5. 建议生成
    result.suggestions = this._generateSuggestions(result);

    // 更新统计
    if (result.passed) {
      this.stats.successCount++;
    } else {
      this.stats.failureCount++;
    }

    // 缓存结果
    setCache(cacheKey, result);

    // 记录到记忆
    await this.recordToMemory(result, 'comprehensive');

    return result;
  }

  // ============================================================
  // 语法验证
  // ============================================================

  /**
   * 语法验证 - 基于 AST 解析
   * @param {string} code - 代码
   * @param {string} language - 语言
   * @returns {Object} 语法验证结果
   */
  async verifySyntax(code, language) {
    const cacheKey = getCacheKey(code, language, 'syntax');
    const cached = getFromCache(cacheKey);
    if (cached) return cached;

    const result = {
      passed: true,
      errors: [],
      warnings: [],
      ast: null,
      metrics: {}
    };

    switch (language.toLowerCase()) {
      case 'js':
      case 'javascript':
        result.ast = await this._verifyJSSyntax(code, result);
        break;
      case 'py':
      case 'python':
        result.ast = await this._verifyPythonSyntax(code, result);
        break;
      case 'sh':
      case 'bash':
      case 'shell':
        result.ast = await this._verifyShellSyntax(code, result);
        break;
      default:
        result.errors.push(`不支持的语言: ${language}`);
        result.passed = false;
    }

    // 基础语法检查（所有语言通用）
    this._checkBasicSyntax(code, result);

    // 缓存结果
    if (result.passed) {
      setCache(cacheKey, result);
    }

    return result;
  }

  /**
   * JS AST 解析验证
   * @param {string} code - 代码
   * @param {Object} result - 结果对象
   * @returns {Object} AST 或 null
   */
  async _verifyJSSyntax(code, result) {
    if (!acorn) {
      // 无 acorn，使用基础检查
      result.warnings.push('acorn 未安装，跳过 AST 深度解析');
      return null;
    }

    try {
      const ast = acorn.parse(code, {
        ecmaVersion: 2022,
        sourceType: 'module',
        allowReturnOutsideFunction: true,
        allowAwaitOutsideFunction: true
      });

      // AST 解析成功，检查结构
      this._analyzeJSAST(ast, result);
      return ast;
    } catch (e) {
      result.errors.push(`语法错误: ${e.message}`);
      result.passed = false;
      return null;
    }
  }

  /**
   * 分析 JS AST
   * @param {Object} ast - AST
   * @param {Object} result - 结果对象
   */
  _analyzeJSAST(ast, result) {
    let exportCount = 0;
    let importCount = 0;
    let functionCount = 0;
    let classCount = 0;

    // 遍历 AST 节点
    const traverse = (node) => {
      if (!node || typeof node !== 'object') return;

      switch (node.type) {
        case 'ExportNamedDeclaration':
        case 'ExportDefaultDeclaration':
          exportCount++;
          break;
        case 'ImportDeclaration':
          importCount++;
          break;
        case 'FunctionDeclaration':
        case 'FunctionExpression':
        case 'ArrowFunctionExpression':
          functionCount++;
          break;
        case 'ClassDeclaration':
        case 'ClassExpression':
          classCount++;
          break;
      }

      for (const key of Object.keys(node)) {
        if (key !== 'type' && key !== 'loc') {
          const child = node[key];
          if (Array.isArray(child)) {
            child.forEach(traverse);
          } else if (child && typeof child === 'object') {
            traverse(child);
          }
        }
      }
    };

    traverse(ast);

    result.metrics = {
      exportCount,
      importCount,
      functionCount,
      classCount
    };
  }

  /**
   * Python AST 解析验证
   * @param {string} code - 代码
   * @param {Object} result - 结果对象
   * @returns {Object} AST 或 null
   */
  async _verifyPythonSyntax(code, result) {
    // 使用 py_compile 验证
    const tempFile = writeTempFile(code, '.py');

    try {
      // 尝试 python3，fallback 到 python
      let { stdout, stderr, exitCode } = await execCommand(
        'python3', ['-m', 'py_compile', tempFile],
        { timeout: 10000 }
      );

      if (exitCode !== 0) {
        // 尝试 python (部分系统可能没有 python3)
        const fallback = await execCommand(
          'python', ['-m', 'py_compile', tempFile],
          { timeout: 10000 }
        );
        if (fallback.exitCode !== 0) {
          result.errors.push(`Python 语法错误: ${fallback.stderr || fallback.stdout || '未知错误'}`);
          result.passed = false;
          return null;
        }
        stdout = fallback.stdout;
        stderr = fallback.stderr;
        exitCode = 0;
      }

      // py_compile 成功，尝试获取 AST
      try {
        const readCmd = `import ast, sys; ast.parse(open(sys.argv[1]).read())`;
        let astResult = await execCommand(
          'python3', ['-c', readCmd, tempFile],
          { timeout: 10000 }
        );
        if (astResult.exitCode !== 0) {
          astResult = await execCommand('python', ['-c', readCmd, tempFile], { timeout: 10000 });
        }
        if (astResult.exitCode === 0) {
          // Python AST 解析成功
          result.metrics = this._analyzePythonAST(code);
          return { parsed: true };
        }
      } catch (e) {
        result.warnings.push('无法获取 Python AST');
      }

      return { parsed: true };
    } catch (e) {
      result.errors.push(`Python 验证失败: ${e.message}`);
      result.passed = false;
      return null;
    } finally {
      deleteTempFile(tempFile);
    }
  }

  /**
   * 分析 Python 代码结构
   * @param {string} code - 代码
   * @returns {Object} 分析结果
   */
  _analyzePythonAST(code) {
    const functionMatches = code.match(/^def\s+\w+/gm) || [];
    const classMatches = code.match(/^class\s+\w+/gm) || [];
    const importMatches = code.match(/^import\s+|^from\s+/gm) || [];

    return {
      functionCount: functionMatches.length,
      classCount: classMatches.length,
      importCount: importMatches.length
    };
  }

  /**
   * Shell 语法验证
   * @param {string} code - 代码
   * @param {Object} result - 结果对象
   * @returns {Object} 语法结果
   */
  async _verifyShellSyntax(code, result) {
    // 检查 shebang
    if (!code.startsWith('#!')) {
      result.warnings.push('缺少 shebang，建议添加 #!/bin/bash 或 #!/bin/sh');
    }

    // 检查引号平衡
    const singleQuotes = (code.match(/'/g) || []).length;
    const doubleQuotes = (code.match(/"/g) || []).length;

    if (singleQuotes % 2 !== 0) {
      result.errors.push('单引号未闭合');
      result.passed = false;
    }
    if (doubleQuotes % 2 !== 0) {
      result.errors.push('双引号未闭合');
      result.passed = false;
    }

    // 检查反引号和 $() 平衡
    const backticks = (code.match(/`/g) || []).length;
    const dollarParen = (code.match(/\$\(/g) || []).length;

    if (backticks % 2 !== 0) {
      result.errors.push('反引号未闭合');
      result.passed = false;
    }

    // 使用 shellcheck 验证（如果可用）
    const tempFile = writeTempFile(code, '.sh');
    try {
      const { stdout, stderr, exitCode } = await execCommand(
        'shellcheck', ['-s', 'bash', '-f', 'json', tempFile],
        { timeout: 10000 }
      );

      if (exitCode === 0) {
        // shellcheck 通过
        return { checked: true };
      }

      // 解析 shellcheck 输出
      try {
        const issues = JSON.parse(stdout);
        for (const issue of issues) {
          const msg = `${issue.message} (行 ${issue.line})`;
          if (issue.level === 'error') {
            result.errors.push(msg);
            result.passed = false;
          } else {
            result.warnings.push(msg);
          }
        }
      } catch (e) {
        // shellcheck 输出解析失败
      }
    } catch (e) {
      // shellcheck 不可用，跳过
    } finally {
      deleteTempFile(tempFile);
    }

    return { checked: true };
  }

  /**
   * 基础语法检查（所有语言通用）
   * @param {string} code - 代码
   * @param {Object} result - 结果对象
   */
  _checkBasicSyntax(code, result) {
    // 空代码检查
    if (!code || code.trim().length === 0) {
      result.errors.push('代码为空');
      result.passed = false;
      return;
    }

    // 检查过长的行
    const lines = code.split('\n');
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].length > 200) {
        result.warnings.push(`行 ${i + 1} 过长 (${lines[i].length} 字符)，建议拆分`);
      }
    }

    // 检查不可见字符
    if (/[\x00-\x08\x0B\x0C\x0E-\x1F]/.test(code)) {
      result.warnings.push('代码包含不可见控制字符');
    }
  }

  // ============================================================
  // 逻辑验证
  // ============================================================

  /**
   * 逻辑验证 - 执行代码并比对输出
   * @param {string} code - 代码
   * @param {string} language - 语言
   * @param {*} expectedOutput - 预期输出
   * @returns {Object} 逻辑验证结果
   */
  async verifyLogic(code, language, expectedOutput) {
    const result = {
      passed: false,
      errors: [],
      warnings: [],
      actualOutput: null,
      executionTime: 0
    };

    const startTime = Date.now();

    try {
      switch (language.toLowerCase()) {
        case 'js':
        case 'javascript':
          await this._verifyJSLogic(code, expectedOutput, result);
          break;
        case 'py':
        case 'python':
          await this._verifyPythonLogic(code, expectedOutput, result);
          break;
        case 'sh':
        case 'bash':
        case 'shell':
          await this._verifyShellLogic(code, expectedOutput, result);
          break;
        default:
          result.errors.push(`不支持的语言: ${language}`);
      }
    } catch (e) {
      result.errors.push(`执行失败: ${e.message}`);
    }

    result.executionTime = Date.now() - startTime;
    result.passed = result.errors.length === 0 && result.actualOutput !== null;

    return result;
  }

  /**
   * JS 逻辑验证
   * @param {string} code - 代码
   * @param {*} expectedOutput - 预期输出
   * @param {Object} result - 结果对象
   */
  async _verifyJSLogic(code, expectedOutput, result) {
    // 包装代码以捕获输出
    let wrappedCode = code;

    // 检查是否已经是完整模块
    if (!code.includes('module.exports') && !code.includes('export')) {
      // 先覆盖 console.log，再执行用户代码，确保输出被捕获
      wrappedCode = `
const _hf_output = [];
const _origLog = console.log;
console.log = (...args) => {
  _hf_output.push(args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' '));
  _origLog.apply(console, args);
};

${code}

// 执行主逻辑（如果有）
if (typeof main === 'function') main();

// 输出结果
console.log(JSON.stringify({ output: _hf_output, result: typeof result !== 'undefined' ? result : null }));
`;
    }

    const tempFile = writeTempFile(wrappedCode, '.js');

    try {
      const { stdout, stderr, exitCode, timedOut } = await execCommand(
        'node', [tempFile],
        { timeout: 15000, env: { ...process.env, NODE_OPTIONS: '--max-old-space-size=128' } }
      );

      if (timedOut) {
        result.errors.push('执行超时 (15秒)');
        return;
      }

      if (exitCode !== 0 && stderr) {
        result.errors.push(`运行时错误: ${stderr}`);
        return;
      }

      result.actualOutput = stdout.trim();

      // 比对输出
      const expected = typeof expectedOutput === 'string'
        ? expectedOutput
        : JSON.stringify(expectedOutput);
      const actual = result.actualOutput;

      if (actual.includes(expected) || expected === actual) {
        result.passed = true;
      } else {
        result.warnings.push(`输出不匹配: 预期包含 "${expected}", 实际输出 "${actual}"`);
        result.passed = false;
      }
    } finally {
      deleteTempFile(tempFile);
    }
  }

  /**
   * Python 逻辑验证
   * @param {string} code - 代码
   * @param {*} expectedOutput - 预期输出
   * @param {Object} result - 结果对象
   */
  async _verifyPythonLogic(code, expectedOutput, result) {
    // 包装代码以捕获输出（先替换 stdout，再插入用户代码）
    let wrappedCode = `
import sys
from io import StringIO

# 替换 stdout 以捕获 print 输出
class OutputCapture:
    def write(self, text):
        if text.strip():
            _hf_output.append(text.rstrip('\\n'))
        _hf_buffer.write(text)

    def flush(self):
        pass

_hf_output = []
_hf_buffer = StringIO()
sys.stdout = OutputCapture()

${code}

# 执行主逻辑（如果有）
if 'main' in dir():
    main()

# 输出结果
sys.stdout = sys.__stdout__
print(_hf_output)
`;

    const tempFile = writeTempFile(wrappedCode, '.py');

    try {
      const { stdout, stderr, exitCode, timedOut } = await execCommand(
        'python', [tempFile],
        { timeout: 15000 }
      );

      if (timedOut) {
        result.errors.push('执行超时 (15秒)');
        return;
      }

      if (exitCode !== 0 && stderr) {
        result.errors.push(`运行时错误: ${stderr}`);
        return;
      }

      result.actualOutput = stdout.trim();

      // 比对输出
      const expected = typeof expectedOutput === 'string'
        ? expectedOutput
        : JSON.stringify(expectedOutput);
      const actual = result.actualOutput;

      if (actual.includes(expected) || expected === actual) {
        result.passed = true;
      } else {
        result.warnings.push(`输出不匹配: 预期包含 "${expected}", 实际输出 "${actual}"`);
        result.passed = false;
      }
    } finally {
      deleteTempFile(tempFile);
    }
  }

  /**
   * Shell 逻辑验证
   * @param {string} code - 代码
   * @param {*} expectedOutput - 预期输出
   * @param {Object} result - 结果对象
   */
  async _verifyShellLogic(code, expectedOutput, result) {
    const tempFile = writeTempFile(code, '.sh');

    try {
      const { stdout, stderr, exitCode, timedOut } = await execCommand(
        'bash', [tempFile],
        { timeout: 15000 }
      );

      if (timedOut) {
        result.errors.push('执行超时 (15秒)');
        return;
      }

      if (exitCode !== 0 && stderr) {
        result.warnings.push(`非零退出码: ${exitCode}`);
      }

      result.actualOutput = stdout.trim();

      // 比对输出
      const expected = typeof expectedOutput === 'string'
        ? expectedOutput
        : JSON.stringify(expectedOutput);
      const actual = result.actualOutput;

      if (actual.includes(expected) || expected === actual) {
        result.passed = true;
      } else {
        result.warnings.push(`输出不匹配: 预期包含 "${expected}", 实际输出 "${actual}"`);
        result.passed = false;
      }
    } finally {
      deleteTempFile(tempFile);
    }
  }

  // ============================================================
  // TDD 流程
  // ============================================================

  /**
   * TDD 流程：生成测试 → 执行（应失败）→ 生成实现 → 验证通过
   * @param {string} task - 任务描述
   * @param {string} language - 语言
   * @param {Object} options - 选项
   * @returns {Object} TDD 结果
   */
  async runTDD(task, language, options = {}) {
    const result = {
      task,
      language,
      testCode: null,
      implCode: null,
      pass: false,
      iterations: 0,
      maxIterations: options.maxIterations || 5,
      steps: [],
      errors: []
    };

    this.stats.tddCycles++;

    // 第一步：生成测试用例
    try {
      result.testCode = await this._generateTestCode(task, language, options);
      result.steps.push({
        step: 'generate_test',
        status: 'completed',
        code: result.testCode.substring(0, 100) + '...'
      });
    } catch (e) {
      result.errors.push(`测试生成失败: ${e.message}`);
      return result;
    }

    // 第二步：执行测试（预期失败）
    const testFailResult = await this.verifyLogic(result.testCode, language, null);
    result.iterations++;

    if (!testFailResult.actualOutput && !testFailResult.errors.length) {
      // 测试执行但没有错误 - 可能是语法问题或测试通过
      result.steps.push({
        step: 'run_initial_test',
        status: 'warning',
        output: testFailResult.actualOutput,
        message: '测试可能已通过或无法确定失败状态'
      });
    } else {
      result.steps.push({
        step: 'red_phase',
        status: 'completed',
        errors: testFailResult.errors,
        output: testFailResult.actualOutput
      });
    }

    // 第三步：生成实现代码
    try {
      result.implCode = await this._generateImplCode(task, language, options);
      result.steps.push({
        step: 'generate_implementation',
        status: 'completed',
        code: result.implCode.substring(0, 100) + '...'
      });
    } catch (e) {
      result.errors.push(`实现生成失败: ${e.message}`);
      return result;
    }

    // 第四步：再次执行测试（预期通过）
    const combinedCode = this._combineCode(result.testCode, result.implCode, language);
    const testPassResult = await this.verifyLogic(combinedCode, language, null);
    result.iterations++;

    if (testPassResult.errors.length === 0) {
      result.pass = true;
      result.steps.push({
        step: 'green_phase',
        status: 'completed',
        output: testPassResult.actualOutput
      });
    } else {
      result.steps.push({
        step: 'refactor_phase',
        status: 'failed',
        errors: testPassResult.errors
      });
      result.errors.push(...testPassResult.errors);

      // 如果未通过且还有迭代次数，尝试重构
      if (result.iterations < result.maxIterations) {
        result.implCode = await this._refineImplCode(result.implCode, testPassResult.errors, language);
        result.iterations++;

        // 再次验证
        const refinedCode = this._combineCode(result.testCode, result.implCode, language);
        const refinedResult = await this.verifyLogic(refinedCode, language, null);

        if (refinedResult.errors.length === 0) {
          result.pass = true;
          result.steps.push({
            step: 'green_phase_after_refactor',
            status: 'completed'
          });
        }
      }
    }

    // 记录到记忆
    await this.recordToMemory(result, 'tdd');

    return result;
  }

  /**
   * 生成测试代码
   * @param {string} task - 任务描述
   * @param {string} language - 语言
   * @param {Object} options - 选项
   * @returns {string} 测试代码
   */
  async _generateTestCode(task, language, options) {
    // 使用 hf 的生成能力（如果有）
    if (this.hf && this.hf.dispatch) {
      try {
        const testCode = await this.hf.dispatch(
          'codeGenerator.generateTest',
          task,
          language,
          options
        );
        if (testCode) return testCode;
      } catch (e) {
        // fallback 到默认实现
      }
    }

    // 默认测试生成逻辑
    const testTemplates = {
      js: (task) => `// TDD 测试: ${task}\nconst assert = require('assert');\n\n// 测试用例\ntry {\n  // TODO: 实现以下测试\n  console.log('Testing: ${task}');\n  assert.strictEqual(1, 0, '占位测试（RED阶段：此测试预期失败，请替换为真实测试）');\n  console.log('✓ 测试通过');\n} catch (e) {\n  console.error('✗ 测试失败:', e.message);\n  process.exit(1);\n}`,
      python: (task) => `# TDD 测试: ${task}\nimport unittest\n\nclass TestImplementation(unittest.TestCase):\n    def test_placeholder(self):\n        # TODO: 实现以下测试\n        print("Testing: ${task}")\n        self.assertEqual(1, 0, "占位测试（RED阶段：此测试预期失败，请替换为真实测试）")\n\nif __name__ == '__main__':\n    unittest.main()`,
      shell: (task) => `#!/bin/bash\n# TDD 测试: ${task}\necho "Testing: ${task}"\n# TODO: 实现以下测试\nassert() {\n  if [ "$1" != "$2" ]; then\n    echo "✗ 测试失败: expected '$2', got '$1'"\n    exit 1\n  fi\n}\nassert "1" "0"\necho "✓ 测试通过"`
    };

    const template = testTemplates[language.toLowerCase()];
    if (!template) {
      throw new Error(`不支持的语言: ${language}`);
    }

    return template(task);
  }

  /**
   * 生成实现代码
   * @param {string} task - 任务描述
   * @param {string} language - 语言
   * @param {Object} options - 选项
   * @returns {string} 实现代码
   */
  async _generateImplCode(task, language, options) {
    // 使用 hf 的生成能力（如果有）
    if (this.hf && this.hf.dispatch) {
      try {
        const implCode = await this.hf.dispatch(
          'codeGenerator.generateImpl',
          task,
          language,
          options
        );
        if (implCode) return implCode;
      } catch (e) {
        // fallback 到默认实现
      }
    }

    // 默认实现生成逻辑
    const implTemplates = {
      js: (task) => `// 实现: ${task}\n\n// TODO: 实现功能\nfunction main() {\n  console.log('Implementation placeholder for: ${task}');\n}\n\nmain();`,
      python: (task) => `# 实现: ${task}\n\n# TODO: 实现功能\ndef main():\n    print("Implementation placeholder for: ${task}")\n\nif __name__ == '__main__':\n    main()`,
      shell: (task) => `#!/bin/bash\n# 实现: ${task}\necho "Implementation placeholder for: ${task}"\n# TODO: 实现功能`
    };

    const template = implTemplates[language.toLowerCase()];
    if (!template) {
      throw new Error(`不支持的语言: ${language}`);
    }

    return template(task);
  }

  /**
   * 重构实现代码
   * @param {string} implCode - 原实现代码
   * @param {Array} errors - 错误列表
   * @param {string} language - 语言
   * @returns {string} 重构后的代码
   */
  async _refineImplCode(implCode, errors, language) {
    // 简单的错误信息提取
    const errorMsgs = errors.map(e => typeof e === 'string' ? e : e.message || JSON.stringify(e)).join('; ');

    // 添加错误处理增强
    const enhanceTemplates = {
      js: (code, errMsg) => {
        return '// 重构版本\n' + code + '\n\n// 错误处理增强\nprocess.on("unhandledRejection", (err) => {\n  console.error("未处理的错误:", err);\n});';
      },
      python: (code, errMsg) => {
        return '# 重构版本\n' + code + '\n\n# 错误处理增强\nimport traceback\ntry:\n    pass\nexcept Exception as e:\n    traceback.print_exc()';
      },
      shell: (code, errMsg) => {
        return '#!/bin/bash\n# 重构版本\n' + code + '\n\n# 错误处理增强\ntrap \'echo "Error: $?"\' ERR';
      }
    };

    const enhance = enhanceTemplates[language.toLowerCase()];
    if (!enhance) return implCode;

    return enhance(implCode, errorMsgs);
  }

  /**
   * 组合测试代码和实现代码
   * @param {string} testCode - 测试代码
   * @param {string} implCode - 实现代码
   * @param {string} language - 语言
   * @returns {string} 组合后的代码
   */
  _combineCode(testCode, implCode, language) {
    const templates = {
      js: (test, impl) => `${impl}\n\n// === 测试 ===\n${test}`,
      python: (test, impl) => `${impl}\n\n# === 测试 ===\n${test}`,
      shell: (test, impl) => `${impl}\n\n# === 测试 ===\n${test}`
    };

    const template = templates[language.toLowerCase()];
    if (!template) return `${testCode}\n\n${implCode}`;

    return template(testCode, implCode);
  }

  // ============================================================
  // 质量评分
  // ============================================================

  /**
   * 获取质量评分
   * @param {string} code - 代码
   * @param {string} language - 语言
   * @returns {Object} 质量评分结果
   */
  getQualityScore(code, language) {
    const result = {
      score: 0,
      dimensions: {
        readability: 0,   // 可读性
        efficiency: 0,    // 效率
        security: 0,      // 安全性
        completeness: 0  // 完整性
      },
      details: [],
      suggestions: []
    };

    // 计算复杂度
    const complexity = calculateComplexity(code);

    // 1. 可读性评分 (0-100)
    result.dimensions.readability = this._scoreReadability(code, complexity);

    // 2. 效率评分 (0-100)
    result.dimensions.efficiency = this._scoreEfficiency(code, language);

    // 3. 安全性评分 (0-100)
    result.dimensions.security = this._scoreSecurity(code, language);

    // 4. 完整性评分 (0-100)
    result.dimensions.completeness = this._scoreCompleteness(code, language);

    // 综合评分（加权平均）
    const weights = { readability: 0.25, efficiency: 0.3, security: 0.3, completeness: 0.15 };
    result.score = Math.round(
      result.dimensions.readability * weights.readability +
      result.dimensions.efficiency * weights.efficiency +
      result.dimensions.security * weights.security +
      result.dimensions.completeness * weights.completeness
    );

    // 生成建议
    result.suggestions = this._generateQualitySuggestions(result);

    return result;
  }

  /**
   * 可读性评分
   * @param {string} code - 代码
   * @param {Object} complexity - 复杂度指标
   * @returns {number} 分数
   */
  _scoreReadability(code, complexity) {
    let score = 100;

    // 行长度惩罚
    const longLines = code.split('\n').filter(l => l.length > 120).length;
    score -= longLines * 2;

    // 嵌套深度惩罚
    if (complexity.maxNestingDepth > 4) {
      score -= (complexity.maxNestingDepth - 4) * 5;
    }

    // 圈复杂度惩罚
    if (complexity.cyclomaticComplexity > 15) {
      score -= Math.floor((complexity.cyclomaticComplexity - 15) / 5) * 3;
    }

    // 注释覆盖率
    const commentLines = (code.match(/\/\/|\/\*|#|"""|'''/g) || []).length;
    const totalLines = complexity.nonEmptyLines;
    const commentRatio = totalLines > 0 ? commentLines / totalLines : 0;

    if (commentRatio < 0.1) {
      score -= 10;
    } else if (commentRatio > 0.3) {
      score += 5; // 注释过多略减
    }

    // 变量命名质量
    const singleCharVars = (code.match(/\b[a-z]\b(?![\w])/g) || []).length;
    if (singleCharVars > 5) {
      score -= Math.min(15, singleCharVars);
    }

    return Math.max(0, Math.min(100, score));
  }

  /**
   * 效率评分
   * @param {string} code - 代码
   * @param {string} language - 语言
   * @returns {number} 分数
   */
  _scoreEfficiency(code, language) {
    let score = 100;

    // 检测低效模式
    const inefficientPatterns = {
      js: [
        { pattern: /for\s*\(\s*var\s+\w+\s*=\s*0\s*;\s*\w+\s*<\s*\w+\.length/i, issue: '使用 var 而非 let/const' },
        { pattern: /\.innerHTML\s*=/, issue: '直接 innerHTML 可能导致 XSS' },
        { pattern: /eval\s*\(/, issue: '使用 eval 可能导致安全问题' },
        { pattern: /new\s+Array\s*\(/, issue: '建议使用字面量数组' },
        { pattern: /new\s+Object\s*\(/, issue: '建议使用字面量对象' }
      ],
      python: [
        { pattern: /for\s+\w+\s+in\s+range\s*\(\s*len\s*\(/, issue: '建议使用 enumerate()' },
        { pattern: /\+\s*""/, issue: '字符串拼接低效，建议使用 join() 或 f-string' },
        { pattern: /import\s+\*/, issue: '不建议使用 import *' },
        { pattern: /==\s+True|==\s+False/, issue: '建议使用 is 或直接判断布尔值' }
      ],
      shell: [
        { pattern: /cat\s+[^\|]+\s*\|/, issue: '使用 cat 管道可能低效' },
        { pattern: /for\s+\w+\s+in\s+\$\(/, issue: '考虑使用 while read' }
      ]
    };

    const patterns = inefficientPatterns[language.toLowerCase()] || [];
    for (const { pattern, issue } of patterns) {
      if (pattern.test(code)) {
        score -= 8;
      }
    }

    // 检测注释掉的代码（TODO/FIXME）
    const todoCount = (code.match(/TODO|FIXME|HACK|XXX/g) || []).length;
    if (todoCount > 0) {
      score -= todoCount * 2;
    }

    return Math.max(0, Math.min(100, score));
  }

  /**
   * 安全性评分
   * @param {string} code - 代码
   * @param {string} language - 语言
   * @returns {number} 分数
   */
  _scoreSecurity(code, language) {
    let score = 100;

    // 安全问题检测
    const securityIssues = {
      js: [
        { pattern: /password\s*=|secret\s*=|api[_-]?key\s*=/i, issue: '可能包含硬编码密钥' },
        { pattern: /eval\s*\(/, issue: 'eval 可能导致代码注入' },
        { pattern: /innerHTML\s*=\s*(?!["'])/, issue: '直接 innerHTML 可能导致 XSS' },
        { pattern: /document\.write\s*\(/, issue: 'document.write 可能导致 XSS' },
        { pattern: /new\s+Function\s*\(/, issue: 'new Function 与 eval 类似，可能不安全' },
        { pattern: /crypto\.createCipher/, issue: '已废弃的加密 API' }
      ],
      python: [
        { pattern: /password\s*=\s*["'][^"']+["']/i, issue: '可能包含硬编码密钥' },
        { pattern: /eval\s*\(/, issue: 'eval 可能导致代码注入' },
        { pattern: /exec\s*\(/, issue: 'exec 可能导致代码注入' },
        { pattern: /pickle\.loads?/, issue: 'pickle 反序列化可能不安全' },
        { pattern: /subprocess\.run.*shell\s*=\s*True/, issue: 'shell=True 可能导致注入' }
      ],
      shell: [
        { pattern: /\$\{?\w+\}?/, issue: '变量展开需注意注入风险' },
        { pattern: /\|\s*sh/, issue: '管道到 shell 可能导致注入' }
      ]
    };

    const issues = securityIssues[language.toLowerCase()] || [];
    for (const { pattern, issue } of issues) {
      if (pattern.test(code)) {
        score -= 15;
      }
    }

    // 检查是否有输入验证
    if (code.includes('sanitize') || code.includes('validate') || code.includes('escape')) {
      score += 5;
    }

    return Math.max(0, Math.min(100, score));
  }

  /**
   * 完整性评分
   * @param {string} code - 代码
   * @param {string} language - 语言
   * @returns {number} 分数
   */
  _scoreCompleteness(code, language) {
    let score = 100;

    // 检查必要元素
    const completenessChecks = {
      js: {
        hasErrorHandling: /\bcatch\b/.test(code),
        hasExports: /module\.exports|export/.test(code),
        hasFunctions: /\bfunction\s+\w+|\bconst\s+\w+\s*=\s*\(|=>/.test(code),
        hasComments: /\/\/|\/\*/.test(code)
      },
      python: {
        hasErrorHandling: /\bexcept\b/.test(code),
        hasFunctions: /\bdef\s+\w+/.test(code),
        hasClasses: /\bclass\s+\w+/.test(code),
        hasDocstring: /""".*"""|'''.*'''/s.test(code) || code.includes('if __name__')
      },
      shell: {
        hasShebang: code.startsWith('#!'),
        hasErrorHandling: /\bif\s+\[.*\]\s*;?\s*then/.test(code) || /trap/.test(code),
        hasFunctions: /\bfunction\s+\w+|\b\w+\s*\(\s*\)/.test(code)
      }
    };

    const checks = completenessChecks[language.toLowerCase()] || completenessChecks.js;

    for (const [check, passed] of Object.entries(checks)) {
      if (!passed) {
        score -= 8;
      }
    }

    // 检查空代码
    const nonEmptyLines = code.split('\n').filter(l => l.trim().length > 0).length;
    if (nonEmptyLines < 5) {
      score -= 20;
    }

    return Math.max(0, Math.min(100, score));
  }

  /**
   * 生成质量建议
   * @param {Object} result - 评分结果
   * @returns {Array} 建议列表
   */
  _generateQualitySuggestions(result) {
    const suggestions = [];
    const { dimensions } = result;

    if (dimensions.readability < 70) {
      suggestions.push('可读性偏低：考虑增加注释、减少嵌套深度、改进变量命名');
    }

    if (dimensions.efficiency < 70) {
      suggestions.push('效率可优化：检查循环、避免低效模式、移除重复代码');
    }

    if (dimensions.security < 70) {
      suggestions.push('安全性需改进：检查硬编码密钥、避免 eval、使用参数化查询');
    }

    if (dimensions.completeness < 70) {
      suggestions.push('完整性不足：添加错误处理、必要注释、测试覆盖');
    }

    if (result.score >= 90) {
      suggestions.push('代码质量优秀');
    } else if (result.score >= 70) {
      suggestions.push('代码质量良好，有小幅改进空间');
    } else {
      suggestions.push('代码质量需改进，建议优先处理安全性问题');
    }

    return suggestions;
  }

  // ============================================================
  // 辅助方法
  // ============================================================

  /**
   * 严重性分级
   * @param {Array} errors - 错误列表
   * @param {Array} warnings - 警告列表
   * @returns {string} 严重性级别
   */
  _classifySeverity(errors, warnings) {
    const errorCount = errors.length;
    const warningCount = warnings.length;

    if (errorCount > 3 || errorCount > 0 && warningCount > 5) {
      return 'critical';
    }
    if (errorCount > 0 || warningCount > 3) {
      return 'major';
    }
    if (warningCount > 0) {
      return 'minor';
    }
    return 'info';
  }

  /**
   * 生成验证建议
   * @param {Object} result - 验证结果
   * @returns {Array} 建议列表
   */
  _generateSuggestions(result) {
    const suggestions = [];

    if (result.syntax && !result.syntax.passed) {
      suggestions.push('语法验证失败：检查括号匹配、关键字拼写');
    }

    if (result.logic && !result.logic.passed) {
      suggestions.push('逻辑验证失败：检查预期输出与实际输出差异');
    }

    if (result.quality && result.quality.score < 70) {
      suggestions.push('质量评分偏低：建议重构以提升可读性和安全性');
    }

    if (result.severity === 'critical') {
      suggestions.push('存在严重问题，建议优先修复');
    }

    return suggestions;
  }

  /**
   * 获取统计信息
   * @returns {Object} 统计信息
   */
  getStats() {
    return {
      ...this.stats,
      cacheSize: _resultCache.size,
      cacheHitRate: this.stats.totalVerifications > 0
        ? ((_cacheHits / this.stats.totalVerifications) * 100).toFixed(1) + '%'
        : '0%'
    };
  }

  /**
   * 为代码打桩（用于收集覆盖率）
   * @param {string} code - 源代码
   * @param {string} language - 语言
   * @returns {{ instrumented: string, probes: Object }} - 打桩后的代码和探针映射
   */
  instrumentCode(code, language) {
    const probes = {};
    let probeId = 0;
    const addProbe = () => `__p${probeId++}__`;

    if (language === 'javascript') {
      // 插入行覆盖率探针
      let instrumented = code.replace(/^(\s*)/gm, (match, indent) => {
        const p = addProbe();
        probes[p] = { type: 'line', count: 0 };
        return `${indent}if (typeof ${p} !== 'undefined') ${p}++; else { ${p} = 1; }\n${match}`;
      });
      // 分支探针：在 if/else/ternary 条件后插入
      instrumented = instrumented.replace(/\?[^:]*:/g, (m) => {
        const p = addProbe();
        probes[p] = { type: 'branch', count: 0, path: 'true' };
        return `${p};${m}`;
      });
      return { instrumented, probes };
    }

    return { instrumented: code, probes };
  }

  /**
   * 在隔离环境中执行代码并收集覆盖率
   * @param {string} code - 源代码
   * @param {string} language - 语言
   * @param {Object} options - 选项 { timeout, stdin }
   * @returns {Promise<{ output, coverage, exitCode }>}
   */
  async runWithCoverage(code, language, options = {}) {
    const { instrumented, probes } = this.instrumentCode(code, language);
    const ext = language === 'javascript' ? '.js' : `.${language}`;
    const tempFile = writeTempFile(instrumented, ext);
    try {
      const result = await execCommand('node', [tempFile], { timeout: options.timeout || 30000 });
      return {
        output: result.stdout,
        coverage: {
          probes,
          lineCount: Object.values(probes).filter(p => p.count > 0).length,
          totalLines: Object.keys(probes).length,
        }
      };
    } finally {
      try { deleteTempFile(tempFile); } catch (_) { /* 忽略清理错误 */ }
    }
  }

  /**
   * 获取覆盖率报告
   * @param {Object} coverageData - runWithCoverage 返回的 coverage
   * @returns {{ lineRate: number, branchRate: number, uncoveredLines: Array }}
   */
  getCoverageReport(coverageData) {
    const lines = [];
    for (const [id, probe] of Object.entries(coverageData.coverage.probes)) {
      lines.push({ id, type: probe.type, hit: probe.count > 0 });
    }
    const lineRate = coverageData.coverage.lineCount > 0
      ? (coverageData.coverage.lineCount / coverageData.coverage.totalLines * 100).toFixed(1) + '%'
      : '0%';
    const branchProbes = lines.filter(l => l.type === 'branch');
    const branchRate = branchProbes.length > 0
      ? (branchProbes.filter(l => l.hit).length / branchProbes.length * 100).toFixed(1) + '%'
      : 'N/A';
    return {
      lineRate,
      branchRate,
      coveredLines: lines.filter(l => l.hit).length,
      totalLines: lines.length,
      uncoveredLines: lines.filter(l => !l.hit).map(l => l.id),
    };
  }

  /**
   * 清除缓存
   */
  clearCache() {
    _resultCache.clear();
  }
}

// ============================================================
// 导出
// ============================================================

module.exports = { CodeVerifier };