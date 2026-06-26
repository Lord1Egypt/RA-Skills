/**
 * 格式化工具函数
 */
/**
 * 格式化日期
 */
export declare function formatDate(date: Date | string): string;
/**
 * 格式化货币
 */
export declare function formatCurrency(amount: number, currency?: string): string;
/**
 * 格式化百分比
 */
export declare function formatPercentage(value: number, decimals?: number): string;
/**
 * 生成唯一 ID
 */
export declare function generateId(prefix?: string): string;
/**
 * 格式化风险等级
 */
export declare function formatRiskLevel(level: 'low' | 'medium' | 'high' | 'critical'): string;
/**
 * 格式化评级
 */
export declare function formatRating(rating: 'A' | 'B' | 'C' | 'D' | 'F'): string;
/**
 * 截断文本
 */
export declare function truncate(text: string, maxLength: number): string;
/**
 * 格式化列表为 Markdown
 */
export declare function formatListMarkdown(items: string[], ordered?: boolean): string;
/**
 * 格式化表格为 Markdown
 */
export declare function formatTableMarkdown(headers: string[], rows: string[][]): string;
//# sourceMappingURL=formatters.d.ts.map