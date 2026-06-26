/**
 * Context Usage Checker - 上下文使用率查询 Skill
 * 
 * 查询当前会话的 Token 使用情况，提供进度条可视化和智能预警
 * 
 * @author Spark
 * @version 1.0.0
 */

// 模型上下文窗口限制
const MODEL_LIMITS: Record<string, number> = {
  'qwen3.5-plus': 256000,
  'qwen3.5': 256000,
  'qwen-max': 32000,
  'qwen-plus': 32000,
  'claude-3-5-sonnet': 200000,
  'claude-3-opus': 200000,
  'claude-3-sonnet': 200000,
  'claude-3-haiku': 200000,
  'gpt-4-turbo': 128000,
  'gpt-4': 128000,
  'gpt-4o': 128000,
  'gpt-3.5-turbo': 16385,
  'gemini-pro': 128000,
  'llama-3-70b': 8192,
  'default': 128000,
};

// 阈值配置
const WARNING_THRESHOLD = 70;      // 警告阈值（%）
const CRITICAL_THRESHOLD = 90;     // 严重警告阈值（%）

/**
 * 估算文本的 token 数量
 * 中文约 1.5 字符/token，英文约 4 字符/token
 */
function estimateTokens(text: string): number {
  if (!text) return 0;
  const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
  const englishChars = text.length - chineseChars;
  return Math.round(chineseChars / 1.5 + englishChars / 4);
}

/**
 * 生成进度条
 * @param percentage 百分比 (0-100)
 * @param length 进度条长度 (默认 20)
 */
function generateProgressBar(percentage: number, length: number = 20): string {
  const filled = Math.round((percentage / 100) * length);
  return '▓'.repeat(filled) + '░'.repeat(length - filled);
}

/**
 * 格式化数字（添加千位分隔符）
 */
function formatNumber(num: number): string {
  return num.toLocaleString();
}

/**
 * 获取模型的上下文窗口限制
 */
function getModelContextLimit(modelName: string): number {
  if (!modelName) return MODEL_LIMITS.default;
  if (MODEL_LIMITS[modelName]) return MODEL_LIMITS[modelName];
  
  // 模糊匹配
  for (const [key, limit] of Object.entries(MODEL_LIMITS)) {
    if (modelName.toLowerCase().includes(key)) return limit;
  }
  return MODEL_LIMITS.default;
}

/**
 * 计算会话的 token 使用统计
 */
function calculateTokenStats(sessionHistory: any[], modelName: string) {
  const limit = getModelContextLimit(modelName);
  let usedTokens = 0;
  
  for (const message of sessionHistory) {
    if (message.content) {
      usedTokens += estimateTokens(message.content);
    }
    if (message.tool_calls) {
      for (const tool of message.tool_calls) {
        usedTokens += estimateTokens(JSON.stringify(tool));
      }
    }
  }
  
  const percentage = Math.min((usedTokens / limit) * 100, 100);
  const remaining = limit - usedTokens;
  
  return {
    used: usedTokens,
    limit,
    percentage,
    remaining,
  };
}

/**
 * 生成上下文状态消息
 */
function generateStatusMessage(stats: any, modelName: string): string {
  const { percentage, used, limit, remaining } = stats;
  
  let icon = '📊';
  let statusText = '正常';
  let advice = '> ✅ 上下文使用正常，可以继续对话';
  
  if (percentage >= CRITICAL_THRESHOLD) {
    icon = '🚨';
    statusText = '严重';
    advice = '> 🚨 **严重警告：** 上下文即将超限！建议立即使用 `/new` 开启新会话';
  } else if (percentage >= WARNING_THRESHOLD) {
    icon = '⚠️';
    statusText = '警告';
    advice = '> 💡 **建议：** 使用 `/new` 开启新会话 或 `/compact` 压缩上下文';
  } else if (percentage >= 50) {
    advice = '> ✅ 上下文使用正常，可以继续对话';
  }
  
  const progressBar = generateProgressBar(percentage);
  
  let message = `### ${icon} 上下文使用状态\n\n`;
  message += `**状态：** ${statusText}\n`;
  message += `**模型：** ${modelName}\n\n`;
  message += `**使用率：** ${percentage.toFixed(1)}%\n`;
  message += `\`${progressBar}\`\n\n`;
  message += `**已使用：** ${formatNumber(used)} tokens\n`;
  message += `**剩余：** ${formatNumber(remaining)} tokens\n`;
  message += `**总计：** ${formatNumber(limit)} tokens\n\n`;
  message += advice;
  
  return message;
}

/**
 * Skill 主函数
 */
export default async function contextUsageChecker(params: any) {
  const { runtime, reply } = params;
  
  try {
    // 获取当前会话历史
    const sessionHistory = runtime?.session?.history || [];
    const modelName = runtime?.agent?.model?.id || 'qwen3.5-plus';
    
    // 计算 token 使用统计
    const stats = calculateTokenStats(sessionHistory, modelName);
    
    // 生成状态消息
    const statusMessage = generateStatusMessage(stats, modelName);
    
    // 回复用户
    await reply({ text: statusMessage });
    
  } catch (error) {
    // 错误处理
    const errorMessage = `### ❌ 查询失败\n\n无法获取上下文使用率：${error instanceof Error ? error.message : String(error)}\n\n请重试或联系管理员。`;
    await reply({ text: errorMessage });
  }
}

// 导出工具函数供其他模块使用
export {
  estimateTokens,
  generateProgressBar,
  formatNumber,
  getModelContextLimit,
  calculateTokenStats,
  generateStatusMessage,
  MODEL_LIMITS,
  WARNING_THRESHOLD,
  CRITICAL_THRESHOLD,
};
