import { WorkoutRecord, WeekPlan } from './types.js';
interface AdjustmentState {
    consecutiveSkipped: number;
    consecutiveTired: number;
    consecutiveGreat: number;
    lastAdjustment: string | null;
    adjustmentHistory: Array<{
        date: string;
        type: string;
        reason: string;
    }>;
}
/**
 * 加载调整状态
 */
export declare function loadAdjustmentState(): AdjustmentState;
/**
 * 保存调整状态
 */
export declare function saveAdjustmentState(state: AdjustmentState): void;
/**
 * 检测异常并返回调整建议
 */
export declare function detectAnomalies(): {
    hasAnomaly: boolean;
    type: string;
    message: string;
    action: 'reduce' | 'increase' | 'inquire' | 'none';
};
/**
 * 更新调整状态（打卡时调用）
 */
export declare function updateAdjustmentState(record: WorkoutRecord): void;
/**
 * 记录跳过（未打卡时调用）
 */
export declare function recordSkip(): void;
/**
 * 重置跳过计数（打卡成功后调用）
 */
export declare function resetSkipCount(): void;
/**
 * 调整计划强度
 */
export declare function adjustPlanIntensity(action: 'reduce' | 'increase'): {
    success: boolean;
    message: string;
    plan?: WeekPlan;
};
/**
 * 生成下周计划（带调整）
 */
export declare function generateNextWeekPlan(): {
    success: boolean;
    message: string;
    plan?: WeekPlan;
};
/**
 * 检查是否需要主动询问
 */
export declare function checkProactiveInquiry(): string | null;
export {};
