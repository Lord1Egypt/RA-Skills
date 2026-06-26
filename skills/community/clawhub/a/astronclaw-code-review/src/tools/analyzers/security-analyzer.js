/**
 * 安全分析器
 * 检测常见安全漏洞和风险模式
 */

// 安全规则定义
const SECURITY_RULES = [
  {
    id: 'hardcoded-secret',
    name: '硬编码密钥',
    description: '代码中硬编码了API密钥、密码等敏感信息',
    severity: 'critical',
    patterns: [
      /['"](?:api[_-]?key|secret|password|token|auth)[_-]?\w*['"]\s*[:=]\s*['"][^'"]{10,}['"]/i,
      /(?:password|passwd)\s*=\s*['"][^'"]+['"]/i,
      /secret[_-]?\w*\s*=\s*['"][^'"]+['"]/i,
      /token\s*=\s*['"][^'"]+['"]/i
    ],
    check: (code) => {
      const issues = [];
      const lines = code.split('\n');
      
      lines.forEach((line, lineNum) => {
        SECURITY_RULES[0].patterns.forEach(pattern => {
          if (pattern.test(line)) {
            issues.push({
              ruleId: 'hardcoded-secret',
              message: '检测到可能硬编码的敏感信息',
              line: lineNum + 1,
              severity: 'critical',
              suggestion: '使用环境变量或安全配置管理系统存储敏感信息',
              codeSnippet: line.trim().substring(0, 100)
            });
          }
        });
      });
      
      return issues;
    }
  },
  {
    id: 'sql-injection',
    name: 'SQL注入风险',
    description: '字符串拼接构建SQL查询，存在注入风险',
    severity: 'critical',
    patterns: [
      /(?:query|execute)\(.*?\$\{.*?\}.*?\)/,
      /(?:query|execute)\(.*?['"]\s*\+\s*\w+\s*\+\s*['"]/,
      /(?:query|execute)\(['"][^'"]*\$\{/,
      /\b(?:SELECT|INSERT|UPDATE|DELETE)\s+.*?\$\{/
    ],
    check: (code) => {
      const issues = [];
      const lines = code.split('\n');
      
      lines.forEach((line, lineNum) => {
        SECURITY_RULES[1].patterns.forEach(pattern => {
          if (pattern.test(line)) {
            issues.push({
              ruleId: 'sql-injection',
              message: '检测到可能的SQL注入风险',
              line: lineNum + 1,
              severity: 'critical',
              suggestion: '使用参数化查询或预编译语句',
              codeSnippet: line.trim().substring(0, 100)
            });
          }
        });
      });
      
      return issues;
    }
  },
  {
    id: 'xss-vulnerability',
    name: 'XSS跨站脚本风险',
    description: '未经验证的用户输入直接输出到HTML',
    severity: 'high',
    patterns: [
      /\.innerHTML\s*=\s*\w+/,
      /document\.write\(.*?\$/,
      /React\.createElement.*?dangerouslySetInnerHTML/,
      /<[^>]*>\$\{.*?\}<\/[^>]*>/
    ],
    check: (code) => {
      const issues = [];
      const lines = code.split('\n');
      
      lines.forEach((line, lineNum) => {
        SECURITY_RULES[2].patterns.forEach(pattern => {
          if (pattern.test(line)) {
            issues.push({
              ruleId: 'xss-vulnerability',
              message: '检测到可能的XSS跨站脚本风险',
              line: lineNum + 1,
              severity: 'high',
              suggestion: '对用户输入进行转义或使用安全的DOM操作API',
              codeSnippet: line.trim().substring(0, 100)
            });
          }
        });
      });
      
      return issues;
    }
  },
  {
    id: 'eval-usage',
    name: 'eval函数使用',
    description: '使用eval()函数执行动态代码，存在安全风险',
    severity: 'high',
    patterns: [
      /\beval\s*\(/,
      /\bFunction\s*\(/,
      /\bsetTimeout\s*\([^,)]*['"][^'"]*['"]/,
      /\bsetInterval\s*\([^,)]*['"][^'"]*['"]/
    ],
    check: (code) => {
      const issues = [];
      const lines = code.split('\n');
      
      lines.forEach((line, lineNum) => {
        SECURITY_RULES[3].patterns.forEach(pattern => {
          if (pattern.test(line)) {
            issues.push({
              ruleId: 'eval-usage',
              message: '检测到eval或类似函数的使用',
              line: lineNum + 1,
              severity: 'high',
              suggestion: '避免使用eval，考虑使用JSON.parse或更安全的替代方案',
              codeSnippet: line.trim().substring(0, 100)
            });
          }
        });
      });
      
      return issues;
    }
  },
  {
    id: 'insecure-random',
    name: '不安全的随机数生成',
    description: '使用Math.random()生成安全相关的随机数',
    severity: 'medium',
    patterns: [
      /Math\.random\(\)/,
      /Date\.now\(\)/
    ],
    check: (code) => {
      const issues = [];
      const lines = code.split('\n');
      
      lines.forEach((line, lineNum) => {
        if (/(?:password|token|key|secret).*Math\.random\(\)/.test(line)) {
          issues.push({
            ruleId: 'insecure-random',
            message: '使用不安全的随机数生成安全相关数据',
            line: lineNum + 1,
            severity: 'medium',
            suggestion: '对于安全相关随机数，使用crypto.getRandomValues()',
            codeSnippet: line.trim().substring(0, 100)
          });
        }
      });
      
      return issues;
    }
  }
];

/**
 * 分析代码安全性
 */
export async function analyzeSecurity(code, options = {}) {
  console.log('🛡️ 分析代码安全性...');
  
  try {
    const issues = [];
    const startTime = Date.now();
    
    // 应用安全规则
    SECURITY_RULES.forEach(rule => {
      try {
        const ruleIssues = rule.check(code);
        issues.push(...ruleIssues);
      } catch (error) {
        console.warn(`安全规则 ${rule.id} 执行失败:`, error.message);
      }
    });
    
    // 检测敏感信息（简化版）
    const sensitiveInfo = detectSensitiveInformation(code);
    issues.push(...sensitiveInfo);
    
    // 计算安全评分 (0-100)
    const score = calculateSecurityScore(issues);
    
    const analysisTime = Date.now() - startTime;
    
    console.log(`✅ 安全分析完成: ${issues.length} 个问题，评分 ${score}/100`);
    
    return {
      score,
      issues,
      metrics: {
        criticalIssues: issues.filter(i => i.severity === 'critical').length,
        highIssues: issues.filter(i => i.severity === 'high').length,
        mediumIssues: issues.filter(i => i.severity === 'medium').length,
        analysisTime,
        rulesChecked: SECURITY_RULES.length
      },
      summary: {
        totalIssues: issues.length,
        byCategory: {
          secrets: issues.filter(i => i.ruleId === 'hardcoded-secret').length,
          injection: issues.filter(i => i.ruleId === 'sql-injection').length,
          xss: issues.filter(i => i.ruleId === 'xss-vulnerability').length,
          eval: issues.filter(i => i.ruleId === 'eval-usage').length,
          random: issues.filter(i => i.ruleId === 'insecure-random').length
        }
      }
    };
    
  } catch (error) {
    console.error('❌ 安全分析失败:', error.message);
    return {
      score: 0,
      issues: [],
      metrics: {},
      error: error.message
    };
  }
}

/**
 * 检测敏感信息
 */
function detectSensitiveInformation(code) {
  const issues = [];
  const lines = code.split('\n');
  
  // 常见敏感信息模式
  const sensitivePatterns = [
    {
      pattern: /(['"])(?:https?:\/\/)?[^'"]*?(?:github|gitlab|bitbucket)[^'"]*?\/[^'"]*?\1/,
      message: '检测到可能的代码仓库URL',
      suggestion: '确保不包含敏感仓库信息'
    },
    {
      pattern: /(['"])[0-9]{9,}\1/,
      message: '检测到可能的身份证号或长数字',
      suggestion: '确保不包含个人身份信息'
    },
    {
      pattern: /(['"])[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\1/,
      message: '检测到可能的邮箱地址',
      suggestion: '确保不包含个人邮箱信息'
    },
    {
      pattern: /(['"])[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}\1/,
      message: '检测到可能的信用卡号',
      suggestion: '确保不包含支付卡信息'
    }
  ];
  
  lines.forEach((line, lineNum) => {
    sensitivePatterns.forEach(({ pattern, message, suggestion }) => {
      if (pattern.test(line)) {
        issues.push({
          ruleId: 'sensitive-info',
          message,
          line: lineNum + 1,
          severity: 'high',
          suggestion,
          codeSnippet: line.trim().substring(0, 100)
        });
      }
    });
  });
  
  return issues;
}

/**
 * 计算安全评分
 */
function calculateSecurityScore(issues) {
  let score = 100;
  
  // 根据安全问题严重程度扣分
  issues.forEach(issue => {
    switch (issue.severity) {
      case 'critical':
        score -= 20;
        break;
      case 'high':
        score -= 15;
        break;
      case 'medium':
        score -= 5;
        break;
      case 'low':
        score -= 1;
        break;
    }
  });
  
  // 关键安全问题直接不及格
  const criticalIssues = issues.filter(i => i.severity === 'critical').length;
  if (criticalIssues > 0) {
    score = Math.min(score, 60 - criticalIssues * 10);
  }
  
  return Math.max(0, Math.round(score));
}

/**
 * 获取安全最佳实践建议
 */
export function getSecurityBestPractices() {
  return [
    '使用环境变量存储敏感配置',
    '对所有用户输入进行验证和转义',
    '使用参数化查询防止SQL注入',
    '使用CSP（内容安全策略）防止XSS',
    '使用HTTPS传输敏感数据',
    '定期更新依赖包修复安全漏洞',
    '实施最小权限原则',
    '记录和监控安全事件',
    '定期进行安全审计和渗透测试',
    '使用安全的随机数生成器（crypto.getRandomValues）'
  ];
}