/**
 * 代码质量分析器
 * 分析代码规范、复杂度、重复代码等
 */

// 简单代码质量规则
const QUALITY_RULES = [
  {
    id: 'long-function',
    name: '函数过长',
    description: '函数体超过50行，建议拆分',
    severity: 'warning',
    pattern: /function\s+\w+\s*\([^)]*\)\s*\{[^}]*(?:\n[^\}]*){50,}\}/,
    check: (code) => {
      const functions = code.match(/function\s+\w+\s*\([^)]*\)\s*\{[^}]*\}/gs) || [];
      const issues = [];
      
      functions.forEach((func, index) => {
        const lines = func.split('\n').length;
        if (lines > 50) {
          issues.push({
            ruleId: 'long-function',
            message: `函数过长 (${lines}行)，建议拆分为更小的函数`,
            line: findLineNumber(code, func),
            severity: 'warning',
            suggestion: '考虑将函数拆分为多个单一职责的小函数'
          });
        }
      });
      
      return issues;
    }
  },
  {
    id: 'complex-condition',
    name: '复杂条件判断',
    description: '条件判断过于复杂，建议简化',
    severity: 'info',
    pattern: /if\s*\([^)]{100,}\)/,
    check: (code) => {
      const matches = code.match(/if\s*\([^)]+\)/g) || [];
      const issues = [];
      
      matches.forEach((condition, index) => {
        if (condition.length > 100) {
          issues.push({
            ruleId: 'complex-condition',
            message: '条件判断过于复杂，可读性差',
            line: findLineNumber(code, condition),
            severity: 'info',
            suggestion: '考虑将复杂条件拆分为多个布尔变量或函数'
          });
        }
      });
      
      return issues;
    }
  },
  {
    id: 'deep-nesting',
    name: '嵌套过深',
    description: '代码嵌套层次超过3层',
    severity: 'warning',
    pattern: /\{[^{}]*\{[^{}]*\{[^{}]*\{[^{}]*/,
    check: (code) => {
      // 简化的嵌套检查
      const lines = code.split('\n');
      const issues = [];
      
      lines.forEach((line, lineNum) => {
        const openBraces = (line.match(/\{/g) || []).length;
        // 这只是简单示例，实际需要更复杂的嵌套分析
        if (openBraces > 2) {
          issues.push({
            ruleId: 'deep-nesting',
            message: '代码块嵌套可能过深',
            line: lineNum + 1,
            severity: 'warning',
            suggestion: '考虑提取嵌套代码到独立函数'
          });
        }
      });
      
      return issues;
    }
  },
  {
    id: 'magic-number',
    name: '魔数',
    description: '代码中使用未命名的数字常量',
    severity: 'info',
    pattern: /[^a-zA-Z0-9_]([0-9]{2,})[^a-zA-Z0-9_]/,
    check: (code) => {
      // 寻找魔数（非0、1、-1的裸数字）
      const magicNumbers = code.match(/(?<![a-zA-Z0-9_])([2-9][0-9]*|-?[2-9])(?![a-zA-Z0-9_])/g) || [];
      const issues = [];
      
      magicNumbers.forEach((number, index) => {
        issues.push({
          ruleId: 'magic-number',
          message: `使用魔数: ${number}`,
          line: findLineNumber(code, number),
          severity: 'info',
          suggestion: `考虑将 ${number} 定义为有意义的常量`
        });
      });
      
      return issues;
    }
  }
];

/**
 * 分析代码质量
 */
export async function analyzeCodeQuality(code, options = {}) {
  console.log('📊 分析代码质量...');
  
  try {
    const issues = [];
    const startTime = Date.now();
    
    // 应用质量规则
    QUALITY_RULES.forEach(rule => {
      try {
        const ruleIssues = rule.check(code);
        issues.push(...ruleIssues);
      } catch (error) {
        console.warn(`规则 ${rule.id} 执行失败:`, error.message);
      }
    });
    
    // 计算复杂度指标（简化版）
    const complexityMetrics = calculateComplexity(code);
    
    // 检测重复代码（简化版）
    const duplicateCode = detectDuplicateCode(code);
    
    // 计算质量评分 (0-100)
    const score = calculateQualityScore(issues, complexityMetrics);
    
    const analysisTime = Date.now() - startTime;
    
    console.log(`✅ 质量分析完成: ${issues.length} 个问题，评分 ${score}/100`);
    
    return {
      score,
      issues,
      metrics: {
        ...complexityMetrics,
        duplicateBlocks: duplicateCode.length,
        analysisTime
      },
      summary: {
        totalIssues: issues.length,
        criticalIssues: issues.filter(i => i.severity === 'critical').length,
        warningIssues: issues.filter(i => i.severity === 'warning').length,
        infoIssues: issues.filter(i => i.severity === 'info').length
      }
    };
    
  } catch (error) {
    console.error('❌ 质量分析失败:', error.message);
    return {
      score: 0,
      issues: [],
      metrics: {},
      error: error.message
    };
  }
}

/**
 * 计算复杂度指标
 */
function calculateComplexity(code) {
  const lines = code.split('\n');
  
  // 简单复杂度估算
  const functions = (code.match(/function\s+\w+\s*\(/g) || []).length +
                   (code.match(/\bconst\s+\w+\s*=\s*\(/g) || []).length +
                   (code.match(/\blet\s+\w+\s*=\s*\(/g) || []).length;
  
  const conditionals = (code.match(/\bif\s*\(/g) || []).length +
                      (code.match(/\belse\b/g) || []).length +
                      (code.match(/\bswitch\s*\(/g) || []).length;
  
  const loops = (code.match(/\bfor\s*\(/g) || []).length +
               (code.match(/\bwhile\s*\(/g) || []).length +
               (code.match(/\bdo\s*\{/g) || []).length;
  
  return {
    linesOfCode: lines.length,
    functions,
    conditionals,
    loops,
    averageFunctionLength: functions > 0 ? Math.round(lines.length / functions) : 0,
    complexityScore: Math.min(100, Math.round((conditionals + loops) * 10))
  };
}

/**
 * 检测重复代码（简化版）
 */
function detectDuplicateCode(code) {
  const lines = code.split('\n');
  const duplicates = [];
  
  // 简单检测：相同的行（忽略空行和简单行）
  const lineCounts = {};
  lines.forEach(line => {
    const trimmed = line.trim();
    if (trimmed.length > 10 && !trimmed.startsWith('//') && !trimmed.startsWith('/*')) {
      lineCounts[trimmed] = (lineCounts[trimmed] || 0) + 1;
    }
  });
  
  // 找出重复的行
  Object.entries(lineCounts).forEach(([line, count]) => {
    if (count > 2) { // 出现2次以上
      duplicates.push({
        line,
        count,
        suggestion: '考虑提取重复代码到函数'
      });
    }
  });
  
  return duplicates.slice(0, 10); // 最多返回10个
}

/**
 * 计算质量评分
 */
function calculateQualityScore(issues, metrics) {
  let score = 100;
  
  // 根据问题扣分
  issues.forEach(issue => {
    switch (issue.severity) {
      case 'critical':
        score -= 10;
        break;
      case 'warning':
        score -= 5;
        break;
      case 'info':
        score -= 1;
        break;
    }
  });
  
  // 根据复杂度扣分
  if (metrics.complexityScore > 50) {
    score -= Math.min(20, (metrics.complexityScore - 50) / 5);
  }
  
  // 根据重复代码扣分
  if (metrics.duplicateBlocks > 5) {
    score -= Math.min(15, metrics.duplicateBlocks);
  }
  
  // 根据函数长度扣分
  if (metrics.averageFunctionLength > 30) {
    score -= Math.min(10, (metrics.averageFunctionLength - 30) / 5);
  }
  
  return Math.max(0, Math.round(score));
}

/**
 * 查找字符串在代码中的行号
 */
function findLineNumber(code, substring) {
  const lines = code.split('\n');
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes(substring)) {
      return i + 1;
    }
  }
  return 1;
}

// 导出辅助函数
export { findLineNumber };