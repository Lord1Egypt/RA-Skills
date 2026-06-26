/**
 * 代码质量专项扫描工具
 */

import { analyzeCodeQuality } from './analyzers/quality-analyzer.js';

export class CodeQualityScanner {
  /**
   * 执行代码质量扫描
   */
  static async execute(args, context) {
    const { filePath, code, options = {} } = args;
    
    console.log('📊 执行代码质量专项扫描...');
    
    try {
      // 获取代码内容
      const codeContent = await CodeQualityScanner.getCodeContent(filePath, code);
      if (!codeContent) {
        throw new Error('无法获取代码内容：请提供filePath或code参数');
      }
      
      // 执行质量分析
      const qualityResult = await analyzeCodeQuality(codeContent, {
        filePath,
        ...options
      });
      
      // 生成详细报告
      const report = CodeQualityScanner.generateQualityReport(qualityResult, codeContent);
      
      console.log(`✅ 代码质量扫描完成: ${filePath || '代码片段'}`);
      console.log(`   评分: ${qualityResult.score}/100`);
      console.log(`   问题数: ${qualityResult.issues.length}`);
      
      return {
        success: true,
        ...report,
        metadata: {
          analysisTime: qualityResult.metrics.analysisTime,
          timestamp: new Date().toISOString(),
          config: context?.config || {}
        }
      };
      
    } catch (error) {
      console.error('❌ 代码质量扫描失败:', error.message);
      return {
        success: false,
        error: {
          message: error.message,
          code: 'QUALITY_SCAN_ERROR'
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
   * 生成质量报告
   */
  static generateQualityReport(qualityResult, codeContent) {
    const { score, issues, metrics, summary } = qualityResult;
    
    // 按严重程度分组问题
    const issuesBySeverity = {
      critical: issues.filter(i => i.severity === 'critical'),
      warning: issues.filter(i => i.severity === 'warning'),
      info: issues.filter(i => i.severity === 'info')
    };
    
    // 按规则类型分组
    const issuesByRule = {};
    issues.forEach(issue => {
      if (!issuesByRule[issue.ruleId]) {
        issuesByRule[issue.ruleId] = [];
      }
      issuesByRule[issue.ruleId].push(issue);
    });
    
    // 生成改进建议
    const improvementSuggestions = CodeQualityScanner.generateImprovementSuggestions(issues, metrics);
    
    return {
      summary: {
        overallScore: score,
        grade: CodeQualityScanner.getGradeFromScore(score),
        totalIssues: issues.length,
        issuesBySeverity: {
          critical: issuesBySeverity.critical.length,
          warning: issuesBySeverity.warning.length,
          info: issuesBySeverity.info.length
        },
        metrics: {
          linesOfCode: metrics.linesOfCode,
          functions: metrics.functions,
          complexityScore: metrics.complexityScore,
          duplicateBlocks: metrics.duplicateBlocks
        }
      },
      detailedAnalysis: {
        issues: issues.map(issue => ({
          ...issue,
          suggestion: issue.suggestion || CodeQualityScanner.getDefaultSuggestion(issue.ruleId)
        })),
        issuesByRule,
        topIssues: issues.slice(0, 10) // 最多显示10个问题
      },
      improvementSuggestions,
      visualization: {
        scoreBreakdown: CodeQualityScanner.calculateScoreBreakdown(issues, metrics),
        trendAnalysis: CodeQualityScanner.analyzeQualityTrend(issues, metrics)
      }
    };
  }
  
  /**
   * 根据评分获取等级
   */
  static getGradeFromScore(score) {
    if (score >= 90) return 'A (优秀)';
    if (score >= 80) return 'B (良好)';
    if (score >= 70) return 'C (中等)';
    if (score >= 60) return 'D (及格)';
    return 'F (不及格)';
  }
  
  /**
   * 生成改进建议
   */
  static generateImprovementSuggestions(issues, metrics) {
    const suggestions = [];
    
    // 基于问题类型的建议
    const criticalIssues = issues.filter(i => i.severity === 'critical');
    if (criticalIssues.length > 0) {
      suggestions.push({
        priority: 'high',
        title: '修复关键问题',
        description: `立即修复 ${criticalIssues.length} 个关键问题`,
        actions: criticalIssues.map(issue => ({
          rule: issue.ruleId,
          description: issue.message,
          suggestion: issue.suggestion
        }))
      });
    }
    
    // 基于复杂度的建议
    if (metrics.complexityScore > 50) {
      suggestions.push({
        priority: 'medium',
        title: '降低代码复杂度',
        description: `代码复杂度较高 (${metrics.complexityScore})`,
        actions: [
          '拆分为更小的函数',
          '减少条件嵌套',
          '使用设计模式简化逻辑'
        ]
      });
    }
    
    // 基于重复代码的建议
    if (metrics.duplicateBlocks > 3) {
      suggestions.push({
        priority: 'medium',
        title: '消除重复代码',
        description: `发现 ${metrics.duplicateBlocks} 处重复代码`,
        actions: [
          '提取公共函数',
          '使用模板或高阶函数',
          '重构重复逻辑'
        ]
      });
    }
    
    // 基于函数长度的建议
    if (metrics.averageFunctionLength > 30) {
      suggestions.push({
        priority: 'low',
        title: '优化函数长度',
        description: `平均函数长度 ${metrics.averageFunctionLength} 行`,
        actions: [
          '遵循单一职责原则',
          '将长函数拆分为多个小函数',
          '提取辅助函数'
        ]
      });
    }
    
    // 通用建议
    suggestions.push({
      priority: 'low',
      title: '持续改进',
      description: '代码质量持续改进建议',
      actions: [
        '建立代码审查流程',
        '使用静态分析工具',
        '编写单元测试',
        '定期重构代码'
      ]
    });
    
    return suggestions;
  }
  
  /**
   * 计算分数分解
   */
  static calculateScoreBreakdown(issues, metrics) {
    const maxScore = 100;
    let currentScore = maxScore;
    
    // 问题扣分
    const issueDeductions = {
      critical: issues.filter(i => i.severity === 'critical').length * 10,
      warning: issues.filter(i => i.severity === 'warning').length * 5,
      info: issues.filter(i => i.severity === 'info').length * 1
    };
    
    // 复杂度扣分
    const complexityDeduction = metrics.complexityScore > 50 ? 
      Math.min(20, (metrics.complexityScore - 50) / 5) : 0;
    
    // 重复代码扣分
    const duplicateDeduction = metrics.duplicateBlocks > 5 ? 
      Math.min(15, metrics.duplicateBlocks) : 0;
    
    currentScore -= (issueDeductions.critical + issueDeductions.warning + issueDeductions.info);
    currentScore -= complexityDeduction;
    currentScore -= duplicateDeduction;
    
    return {
      baseScore: maxScore,
      deductions: {
        criticalIssues: issueDeductions.critical,
        warningIssues: issueDeductions.warning,
        infoIssues: issueDeductions.info,
        complexity: complexityDeduction,
        duplicateCode: duplicateDeduction
      },
      finalScore: Math.max(0, currentScore)
    };
  }
  
  /**
   * 分析质量趋势
   */
  static analyzeQualityTrend(issues, metrics) {
    // 简化的趋势分析
    const totalIssues = issues.length;
    const criticalRatio = issues.filter(i => i.severity === 'critical').length / Math.max(1, totalIssues);
    const complexityRatio = metrics.complexityScore / 100;
    
    let trend = 'stable';
    let confidence = 'medium';
    
    if (criticalRatio > 0.3 || complexityRatio > 0.7) {
      trend = 'declining';
      confidence = 'high';
    } else if (totalIssues === 0 && complexityRatio < 0.3) {
      trend = 'improving';
      confidence = 'medium';
    }
    
    return {
      trend,
      confidence,
      indicators: {
        criticalIssueRatio: criticalRatio,
        complexityLevel: complexityRatio,
        issueDensity: totalIssues / Math.max(1, metrics.linesOfCode / 100)
      },
      recommendations: CodeQualityScanner.getTrendRecommendations(trend, criticalRatio, complexityRatio)
    };
  }
  
  /**
   * 获取趋势建议
   */
  static getTrendRecommendations(trend, criticalRatio, complexityRatio) {
    if (trend === 'declining') {
      return [
        '立即进行代码重构',
        '加强代码审查',
        '优先修复关键问题',
        '降低代码复杂度'
      ];
    } else if (trend === 'improving') {
      return [
        '保持良好实践',
        '继续定期审查',
        '关注技术债务',
        '预防复杂度增长'
      ];
    } else {
      return [
        '持续监控代码质量',
        '逐步改进问题区域',
        '平衡新功能和重构',
        '建立质量基线'
      ];
    }
  }
  
  /**
   * 获取默认建议
   */
  static getDefaultSuggestion(ruleId) {
    const suggestionMap = {
      'long-function': '将函数拆分为多个小函数，每个函数负责单一职责',
      'complex-condition': '将复杂条件拆分为多个布尔变量或辅助函数',
      'deep-nesting': '减少嵌套层次，提取嵌套代码到独立函数',
      'magic-number': '将数字常量定义为有意义的命名常量'
    };
    
    return suggestionMap[ruleId] || '参考编码规范和最佳实践';
  }
}