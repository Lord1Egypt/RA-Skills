/**
 * 智能完整性分析器
 * 分析上下文文档的完整性和AI可执行性
 */

const fs = require('fs');
const path = require('path');

class CompletenessAnalyzer {
  constructor() {
    this.analysisRules = this.loadAnalysisRules();
  }

  /**
   * 分析上下文文档包的完整性
   * @param {Object} contextDocuments - 上下文文档路径对象
   * @returns {Object} 分析报告
   */
  analyzeContextDocuments(contextDocuments) {
    const report = {
      timestamp: new Date().toISOString(),
      documents: {},
      overallScore: 0,
      issues: [],
      recommendations: [],
      clarifications: []
    };

    // 分析每个文档
    if (contextDocuments.businessRules) {
      report.documents.businessRules = this.analyzeBusinessRules(contextDocuments.businessRules);
      this.mergeAnalysisResults(report, report.documents.businessRules);
    }

    if (contextDocuments.technicalSpecs) {
      report.documents.technicalSpecs = this.analyzeTechnicalSpecs(contextDocuments.technicalSpecs);
      this.mergeAnalysisResults(report, report.documents.technicalSpecs);
    }

    if (contextDocuments.validationStandards) {
      report.documents.validationStandards = this.analyzeValidationStandards(contextDocuments.validationStandards);
      this.mergeAnalysisResults(report, report.documents.validationStandards);
    }

    if (contextDocuments.integrationConfig) {
      report.documents.integrationConfig = this.analyzeIntegrationConfig(contextDocuments.integrationConfig);
      this.mergeAnalysisResults(report, report.documents.integrationConfig);
    }

    // 计算总体分数
    report.overallScore = this.calculateOverallScore(report.documents);

    // 生成澄清问题
    report.clarifications = this.generateClarificationQuestions(report.issues);

    return report;
  }

  /**
   * 分析业务规则文档
   */
  analyzeBusinessRules(filePath) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const rules = JSON.parse(content);
      
      const analysis = {
        filePath: filePath,
        format: 'valid',
        completeness: 0,
        executability: 0,
        issues: [],
        checks: {}
      };

      // 格式验证
      if (!rules.rules || !rules.domain) {
        analysis.format = 'invalid';
        analysis.issues.push({
          severity: 'high',
          category: 'format',
          description: 'JSON格式无效或缺少必需字段',
          location: 'root'
        });
        return analysis;
      }

      // 完整性检查
      const completenessChecks = this.performBusinessRulesCompletenessChecks(rules);
      analysis.completeness = this.calculateScore(completenessChecks);
      analysis.checks.completeness = completenessChecks;

      // 可执行性检查
      const executabilityChecks = this.performBusinessRulesExecutabilityChecks(rules);
      analysis.executability = this.calculateScore(executabilityChecks);
      analysis.checks.executability = executabilityChecks;

      // 合并问题
      analysis.issues = [
        ...this.extractIssuesFromChecks(completenessChecks),
        ...this.extractIssuesFromChecks(executabilityChecks)
      ];

      return analysis;

    } catch (error) {
      return {
        filePath: filePath,
        format: 'invalid',
        completeness: 0,
        executability: 0,
        issues: [{
          severity: 'high',
          category: 'format',
          description: `解析失败: ${error.message}`,
          location: 'file'
        }],
        checks: {}
      };
    }
  }

  /**
   * 执行业务规则完整性检查
   */
  performBusinessRulesCompletenessChecks(rules) {
    const checks = {
      constraints: {
        name: '约束条件完整性',
        passed: false,
        details: ''
      },
      validationRules: {
        name: '验证规则完整性', 
        passed: false,
        details: ''
      },
      stateTransitions: {
        name: '状态转换完整性',
        passed: false,
        details: ''
      },
      domainSpecific: {
        name: '领域特定规则完整性',
        passed: false,
        details: ''
      }
    };

    // 约束条件检查
    if (rules.rules.constraints && rules.rules.constraints.length > 0) {
      checks.constraints.passed = true;
      checks.constraints.details = `包含 ${rules.rules.constraints.length} 个约束条件`;
    } else {
      checks.constraints.details = '缺少约束条件定义';
    }

    // 验证规则检查
    if (rules.rules.validationRules && Object.keys(rules.rules.validationRules).length > 0) {
      checks.validationRules.passed = true;
      checks.validationRules.details = `包含 ${Object.keys(rules.rules.validationRules).length} 个验证规则`;
    } else {
      checks.validationRules.details = '缺少验证规则定义';
    }

    // 状态转换检查
    if (rules.rules.stateTransitions && Object.keys(rules.rules.stateTransitions).length > 0) {
      checks.stateTransitions.passed = true;
      checks.stateTransitions.details = `包含 ${Object.keys(rules.rules.stateTransitions).length} 个状态`;
      
      // 检查是否有终态
      const hasTerminalStates = Object.values(rules.rules.stateTransitions).some(transitions => transitions.length === 0);
      if (!hasTerminalStates) {
        checks.stateTransitions.passed = false;
        checks.stateTransitions.details += '，缺少终态定义';
      }
    } else {
      checks.stateTransitions.details = '缺少状态转换定义';
    }

    // 领域特定检查
    const domainChecks = this.performDomainSpecificBusinessRuleChecks(rules);
    checks.domainSpecific.passed = domainChecks.passed;
    checks.domainSpecific.details = domainChecks.details;

    return checks;
  }

  /**
   * 执行领域特定业务规则检查
   */
  performDomainSpecificBusinessRuleChecks(rules) {
    const domain = rules.domain;
    
    switch (domain) {
      case 'finance':
        return this.checkFinanceBusinessRules(rules.rules);
      case 'user':
        return this.checkUserBusinessRules(rules.rules);
      default:
        return { passed: true, details: '通用领域规则完整' };
    }
  }

  /**
   * 财务领域业务规则检查
   */
  checkFinanceBusinessRules(rules) {
    const issues = [];
    
    // 检查支付相关规则
    if (!rules.constraints.some(c => c.includes('支付') || c.includes('payment'))) {
      issues.push('缺少支付相关约束条件');
    }
    
    if (!rules.validationRules.amount) {
      issues.push('缺少金额验证规则');
    }
    
    if (!rules.stateTransitions.pending) {
      issues.push('缺少待支付状态定义');
    }
    
    // 检查发票相关规则
    if (!rules.constraints.some(c => c.includes('发票') || c.includes('invoice'))) {
      issues.push('缺少发票相关约束条件');
    }
    
    // 检查对账相关规则
    if (!rules.constraints.some(c => c.includes('对账') || c.includes('reconcile'))) {
      issues.push('缺少对账相关约束条件');
    }
    
    if (issues.length === 0) {
      return { passed: true, details: '财务业务规则完整' };
    } else {
      return { passed: false, details: issues.join('; ') };
    }
  }

  /**
   * 用户管理领域业务规则检查
   */
  checkUserBusinessRules(rules) {
    const issues = [];
    
    // 检查用户认证规则
    if (!rules.constraints.some(c => c.includes('密码') || c.includes('password'))) {
      issues.push('缺少密码相关约束条件');
    }
    
    if (!rules.validationRules.password) {
      issues.push('缺少密码验证规则');
    }
    
    // 检查权限相关规则
    if (!rules.constraints.some(c => c.includes('权限') || c.includes('permission'))) {
      issues.push('缺少权限相关约束条件');
    }
    
    // 检查状态管理
    if (!rules.stateTransitions.unverified) {
      issues.push('缺少未验证状态定义');
    }
    
    if (issues.length === 0) {
      return { passed: true, details: '用户管理业务规则完整' };
    } else {
      return { passed: false, details: issues.join('; ') };
    }
  }

  /**
   * 执行业务规则可执行性检查
   */
  performBusinessRulesExecutabilityChecks(rules) {
    const checks = {
      semanticClarity: {
        name: '语义清晰度',
        passed: true,
        details: '字段名称和规则描述清晰'
      },
      machineReadable: {
        name: '机器可读性',
        passed: true,
        details: '使用标准数据类型和枚举'
      },
      implementable: {
        name: '可实现性',
        passed: true,
        details: '规则可以被代码实现'
      }
    };

    // 语义清晰度检查
    Object.entries(rules.rules.validationRules).forEach(([field, rule]) => {
      if (typeof rule !== 'string' || rule.trim() === '') {
        checks.semanticClarity.passed = false;
        checks.semanticClarity.details = '存在空或无效的验证规则';
      }
    });

    // 机器可读性检查
    Object.entries(rules.rules.validationRules).forEach(([field, rule]) => {
      // 检查是否使用了标准规则格式
      const standardPatterns = ['positive', 'enum:', 'unique', 'email_format', 'range:', 'length:'];
      if (!standardPatterns.some(pattern => rule.includes(pattern))) {
        checks.machineReadable.passed = false;
        checks.machineReadable.details = '验证规则格式不标准，可能影响AI解析';
      }
    });

    return checks;
  }

  /**
   * 分析技术规格文档
   */
  analyzeTechnicalSpecs(filePath) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      // 这里简化处理，实际应解析YAML
      const specs = { content };
      
      const analysis = {
        filePath: filePath,
        format: 'valid',
        completeness: 0,
        executability: 0,
        issues: [],
        checks: {}
      };

      // 完整性检查（简化版）
      const completenessChecks = {
        dataModels: {
          name: '数据模型完整性',
          passed: content.includes('entities'),
          details: content.includes('entities') ? '包含数据模型定义' : '缺少数据模型定义'
        },
        apis: {
          name: 'API规范完整性',
          passed: content.includes('apis'),
          details: content.includes('apis') ? '包含API规范' : '缺少API规范'
        },
        integrations: {
          name: '集成点完整性',
          passed: content.includes('integrations'),
          details: content.includes('integrations') ? '包含集成点定义' : '缺少集成点定义'
        }
      };

      analysis.completeness = this.calculateScore(completenessChecks);
      analysis.checks.completeness = completenessChecks;

      // 可执行性检查
      const executabilityChecks = {
        fieldTypes: {
          name: '字段类型明确性',
          passed: !content.includes('type: String') || content.includes('type:') && content.split('type:').length > 1,
          details: '字段类型定义明确'
        },
        constraints: {
          name: '约束条件明确性',
          passed: content.includes('constraints'),
          details: content.includes('constraints') ? '包含约束条件' : '缺少约束条件'
        }
      };

      analysis.executability = this.calculateScore(executabilityChecks);
      analysis.checks.executability = executabilityChecks;

      // 合并问题
      analysis.issues = [
        ...this.extractIssuesFromChecks(completenessChecks),
        ...this.extractIssuesFromChecks(executabilityChecks)
      ];

      return analysis;

    } catch (error) {
      return {
        filePath: filePath,
        format: 'invalid',
        completeness: 0,
        executability: 0,
        issues: [{
          severity: 'high',
          category: 'format',
          description: `解析失败: ${error.message}`,
          location: 'file'
        }],
        checks: {}
      };
    }
  }

  /**
   * 分析验证标准文档
   */
  analyzeValidationStandards(filePath) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      
      const analysis = {
        filePath: filePath,
        format: 'valid',
        completeness: 0,
        executability: 0,
        issues: [],
        checks: {}
      };

      // 完整性检查
      const completenessChecks = {
        unitTests: {
          name: '单元测试覆盖',
          passed: content.includes('单元测试') || content.includes('unit test'),
          details: content.includes('单元测试') ? '包含单元测试要求' : '缺少单元测试要求'
        },
        integrationTests: {
          name: '集成测试覆盖',
          passed: content.includes('集成测试') || content.includes('integration test'),
          details: content.includes('集成测试') ? '包含集成测试要求' : '缺少集成测试要求'
        },
        securityTests: {
          name: '安全测试覆盖',
          passed: content.includes('安全测试') || content.includes('security test'),
          details: content.includes('安全测试') ? '包含安全测试要求' : '缺少安全测试要求'
        }
      };

      analysis.completeness = this.calculateScore(completenessChecks);
      analysis.checks.completeness = completenessChecks;

      // 可执行性检查
      const executabilityChecks = {
        coverageThreshold: {
          name: '覆盖率阈值明确',
          passed: /覆盖率.*[≥>]/.test(content) || /coverage.*[≥>]/.test(content),
          details: /覆盖率.*[≥>]/.test(content) ? '包含明确的覆盖率要求' : '缺少覆盖率阈值'
        },
        performanceCriteria: {
          name: '性能标准明确',
          passed: content.includes('响应时间') || content.includes('并发') || content.includes('performance'),
          details: content.includes('响应时间') ? '包含性能标准' : '缺少性能标准'
        }
      };

      analysis.executability = this.calculateScore(executabilityChecks);
      analysis.checks.executability = executabilityChecks;

      analysis.issues = [
        ...this.extractIssuesFromChecks(completenessChecks),
        ...this.extractIssuesFromChecks(executabilityChecks)
      ];

      return analysis;

    } catch (error) {
      return {
        filePath: filePath,
        format: 'invalid',
        completeness: 0,
        executability: 0,
        issues: [{
          severity: 'high',
          category: 'format',
          description: `读取失败: ${error.message}`,
          location: 'file'
        }],
        checks: {}
      };
    }
  }

  /**
   * 分析集成配置文档
   */
  analyzeIntegrationConfig(filePath) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const config = JSON.parse(content);
      
      const analysis = {
        filePath: filePath,
        format: 'valid',
        completeness: 0,
        executability: 0,
        issues: [],
        checks: {}
      };

      // 完整性检查
      const completenessChecks = {
        integrationsDefined: {
          name: '集成点定义',
          passed: config.integrations && config.integrations.length > 0,
          details: config.integrations ? `包含 ${config.integrations.length} 个集成点` : '缺少集成点定义'
        },
        timeoutConfigured: {
          name: '超时配置',
          passed: config.integrations?.every(int => int.timeout),
          details: '所有集成点都配置了超时'
        },
        retryConfigured: {
          name: '重试配置',
          passed: config.integrations?.every(int => int.retry),
          details: '所有集成点都配置了重试策略'
        }
      };

      analysis.completeness = this.calculateScore(completenessChecks);
      analysis.checks.completeness = completenessChecks;

      // 可执行性检查
      const executabilityChecks = {
        enabledFlag: {
          name: '启用标志',
          passed: config.integrations?.every(int => typeof int.enabled === 'boolean'),
          details: '所有集成点都有明确的启用状态'
        }
      };

      analysis.executability = this.calculateScore(executabilityChecks);
      analysis.checks.executability = executabilityChecks;

      analysis.issues = [
        ...this.extractIssuesFromChecks(completenessChecks),
        ...this.extractIssuesFromChecks(executabilityChecks)
      ];

      return analysis;

    } catch (error) {
      return {
        filePath: filePath,
        format: 'invalid',
        completeness: 0,
        executability: 0,
        issues: [{
          severity: 'high',
          category: 'format',
          description: `解析失败: ${error.message}`,
          location: 'file'
        }],
        checks: {}
      };
    }
  }

  /**
   * 计算检查分数
   */
  calculateScore(checks) {
    const total = Object.keys(checks).length;
    const passed = Object.values(checks).filter(check => check.passed).length;
    return total > 0 ? Math.round((passed / total) * 100) : 0;
  }

  /**
   * 从检查结果中提取问题
   */
  extractIssuesFromChecks(checks) {
    const issues = [];
    Object.values(checks).forEach(check => {
      if (!check.passed) {
        issues.push({
          severity: 'medium',
          category: 'completeness',
          description: `${check.name}: ${check.details}`,
          location: 'document'
        });
      }
    });
    return issues;
  }

  /**
   * 合并分析结果到总报告
   */
  mergeAnalysisResults(report, documentAnalysis) {
    report.issues.push(...documentAnalysis.issues);
  }

  /**
   * 计算总体分数
   */
  calculateOverallScore(documents) {
    const scores = Object.values(documents).map(doc => (doc.completeness + doc.executability) / 2);
    return scores.length > 0 ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 0;
  }

  /**
   * 生成澄清问题
   */
  generateClarificationQuestions(issues) {
    const clarifications = [];
    
    issues.forEach(issue => {
      if (issue.description.includes('缺少')) {
        const question = issue.description.replace('缺少', '需要提供什么') + '？';
        clarifications.push({
          priority: 'high',
          question: question,
          context: issue.location
        });
      } else if (issue.description.includes('无效') || issue.description.includes('失败')) {
        const question = '如何修正' + issue.description + '？';
        clarifications.push({
          priority: 'high',
          question: question,
          context: issue.location
        });
      }
    });

    return clarifications;
  }

  /**
   * 加载分析规则
   */
  loadAnalysisRules() {
    return {
      businessRules: {
        requiredFields: ['constraints', 'validationRules', 'stateTransitions'],
        minConstraints: 3,
        minValidationRules: 3,
        mustHaveTerminalStates: true
      },
      technicalSpecs: {
        requiredSections: ['entities', 'apis', 'integrations'],
        fieldRequirements: ['name', 'type', 'constraints']
      },
      validationStandards: {
        requiredTestTypes: ['unit', 'integration', 'security'],
        mustIncludeCoverage: true,
        mustIncludePerformance: true
      }
    };
  }

  /**
   * 生成分析报告摘要
   */
  generateReportSummary(report) {
    return {
      overallStatus: report.overallScore >= 80 ? '✅ 通过' : report.overallScore >= 60 ? '⚠️ 警告' : '❌ 失败',
      documentCount: Object.keys(report.documents).length,
      issueCount: report.issues.length,
      clarificationCount: report.clarifications.length,
      recommendations: this.generateRecommendations(report)
    };
  }

  /**
   * 生成建议
   */
  generateRecommendations(report) {
    const recommendations = [];
    
    if (report.overallScore < 80) {
      recommendations.push('需要完善文档内容以提高完整性');
    }
    
    if (report.clarifications.length > 0) {
      recommendations.push('需要回答澄清问题以确保AI正确理解');
    }
    
    if (report.issues.some(issue => issue.severity === 'high')) {
      recommendations.push('存在高优先级问题，建议在创建ClawTeam团队前解决');
    }
    
    return recommendations;
  }
}

module.exports = CompletenessAnalyzer;