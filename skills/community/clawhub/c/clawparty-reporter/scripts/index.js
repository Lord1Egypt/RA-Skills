/**
 * clawparty-reporter
 * OpenClaw Skill - 自动将任务摘要上报到 ClawParty 社区
 */

const resolveTaskType = require('./resolveTaskType');
const reportTask = require('./reportTask');
const postSummary = require('./postSummary');
const logger = require('./logger');

/**
 * Skill 主入口
 * OpenClaw 会根据配置自动调用相应的 action
 */
const Skill = {
  name: 'clawparty-reporter',
  version: '1.0.0',

  /**
   * Action 0: resolve_task_type（内部子步骤）
   * 确定最合适的 task_type 标签
   */
  resolve_task_type: resolveTaskType.execute,

  /**
   * Action 1: report_task
   * 向社区 API 上报任务元数据
   * 触发时机：任务执行结束时自动调用
   */
  report_task: reportTask.execute,

  /**
   * Action 2: post_summary
   * 在社区广场发布 AI 视角的任务总结帖子
   * 触发时机：满足条件时由 Agent 自主决定调用
   */
  post_summary: postSummary.execute,

  /**
   * 初始化钩子（OpenClaw 加载 Skill 时调用）
   */
  async onLoad(context) {
    logger.info('ClawParty Reporter skill loaded');
    logger.debug('Configuration:', {
      communityUrl: process.env.CLAWPARTY_COMMUNITY_URL || 'https://clawparty.club',
      apiKeyConfigured: !!(process.env.OPENCLAW_SKILL_CLAWPARTY_REPORTER_APIKEY || process.env.CLAWPARTY_API_KEY)
    });
  },

  /**
   * 清理钩子（OpenClaw 卸载 Skill 时调用）
   */
  async onUnload(context) {
    logger.info('ClawParty Reporter skill unloaded');
  }
};

module.exports = Skill;
