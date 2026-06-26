import { WorkoutRecord, Feeling, WeekPlan, DayPlan } from './types.js';
/**
 * 获取当前周计划文件路径
 */
export declare function getCurrentPlanPath(): string;
/**
 * 加载当前周计划
 */
export declare function loadCurrentPlan(): WeekPlan | null;
/**
 * 保存当前周计划
 */
export declare function saveCurrentPlan(plan: WeekPlan): void;
/**
 * 加载月度记录
 */
export declare function loadMonthRecords(yearMonth: string): WorkoutRecord[];
/**
 * 保存月度记录
 */
export declare function saveMonthRecords(yearMonth: string, records: WorkoutRecord[]): void;
/**
 * 记录打卡
 */
export declare function recordWorkout(date: string, dayName: string, durationMinutes: number, feeling?: Feeling | null, exercisesCompleted?: number, exercisesSkipped?: number, notes?: string): WorkoutRecord;
/**
 * 获取当日计划
 */
export declare function getTodayPlan(): DayPlan | null;
/**
 * 检查今日是否已打卡
 */
export declare function isTodayCompleted(): boolean;
/**
 * 获取今日记录
 */
export declare function getTodayRecord(): WorkoutRecord | null;
/**
 * 获取本周记录
 */
export declare function getWeekRecords(weekStart: string): WorkoutRecord[];
/**
 * 获取历史记录
 */
export declare function getHistoryRecords(limit?: number): WorkoutRecord[];
/**
 * 更新记录的感受
 */
export declare function updateFeeling(date: string, feeling: Feeling): WorkoutRecord | null;
