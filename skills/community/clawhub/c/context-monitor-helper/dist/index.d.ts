/**
 * context-monitor-helper - 上下文使用率监控 Skill
 *
 * 实时监控会话上下文使用率，在消息底部显示占用百分比
 * 超过阈值时提醒用户使用 /new 或 /compact
 */
interface ContextMonitorConfig {
    warningThreshold: number;
    criticalThreshold: number;
    showProgressBar: boolean;
    showTokenCount: boolean;
    enabled: boolean;
}
interface TokenStats {
    used: number;
    limit: number;
    percentage: number;
}
declare const DEFAULT_CONFIG: ContextMonitorConfig;
declare function estimateTokens(text: string): number;
declare function getModelContextLimit(modelName: string): number;
declare function generateProgressBar(percentage: number, length?: number): string;
declare function generateStatusMessage(stats: TokenStats, config: ContextMonitorConfig): string;
export default function main(message: string, context: any): Promise<string>;
export { estimateTokens, getModelContextLimit, generateProgressBar, generateStatusMessage, DEFAULT_CONFIG };
//# sourceMappingURL=index.d.ts.map