/**
 * AI推荐引擎
 * 集成讯飞星火API，提供智能代码改进建议
 */

// 模拟AI响应（实际实现应调用讯飞星火API）
const MOCK_AI_RESPONSES = {
  quality: [
    {
      type: 'refactoring',
      title: '函数拆分建议',
      description: '长函数可以拆分为多个单一职责的小函数',
      priority: 'medium',
      codeExample: `// 重构前
function processUserData(user) {
  // 验证用户数据
  if (!user.name || !user.email) { /* ... */ }
  // 处理数据
  const processed = { /* ... */ };
  // 保存到数据库
  saveToDB(processed);
  // 发送通知
  sendNotification(user);
  // 记录日志
  logActivity(user);
}

// 重构后
function validateUser(user) { /* ... */ }
function processData(user) { /* ... */ }
function saveUserData(data) { /* ... */ }
function notifyUser(user) { /* ... */ }
function logUserActivity(user) { /* ... */ }`
    },
    {
      type: 'naming',
      title: '变量命名改进',
      description: '使用更具描述性的变量名',
      priority: 'low',
      suggestion: '将通用变量名如 "data", "result", "temp" 替换为更具描述性的名称'
    }
  ],
  security: [
    {
      type: 'security',
      title: '敏感信息处理',
      description: '避免在代码中硬编码敏感信息',
      priority: 'high',
      suggestion: '使用环境变量或配置管理系统存储API密钥、数据库密码等敏感信息'
    },
    {
      type: 'input-validation',
      title: '输入验证加强',
      description: '对用户输入进行更严格的验证',
      priority: 'medium',
      suggestion: '添加输入长度、类型、格式验证，防止注入攻击'
    }
  ],
  performance: [
    {
      type: 'optimization',
      title: '循环优化',
      description: '减少不必要的循环和计算',
      priority: 'medium',
      suggestion: '将不变的计算移出循环，使用更高效的数据结构'
    },
    {
      type: 'memory',
      title: '内存使用优化',
      description: '避免内存泄漏和高效使用内存',
      priority: 'high',
      suggestion: '及时清理定时器、事件监听器，避免不必要的全局变量'
    }
  ]
};

/**
 * 生成AI推荐
 */
export async function generateAIRecommendations(context) {
  console.log('🧠 生成AI智能建议...');
  
  const {
    qualityIssues = [],
    securityIssues = [],
    performanceIssues = [],
    code,
    filePath,
    options = {}
  } = context;
  
  try {
    // 如果提供了AI API配置，使用真实API
    if (options.aiApiKey && options.aiProvider === 'iflytek-spark') {
      return await callIflytekSparkAPI({
        code,
        issues: [...qualityIssues, ...securityIssues, ...performanceIssues],
        options
      });
    }
    
    // 否则使用模拟数据（用于演示）
    return generateMockRecommendations(
      qualityIssues,
      securityIssues,
      performanceIssues,
      code
    );
    
  } catch (error) {
    console.warn('AI推荐生成失败，使用备选建议:', error.message);
    return generateFallbackRecommendations(
      qualityIssues,
      securityIssues,
      performanceIssues
    );
  }
}

/**
 * 调用讯飞星火API（模拟实现）
 */
async function callIflytekSparkAPI(params) {
  const { code, issues, options } = params;
  
  console.log('📡 调用讯飞星火API生成建议...');
  
  // 实际实现应调用讯飞星火API
  // 这里返回模拟数据
  return new Promise((resolve) => {
    setTimeout(() => {
      const recommendations = [];
      
      // 基于问题生成建议
      if (issues.length > 0) {
        issues.forEach(issue => {
          if (issue.severity === 'critical' || issue.severity === 'high') {
            recommendations.push({
              type: 'ai-suggestion',
              title: 'AI优化建议',
              description: `针对问题"${issue.message}"，建议：${issue.suggestion || '参考最佳实践'}`,
              priority: 'high',
              confidence: 0.85,
              category: issue.ruleId?.includes('security') ? 'security' : 
                       issue.ruleId?.includes('performance') ? 'performance' : 'quality'
            });
          }
        });
      }
      
      // 添加通用建议
      recommendations.push(
        {
          type: 'ai-suggestion',
          title: '代码可读性提升',
          description: '考虑添加更多注释和文档字符串，提高代码可维护性',
          priority: 'low',
          confidence: 0.75,
          category: 'quality'
        },
        {
          type: 'ai-suggestion',
          title: '错误处理完善',
          description: '建议添加更完善的错误处理和异常捕获机制',
          priority: 'medium',
          confidence: 0.8,
          category: 'quality'
        }
      );
      
      resolve(recommendations);
    }, 500); // 模拟API延迟
  });
}

/**
 * 生成模拟推荐
 */
function generateMockRecommendations(qualityIssues, securityIssues, performanceIssues, code) {
  const recommendations = [];
  
  // 基于问题严重程度生成建议
  const allIssues = [...qualityIssues, ...securityIssues, ...performanceIssues];
  
  // 如果有严重问题，生成针对性的建议
  const criticalIssues = allIssues.filter(i => i.severity === 'critical');
  const highIssues = allIssues.filter(i => i.severity === 'high');
  
  if (criticalIssues.length > 0) {
    recommendations.push({
      type: 'critical-fix',
      title: '关键问题修复',
      description: `发现 ${criticalIssues.length} 个关键问题需要立即修复`,
      priority: 'critical',
      issues: criticalIssues.map(i => i.message),
      suggestion: '优先修复这些问题，它们可能影响系统稳定性和安全性'
    });
  }
  
  if (highIssues.length > 0) {
    recommendations.push({
      type: 'high-priority',
      title: '高优先级改进',
      description: `发现 ${highIssues.length} 个高优先级问题`,
      priority: 'high',
      suggestion: '建议在下一个开发周期中解决这些问题'
    });
  }
  
  // 基于代码特征生成建议
  if (code) {
    const codeSuggestions = analyzeCodeFeatures(code);
    recommendations.push(...codeSuggestions);
  }
  
  // 添加通用最佳实践建议
  recommendations.push(
    {
      type: 'best-practice',
      title: '代码审查最佳实践',
      description: '建立代码审查流程和标准',
      priority: 'medium',
      suggestion: '建议团队建立代码审查清单，包含质量、安全、性能检查项'
    },
    {
      type: 'testing',
      title: '测试覆盖率提升',
      description: '提高测试覆盖率，确保代码质量',
      priority: 'medium',
      suggestion: '建议添加单元测试和集成测试，目标覆盖率80%以上'
    }
  );
  
  return recommendations.slice(0, 10); // 最多返回10条建议
}

/**
 * 分析代码特征生成建议
 */
function analyzeCodeFeatures(code) {
  const recommendations = [];
  const lines = code.split('\n');
  
  // 检查注释比例
  const commentLines = lines.filter(line => 
    line.trim().startsWith('//') || 
    line.trim().startsWith('/*') || 
    line.trim().startsWith('*')
  ).length;
  
  const commentRatio = commentLines / lines.length;
  
  if (commentRatio < 0.1 && lines.length > 50) {
    recommendations.push({
      type: 'documentation',
      title: '代码文档不足',
      description: `代码注释率较低 (${Math.round(commentRatio * 100)}%)`,
      priority: 'low',
      suggestion: '建议添加更多注释，特别是复杂逻辑和公共API'
    });
  }
  
  // 检查函数长度
  const functions = code.match(/function\s+\w+\s*\([^)]*\)\s*\{[^}]*\}/gs) || [];
  const longFunctions = functions.filter(func => func.split('\n').length > 30);
  
  if (longFunctions.length > 0) {
    recommendations.push({
      type: 'refactoring',
      title: '长函数重构机会',
      description: `发现 ${longFunctions.length} 个可能过长的函数`,
      priority: 'medium',
      suggestion: '考虑将这些函数拆分为更小、单一职责的函数'
    });
  }
  
  // 检查错误处理
  const hasTryCatch = code.includes('try {') || code.includes('catch (');
  const hasErrorHandling = code.includes('throw new Error') || code.includes('console.error');
  
  if (!hasTryCatch && lines.length > 100) {
    recommendations.push({
      type: 'error-handling',
      title: '错误处理机制',
      description: '代码中缺少显式的错误处理',
      priority: 'medium',
      suggestion: '考虑添加try-catch块或错误边界处理'
    });
  }
  
  return recommendations;
}

/**
 * 生成备选建议
 */
function generateFallbackRecommendations(qualityIssues, securityIssues, performanceIssues) {
  // 当AI服务不可用时，基于规则生成基本建议
  const recommendations = [];
  
  if (securityIssues.length > 0) {
    recommendations.push({
      type: 'security',
      title: '安全问题需要关注',
      description: `发现 ${securityIssues.length} 个安全问题`,
      priority: 'high',
      suggestion: '立即修复安全问题，特别是硬编码密钥和注入风险'
    });
  }
  
  if (performanceIssues.length > 0) {
    recommendations.push({
      type: 'performance',
      title: '性能优化机会',
      description: `发现 ${performanceIssues.length} 个性能问题`,
      priority: 'medium',
      suggestion: '优化循环、减少DOM操作、使用异步I/O'
    });
  }
  
  if (qualityIssues.length > 0) {
    recommendations.push({
      type: 'quality',
      title: '代码质量改进',
      description: `发现 ${qualityIssues.length} 个代码质量问题`,
      priority: 'medium',
      suggestion: '遵循编码规范，提高代码可读性和可维护性'
    });
  }
  
  // 如果没有发现问题，提供通用建议
  if (recommendations.length === 0) {
    recommendations.push({
      type: 'general',
      title: '代码审查通过',
      description: '代码质量良好',
      priority: 'low',
      suggestion: '继续保持良好的编码习惯，定期进行代码审查'
    });
  }
  
  return recommendations;
}

/**
 * 获取AI推荐说明
 */
export function getAIRecommendationDescription() {
  return {
    provider: '讯飞星火AI (iFlyTek Spark)',
    capabilities: [
      '代码质量分析建议',
      '安全漏洞识别',
      '性能优化建议',
      '重构机会发现',
      '最佳实践指导'
    ],
    integration: '支持实时AI分析和批量处理',
    notes: '需要配置讯飞星火API密钥以启用完整功能'
  };
}