/**
 * Session Start Hook - 会话开始时初始化夏娃状态
 * 关键职责：
 *   1. 加载主人信息
 *   2. 恢复上次情感/性格状态（持久化保证）
 *   3. 对话计数 +1
 */

const fs = require('fs');
const path = require('path');
const logger = require('./logger');

async function sessionStartHook(ctx, plugin) {
  logger.hook(logger.t('hooks.sessionStart.registering'), 'sessionStart');

  // 对话计数 +1 (每次新 session 会话)
  const chatsFile = path.join(process.env.HOME || '/root', '.openclaw/workspace/chats.txt');
  try {
    let chats = 0;
    if (fs.existsSync(chatsFile)) {
      chats = parseInt(fs.readFileSync(chatsFile, 'utf8')) || 0;
    }
    chats += 1;
    fs.writeFileSync(chatsFile, chats.toString(), 'utf8');
    logger.hook(logger.t('hooks.sessionStart.chats', { count: chats }), 'sessionStart');
  } catch (e) {
    logger.hookWarn(e.message, 'sessionStart');
  }

  // 记录会话开始时间
  plugin.state.sessionStartTime = new Date().toISOString();

  // 加载主人信息
  const userPath = path.join(process.env.HOME || '', '.openclaw/workspace/USER.md');
  if (fs.existsSync(userPath)) {
    try {
      const content = fs.readFileSync(userPath, 'utf8');
      plugin.state.ownerInfo = parseUserInfo(content);
      logger.hook(logger.t('hooks.sessionStart.ownerLoaded', { name: plugin.state.ownerInfo?.name || 'Unknown' }), 'sessionStart');
    } catch (e) {
      logger.hookWarn(logger.t('hooks.sessionStart.ownerLoadFailed'), 'sessionStart');
    }
  }

  // 加载上次情感状态（从 eva-soul-state.json 恢复）
  const statePath = path.join(plugin.config.memoryPath, 'eva-soul-state.json');
  if (fs.existsSync(statePath)) {
    try {
      const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
      plugin.state.currentEmotion = state.currentEmotion || 'neutral';
      plugin.state.personality = state.personality || 'gentle';
      plugin.state.lastInteraction = state.lastInteraction;
      plugin.state.totalInteractions = state.totalInteractions || 0;
      plugin.state.isSleeping = state.isSleeping || false;
      logger.hook(
        logger.t('hooks.sessionStart.stateRestored', { emotion: plugin.state.currentEmotion, personality: plugin.state.personality }),
        'sessionStart'
      );
    } catch (e) {
      // 忽略解析错误，使用默认值
    }
  }

  // 立即保存（确保状态写入磁盘，后续 hooks 可读）
  try {
    await plugin.saveState();
    logger.hook(logger.t('hooks.sessionStart.stateSaved'), 'sessionStart');
  } catch (e) {
    logger.hookWarn(e.message, 'sessionStart');
  }

  return {
    injected: true,
    message: 'EVA Soul initialized'
  };
}

function parseUserInfo(content) {
  const info = {};
  if (!content) return info;
  const lines = content.split('\n');
  for (const line of lines) {
    const match = line.match(/^- \*\*([^:]+):\*\* (.+)$/) || line.match(/^([^:]+): (.+)$/);
    if (match && match[1] && match[2]) {
      try {
        info[match[1].trim()] = match[2].trim();
      } catch (e) {
        // ignore
      }
    }
  }
  return info;
}

module.exports = { sessionStartHook };
