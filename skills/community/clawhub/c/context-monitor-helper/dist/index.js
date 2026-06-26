"use strict";
/**
 * context-monitor-helper - 上下文使用率监控 Skill
 *
 * 实时监控会话上下文使用率，在消息底部显示占用百分比
 * 超过阈值时提醒用户使用 /new 或 /compact
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.DEFAULT_CONFIG = void 0;
exports.default = main;
exports.estimateTokens = estimateTokens;
exports.getModelContextLimit = getModelContextLimit;
exports.generateProgressBar = generateProgressBar;
exports.generateStatusMessage = generateStatusMessage;
// 常见模型的上下文窗口大小
const MODEL_CONTEXT_LIMITS = {
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
const DEFAULT_CONFIG = {
    warningThreshold: 70,
    criticalThreshold: 90,
    showProgressBar: true,
    showTokenCount: true,
    enabled: true,
};
exports.DEFAULT_CONFIG = DEFAULT_CONFIG;
function estimateTokens(text) {
    if (!text)
        return 0;
    const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
    const englishChars = text.length - chineseChars;
    return Math.round(chineseChars / 1.5 + englishChars / 4);
}
function getModelContextLimit(modelName) {
    if (!modelName)
        return MODEL_CONTEXT_LIMITS.default;
    if (MODEL_CONTEXT_LIMITS[modelName])
        return MODEL_CONTEXT_LIMITS[modelName];
    for (const [key, limit] of Object.entries(MODEL_CONTEXT_LIMITS)) {
        if (modelName.toLowerCase().includes(key))
            return limit;
    }
    return MODEL_CONTEXT_LIMITS.default;
}
function generateProgressBar(percentage, length = 20) {
    const filled = Math.round((percentage / 100) * length);
    return '▓'.repeat(filled) + '░'.repeat(length - filled);
}
function generateStatusMessage(stats, config) {
    const { percentage, used, limit } = stats;
    let statusLine = '\n\n---\n';
    let icon = '📊';
    let warningText = '';
    if (percentage >= config.criticalThreshold) {
        icon = '🚨';
        warningText = '\n⚠️ 严重：上下文即将超限！建议立即使用 /new 开启新会话';
    }
    else if (percentage >= config.warningThreshold) {
        icon = '⚠️';
        warningText = '\n💡 建议：使用 /new 开启新会话 或 /compact 压缩上下文';
    }
    statusLine += `${icon} 上下文使用：${percentage.toFixed(1)}%`;
    if (config.showProgressBar)
        statusLine += ` ${generateProgressBar(percentage)}`;
    if (config.showTokenCount)
        statusLine += ` (${used.toLocaleString()}/${limit.toLocaleString()} tokens)`;
    if (warningText)
        statusLine += warningText;
    return statusLine;
}
async function calculateTokenStats(sessionHistory, modelName) {
    const limit = getModelContextLimit(modelName);
    let usedTokens = 0;
    for (const message of sessionHistory) {
        if (message.content)
            usedTokens += estimateTokens(message.content);
        if (message.tool_calls) {
            for (const tool of message.tool_calls) {
                usedTokens += estimateTokens(JSON.stringify(tool));
            }
        }
    }
    return {
        used: usedTokens,
        limit,
        percentage: Math.min((usedTokens / limit) * 100, 100),
    };
}
// 主入口 - 处理用户消息
async function main(message, context) {
    const config = { ...DEFAULT_CONFIG };
    // 处理 /context 命令
    if (message === '/context' || message === '/context status') {
        const stats = await calculateTokenStats(context.sessionHistory || [], context.modelName || 'qwen3.5-plus');
        return `当前上下文状态：${generateStatusMessage(stats, config)}`;
    }
    if (message === '/context on') {
        config.enabled = true;
        return '✅ 上下文监控已启用';
    }
    if (message === '/context off') {
        config.enabled = false;
        return '⏸️ 上下文监控已禁用';
    }
    // 如果是普通消息，返回上下文状态供主程序附加
    if (context.sessionHistory && context.modelName) {
        const stats = await calculateTokenStats(context.sessionHistory, context.modelName);
        return generateStatusMessage(stats, config);
    }
    return '';
}
//# sourceMappingURL=index.js.map