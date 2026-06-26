import { DayPlan, WeekPlan, WeeklySummary, Feeling } from './types.js';
/**
 * 搜索动作教学视频
 */
export declare function searchExerciseVideo(exerciseName: string): Promise<{
    url: string;
    title: string;
    author: string;
} | null>;
/**
 * 批量搜索动作视频
 */
export declare function searchExerciseVideos(exercises: string[]): Promise<Map<string, {
    url: string;
    title: string;
    author: string;
}>>;
/**
 * 发送消息到企业微信
 * 通过 OpenClaw 的 message 工具实现
 */
export declare function sendWecomMessage(message: string): Promise<boolean>;
/**
 * 格式化训练提醒消息（包含动作讲解）
 */
export declare function formatWorkoutReminder(plan: DayPlan, includeDetails?: boolean): string;
/**
 * 格式化带视频链接的完整训练计划（异步版本）
 */
export declare function formatWorkoutReminderWithVideoLinks(plan: DayPlan): Promise<string>;
/**
 * 格式化带视频链接的训练计划
 */
export declare function formatWorkoutReminderWithVideos(plan: DayPlan, videoLinks: Map<string, string>): string;
/**
 * 格式化单个动作的详细讲解
 */
export declare function formatExerciseDetail(name: string): string;
/**
 * 格式化单个动作的详细讲解（包含视频链接）
 */
export declare function formatExerciseDetailWithVideo(name: string): Promise<string>;
/**
 * 格式化所有动作的简要讲解
 */
export declare function formatAllExerciseBriefs(plan: DayPlan): string;
/**
 * 格式化所有动作的完整讲解（包含视频链接）
 */
export declare function formatAllExerciseBriefsWithVideos(plan: DayPlan): Promise<string>;
/**
 * 格式化早间总结消息
 */
export declare function formatMorningSummary(plan: DayPlan | null): string;
/**
 * 格式化打卡成功消息
 */
export declare function formatCheckinSuccess(dayName: string, duration: number, feeling: Feeling | null): string;
/**
 * 格式化周总结消息
 */
export declare function formatWeeklySummary(summary: WeeklySummary): string;
/**
 * 格式化本周进度消息
 */
export declare function formatWeekProgress(plan: WeekPlan, completedDates: string[], records: Map<string, {
    feeling: Feeling | null;
    duration: number;
}>): string;
/**
 * 格式化统计消息
 */
export declare function formatStatsMessage(stats: {
    totalWorkouts: number;
    totalMinutes: number;
    currentStreak: number;
    longestStreak: number;
    thisMonth: {
        workouts: number;
        minutes: number;
    };
}): string;
