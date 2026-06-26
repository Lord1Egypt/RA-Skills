// 类型定义

export type Gender = 'male' | 'female';
export type Goal = 'build_muscle' | 'lose_fat' | 'shape' | 'maintain' | 'endurance';
export type Location = 'gym' | 'home' | 'outdoor';
export type Experience = 'beginner' | 'intermediate' | 'advanced';
export type Feeling = 'great' | 'okay' | 'tired';

// ==================== 周期化训练 ====================

export type PhaseType = 'strength' | 'hypertrophy' | 'endurance' | 'deload';
export type PhaseIntensity = 'low' | 'medium' | 'high';

export interface TrainingPhase {
  type: PhaseType;
  weekNumber: number;        // 周期内的第几周
  totalWeeks: number;        // 这个阶段共几周
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

// ==================== 肌群进展追踪 ====================

export type MuscleGroup = 
  | 'chest'      // 胸肌
  | 'back'       // 背部
  | 'shoulder'   // 肩部
  | 'biceps'     // 二头肌
  | 'triceps'    // 三头肌
  | 'leg'        // 腿部
  | 'core'       // 核心
  | 'cardio';    // 有氧

export interface MuscleProgress {
  muscle: MuscleGroup;
  totalSets: number;         // 累计组数
  totalReps: number;         // 累计次数
  lastTrained: string | null;
  weeklyFrequency: number;   // 平均每周训练次数
  strengthProgress: number;  // 力量进展评分 (-100 ~ 100)
  hypertrophyProgress: number; // 肌肥大进展评分
  sorenessLevel: number;     // 酸痛程度 (1-10)
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

// ==================== 多维度反馈 ====================

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
    level: number;  // 1-10
  }[];
  motivation: number;  // 1-10
  notes?: string;
}

export interface FeedbackState {
  recentFeedback: MultiDimensionFeedback[];
  averageSleep: number;
  averageEnergy: number;
  averageStress: number;
  recoveryScore: number;  // 0-100 恢复指数
}

// ==================== 原有类型 ====================

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
