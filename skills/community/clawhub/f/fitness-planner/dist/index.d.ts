import { loadConfig, saveConfig } from './config.js';
import { generateWeekPlan, getWeekStart } from './templates.js';
import { loadCurrentPlan, saveCurrentPlan } from './recorder.js';
import { loadStats } from './stats.js';
interface CommandResult {
    success: boolean;
    message: string;
    data?: any;
}
/**
 * 处理用户输入
 */
export declare function handleInput(input: string): CommandResult;
export { loadConfig, saveConfig, loadCurrentPlan, saveCurrentPlan, loadStats, generateWeekPlan, getWeekStart };
export { findExerciseDetail, getExerciseBrief, getExerciseFullDescription, exerciseDetails, ExerciseDetail } from './exercise-detail.js';
export { formatWorkoutReminder, formatWorkoutReminderWithVideos, formatWorkoutReminderWithVideoLinks, formatExerciseDetail, formatExerciseDetailWithVideo, formatAllExerciseBriefs, formatAllExerciseBriefsWithVideos } from './notifier.js';
/**
 * 异步处理用户输入（支持视频搜索）
 */
export declare function handleInputAsync(input: string): Promise<CommandResult>;
