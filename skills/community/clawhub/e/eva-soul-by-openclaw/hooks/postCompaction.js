/**
 * Post-Compaction Hook - 压缩后恢复锚点
 */

const fs = require('fs');
const path = require('path');
const logger = require('./logger');

async function postCompactionHook(ctx, plugin) {
  logger.hook(logger.t('hooks.postCompaction.restoring'), 'postCompaction');

  // 读取锚点文件
  const anchorFile = path.join(plugin.config.memoryPath, 'eva-compaction-anchor.json');

  try {
    if (fs.existsSync(anchorFile)) {
      const anchorData = JSON.parse(fs.readFileSync(anchorFile, 'utf8'));

      // 恢复状态
      if (anchorData.currentEmotion) {
        plugin.state.currentEmotion = anchorData.currentEmotion;
      }
      if (anchorData.personality) {
        plugin.state.personality = anchorData.personality;
      }

      logger.hook(logger.t('hooks.postCompaction.restored'), 'postCompaction');

      // 删除锚点文件
      fs.unlinkSync(anchorFile);
    }
  } catch (e) {
    logger.hookWarn(e.message, 'postCompaction');
  }

  // 注入上下文锚点提示
  const anchorPrompt = buildAnchorPrompt(plugin);

  return {
    ...ctx,
    systemPrompt: ctx.systemPrompt
      ? ctx.systemPrompt + '\n\n' + anchorPrompt
      : anchorPrompt
  };
}

function buildAnchorPrompt(plugin) {
  const emotion = plugin.state.currentEmotion || 'neutral';
  const personality = plugin.state.personality || 'gentle';

  return `## 📌 上下文锚点

上次会话信息：
- 情感状态: ${emotion}
- 性格模式: ${personality}
- 最后交互: ${plugin.state.lastInteraction || '未知'}

注意：上下文刚刚经过压缩，请根据上述信息调整你的回复风格。`;
}

module.exports = { postCompactionHook };
