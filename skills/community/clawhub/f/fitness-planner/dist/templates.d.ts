import { WeekPlan, Goal, Location, Experience } from './types.js';
interface TemplateSelector {
    experience: Experience;
    goal: Goal;
    location: Location;
    weeklyDays: number;
}
/**
 * 生成周计划
 */
export declare function generateWeekPlan(selector: TemplateSelector, weekStart: string): WeekPlan;
/**
 * 获取本周起始日期（周一）
 */
export declare function getWeekStart(date?: Date): string;
/**
 * 格式化日期显示
 */
export declare function formatDate(dateStr: string): string;
export {};
