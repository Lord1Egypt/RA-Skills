/**
 * Code Review Workflow - 代码审查工作流
 * 
 * 功能：
 * - 自动审查代码质量
 * - 检查安全漏洞
 * - 检查性能问题
 * - 检查测试覆盖率
 * - 生成审查报告
 * 
 * @example
 * const result = await codeReviewWorkflow({
 *   prNumber: 123,
 *   files: ['src/a.js', 'src/b.js'],
 *   autoComment: true,
 * });
 */

import { HarnessOrchestrator } from '../harness/orchestrator.js';
import { createValidator, validators } from '../harness/utils/validator.js';

// ============================================================================
// 配置
// ============================================================================

const DEFAULT_CONFIG = {
  maxParallel: 5,
  timeoutSeconds: 300,
  enableLint: true,
  enableSecurity: true,
  enablePerformance: true,
  enableTests: true,
  autoComment: false,
  minApprovalScore: 0.8,
};

// ============================================================================
// 审查规则
// ============================================================================

const REVIEW_RULES = {
  lint: [
    '代码风格一致性',
    '命名规范',
    '代码格式',
    '未使用变量',
    '复杂度过高',
  ],
  security: [
    'SQL 注入风险',
    'XSS 漏洞',
    '敏感信息泄露',
    '不安全的依赖',
    '权限校验缺失',
  ],
  performance: [
    '不必要的循环',
    '内存泄漏风险',
    '异步处理不当',
    '缓存缺失',
    '数据库查询优化',
  ],
  tests: [
    '测试覆盖率',
    '边界条件测试',
    '错误处理测试',
    '集成测试',
  ],
};

// ============================================================================
// 代码审查工作流类
// ============================================================================

export class CodeReviewWorkflow {
  constructor(config = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.orchestrator = new HarnessOrchestrator({
      maxParallel: this.config.maxParallel,
      timeoutSeconds: this.config.timeoutSeconds,
      retryAttempts: 2,
    });
  }

  /**
   * 执行代码审查
   * 
   * @param {Object} options
   * @param {number} options.prNumber - PR 编号
   * @param {Array} options.files - 变更文件列表
   * @param {string} options.repo - 仓库名称
   * @param {boolean} options.autoComment - 是否自动评论
   * @returns {Promise<Object>} 审查结果
   */
  async execute(options) {
    const { prNumber, files = [], repo, autoComment = this.config.autoComment } = options;

    console.log(`[CodeReview] Starting review for PR #${prNumber}`);
    console.log(`[CodeReview] Files to review: ${files.length}`);

    // 构建子任务
    const subTasks = this.buildSubTasks(files, repo);

    // 执行审查
    const result = await this.orchestrator.execute({
      task: `审查 PR #${prNumber}`,
      pattern: 'parallel',
      subTasks,
    });

    // 生成报告
    const report = this.generateReport(result, options);

    // 自动评论（可选）
    if (autoComment && prNumber) {
      await this.postComment(prNumber, report);
    }

    return {
      success: result.success,
      report,
      rawResult: result,
    };
  }

  /**
   * 构建子任务
   */
  buildSubTasks(files, repo) {
    const subTasks = [];

    // 1. 代码风格检查
    if (this.config.enableLint) {
      subTasks.push({
        task: `检查代码风格：${files.join(', ')}`,
        agent: 'linter-agent',
        context: { files, repo, rules: REVIEW_RULES.lint },
        priority: 1,
      });
    }

    // 2. 安全检查
    if (this.config.enableSecurity) {
      subTasks.push({
        task: `检查安全漏洞：${files.join(', ')}`,
        agent: 'security-agent',
        context: { files, repo, rules: REVIEW_RULES.security },
        priority: 2,
      });
    }

    // 3. 性能检查
    if (this.config.enablePerformance) {
      subTasks.push({
        task: `检查性能问题：${files.join(', ')}`,
        agent: 'performance-agent',
        context: { files, repo, rules: REVIEW_RULES.performance },
        priority: 3,
      });
    }

    // 4. 测试检查
    if (this.config.enableTests) {
      subTasks.push({
        task: `检查测试覆盖率和质量`,
        agent: 'test-agent',
        context: { files, repo, rules: REVIEW_RULES.tests },
        priority: 4,
      });
    }

    return subTasks;
  }

  /**
   * 生成审查报告
   */
  generateReport(result, options) {
    const { prNumber, files } = options;
    const outputs = result.outputs || [];
    const errors = result.errors || [];

    // 合并所有审查结果
    const allIssues = [];
    const summaries = [];

    for (const output of outputs) {
      if (output.issues) {
        allIssues.push(...output.issues);
      }
      if (output.summary) {
        summaries.push(output.summary);
      }
    }

    // 分类问题
    const issuesByType = {
      critical: allIssues.filter(i => i.severity === 'critical'),
      major: allIssues.filter(i => i.severity === 'major'),
      minor: allIssues.filter(i => i.severity === 'minor'),
      suggestion: allIssues.filter(i => i.severity === 'suggestion'),
    };

    // 计算评分
    const score = this.calculateScore(issuesByType, files.length);

    // 生成报告
    const report = {
      prNumber,
      timestamp: new Date().toISOString(),
      filesReviewed: files.length,
      score,
      approval: score >= this.config.minApprovalScore,
      summary: {
        total: allIssues.length,
        critical: issuesByType.critical.length,
        major: issuesByType.major.length,
        minor: issuesByType.minor.length,
        suggestion: issuesByType.suggestion.length,
      },
      issues: issuesByType,
      summaries,
      errors,
      recommendations: this.generateRecommendations(issuesByType),
    };

    return report;
  }

  /**
   * 计算评分
   */
  calculateScore(issuesByType, fileCount) {
    const weights = {
      critical: -10,
      major: -5,
      minor: -2,
      suggestion: 0,
    };

    let score = 100;

    for (const [type, issues] of Object.entries(issuesByType)) {
      score += issues.length * weights[type];
    }

    // 归一化到 0-1
    return Math.max(0, Math.min(1, score / 100));
  }

  /**
   * 生成建议
   */
  generateRecommendations(issuesByType) {
    const recommendations = [];

    if (issuesByType.critical.length > 0) {
      recommendations.push({
        priority: 'high',
        action: '立即修复严重问题',
        details: issuesByType.critical.map(i => i.description),
      });
    }

    if (issuesByType.major.length > 0) {
      recommendations.push({
        priority: 'medium',
        action: '优先修复主要问题',
        details: issuesByType.major.map(i => i.description),
      });
    }

    if (issuesByType.minor.length > 5) {
      recommendations.push({
        priority: 'low',
        action: '考虑重构以减少小问题',
        details: ['问题数量较多，建议代码重构'],
      });
    }

    return recommendations;
  }

  /**
   * 发布评论到 PR
   */
  async postComment(prNumber, report) {
    // TODO: 实际实现应该调用 GitHub/GitLab API
    const comment = this.formatComment(report);
    console.log(`[CodeReview] Would post comment to PR #${prNumber}:`);
    console.log(comment);
    
    // await githubAPI.createComment(prNumber, comment);
    return { success: true, comment };
  }

  /**
   * 格式化评论
   */
  formatComment(report) {
    const { score, approval, summary, issues } = report;

    const emoji = approval ? '✅' : '❌';
    const scoreEmoji = score >= 0.9 ? '🟢' : score >= 0.7 ? '🟡' : '🔴';

    let comment = `## ${emoji} 代码审查报告\n\n`;
    comment += `**评分:** ${scoreEmoji} ${(score * 100).toFixed(0)}/100\n`;
    comment += `**结果:** ${approval ? '✅ 通过' : '❌ 需要修复'}\n\n`;
    comment += `---\n\n`;
    comment += `### 问题统计\n`;
    comment += `| 级别 | 数量 |\n`;
    comment += `|------|------|\n`;
    comment += `| 🔴 严重 | ${summary.critical} |\n`;
    comment += `| 🟠 主要 | ${summary.major} |\n`;
    comment += `| 🟡 次要 | ${summary.minor} |\n`;
    comment += `| 💡 建议 | ${summary.suggestion} |\n\n`;

    if (issues.critical.length > 0) {
      comment += `### 🔴 严重问题\n`;
      for (const issue of issues.critical) {
        comment += `- ${issue.description}\n`;
      }
      comment += `\n`;
    }

    if (issues.major.length > 0) {
      comment += `### 🟠 主要问题\n`;
      for (const issue of issues.major) {
        comment += `- ${issue.description}\n`;
      }
      comment += `\n`;
    }

    comment += `---\n`;
    comment += `_Generated by Harness CodeReview Workflow_`;

    return comment;
  }

  /**
   * 获取审查状态
   */
  getStatus() {
    return this.orchestrator.getStatus();
  }
}

// ============================================================================
// 快捷函数
// ============================================================================

/**
 * 快速执行代码审查
 */
export async function codeReview(options) {
  const workflow = new CodeReviewWorkflow(options.config);
  return workflow.execute(options);
}

export default CodeReviewWorkflow;
