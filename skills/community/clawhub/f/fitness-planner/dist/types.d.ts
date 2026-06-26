export type Gender = 'male' | 'female';
export type Goal = 'build_muscle' | 'lose_fat' | 'shape' | 'maintain' | 'endurance';
export type Location = 'gym' | 'home' | 'outdoor';
export type Experience = 'beginner' | 'intermediate' | 'advanced';
export type Feeling = 'great' | 'okay' | 'tired';
export type PhaseType = 'strength' | 'hypertrophy' | 'endurance' | 'deload';
export type PhaseIntensity = 'low' | 'medium' | 'high';
export interface TrainingPhase {
    type: PhaseType;
    weekNumber: number;
    totalWeeks: number;
    startDate: string;
    endDate: string;
    intensity: PhaseIntensity;
    description: string;
}
export interface PeriodizationState {
    currentPhase: TrainingPhase;
    phaseHistory: TrainingPhase[];
    totalWeeksTrained: number;
}
export type MuscleGroup = 'chest' | 'back' | 'shoulder' | 'biceps' | 'triceps' | 'leg' | 'core' | 'cardio';
export interface MuscleProgress {
    muscle: MuscleGroup;
    totalSets: number;
    totalReps: number;
    lastTrained: string | null;
    weeklyFrequency: number;
    strengthProgress: number;
    hypertrophyProgress: number;
    sorenessLevel: number;
    lastSoreness: string | null;
    personalRecords: {
        exercise: string;
        weight: number;
        reps: number;
        date: string;
    }[];
}
export interface MuscleProgressState {
    muscles: Record<MuscleGroup, MuscleProgress>;
    lastUpdated: string;
}
export type SleepQuality = 'poor' | 'fair' | 'good' | 'excellent';
export type StressLevel = 'low' | 'medium' | 'high';
export type DietQuality = 'poor' | 'fair' | 'good' | 'excellent';
export type EnergyLevel = 'low' | 'medium' | 'high';
export interface MultiDimensionFeedback {
    date: string;
    sleep: {
        quality: SleepQuality;
        hours: number;
    };
    stress: StressLevel;
    diet: DietQuality;
    energy: EnergyLevel;
    soreness: {
        muscles: MuscleGroup[];
        level: number;
    }[];
    motivation: number;
    notes?: string;
}
export interface FeedbackState {
    recentFeedback: MultiDimensionFeedback[];
    averageSleep: number;
    averageEnergy: number;
    averageStress: number;
    recoveryScore: number;
}
export interface UserConfig {
    gender: Gender | null;
    age: number | null;
    goal: Goal | null;
    location: Location | null;
    weeklyDays: number | null;
    sessionDuration: number | null;
    experience: Experience | null;
    limitations: string[];
}
export interface NotificationConfig {
    channel: 'wecom' | 'wechat';
    advanceMinutes: number;
    morningSummary: boolean;
    weeklySummaryDay: 'sunday' | 'saturday';
    weeklySummaryTime: string;
}
export interface Config {
    user: UserConfig;
    notification: NotificationConfig;
    createdAt: string | null;
    updatedAt: string | null;
}
export interface Exercise {
    name: string;
    sets: number;
    reps: string;
    rest: string;
    weight?: string;
    notes?: string;
}
export interface DayPlan {
    day: number;
    date: string;
    name: string;
    focus: string;
    exercises: Exercise[];
    estimatedDuration: number;
}
export interface WeekPlan {
    weekStart: string;
    planType: string;
    days: DayPlan[];
}
export interface WorkoutRecord {
    date: string;
    dayName: string;
    completedAt: string;
    durationMinutes: number;
    feeling: Feeling | null;
    exercisesCompleted: number;
    exercisesSkipped: number;
    notes?: string;
}
export interface Stats {
    totalWorkouts: number;
    totalMinutes: number;
    currentStreak: number;
    longestStreak: number;
    thisMonth: {
        workouts: number;
        minutes: number;
        feelingDistribution: {
            great: number;
            okay: number;
            tired: number;
        };
    };
    lastWorkout: string | null;
}
export interface WeeklySummary {
    weekStart: string;
    weekEnd: string;
    totalDays: number;
    completedDays: number;
    totalMinutes: number;
    feelingDistribution: {
        great: number;
        okay: number;
        tired: number;
    };
    skippedDays: string[];
    recommendations: string[];
}
