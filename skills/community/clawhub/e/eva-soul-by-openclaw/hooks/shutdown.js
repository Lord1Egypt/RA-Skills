/**
 * Shutdown Hook - 关闭时保存状态
 */

const logger = require('./logger');

async function shutdownHook(ctx, plugin) {
  logger.hook(logger.t('hooks.shutdown.saving'), 'shutdown');

  // 更新最终状态
  plugin.state.lastShutdown = new Date().toISOString();
  plugin.state.sessionCount = (plugin.state.sessionCount || 0) + 1;

  // 保存状态
  try {
    await plugin.saveState();
    logger.hook(logger.t('hooks.shutdown.saved'), 'shutdown');
  } catch (e) {
    logger.hookWarn(e.message, 'shutdown');
  }

  return ctx;
}

module.exports = { shutdownHook };
