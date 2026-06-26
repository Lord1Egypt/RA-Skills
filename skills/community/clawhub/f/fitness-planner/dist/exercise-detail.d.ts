export interface ExerciseDetail {
    name: string;
    aliases: string[];
    category: 'chest' | 'back' | 'shoulder' | 'leg' | 'biceps' | 'triceps' | 'core' | 'cardio';
    equipment: string[];
    difficulty: 'beginner' | 'intermediate' | 'advanced';
    steps: string[];
    tips: string[];
    commonErrors: string[];
    videoSearchKeywords: string;
}
export declare const exerciseDetails: ExerciseDetail[];
/**
 * 根据动作名称查找详细讲解
 */
export declare function findExerciseDetail(name: string): ExerciseDetail | undefined;
/**
 * 获取动作的简要讲解（用于消息输出）
 */
export declare function getExerciseBrief(name: string): string;
/**
 * 获取动作的完整讲解
 */
export declare function getExerciseFullDescription(name: string): string;
