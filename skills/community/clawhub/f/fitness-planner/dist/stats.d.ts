import { Stats, WeeklySummary, WorkoutRecord } from './types.js';
/**
 * 加载统计数据
 */
export declare function loadStats(): Stats;
/**
 * 保存统计数据
 */
export declare function saveStats(stats: Stats): void;
/**
 * 更新统计数据（打卡后调用）
 */
export declare function updateStats(record: WorkoutRecord): Stats;
/**
 * 重新计算所有统计数据
 */
export declare function recalculateStats(): Stats;
/**
 * 生成周总结
 */
export declare function generateWeeklySummary(weekStart: string): WeeklySummary;
/**
 * 格式化时长显示
 */
export declare function formatDuration(minutes: number): string;
