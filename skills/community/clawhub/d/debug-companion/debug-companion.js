/**
 * 调试伴侣 (Debug Companion) v1.0.0
 * 
 * 功能：根据错误信息/traceback 自动分析根因并给出修复建议
 * 工具：Tavily Search + Code Search
 */

const DEBUG_COMPANION = {
  name: '调试伴侣',
  version: '1.0.0',

  // 常见错误模式及对应语言
  errorPatterns: {
    python: {
      typeError: /TypeError:\s*(.+)/,
      valueError: /ValueError:\s*(.+)/,
      indexError: /IndexError:\s*(.+)/,
      keyError: /KeyError:\s*(.+)/,
      attributeError: /AttributeError:\s*(.+)/,
      importError: /(?:ImportError|ModuleNotFoundError):\s*(.+)/,
      syntaxError: /SyntaxError:\s*(.+)/,
      nameError: /NameError:\s*(.+)/,
      fileNotFoundError: /FileNotFoundError:\s*(.+)/
    },
    javascript: {
      typeError: /TypeError:\s*(.+)/,
      referenceError: /ReferenceError:\s*(.+)/,
      syntaxError: /SyntaxError:\s*(.+)/,
      rangeError: /RangeError:\s*(.+)/,
      uriError: /URIError:\s*(.+)/
    },
    java: {
      nullPointerException: /NullPointerException:\s*(.+)/,
      indexOutOfBounds: /IndexOutOfBoundsException:\s*(.+)/,
      illegalArgument: /IllegalArgumentException:\s*(.+)/,
      classNotFound: /ClassNotFoundException:\s*(.+)/
    }
  },

  // 错误描述库（常见错误的中文解释）
  errorExplanations: {
    'Cannot read property': '尝试访问一个 undefined 或 null 对象的属性',
    'is not defined': '变量或函数未定义，可能是拼写错误或作用域问题',
    'list index out of range': '访问的索引超出了列表/数组的长度',
    'KeyError': '字典/映射中不存在指定的键',
    'NullPointerException': '空指针异常，对象为 null 时调用了其方法',
    'ENOENT': '系统找不到指定的文件或目录',
    'Permission denied': '权限不足，无法访问该文件或执行该操作',
    'undefined is not a function': '尝试调用一个 undefined 的函数',
    'cannot read': '无法读取，通常是因为值为 null 或 undefined'
  },

  /**
   * 主分析函数
   * @param {string} errorInfo - 错误信息/traceback
   * @param {object} context - 上下文信息（可选）
   * @returns {object} 分析结果
   */
  async analyze(errorInfo, context = {}) {
    const result = {
      parsed: null,
      analysis: null,
      suggestions: [],
      references: []
    };

    // 1. 解析错误信息
    result.parsed = this.parseError(errorInfo);
    
    // 2. 生成根因分析
    result.analysis = this.analyzeRootCause(result.parsed, context);
    
    // 3. 获取修复建议和参考资料
    const searchResults = await this.searchSolutions(result.parsed, context);
    result.suggestions = searchResults.suggestions;
    result.references = searchResults.references;

    return result;
  },

  /**
   * 解析错误信息，提取关键信息
   */
  parseError(errorInfo) {
    const lines = errorInfo.trim().split('\n');
    const firstLine = lines[0];
    
    // 尝试识别编程语言
    const language = this.detectLanguage(errorInfo);
    
    // 提取错误类型和消息
    const errorTypeMatch = firstLine.match(/^([A-Z][a-zA-Z]+(?:Error|Exception|Error)):?\s*(.*)/);
    const errorType = errorTypeMatch ? errorTypeMatch[1] : 'UnknownError';
    const errorMessage = errorTypeMatch ? errorTypeMatch[2] : firstLine;
    
    // 提取文件路径和行号
    const filePathMatch = errorInfo.match(/File ["'](.+?)["'](?:,\s*line\s*(\d+))?/);
    const filePath = filePathMatch ? filePathMatch[1] : null;
    const lineNumber = filePathMatch && filePathMatch[2] ? filePathMatch[2] : null;
    
    // 提取函数名
    const functionMatch = errorInfo.match(/in\s+([a-zA-Z_][a-zA-Z0-9_]*)/);
    const functionName = functionMatch ? functionMatch[1] : null;

    return {
      raw: errorInfo,
      language,
      errorType,
      errorMessage,
      filePath,
      lineNumber,
      functionName,
      fullFirstLine: firstLine
    };
  },

  /**
   * 检测编程语言
   */
  detectLanguage(errorInfo) {
    if (errorInfo.includes('Python') || errorInfo.includes('Traceback') || 
        errorInfo.includes('File "<stdin>"') || errorInfo.match(/line \d+/)) {
      return 'python';
    }
    if (errorInfo.includes('JavaScript') || errorInfo.includes('ReferenceError') ||
        errorInfo.includes('TypeError') || errorInfo.includes('at ')) {
      return 'javascript';
    }
    if (errorInfo.includes('java.') || errorInfo.includes('Exception in thread')) {
      return 'java';
    }
    if (errorInfo.includes('go.') || errorInfo.includes('goroutine')) {
      return 'go';
    }
    if (errorInfo.includes('rust') || errorInfo.includes('panicked')) {
      return 'rust';
    }
    return 'unknown';
  },

  /**
   * 根因分析
   */
  analyzeRootCause(parsed, context = {}) {
    const { errorType, errorMessage, language } = parsed;
    
    // 使用已知错误描述库
    let explanation = null;
    for (const [pattern, desc] of Object.entries(this.errorExplanations)) {
      if (errorMessage.includes(pattern) || errorType.includes(pattern)) {
        explanation = desc;
        break;
      }
    }

    // 如果没有匹配，返回通用分析
    if (!explanation) {
      explanation = this.getGenericExplanation(errorType, errorMessage, language);
    }

    return {
      summary: explanation,
      language,
      likelyCauses: this.getLikelyCauses(errorType, errorMessage, language),
      context: context
    };
  },

  /**
   * 获取通用解释
   */
  getGenericExplanation(errorType, errorMessage, language) {
    const explanations = {
      TypeError: '类型错误，通常是操作了错误类型的数据',
      ValueError: '值错误，输入的数据不符合预期格式或范围',
      ReferenceError: '引用错误，变量或函数未在当前作用域声明',
      SyntaxError: '语法错误，代码不符合语言的语法规则',
      IndexError: '索引错误，访问的索引超出容器边界',
      KeyError: '键错误，字典/映射中不存在指定的键',
      AttributeError: '属性错误，对象没有该属性',
      ImportError: '导入错误，无法找到或导入指定的模块',
      NameError: '名称错误，变量名未定义或拼写错误',
      FileNotFoundError: '文件未找到错误，指定路径的文件不存在',
      NullPointerException: '空指针异常，对象为 null 时调用了其方法',
      RuntimeError: '运行时错误，程序执行过程中发生意外情况'
    };
    return explanations[errorType] || `遇到 ${errorType} 错误，需要进一步分析`;
  },

  /**
   * 获取可能的原因列表
   */
  getLikelyCauses(errorType, errorMessage, language) {
    const causes = [];
    
    if (errorType === 'TypeError') {
      causes.push('变量或表达式的类型不符合操作要求');
      causes.push('尝试对 undefined 或 null 调用方法');
      causes.push('函数返回值的类型与预期不符');
    }
    if (errorType === 'ReferenceError' || errorType === 'NameError') {
      causes.push('变量未声明或未赋值');
      causes.push('变量名拼写错误或大小写不匹配');
      causes.push('在函数外部访问了局部变量');
    }
    if (errorType === 'IndexError') {
      causes.push('循环索引超出列表长度');
      causes.push('数组下标计算错误');
      causes.push('空列表/数组访问索引 0');
    }
    if (errorType === 'FileNotFoundError' || errorType === 'ENOENT') {
      causes.push('文件路径错误');
      causes.push('当前工作目录不正确');
      causes.push('文件名或目录名拼写错误');
    }

    return causes;
  },

  /**
   * 搜索解决方案
   */
  async searchSolutions(parsed, context = {}) {
    const { errorType, errorMessage, language } = parsed;
    const suggestions = [];
    const references = [];

    // 构建搜索关键词
    const searchQuery = `${language || ''} ${errorType} ${errorMessage}`.trim().substring(0, 200);
    
    // 模拟 Tavily 搜索结果（实际使用时替换为真实 API 调用）
    const mockSearchResults = [
      {
        title: `${errorType} - 官方文档`,
        url: `https://docs.python.org/3/library/exceptions.html#${errorType}`,
        snippet: `官方异常说明文档`
      },
      {
        title: `Stack Overflow: ${errorType}解决方案`,
        url: `https://stackoverflow.com/questions/tagged/${errorType.toLowerCase()}`,
        snippet: '开发者社区讨论'
      }
    ];

    for (const result of mockSearchResults) {
      references.push({
        title: result.title,
        url: result.url,
        source: this.extractDomain(result.url)
      });
    }

    // 生成修复建议
    suggestions.push(...this.generateSuggestions(parsed));

    return { suggestions, references };
  },

  /**
   * 提取域名
   */
  extractDomain(url) {
    try {
      return new URL(url).hostname.replace('www.', '');
    } catch {
      return url;
    }
  },

  /**
   * 生成具体修复建议
   */
  generateSuggestions(parsed) {
    const { errorType, errorMessage, filePath, lineNumber } = parsed;
    const suggestions = [];

    if (errorType === 'TypeError') {
      if (errorMessage.includes('Cannot read')) {
        suggestions.push({
          step: '添加防御性检查',
          code: `if (data && data.property) {
  // 安全访问属性
}`,
          tip: '在使用属性前先检查对象是否存在'
        });
        suggestions.push({
          step: '使用可选链操作符',
          code: `const value = data?.property?.nested?.value;`,
          tip: '可选链操作符可以安全地访问深层属性'
        });
      }
    }

    if (errorType === 'ReferenceError' || errorType === 'NameError') {
      suggestions.push({
        step: '检查变量是否已声明',
        code: `// 确保变量在使用前已声明
const myVar = getValue(); // 或 let/var
console.log(myVar);`,
        tip: '检查变量名拼写是否正确，注意大小写'
      });
    }

    if (errorType === 'IndexError' || errorType === 'RangeError') {
      suggestions.push({
        step: '添加边界检查',
        code: `if (index >= 0 && index < array.length) {
  // 安全访问
  console.log(array[index]);
}`,
        tip: '访问数组元素前检查索引是否在有效范围内'
      });
    }

    if (errorType === 'FileNotFoundError' || errorType.includes('ENOENT')) {
      suggestions.push({
        step: '检查文件路径',
        code: `const fs = require('fs');
const path = require('path');

// 使用绝对路径
const filePath = path.join(__dirname, 'data.txt');

// 检查文件是否存在
if (fs.existsSync(filePath)) {
  const content = fs.readFileSync(filePath, 'utf8');
}`,
        tip: '使用 path.join 构建路径，检查文件是否存在'
      });
    }

    // 默认建议
    if (suggestions.length === 0) {
      suggestions.push({
        step: '查看官方文档',
        code: `// 搜索官方文档获取更多信息
// ${errorType}: ${errorMessage}`,
        tip: '查阅官方文档了解该错误的详细说明'
      });
    }

    return suggestions;
  },

  /**
   * 格式化输出结果
   */
  formatOutput(result) {
    const { parsed, analysis, suggestions, references } = result;

    let output = `## 🔍 错误解析\n`;
    output += `**错误类型**：${parsed.errorType}\n`;
    if (parsed.filePath) {
      output += `**问题文件**：${parsed.filePath}${parsed.lineNumber ? `:${parsed.lineNumber}` : ''}\n`;
    }
    if (parsed.functionName) {
      output += `**问题函数**：${parsed.functionName}\n`;
    }
    output += `**错误信息**：${parsed.errorMessage}\n\n`;

    output += `## 🎯 根因分析\n`;
    output += `**解释**：${analysis.summary}\n\n`;
    if (analysis.likelyCauses && analysis.likelyCauses.length > 0) {
      output += `**可能原因**：\n`;
      analysis.likelyCauses.forEach(cause => {
        output += `- ${cause}\n`;
      });
      output += '\n';
    }

    output += `## ✅ 修复建议\n`;
    suggestions.forEach((suggestion, index) => {
      output += `**${index + 1}. ${suggestion.step}**\n`;
      if (suggestion.code) {
        output += '```\n' + suggestion.code + '\n```\n';
      }
      if (suggestion.tip) {
        output += `💡 ${suggestion.tip}\n`;
      }
      output += '\n';
    });

    if (references && references.length > 0) {
      output += `## 📚 参考资料\n`;
      references.forEach(ref => {
        output += `- [${ref.title}](${ref.url}) - ${ref.source}\n`;
      });
    }

    return output;
  }
};

// 导出模块
module.exports = DEBUG_COMPANION;

// 如果直接运行，执行测试
if (require.main === module) {
  const testError = `TypeError: Cannot read property 'map' of undefined
    at processData (/app/utils.js:15:20)
    at handleRequest (/app/server.js:42:10)`;

  console.log('测试错误信息解析：');
  console.log(DEBUG_COMPANION.parseError(testError));
  console.log('\n生成修复建议：');
  console.log(DEBUG_COMPANION.generateSuggestions(DEBUG_COMPANION.parseError(testError)));
}
