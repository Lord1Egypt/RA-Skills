/**
 * 通知推送模块
 * 复用 OpenClaw 的消息发送能力 + 可靠队列
 */

import { execSync } from 'child_process';
import { createLogger } from '../core/logger.js';
import { enqueueNotification, startNotificationProcessor } from '../utils/notificationQueue.js';

const logger = createLogger('Notifier');

// 启动后台通知处理器
let processorStarted = false;

/**
 * 启动可靠通知系统
 * @param {string} chatId
 */
export function startReliableNotifier(chatId) {
  if (processorStarted) return;
  
  startNotificationProcessor(chatId, async (notif) => {
    try {
      const success = await sendMessageDirect(notif.chat_id, formatNotification(notif));
      return success;
    } catch (error) {
      await logger.error('Failed to send notification', error);
      return false;
    }
  });
  
  processorStarted = true;
  logger.info('Reliable notification processor started');
}

/**
 * 格式化通知内容
 * @param {Object} notif
 * @returns {string}
 */
function formatNotification(notif) {
  switch (notif.type) {
    case 'research_complete':
      return formatResearchComplete(notif.data);
    case 'progress':
      return formatProgress(notif.data);
    case 'monitor_trigger':
      return formatMonitorTrigger(notif.data);
    default:
      return JSON.stringify(notif.data);
  }
}

/**
 * 直接发送消息（不经过队列）
 * @param {string} chatId
 * @param {string} text
 * @param {string} channel
 * @returns {Promise<boolean>}
 */
async function sendMessageDirect(chatId, text, channel = 'feishu') {
  try {
    // 方法1: 使用 OpenClaw CLI
    const result = execSync(
      `openclaw message send --channel ${channel} --target "${chatId}" --text "${text}"`,
      { encoding: 'utf-8', timeout: 10000 }
    );
    await logger.info(`Message sent to ${chatId}`);
    return true;
  } catch (error) {
    await logger.error(`Failed to send message via OpenClaw`, error);
    return false;
  }
}

/**
 * 发送消息（经过可靠队列）
 * @param {string} chatId - 目标聊天 ID
 * @param {string} text - 消息内容
 * @param {string} channel - 渠道（默认 feishu）
 * @returns {Promise<boolean>}
 */
export async function sendMessage(chatId, text, channel = 'feishu') {
  // 先尝试直接发送
  const directSuccess = await sendMessageDirect(chatId, text, channel);
  
  if (directSuccess) {
    return true;
  }
  
  // 如果失败，加入队列重试
  await logger.info(`Direct send failed, enqueueing for retry: ${chatId}`);
  
  await enqueueNotification({
    chatId,
    type: 'generic',
    data: { text, channel }
  });
  
  return false;
}

/**
 * 格式化研究完成通知
 * @param {Object} data
 * @returns {string}
 */
function formatResearchComplete(data) {
  const { topic, taskId, reportUrl, duration, monitorSuggestions = [] } = data;
  
  const monitorText = monitorSuggestions.length > 0 
    ? `\n🔔 建议监控：${monitorSuggestions.join('、')} 等 ${monitorSuggestions.length} 项\n💡 回复 Y 创建，N 跳过`
    : '';
  
  return `✅ 研究完成：${topic}

⏱️ 耗时：${duration} 分钟
📝 任务ID：${taskId}

🔗 ${reportUrl}
${monitorText}`;
}

/**
 * 发送研究完成通知
 * @param {Object} options
 * @param {string} options.chatId - 聊天 ID
 * @param {string} options.taskId - 任务 ID
 * @param {string} options.topic - 研究主题
 * @param {string} options.reportUrl - 报告链接
 * @param {number} options.duration - 耗时（分钟）
 * @param {Array} options.monitorSuggestions - 监控建议
 */
export async function sendResearchCompleteNotification({
  chatId,
  taskId,
  topic,
  reportUrl,
  duration,
  monitorSuggestions = []
}) {
  // 启动可靠通知系统
  startReliableNotifier(chatId);
  
  // 直接发送
  const message = formatResearchComplete({ topic, taskId, reportUrl, duration, monitorSuggestions });
  const success = await sendMessage(chatId, message);
  
  if (!success) {
    // 如果直接发送失败，加入队列
    await enqueueNotification({
      chatId,
      type: 'research_complete',
      data: { topic, taskId, reportUrl, duration, monitorSuggestions }
    });
  }
}

/**
 * 格式化进度通知
 * @param {Object} data
 * @returns {string}
 */
function formatProgress(data) {
  const { topic, elapsedMinutes } = data;
  
  const stageDescriptions = {
    0: '初始化研究任务',
    10: '全网信息搜集与初步筛选',
    30: '多源交叉验证与事实核查',
    50: '深度分析与逻辑推理',
    60: '报告生成与质量检查'
  };
  
  const stage = Object.keys(stageDescriptions)
    .map(Number)
    .filter(t => elapsedMinutes >= t)
    .pop() || 0;
  
  return `🔄 研究进度更新

📋 主题：${topic}
⏱️ 已用时：${elapsedMinutes} 分钟
📊 当前阶段：${stageDescriptions[stage]}

预计剩余时间：${60 - elapsedMinutes} 分钟`;
}

/**
 * 发送进度更新通知
 * @param {Object} options
 * @param {string} options.chatId - 聊天 ID
 * @param {string} options.taskId - 任务 ID
 * @param {string} options.topic - 研究主题
 * @param {string} options.progress - 进度描述
 * @param {number} options.elapsedMinutes - 已耗时（分钟）
 */
export async function sendProgressNotification({
  chatId,
  taskId,
  topic,
  progress,
  elapsedMinutes
}) {
  // 进度通知重要性较低，直接发送即可
  const message = formatProgress({ topic, elapsedMinutes });
  await sendMessage(chatId, message);
}

/**
 * 格式化监控触发通知
 * @param {Object} data
 * @returns {string}
 */
function formatMonitorTrigger(data) {
  const { monitorTitle, message, category = 'Data' } = data;
  const timestamp = new Date().toLocaleString('zh-CN');
  
  return `🔔 监控触发提醒

📊 监控：${monitorTitle}
📂 分类：${category}
⏰ 时间：${timestamp}

${message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 使用 /cn 查看最近通知`;
}

/**
 * 发送监控触发通知
 * @param {Object} options
 * @param {string} options.chatId - 聊天 ID
 * @param {string} options.monitorId - 监控 ID
 * @param {string} options.monitorTitle - 监控标题
 * @param {string} options.message - 触发消息
 * @param {string} options.category - 分类
 */
export async function sendMonitorTriggerNotification({
  chatId,
  monitorId,
  monitorTitle,
  message,
  category = 'Data'
}) {
  // 启动可靠通知系统
  startReliableNotifier(chatId);
  
  // 直接发送
  const notification = formatMonitorTrigger({ monitorTitle, message, category });
  const success = await sendMessage(chatId, notification);
  
  if (!success) {
    // 如果失败，加入队列（监控触发很重要）
    await enqueueNotification({
      chatId,
      type: 'monitor_trigger',
      data: { monitorId, monitorTitle, message, category }
    });
  }
}

/**
 * 格式化监控建议通知
 * @param {Object} data
 * @returns {string}
 */
function formatMonitorSuggestion(data) {
  const { topic, suggestions } = data;
  
  const suggestionsText = suggestions
    .map((s, i) => `${i + 1}. ${s.title} - ${s.description}`)
    .join('\n');
  
  return `💡 监控建议

研究主题：${topic}

基于研究报告，建议关注以下监控项：
${suggestionsText}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
回复 Y 确认创建这些监控项
回复 N 跳过`;
}

/**
 * 发送监控建议通知
 * @param {Object} options
 * @param {string} options.chatId - 聊天 ID
 * @param {string} options.taskId - 任务 ID
 * @param {string} options.topic - 研究主题
 * @param {Array} options.suggestions - 监控建议列表
 */
export async function sendMonitorSuggestionNotification({
  chatId,
  taskId,
  topic,
  suggestions
}) {
  if (!suggestions || suggestions.length === 0) return;
  
  // 启动可靠通知系统
  startReliableNotifier(chatId);
  
  // 直接发送
  const message = formatMonitorSuggestion({ topic, suggestions });
  const success = await sendMessage(chatId, message);
  
  if (!success) {
    // 如果失败，加入队列
    await enqueueNotification({
      chatId,
      type: 'monitor_suggestion',
      data: { taskId, topic, suggestions }
    });
  }
}
