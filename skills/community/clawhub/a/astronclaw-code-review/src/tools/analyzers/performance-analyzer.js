/**
 * 性能分析器
 * 检测潜在性能问题和优化机会
 */

// 性能规则定义
const PERFORMANCE_RULES = [
  {
    id: 'nested-loops',
    name: '嵌套循环',
    description: '多层嵌套循环可能导致性能问题',
    severity: 'warning',
    patterns: [
      /for\s*\([^)]*\)\s*\{[^{}]*for\s*\([^)]*\)/,
      /while\s*\([^)]*\)\s*\{[^{}]*while\s*\([^)]*\)/,
      /forEach.*?=>.*?\{[^{}]*forEach/
    ],
    check: (code) => {
      const issues = [];
      const lines = code.split('\n');
      
      // 简化的嵌套循环检测
      let inLoop = false;
      lines.forEach((line, lineNum) => {
        if (line.includes('for(') || line.includes('for (') || 
            line.includes('while(') || line.includes('forEach')) {
          if (inLoop) {
            issues.push({
              ruleId: 'nested-loops',
              message: '检测到可能的嵌套循环',
              line: lineNum + 1,
              severity: 'warning',
              suggestion: '考虑优化算法复杂度，或使用更高效的数据结构',
              complexity: 'O(n²) 或更高'
            });
          }
          inLoop = true;
        } else if (line.includes('}')) {
          inLoop = false;
        }
      });
      
      return issues;
    }
  },
  {
    id: 'large-array-creation',
    name: '大型数组操作',
    description: '在循环中创建大型数组或进行大量数组操作',
    severity: 'info',
    patterns: [
      /new Array\([0-9]{4,}\)/,
      /Array\([0-9]{4,}\)/,
      /\[\][\s\S]{0,100}\.push\([^)]*\)[\s\S]{0,100}for/
    ],
    check: (code) => {
      const issues = [];
      const lines = code.split('\n');
      
      lines.forEach((line, lineNum) => {
        if (/new Array\([0-9]{3,}\)/.test(line)) {
          const sizeMatch = line.match(/new Array\(([0-9]+)\)/);
          const size = sizeMatch ? parseInt(sizeMatch[1]) : 0;
          if (size > 1000) {
            issues.push({
              ruleId: 'large-array-creation',
              message: `创建大型数组 (${size} 个元素)`,
              line: lineNum + 1,
              severity: size > 10000 ? 'warning' : 'info',
              suggestion: '考虑使用分页或懒加载，避免一次性加载大量数据'
            });
          }
        }
      });
      
      return issues;
    }
  },
  {
    id: 'dom-manipulation-in-loop',
    name: '循环中的DOM操作',
    description: '在循环中频繁操作DOM，导致性能问题',
    severity: 'warning',
    patterns: [
      /for[^{]*\{[^}]*\.(?:innerHTML|appendChild|removeChild)[^}]*\}/,
      /forEach[^{]*\{[^}]*\.(?:innerHTML|appendChild|removeChild)[^}]*\}/
    ],
    check: (code) => {
      const issues = [];
      const lines = code.split('\n');
      
      // 简化检测：查找循环中的DOM操作
      let inLoop = false;
      let loopStart = -1;
      
      lines.forEach((line, lineNum) => {
        if (line.includes('for(') || line.includes('for (') || 
            line.includes('while(') || line.includes('forEach')) {
          inLoop = true;
          loopStart = lineNum;
        } else if (inLoop && (line.includes('.innerHTML') || 
                   line.includes('.appendChild') || 
                   line.includes('.removeChild'))) {
          issues.push({
            ruleId: 'dom-manipulation-in-loop',
            message: '在循环中操作DOM',
            line: lineNum + 1,
            severity: 'warning',
            suggestion: '考虑使用DocumentFragment或离线DOM操作，减少重绘重排',
            loopStart: loopStart + 1
          });
        } else if (line.includes('}')) {
          inLoop = false;
        }
      });
      
      return issues;
    }
  },
  {
    id: 'synchronous-io',
    name: '同步I/O操作',
    description: '在Node.js中使用同步文件操作阻塞事件循环',
    severity: 'warning',
    patterns: [
      /require\(['"]fs['"]\)[^]*?\.(?:readFileSync|writeFileSync|readdirSync)/,
      /fs\.(?:readFileSync|writeFileSync|readdirSync)/
    ],
    check: (code) => {
      const issues = [];
      const lines = code.split('\n');
      
      lines.forEach((line, lineNum) => {
        if (line.includes('Sync(') && (line.includes('fs.') || line.includes('require("fs")'))) {
          issues.push({
            ruleId: 'synchronous-io',
            message: '使用同步I/O操作',
            line: lineNum + 1,
            severity: 'warning',
            suggestion: '考虑使用异步版本（如readFile代替readFileSync）以避免阻塞事件循环'
          });
        }
      });
      
      return issues;
    }
  },
  {
    id: 'memory-leak-pattern',
    name: '内存泄漏模式',
    description: '可能导致内存泄漏的代码模式',
    severity: 'high',
    patterns: [
      /setInterval[^{]*\{[^}]*[^}]*\}[^)]*\)[^;]*;/,
      /addEventListener[^{]*\{[^}]*[^}]*\}[^)]*\)[^;]*;/
    ],
    check: (code) => {
      const issues = [];
      const lines = code.split('\n');
      
      lines.forEach((line, lineNum) => {
        if (line.includes('setInterval') && !line.includes('clearInterval')) {
          issues.push({
            ruleId: 'memory-leak-pattern',
            message: 'setInterval未保存返回值，可能导致无法清除',
            line: lineNum + 1,
            severity: 'high',
            suggestion: '保存setInterval返回值，在适当时机调用clearInterval'
          });
        }
        
        if (line.includes('addEventListener') && !line.includes('removeEventListener')) {
          issues.push({
            ruleId: 'memory-leak-pattern',
            message: '添加事件监听器但未移除',
            line: lineNum + 1,
            severity: 'warning',
            suggestion: '确保在适当时机调用removeEventListener'
          });
        }
      });
      
      return issues;
    }
  },
  {
    id: 'inefficient-string-concat',
    name: '低效字符串拼接',
    description: '在循环中使用字符串拼接而非数组join',
    severity: 'info',
    check: (code) => {
      const issues = [];
      const lines = code.split('\n');
      
      // 检测循环中的字符串拼接
      let inLoop = false;
      lines.forEach((line, lineNum) => {
        if (line.includes('for(') || line.includes('for (') || 
            line.includes('while(') || line.includes('forEach')) {
          inLoop = true;
        } else if (inLoop && line.includes('+=') && line.includes('"')) {
          issues.push({
            ruleId: 'inefficient-string-concat',
            message: '在循环中使用字符串拼接',
            line: lineNum + 1,
            severity: 'info',
            suggestion: '考虑使用数组push+join方式，性能更优'
          });
        } else if (line.includes('}')) {
          inLoop = false;
        }
      });
      
      return issues;
    }
  }
];

/**
 * 分析代码性能
 */
export async function analyzePerformance(code, options = {}) {
  console.log('⚡ 分析代码性能...');
  
  try {
    const issues = [];
    const startTime = Date.now();
    
    // 应用性能规则
    PERFORMANCE_RULES.forEach(rule => {
      try {
        const ruleIssues = rule.check(code);
        issues.push(...ruleIssues);
      } catch (error) {
        console.warn(`性能规则 ${rule.id} 执行失败:`, error.message);
      }
    });
    
    // 计算性能指标
    const performanceMetrics = calculatePerformanceMetrics(code);
    
    // 计算性能评分 (0-100)
    const score = calculatePerformanceScore(issues, performanceMetrics);
    
    const analysisTime = Date.now() - startTime;
    
    console.log(`✅ 性能分析完成: ${issues.length} 个问题，评分 ${score}/100`);
    
    return {
      score,
      issues,
      metrics: {
        ...performanceMetrics,
        analysisTime,
        rulesChecked: PERFORMANCE_RULES.length
      },
      summary: {
        totalIssues: issues.length,
        highIssues: issues.filter(i => i.severity === 'high').length,
        warningIssues: issues.filter(i => i.severity === 'warning').length,
        infoIssues: issues.filter(i => i.severity === 'info').length,
        byCategory: {
          loops: issues.filter(i => i.ruleId === 'nested-loops').length,
          memory: issues.filter(i => i.ruleId === 'memory-leak-pattern' || i.ruleId === 'large-array-creation').length,
          dom: issues.filter(i => i.ruleId === 'dom-manipulation-in-loop').length,
          io: issues.filter(i => i.ruleId === 'synchronous-io').length,
          strings: issues.filter(i => i.ruleId === 'inefficient-string-concat').length
        }
      }
    };
    
  } catch (error) {
    console.error('❌ 性能分析失败:', error.message);
    return {
      score: 0,
      issues: [],
      metrics: {},
      error: error.message
    };
  }
}

/**
 * 计算性能指标
 */
function calculatePerformanceMetrics(code) {
  const lines = code.split('\n');
  
  // 统计各种结构
  const loops = (code.match(/\bfor\s*\(/g) || []).length +
               (code.match(/\bwhile\s*\(/g) || []).length +
               (code.match(/\bforEach\b/g) || []).length;
  
  const domOperations = (code.match(/\.innerHTML/g) || []).length +
                       (code.match(/\.appendChild/g) || []).length +
                       (code.match(/\.removeChild/g) || []).length;
  
  const syncOperations = (code.match(/Sync\(/g) || []).length;
  
  const eventListeners = (code.match(/addEventListener/g) || []).length;
  
  const intervals = (code.match(/setInterval/g) || []).length;
  
  // 估算时间复杂度（简化）
  let complexityEstimate = 'O(n)';
  if (code.includes('for') && code.includes('for')) {
    complexityEstimate = 'O(n²) 或更高';
  }
  
  return {
    linesOfCode: lines.length,
    loops,
    domOperations,
    syncOperations,
    eventListeners,
    intervals,
    estimatedComplexity: complexityEstimate,
    potentialBottlenecks: identifyBottlenecks(code)
  };
}

/**
 * 识别性能瓶颈
 */
function identifyBottlenecks(code) {
  const bottlenecks = [];
  const lines = code.split('\n');
  
  lines.forEach((line, lineNum) => {
    // 检测可能的重计算
    if (line.includes('Math.') && (line.includes('for') || line.includes('while'))) {
      bottlenecks.push({
        line: lineNum + 1,
        type: 'recomputation',
        description: '循环中可能重复计算数学函数',
        suggestion: '考虑将计算结果缓存到循环外部'
      });
    }
    
    // 检测可能的重样式计算
    if (line.includes('.style.') && (line.includes('for') || line.includes('while'))) {
      bottlenecks.push({
        line: lineNum + 1,
        type: 'style-recalculation',
        description: '循环中修改元素样式',
        suggestion: '考虑批量修改样式或使用CSS类切换'
      });
    }
  });
  
  return bottlenecks.slice(0, 5); // 最多返回5个
}

/**
 * 计算性能评分
 */
function calculatePerformanceScore(issues, metrics) {
  let score = 100;
  
  // 根据性能问题扣分
  issues.forEach(issue => {
    switch (issue.severity) {
      case 'high':
        score -= 15;
        break;
      case 'warning':
        score -= 8;
        break;
      case 'info':
        score -= 2;
        break;
    }
  });
  
  // 根据指标扣分
  if (metrics.loops > 10) {
    score -= Math.min(10, (metrics.loops - 10) / 2);
  }
  
  if (metrics.domOperations > 5) {
    score -= Math.min(10, metrics.domOperations);
  }
  
  if (metrics.syncOperations > 3) {
    score -= Math.min(15, metrics.syncOperations * 5);
  }
  
  if (metrics.estimatedComplexity.includes('O(n²)')) {
    score -= 10;
  }
  
  if (metrics.potentialBottlenecks.length > 0) {
    score -= Math.min(10, metrics.potentialBottlenecks.length * 2);
  }
  
  return Math.max(0, Math.round(score));
}

/**
 * 获取性能优化建议
 */
export function getPerformanceOptimizationTips() {
  return [
    '避免在循环中操作DOM，使用DocumentFragment',
    '使用事件委托减少事件监听器数量',
    '对大量数据使用分页或虚拟滚动',
    '使用Web Worker处理CPU密集型任务',
    '懒加载非关键资源',
    '使用CSS动画替代JavaScript动画',
    '压缩和缓存静态资源',
    '使用CDN加速资源加载',
    '减少HTTP请求数量',
    '使用浏览器开发者工具分析性能瓶颈'
  ];
}