/**
 * 综合代码审查工具
 * 集成质量、安全、性能分析，提供AI智能建议
 */

import { analyzeCodeQuality } from './analyzers/quality-analyzer.js';
import { analyzeSecurity } from './analyzers/security-analyzer.js';
import { analyzePerformance } from './analyzers/performance-analyzer.js';
import { generateAIRecommendations } from './ai/recommendation-engine.js';

export class CodeReviewTool {
  /**
   * 主执行函数
   */
  static async execute(args, context) {
    const { filePath, code, options = {} } = args;
    const { config = {} } = context;
    
    console.log(`🔍 开始综合代码审查: ${filePath || '代码片段'}`);
    
    try {
      // 1. 准备代码内容
      const codeContent = await CodeReviewTool.getCodeContent(filePath, code);
      if (!codeContent) {
        throw new Error('无法获取代码内容：请提供filePath或code参数');
      }
      
      // 2. 并行执行各项分析
      const analysisPromises = [];
      
      // 代码质量分析（总是执行）
      analysisPromises.push(
        analyzeCodeQuality(codeContent, { filePath, ...options })
      );
      
      // 安全检查（根据配置）
      if (config.includeSecurity !== false) {
        analysisPromises.push(
          analyzeSecurity(codeContent, { filePath, ...options })
        );
      }
      
      // 性能分析（根据配置）
      if (config.includePerformance !== false) {
        analysisPromises.push(
          analyzePerformance(codeContent, { filePath, ...options })
        );
      }
      
      // 3. 等待所有分析完成
      const [qualityResult, securityResult, performanceResult] = await Promise.all(
        analysisPromises.map(p => p.catch(e => ({ error: e.message, issues: [] })))
      );
      
      // 4. AI智能建议（根据配置）
      let aiRecommendations = [];
      if (config.aiEnabled !== false) {
        try {
          aiRecommendations = await generateAIRecommendations({
            qualityIssues: qualityResult.issues || [],
            securityIssues: securityResult?.issues || [],
            performanceIssues: performanceResult?.issues || [],
            code: codeContent,
            filePath
          });
        } catch (aiError) {
          console.warn('AI建议生成失败:', aiError.message);
          aiRecommendations = [{ type: 'warning', message: 'AI建议生成失败: ' + aiError.message }];
        }
      }
      
      // 5. 计算总体评分
      const overallScore = CodeReviewTool.calculateOverallScore(
        qualityResult,
        securityResult,
        performanceResult
      );
      
      // 6. 生成审查结果
      const reviewResult = {
        success: true,
        summary: {
          filePath: filePath || 'inline-code',
          timestamp: new Date().toISOString(),
          overallScore,
          grade: CodeReviewTool.getGradeFromScore(overallScore),
          fileSize: codeContent.length,
          linesOfCode: CodeReviewTool.countLines(codeContent)
        },
        analysis: {
          quality: qualityResult,
          security: securityResult || { enabled: false, issues: [] },
          performance: performanceResult || { enabled: false, issues: [] }
        },
        recommendations: {
          ai: aiRecommendations,
          priority: CodeReviewTool.prioritizeRecommendations(
            qualityResult?.issues || [],
            securityResult?.issues || [],
            performanceResult?.issues || [],
            aiRecommendations
          )
        },
        metadata: {
          analysisTime: Date.now() - context.startTime,
          config,
          language: CodeReviewTool.detectLanguage(codeContent, filePath)
        }
      };
      
      console.log(`✅ 代码审查完成: ${filePath || '代码片段'}`);
      console.log(`  总体评分: ${overallScore}/100 (${reviewResult.summary.grade})`);
      console.log(`  发现问题: ${CodeReviewTool.countTotalIssues(reviewResult)} 个`);
      
      return reviewResult;
      
    } catch (error) {
      console.error('❌ 代码审查失败:', error.message);
      return {
        success: false,
        error: {
          message: error.message,
          code: 'CODE_REVIEW_ERROR',
          details: error.stack
        },
        summary: {
          filePath,
          timestamp: new Date().toISOString(),
          overallScore: 0,
          grade: 'F'
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
        // 注意：在实际实现中需要文件系统访问权限
        // 这里使用简化版本
        const fs = await import('fs');
        return fs.readFileSync(filePath, 'utf-8');
      } catch (error) {
        throw new Error(`无法读取文件 ${filePath}: ${error.message}`);
      }
    }
    
    return null;
  }
  
  /**
   * 计算总体评分
   */
  static calculateOverallScore(quality, security, performance) {
    const weights = {
      quality: 0.5,
      security: 0.3,
      performance: 0.2
    };
    
    let totalScore = 0;
    let totalWeight = 0;
    
    // 质量评分
    if (quality && typeof quality.score === 'number') {
      totalScore += quality.score * weights.quality;
      totalWeight += weights.quality;
    }
    
    // 安全评分（如果有）
    if (security && typeof security.score === 'number') {
      totalScore += security.score * weights.security;
      totalWeight += weights.security;
    } else {
      // 安全检查未启用，按权重比例调整
      totalWeight += weights.security;
    }
    
    // 性能评分（如果有）
    if (performance && typeof performance.score === 'number') {
      totalScore += performance.score * weights.performance;
      totalWeight += weights.performance;
    } else {
      // 性能检查未启用，按权重比例调整
      totalWeight += weights.performance;
    }
    
    // 按实际启用的权重比例调整分数
    const adjustedScore = totalWeight > 0 ? (totalScore / totalWeight) : 100;
    return Math.round(Math.max(0, Math.min(100, adjustedScore)));
  }
  
  /**
   * 根据评分获取等级
   */
  static getGradeFromScore(score) {
    if (score >= 90) return 'A';
    if (score >= 80) return 'B';
    if (score >= 70) return 'C';
    if (score >= 60) return 'D';
    return 'F';
  }
  
  /**
   * 统计行数
   */
  static countLines(code) {
    return code.split('\n').length;
  }
  
  /**
   * 检测编程语言
   */
  static detectLanguage(code, filePath) {
    const extensions = {
      '.js': 'JavaScript',
      '.ts': 'TypeScript',
      '.jsx': 'React JSX',
      '.tsx': 'React TSX',
      '.py': 'Python',
      '.java': 'Java',
      '.go': 'Go',
      '.rs': 'Rust',
      '.cpp': 'C++',
      '.c': 'C',
      '.php': 'PHP',
      '.rb': 'Ruby',
      '.swift': 'Swift',
      '.kt': 'Kotlin'
    };
    
    if (filePath) {
      for (const [ext, lang] of Object.entries(extensions)) {
        if (filePath.endsWith(ext)) {
          return lang;
        }
      }
    }
    
    // 基于代码内容猜测
    if (code.includes('import React') || code.includes('from "react"')) {
      return 'React';
    }
    if (code.includes('def ') && code.includes(':')) {
      return 'Python';
    }
    if (code.includes('function') || code.includes('const ') || code.includes('let ')) {
      return 'JavaScript';
    }
    
    return 'Unknown';
  }
  
  /**
   * 优先级排序建议
   */
  static prioritizeRecommendations(qualityIssues, securityIssues, performanceIssues, aiRecommendations) {
    const allIssues = [
      ...securityIssues.map(i => ({ ...i, priority: 'critical', category: 'security' })),
      ...performanceIssues.map(i => ({ ...i, priority: 'high', category: 'performance' })),
      ...qualityIssues.map(i => ({ ...i, priority: 'medium', category: 'quality' }))
    ];
    
    // 添加AI建议
    aiRecommendations.forEach(rec => {
      allIssues.push({
        ...rec,
        category: 'ai-suggestion',
        priority: rec.priority || 'medium'
      });
    });
    
    // 按优先级排序
    const priorityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
    return allIssues.sort((a, b) => {
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    });
  }
  
  /**
   * 统计总问题数
   */
  static countTotalIssues(reviewResult) {
    return (
      (reviewResult.analysis.quality.issues?.length || 0) +
      (reviewResult.analysis.security.issues?.length || 0) +
      (reviewResult.analysis.performance.issues?.length || 0)
    );
  }
}