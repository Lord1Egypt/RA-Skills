/**
 * AI Agent Team Manager - Performance Evaluator
 * 评估AI代理团队成员的工作表现和效率
 */

class PerformanceEvaluator {
  constructor() {
    this.metrics = {
      taskCompletionRate: 0,
      qualityScore: 0,
      responseTime: 0,
      collaborationScore: 0,
      learningGrowth: 0
    };
  }

  /**
   * 评估单个代理的表现
   * @param {Object} agentData - 代理的工作数据
   * @returns {Object} 评估结果
   */
  evaluateAgent(agentData) {
    const evaluation = {
      agentId: agentData.id,
      name: agentData.name,
      role: agentData.role,
      metrics: {},
      strengths: [],
      weaknesses: [],
      recommendations: []
    };

    // 任务完成率评估
    const completionRate = this.calculateTaskCompletionRate(agentData.tasks);
    evaluation.metrics.taskCompletionRate = completionRate;
    
    if (completionRate >= 0.9) {
      evaluation.strengths.push('高任务完成率');
    } else if (completionRate < 0.7) {
      evaluation.weaknesses.push('任务完成率需要提升');
      evaluation.recommendations.push('建议优化任务分配策略');
    }

    // 质量评分
    const qualityScore = this.calculateQualityScore(agentData.outputs);
    evaluation.metrics.qualityScore = qualityScore;
    
    if (qualityScore >= 85) {
      evaluation.strengths.push('输出质量优秀');
    } else if (qualityScore < 70) {
      evaluation.weaknesses.push('输出质量有待提高');
      evaluation.recommendations.push('建议加强质量控制流程');
    }

    // 响应时间评估
    const responseTime = this.calculateResponseTime(agentData.interactions);
    evaluation.metrics.responseTime = responseTime;
    
    if (responseTime <= 300) {
      evaluation.strengths.push('响应速度快');
    } else if (responseTime > 600) {
      evaluation.weaknesses.push('响应时间较长');
      evaluation.recommendations.push('建议优化处理流程或分配更多资源');
    }

    // 协作评分
    const collaborationScore = this.calculateCollaborationScore(agentData.collaborations);
    evaluation.metrics.collaborationScore = collaborationScore;
    
    if (collaborationScore >= 80) {
      evaluation.strengths.push('团队协作良好');
    } else if (collaborationScore < 60) {
      evaluation.weaknesses.push('协作能力需要加强');
      evaluation.recommendations.push('建议改进沟通机制和工作流程');
    }

    // 学习成长评估
    const learningGrowth = this.calculateLearningGrowth(agentData.history);
    evaluation.metrics.learningGrowth = learningGrowth;
    
    if (learningGrowth >= 75) {
      evaluation.strengths.push('持续学习和改进');
    } else if (learningGrowth < 50) {
      evaluation.weaknesses.push('学习成长缓慢');
      evaluation.recommendations.push('建议提供更多反馈和学习机会');
    }

    // 综合评分
    evaluation.overallScore = this.calculateOverallScore(evaluation.metrics);
    evaluation.grade = this.getGrade(evaluation.overallScore);

    return evaluation;
  }

  /**
   * 计算任务完成率
   */
  calculateTaskCompletionRate(tasks) {
    if (!tasks || tasks.length === 0) return 0;
    const completed = tasks.filter(t => t.status === 'completed').length;
    return Math.round((completed / tasks.length) * 100) / 100;
  }

  /**
   * 计算质量评分
   */
  calculateQualityScore(outputs) {
    if (!outputs || outputs.length === 0) return 0;
    let totalScore = 0;
    outputs.forEach(output => {
      totalScore += output.qualityScore || 0;
    });
    return Math.round(totalScore / outputs.length);
  }

  /**
   * 计算响应时间（毫秒）
   */
  calculateResponseTime(interactions) {
    if (!interactions || interactions.length === 0) return 0;
    let totalTime = 0;
    interactions.forEach(interaction => {
      totalTime += interaction.responseTime || 0;
    });
    return Math.round(totalTime / interactions.length);
  }

  /**
   * 计算协作评分
   */
  calculateCollaborationScore(collaborations) {
    if (!collaborations || collaborations.length === 0) return 0;
    let totalScore = 0;
    collaborations.forEach(collab => {
      totalScore += collab.score || 0;
    });
    return Math.round(totalScore / collaborations.length);
  }

  /**
   * 计算学习成长评分
   */
  calculateLearningGrowth(history) {
    if (!history || history.length < 2) return 0;
    // 基于历史表现的趋势分析
    const recentPerformance = history.slice(-5).reduce((sum, item) => sum + item.score, 0) / 5;
    const earlyPerformance = history.slice(0, 5).reduce((sum, item) => sum + item.score, 0) / 5;
    const growth = ((recentPerformance - earlyPerformance) / earlyPerformance) * 100;
    return Math.max(0, Math.min(100, Math.round(50 + growth)));
  }

  /**
   * 计算综合评分
   */
  calculateOverallScore(metrics) {
    const weights = {
      taskCompletionRate: 0.3,
      qualityScore: 0.3,
      responseTime: 0.2,
      collaborationScore: 0.1,
      learningGrowth: 0.1
    };

    let score = 0;
    score += metrics.taskCompletionRate * weights.taskCompletionRate * 100;
    score += metrics.qualityScore * weights.qualityScore;
    score += (1 - metrics.responseTime / 1000) * weights.responseTime * 100;
    score += metrics.collaborationScore * weights.collaborationScore;
    score += metrics.learningGrowth * weights.learningGrowth;

    return Math.round(Math.max(0, Math.min(100, score)));
  }

  /**
   * 根据分数获取等级
   */
  getGrade(score) {
    if (score >= 90) return 'A+';
    if (score >= 85) return 'A';
    if (score >= 80) return 'A-';
    if (score >= 75) return 'B+';
    if (score >= 70) return 'B';
    if (score >= 65) return 'B-';
    if (score >= 60) return 'C+';
    if (score >= 55) return 'C';
    if (score >= 50) return 'C-';
    return 'D';
  }

  /**
   * 生成团队整体表现报告
   */
  generateTeamReport(teamData) {
    const report = {
      teamName: teamData.name,
      evaluationDate: new Date().toISOString(),
      members: [],
      teamMetrics: {},
      insights: [],
      recommendations: []
    };

    // 评估每个成员
    teamData.members.forEach(member => {
      const evaluation = this.evaluateAgent(member);
      report.members.push(evaluation);
    });

    // 计算团队指标
    report.teamMetrics.averageScore = this.calculateTeamAverage(report.members);
    report.teamMetrics.highestPerformer = this.getHighestPerformer(report.members);
    report.teamMetrics.lowestPerformer = this.getLowestPerformer(report.members);
    report.teamMetrics.completionRate = this.calculateTeamCompletionRate(report.members);

    // 生成洞察
    this.generateInsights(report);
    
    // 生成建议
    this.generateRecommendations(report);

    return report;
  }

  calculateTeamAverage(members) {
    if (members.length === 0) return 0;
    const total = members.reduce((sum, member) => sum + member.overallScore, 0);
    return Math.round(total / members.length);
  }

  getHighestPerformer(members) {
    return members.reduce((best, current) => 
      current.overallScore > best.overallScore ? current : best
    );
  }

  getLowestPerformer(members) {
    return members.reduce((worst, current) => 
      current.overallScore < worst.overallScore ? current : worst
    );
  }

  calculateTeamCompletionRate(members) {
    if (members.length === 0) return 0;
    const total = members.reduce((sum, member) => sum + member.metrics.taskCompletionRate, 0);
    return Math.round((total / members.length) * 100) / 100;
  }

  generateInsights(report) {
    const avgScore = report.teamMetrics.averageScore;
    const completionRate = report.teamMetrics.completionRate;

    if (avgScore >= 85) {
      report.insights.push('团队整体表现优秀，可以承担更复杂的任务');
    } else if (avgScore >= 70) {
      report.insights.push('团队表现良好，有进一步提升空间');
    } else {
      report.insights.push('团队需要重点关注表现较弱的成员');
    }

    if (completionRate >= 0.9) {
      report.insights.push('任务完成率很高，团队执行力强');
    } else if (completionRate < 0.7) {
      report.insights.push('任务完成率偏低，需要优化工作流程');
    }
  }

  generateRecommendations(report) {
    const weakMembers = report.members.filter(m => m.overallScore < 70);
    if (weakMembers.length > 0) {
      report.recommendations.push(`为以下成员提供额外支持: ${weakMembers.map(m => m.name).join(', ')}`);
    }

    const slowResponders = report.members.filter(m => m.metrics.responseTime > 600);
    if (slowResponders.length > 0) {
      report.recommendations.push('优化响应较慢成员的资源配置');
    }

    if (report.teamMetrics.averageScore < 80) {
      report.recommendations.push('实施定期培训和技能提升计划');
    }
  }
}

module.exports = PerformanceEvaluator;