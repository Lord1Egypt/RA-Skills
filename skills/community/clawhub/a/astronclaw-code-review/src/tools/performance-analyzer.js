/**
 * 性能分析工具
 */

import { analyzePerformance, getPerformanceOptimizationTips } from './analyzers/performance-analyzer.js';

export class PerformanceAnalyzer {
  /**
   * 执行性能分析
   */
  static async execute(args, context) {
    const { filePath, code, options = {} } = args;
    
    console.log('⚡ 执行性能分析...');
    
    try {
      // 获取代码内容
      const codeContent = await this.getCodeContent(filePath, code);
      if (!codeContent) {
        throw new Error('无法获取代码内容：请提供filePath或code参数');
      }
      
      // 执行性能分析
      const performanceResult = await analyzePerformance(codeContent, {
        filePath,
        ...options
      });
      
      // 生成性能报告
      const report = this.generatePerformanceReport(performanceResult, codeContent);
      
      console.log(`✅ 性能分析完成: ${filePath || '代码片段'}`);
      console.log(`   评分: ${performanceResult.score}/100`);
      console.log(`   问题数: ${performanceResult.issues.length}`);
      
      return {
        success: true,
        ...report,
        metadata: {
          analysisTime: performanceResult.metrics.analysisTime,
          timestamp: new Date().toISOString(),
          config: context?.config || {}
        }
      };
      
    } catch (error) {
      console.error('❌ 性能分析失败:', error.message);
      return {
        success: false,
        error: {
          message: error.message,
          code: 'PERFORMANCE_ANALYSIS_ERROR'
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
   * 生成性能报告
   */
  static generatePerformanceReport(performanceResult, codeContent) {
    const { score, issues, metrics, summary } = performanceResult;
    
    // 按严重程度和类别分组问题
    const issuesBySeverity = {
      high: issues.filter(i => i.severity === 'high'),
      warning: issues.filter(i => i.severity === 'warning'),
      info: issues.filter(i => i.severity === 'info')
    };
    
    const issuesByCategory = {};
    issues.forEach(issue => {
      const category = this.getIssueCategory(issue.ruleId);
      if (!issuesByCategory[category]) {
        issuesByCategory[category] = [];
      }
      issuesByCategory[category].push(issue);
    });
    
    // 性能瓶颈分析
    const bottlenecks = this.identifyPerformanceBottlenecks(issues, metrics);
    
    // 优化建议
    const optimizationSuggestions = this.generateOptimizationSuggestions(issues, metrics);
    
    // 性能最佳实践
    const bestPractices = getPerformanceOptimizationTips();
    
    // 性能指标基准
    const benchmarks = this.generatePerformanceBenchmarks(metrics);
    
    return {
      summary: {
        overallScore: score,
        performanceLevel: this.getPerformanceLevel(score),
        totalIssues: issues.length,
        criticalBottlenecks: bottlenecks.critical.length,
        metrics: {
          linesOfCode: metrics.linesOfCode,
          loops: metrics.loops,
          domOperations: metrics.domOperations,
          syncOperations: metrics.syncOperations,
          estimatedComplexity: metrics.estimatedComplexity,
          analysisTime: metrics.analysisTime
        },
        categorySummary: summary.byCategory
      },
      detailedAnalysis: {
        issues: issues.map(issue => ({
          ...issue,
          category: this.getIssueCategory(issue.ruleId),
          impact: this.assessPerformanceImpact(issue)
        })),
        issuesBySeverity,
        issuesByCategory,
        topPerformanceIssues: issues.slice(0, 10)
      },
      bottlenecks,
      optimizationPlan: {
        suggestions: optimizationSuggestions,
        priority: this.prioritizeOptimizations(issues, bottlenecks),
        estimatedGain: this.estimatePerformanceGain(issues, metrics)
      },
      benchmarks,
      bestPractices,
      monitoringRecommendations: this.generateMonitoringRecommendations(issues, metrics)
    };
  }
  
  /**
   * 获取问题类别
   */
  static getIssueCategory(ruleId) {
    const categoryMap = {
      'nested-loops': '算法复杂度',
      'large-array-creation': '内存使用',
      'dom-manipulation-in-loop': 'DOM操作',
      'synchronous-io': 'I/O性能',
      'memory-leak-pattern': '内存管理',
      'inefficient-string-concat': '字符串操作'
    };
    
    return categoryMap[ruleId] || '其他';
  }
  
  /**
   * 识别性能瓶颈
   */
  static identifyPerformanceBottlenecks(issues, metrics) {
    const bottlenecks = {
      critical: [],
      high: [],
      medium: [],
      potential: metrics.potentialBottlenecks || []
    };
    
    issues.forEach(issue => {
      const impact = this.assessPerformanceImpact(issue);
      
      if (issue.severity === 'high' || impact === 'high') {
        bottlenecks.high.push({
          issue: issue.message,
          rule: issue.ruleId,
          line: issue.line,
          impact,
          suggestion: issue.suggestion
        });
      } else if (issue.severity === 'warning' || impact === 'medium') {
        bottlenecks.medium.push({
          issue: issue.message,
          rule: issue.ruleId,
          line: issue.line,
          impact,
          suggestion: issue.suggestion
        });
      }
    });
    
    // 基于指标识别额外瓶颈
    if (metrics.loops > 15) {
      bottlenecks.critical.push({
        issue: `循环数量过多 (${metrics.loops} 个)`,
        impact: 'high',
        suggestion: '优化算法，减少循环嵌套，考虑使用更高效的数据结构'
      });
    }
    
    if (metrics.domOperations > 10) {
      bottlenecks.high.push({
        issue: `DOM操作频繁 (${metrics.domOperations} 次)`,
        impact: 'high',
        suggestion: '批量DOM操作，使用DocumentFragment，减少重绘重排'
      });
    }
    
    if (metrics.syncOperations > 5) {
      bottlenecks.critical.push({
        issue: `同步I/O操作过多 (${metrics.syncOperations} 次)`,
        impact: 'critical',
        suggestion: '改为异步操作，避免阻塞事件循环'
      });
    }
    
    return bottlenecks;
  }
  
  /**
   * 评估性能影响
   */
  static assessPerformanceImpact(issue) {
    const impactMap = {
      'nested-loops': 'high',
      'large-array-creation': 'medium',
      'dom-manipulation-in-loop': 'high',
      'synchronous-io': 'critical',
      'memory-leak-pattern': 'high',
      'inefficient-string-concat': 'low'
    };
    
    return impactMap[issue.ruleId] || issue.severity;
  }
  
  /**
   * 生成优化建议
   */
  static generateOptimizationSuggestions(issues, metrics) {
    const suggestions = [];
    
    // 基于问题类型的建议
    const highImpactIssues = issues.filter(i => 
      this.assessPerformanceImpact(i) === 'high' || 
      this.assessPerformanceImpact(i) === 'critical'
    );
    
    if (highImpactIssues.length > 0) {
      suggestions.push({
        priority: 'high',
        title: '关键性能优化',
        description: `解决 ${highImpactIssues.length} 个高影响性能问题`,
        actions: highImpactIssues.map(issue => ({
          issue: issue.message,
          solution: issue.suggestion || this.getDefaultOptimization(issue.ruleId)
        }))
      });
    }
    
    // 基于指标的建议
    if (metrics.loops > 10) {
      suggestions.push({
        priority: 'medium',
        title: '算法优化',
        description: `减少循环数量，优化算法复杂度`,
        actions: [
          '使用更高效的数据结构（如Set、Map）',
          '避免嵌套循环',
          '使用缓存减少重复计算',
          '考虑分治或动态规划'
        ]
      });
    }
    
    if (metrics.domOperations > 5) {
      suggestions.push({
        priority: 'high',
        title: 'DOM操作优化',
        description: '减少DOM操作，提高渲染性能',
        actions: [
          '使用DocumentFragment批量操作',
          '避免在循环中修改样式',
          '使用CSS动画替代JS动画',
          '实施虚拟滚动或分页'
        ]
      });
    }
    
    if (metrics.syncOperations > 0) {
      suggestions.push({
        priority: 'critical',
        title: '异步化改造',
        description: '将同步操作改为异步，避免阻塞',
        actions: [
          '使用Promise/async-await',
          '实施非阻塞I/O',
          '使用流式处理大数据',
          '考虑Web Worker处理CPU密集型任务'
        ]
      });
    }
    
    // 内存优化建议
    const memoryIssues = issues.filter(i => 
      i.ruleId === 'memory-leak-pattern' || 
      i.ruleId === 'large-array-creation'
    );
    
    if (memoryIssues.length > 0) {
      suggestions.push({
        priority: 'medium',
        title: '内存优化',
        description: '改进内存使用模式',
        actions: [
          '及时清理定时器和事件监听器',
          '使用对象池或缓存',
          '避免全局变量',
          '实施懒加载和代码分割'
        ]
      });
    }
    
    return suggestions;
  }
  
  /**
   * 获取默认优化方案
   */
  static getDefaultOptimization(ruleId) {
    const optimizationMap = {
      'nested-loops': '优化算法复杂度，考虑使用哈希表或索引',
      'large-array-creation': '使用分页或流式处理，避免一次性加载',
      'dom-manipulation-in-loop': '批量DOM操作，减少重绘重排',
      'synchronous-io': '改为异步操作，使用Promise或async/await',
      'memory-leak-pattern': '及时清理资源，使用弱引用',
      'inefficient-string-concat': '使用数组join或模板字符串'
    };
    
    return optimizationMap[ruleId] || '参考性能最佳实践';
  }
  
  /**
   * 优先级排序优化
   */
  static prioritizeOptimizations(issues, bottlenecks) {
    const priorities = {
      immediate: bottlenecks.critical,
      high: bottlenecks.high,
      medium: issues.filter(i => 
        i.severity === 'warning' && 
        this.assessPerformanceImpact(i) === 'medium'
      ),
      low: issues.filter(i => 
        i.severity === 'info' || 
        this.assessPerformanceImpact(i) === 'low'
      )
    };
    
    return priorities;
  }
  
  /**
   * 估计性能提升
   */
  static estimatePerformanceGain(issues, metrics) {
    let estimatedGain = 0;
    
    // 基于问题数量估计
    const criticalCount = issues.filter(i => 
      this.assessPerformanceImpact(i) === 'critical'
    ).length;
    
    const highCount = issues.filter(i => 
      this.assessPerformanceImpact(i) === 'high'
    ).length;
    
    estimatedGain += criticalCount * 30; // 每个关键问题预计提升30%
    estimatedGain += highCount * 15;     // 每个高影响问题预计提升15%
    
    // 基于指标估计
    if (metrics.loops > 10) {
      estimatedGain += Math.min(40, (metrics.loops - 10) * 2);
    }
    
    if (metrics.domOperations > 5) {
      estimatedGain += Math.min(30, metrics.domOperations * 3);
    }
    
    if (metrics.syncOperations > 0) {
      estimatedGain += Math.min(50, metrics.syncOperations * 10);
    }
    
    return {
      estimatedPercentage: Math.min(80, estimatedGain),
      confidence: estimatedGain > 30 ? '高' : estimatedGain > 15 ? '中' : '低',
      factors: {
        criticalIssues: criticalCount,
        highImpactIssues: highCount,
        loopOptimization: metrics.loops > 10,
        domOptimization: metrics.domOperations > 5,
        ioOptimization: metrics.syncOperations > 0
      }
    };
  }
  
  /**
   * 生成性能基准
   */
  static generatePerformanceBenchmarks(metrics) {
    const benchmarks = {
      loops: {
        current: metrics.loops,
        target: Math.max(5, Math.floor(metrics.loops * 0.7)),
        improvement: `减少 ${Math.max(1, Math.floor(metrics.loops * 0.3))} 个循环`
      },
      domOperations: {
        current: metrics.domOperations,
        target: Math.max(2, Math.floor(metrics.domOperations * 0.5)),
        improvement: `减少 ${Math.max(1, Math.floor(metrics.domOperations * 0.5))} 次DOM操作`
      },
      syncOperations: {
        current: metrics.syncOperations,
        target: 0,
        improvement: '完全异步化'
      },
      complexity: {
        current: metrics.estimatedComplexity,
        target: 'O(n)',
        improvement: '降低算法复杂度'
      }
    };
    
    return benchmarks;
  }
  
  /**
   * 根据评分获取性能等级
   */
  static getPerformanceLevel(score) {
    if (score >= 90) return '优秀';
    if (score >= 80) return '良好';
    if (score >= 70) return '中等';
    if (score >= 60) return '及格';
    return '需要优化';
  }
  
  /**
   * 生成监控建议
   */
  static generateMonitoringRecommendations(issues, metrics) {
    const recommendations = [];
    
    if (issues.some(i => i.ruleId === 'memory-leak-pattern')) {
      recommendations.push({
        area: '内存监控',
        metrics: ['heap usage', 'garbage collection frequency', 'memory leaks'],
        tools: ['Chrome DevTools Memory tab', 'Node.js --inspect', 'performance.memory API']
      });
    }
    
    if (issues.some(i => i.ruleId === 'nested-loops' || metrics.loops > 10)) {
      recommendations.push({
        area: 'CPU监控',
        metrics: ['CPU usage', 'event loop lag', 'function execution time'],
        tools: ['Chrome DevTools Performance tab', 'Node.js profiler', 'console.time']
      });
    }
    
    if (issues.some(i => i.ruleId === 'dom-manipulation-in-loop' || metrics.domOperations > 5)) {
      recommendations.push({
        area: '渲染性能',
        metrics: ['FPS', 'layout thrashing', 'paint time'],
        tools: ['Chrome DevTools Rendering tab', 'Lighthouse', 'Web Vitals']
      });
    }
    
    // 通用监控建议
    recommendations.push({
      area: '综合监控',
      metrics: ['response time', 'error rate', 'throughput'],
      tools: ['Application Performance Monitoring (APM)', 'logging', 'alerting']
    });
    
    return recommendations;
  }
}