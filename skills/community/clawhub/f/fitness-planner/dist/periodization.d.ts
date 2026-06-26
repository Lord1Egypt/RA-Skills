import { TrainingPhase, PeriodizationState, MuscleGroup, MuscleProgressState, MultiDimensionFeedback, FeedbackState, SleepQuality, StressLevel, EnergyLevel, WeekPlan, DayPlan, Exercise } from './types.js';
export declare const muscleGroupNames: Record<MuscleGroup, string>;
declare function loadPeriodizationState(): PeriodizationState;
declare function savePeriodizationState(state: PeriodizationState): void;
/**
 * 根据阶段调整训练计划
 */
export declare function adjustPlanForPhase(plan: WeekPlan, phase: TrainingPhase): WeekPlan;
/**
 * 推进到下一阶段
 */
export declare function advancePhase(): {
    message: string;
    newPhase: TrainingPhase;
};
/**
 * 获取当前阶段信息
 */
export declare function getCurrentPhase(): TrainingPhase;
/**
 * 更新阶段周数
 */
export declare function incrementPhaseWeek(): void;
export declare function loadMuscleProgress(): MuscleProgressState;
/**
 * 获取动作涉及的目标肌群
 */
export declare function getExerciseMuscles(exerciseName: string): MuscleGroup[];
/**
 * 记录肌群训练
 */
export declare function recordMuscleTraining(exercises: Exercise[]): void;
/**
 * 记录肌群酸痛
 */
export declare function recordSoreness(muscles: MuscleGroup[], level: number): void;
/**
 * 分析肌群训练不平衡
 */
export declare function analyzeMuscleBalance(): {
    undertrained: MuscleGroup[];
    overtrained: MuscleGroup[];
    recovered: MuscleGroup[];
    recommendations: string[];
};
/**
 * 根据肌群进展推荐动作调整
 */
export declare function recommendExerciseAdjustments(plan: DayPlan): {
    addExercises: Exercise[];
    removeExercises: string[];
    notes: string[];
};
export declare function loadFeedbackState(): FeedbackState;
/**
 * 记录多维度反馈
 */
export declare function recordFeedback(feedback: MultiDimensionFeedback): void;
/**
 * 快速反馈记录
 */
export declare function recordQuickFeedback(sleepHours: number, sleepQuality: SleepQuality, energy: EnergyLevel, stress: StressLevel): MultiDimensionFeedback;
/**
 * 分析恢复状态并给出建议
 */
export declare function analyzeRecoveryStatus(): {
    score: number;
    status: 'poor' | 'fair' | 'good' | 'excellent';
    recommendations: string[];
    shouldReduceIntensity: boolean;
};
/**
 * 综合分析 - 用于训练前决策
 */
export declare function getPreWorkoutAnalysis(): {
    phase: TrainingPhase;
    recovery: ReturnType<typeof analyzeRecoveryStatus>;
    muscleBalance: ReturnType<typeof analyzeMuscleBalance>;
    overallRecommendation: string;
};
export { loadPeriodizationState, savePeriodizationState };
