/**
 * Context Usage Checker - 上下文使用率查询 Skill
 *
 * 查询当前会话的 Token 使用情况，提供进度条可视化和智能预警
 *
 * @author Spark
 * @version 1.0.0
 */
declare const MODEL_LIMITS: Record<string, number>;
declare const WARNING_THRESHOLD = 70;
declare const CRITICAL_THRESHOLD = 90;
/**
 * 估算文本的 token 数量
 * 中文约 1.5 字符/token，英文约 4 字符/token
 */
declare function estimateTokens(text: string): number;
/**
 * 生成进度条
 * @param percentage 百分比 (0-100)
 * @param length 进度条长度 (默认 20)
 */
declare function generateProgressBar(percentage: number, length?: number): string;
/**
 * 格式化数字（添加千位分隔符）
 */
declare function formatNumber(num: number): string;
/**
 * 获取模型的上下文窗口限制
 */
declare function getModelContextLimit(modelName: string): number;
/**
 * 计算会话的 token 使用统计
 */
declare function calculateTokenStats(sessionHistory: any[], modelName: string): {
    used: number;
    limit: number;
    percentage: number;
    remaining: number;
};
/**
 * 生成上下文状态消息
 */
declare function generateStatusMessage(stats: any, modelName: string): string;
/**
 * Skill 主函数
 */
export default function contextUsageChecker(params: any): Promise<void>;
export { estimateTokens, generateProgressBar, formatNumber, getModelContextLimit, calculateTokenStats, generateStatusMessage, MODEL_LIMITS, WARNING_THRESHOLD, CRITICAL_THRESHOLD, };
//# sourceMappingURL=index.d.ts.map