// 类型定义

export type Gender = 'male' | 'female';
export type Goal = 'build_muscle' | 'lose_fat' | 'shape' | 'maintain' | 'endurance';
export type Location = 'gym' | 'home' | 'outdoor';
export type Experience = 'beginner' | 'intermediate' | 'advanced';
export type Feeling = 'great' | 'okay' | 'tired';

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
