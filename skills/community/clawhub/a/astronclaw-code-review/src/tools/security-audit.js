/**
 * 安全审计工具
 */

import { analyzeSecurity, getSecurityBestPractices } from './analyzers/security-analyzer.js';

export class SecurityAuditTool {
  /**
   * 执行安全审计
   */
  static async execute(args, context) {
    const { filePath, code, options = {} } = args;
    
    console.log('🛡️ 执行安全审计...');
    
    try {
      // 获取代码内容
      const codeContent = await SecurityAuditTool.getCodeContent(filePath, code);
      if (!codeContent) {
        throw new Error('无法获取代码内容：请提供filePath或code参数');
      }
      
      // 执行安全分析
      const securityResult = await analyzeSecurity(codeContent, {
        filePath,
        ...options
      });
      
      // 生成安全报告
      const report = SecurityAuditTool.generateSecurityReport(securityResult, codeContent);
      
      console.log(`✅ 安全审计完成: ${filePath || '代码片段'}`);
      console.log(`   评分: ${securityResult.score}/100`);
      console.log(`   问题数: ${securityResult.issues.length}`);
      
      return {
        success: true,
        ...report,
        metadata: {
          analysisTime: securityResult.metrics.analysisTime,
          timestamp: new Date().toISOString(),
          config: context?.config || {}
        }
      };
      
    } catch (error) {
      console.error('❌ 安全审计失败:', error.message);
      return {
        success: false,
        error: {
          message: error.message,
          code: 'SECURITY_AUDIT_ERROR'
        },
        summary: {
          score: 0,
          issues: [],
          timestamp: new Date().toISOString()
        }
      };
    }
  }
  
  /**
   * 获取代码内容
   */
  static async getCodeContent(filePath, code) {
    if (code) {
      return code;
    }
    
    if (filePath) {
      try {
        const fs = await import('fs');
        return fs.readFileSync(filePath, 'utf-8');
      } catch (error) {
        throw new Error(`无法读取文件 ${filePath}: ${error.message}`);
      }
    }
    
    return null;
  }
  
  /**
   * 生成安全报告
   */
  static generateSecurityReport(securityResult, codeContent) {
    const { score, issues, metrics, summary } = securityResult;
    
    // 按严重程度和类别分组问题
    const issuesBySeverity = {
      critical: issues.filter(i => i.severity === 'critical'),
      high: issues.filter(i => i.severity === 'high'),
      medium: issues.filter(i => i.severity === 'medium'),
      low: issues.filter(i => i.severity === 'low')
    };
    
    const issuesByCategory = {};
    issues.forEach(issue => {
      const category = SecurityAuditTool.getIssueCategory(issue.ruleId);
      if (!issuesByCategory[category]) {
        issuesByCategory[category] = [];
      }
      issuesByCategory[category].push(issue);
    });
    
    // 风险评估
    const riskAssessment = SecurityAuditTool.assessSecurityRisk(issues, metrics);
    
    // 修复优先级
    const fixPriorities = SecurityAuditTool.prioritizeFixes(issues);
    
    // 安全最佳实践
    const bestPractices = getSecurityBestPractices();
    
    return {
      summary: {
        overallScore: score,
        riskLevel: riskAssessment.level,
        totalIssues: issues.length,
        criticalIssues: issuesBySeverity.critical.length,
        highIssues: issuesBySeverity.high.length,
        metrics: {
          analysisTime: metrics.analysisTime,
          rulesChecked: metrics.rulesChecked,
          vulnerabilitiesByType: summary.byCategory
        }
      },
      detailedAnalysis: {
        issues: issues.map(issue => ({
          ...issue,
          category: SecurityAuditTool.getIssueCategory(issue.ruleId),
          remediation: SecurityAuditTool.getRemediation(issue.ruleId)
        })),
        issuesBySeverity,
        issuesByCategory,
        topVulnerabilities: issues.slice(0, 10) // 最多显示10个漏洞
      },
      riskAssessment,
      remediationPlan: {
        priorities: fixPriorities,
        timeline: SecurityAuditTool.generateRemediationTimeline(fixPriorities),
        recommendations: SecurityAuditTool.generateSecurityRecommendations(issues, riskAssessment)
      },
      bestPractices,
      compliance: SecurityAuditTool.checkCompliance(issues)
    };
  }
  
  /**
   * 获取问题类别
   */
  static getIssueCategory(ruleId) {
    const categoryMap = {
      'hardcoded-secret': '敏感信息',
      'sql-injection': '注入攻击',
      'xss-vulnerability': '跨站脚本',
      'eval-usage': '代码执行',
      'insecure-random': '密码学安全',
      'sensitive-info': '数据泄露'
    };
    
    return categoryMap[ruleId] || '其他';
  }
  
  /**
   * 风险评估
   */
  static assessSecurityRisk(issues, metrics) {
    const criticalCount = issues.filter(i => i.severity === 'critical').length;
    const highCount = issues.filter(i => i.severity === 'high').length;
    
    let riskLevel = '低';
    let score = 100;
    
    if (criticalCount > 0) {
      riskLevel = '严重';
      score = Math.max(0, 40 - criticalCount * 10);
    } else if (highCount > 2) {
      riskLevel = '高';
      score = 50;
    } else if (highCount > 0 || issues.length > 5) {
      riskLevel = '中';
      score = 70;
    }
    
    return {
      level: riskLevel,
      score,
      factors: {
        criticalVulnerabilities: criticalCount,
        highVulnerabilities: highCount,
        totalVulnerabilities: issues.length,
        exposure: SecurityAuditTool.calculateExposure(issues)
      },
      impact: SecurityAuditTool.assessImpact(issues)
    };
  }
  
  /**
   * 计算暴露风险
   */
  static calculateExposure(issues) {
    // 简化的暴露风险计算
    const exposureFactors = {
      critical: 5,
      high: 3,
      medium: 2,
      low: 1
    };
    
    let totalExposure = 0;
    issues.forEach(issue => {
      totalExposure += exposureFactors[issue.severity] || 1;
    });
    
    if (totalExposure > 20) return '高';
    if (totalExposure > 10) return '中';
    return '低';
  }
  
  /**
   * 评估影响
   */
  static assessImpact(issues) {
    const impacts = {
      dataBreach: issues.some(i => i.ruleId === 'hardcoded-secret' || i.ruleId === 'sensitive-info'),
      systemCompromise: issues.some(i => i.ruleId === 'sql-injection' || i.ruleId === 'eval-usage'),
      userAffected: issues.some(i => i.ruleId === 'xss-vulnerability'),
      businessContinuity: false // 简化的评估
    };
    
    return impacts;
  }
  
  /**
   * 优先级排序修复
   */
  static prioritizeFixes(issues) {
    const priorities = {
      immediate: [],
      high: [],
      medium: [],
      low: []
    };
    
    issues.forEach(issue => {
      switch (issue.severity) {
        case 'critical':
          priorities.immediate.push({
            issue: issue.message,
            rule: issue.ruleId,
            line: issue.line,
            estimatedEffort: '1-2小时'
          });
          break;
        case 'high':
          priorities.high.push({
            issue: issue.message,
            rule: issue.ruleId,
            line: issue.line,
            estimatedEffort: '2-4小时'
          });
          break;
        case 'medium':
          priorities.medium.push({
            issue: issue.message,
            rule: issue.ruleId,
            line: issue.line,
            estimatedEffort: '4-8小时'
          });
          break;
        default:
          priorities.low.push({
            issue: issue.message,
            rule: issue.ruleId,
            line: issue.line,
            estimatedEffort: '1-2天'
          });
      }
    });
    
    return priorities;
  }
  
  /**
   * 生成修复时间线
   */
  static generateRemediationTimeline(priorities) {
    const timeline = [];
    
    if (priorities.immediate.length > 0) {
      timeline.push({
        phase: '立即修复 (24小时内)',
        tasks: priorities.immediate.length,
        focus: '关键安全问题'
      });
    }
    
    if (priorities.high.length > 0) {
      timeline.push({
        phase: '短期修复 (1周内)',
        tasks: priorities.high.length,
        focus: '高风险问题'
      });
    }
    
    if (priorities.medium.length > 0) {
      timeline.push({
        phase: '中期改进 (1个月内)',
        tasks: priorities.medium.length,
        focus: '中等风险问题'
      });
    }
    
    if (priorities.low.length > 0) {
      timeline.push({
        phase: '长期优化 (3个月内)',
        tasks: priorities.low.length,
        focus: '低风险问题和最佳实践'
      });
    }
    
    return timeline;
  }
  
  /**
   * 生成安全建议
   */
  static generateSecurityRecommendations(issues, riskAssessment) {
    const recommendations = [];
    
    if (riskAssessment.level === '严重' || riskAssessment.level === '高') {
      recommendations.push({
        type: '紧急',
        title: '立即安全加固',
        description: '系统存在严重安全风险',
        actions: [
          '立即修复所有关键漏洞',
          '暂停高风险功能',
          '加强安全监控',
          '进行渗透测试'
        ]
      });
    }
    
    if (issues.some(i => i.ruleId === 'hardcoded-secret')) {
      recommendations.push({
        type: '配置',
        title: '敏感信息管理',
        description: '改进敏感信息存储方式',
        actions: [
          '使用环境变量',
          '实施密钥管理服务',
          '定期轮换密钥',
          '实施访问控制'
        ]
      });
    }
    
    if (issues.some(i => i.ruleId === 'sql-injection' || i.ruleId === 'xss-vulnerability')) {
      recommendations.push({
        type: '输入验证',
        title: '加强输入验证',
        description: '防止注入攻击',
        actions: [
          '实施参数化查询',
          '输入验证和清理',
          '输出编码',
          '实施CSP策略'
        ]
      });
    }
    
    // 通用建议
    recommendations.push({
      type: '流程',
      title: '安全开发流程',
      description: '建立安全开发文化',
      actions: [
        '实施安全培训',
        '建立代码审查流程',
        '定期安全审计',
        '漏洞管理流程'
      ]
    });
    
    return recommendations;
  }
  
  /**
   * 获取修复方案
   */
  static getRemediation(ruleId) {
    const remediationMap = {
      'hardcoded-secret': '使用环境变量或密钥管理服务存储敏感信息',
      'sql-injection': '使用参数化查询或ORM框架，避免字符串拼接',
      'xss-vulnerability': '对用户输入进行转义，使用安全的DOM API',
      'eval-usage': '避免使用eval，使用JSON.parse或其他安全替代方案',
      'insecure-random': '使用crypto.getRandomValues生成安全随机数',
      'sensitive-info': '移除或加密敏感信息，实施访问控制'
    };
    
    return remediationMap[ruleId] || '参考安全最佳实践';
  }
  
  /**
   * 检查合规性
   */
  static checkCompliance(issues) {
    // 简化的合规性检查
    const standards = {
      'OWASP Top 10': !issues.some(i => 
        i.ruleId === 'sql-injection' || 
        i.ruleId === 'xss-vulnerability' ||
        i.ruleId === 'hardcoded-secret'
      ),
      'GDPR': !issues.some(i => i.ruleId === 'sensitive-info'),
      'PCI DSS': issues.length === 0, // 严格要求
      '基本安全': issues.filter(i => i.severity === 'critical' || i.severity === 'high').length === 0
    };
    
    return standards;
  }
}