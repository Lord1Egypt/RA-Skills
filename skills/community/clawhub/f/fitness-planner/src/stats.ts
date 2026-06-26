// 统计模块

import * as fs from 'fs';
import * as path from 'path';
import { Stats, WeeklySummary, WorkoutRecord, Feeling } from './types.js';
import { loadMonthRecords, loadCurrentPlan, getWeekRecords } from './recorder.js';

const BASE_DIR = path.join(process.env.HOME || '/root', '.openclaw/workspace/fitness-planner');
const STATS_FILE = path.join(BASE_DIR, 'stats.json');

const defaultStats: Stats = {
  totalWorkouts: 0,
  totalMinutes: 0,
  currentStreak: 0,
  longestStreak: 0,
  thisMonth: {
    workouts: 0,
    minutes: 0,
    feelingDistribution: {
      great: 0,
      okay: 0,
      tired: 0
    }
  },
  lastWorkout: null
};

/**
 * 加载统计数据
 */
export function loadStats(): Stats {
  if (!fs.existsSync(STATS_FILE)) {
    saveStats(defaultStats);
    return defaultStats;
  }
  const content = fs.readFileSync(STATS_FILE, 'utf-8');
  const raw = JSON.parse(content);
  
  // 兼容 snake_case 格式
  const stats: Stats = {
    totalWorkouts: raw.totalWorkouts ?? raw.total_workouts ?? 0,
    totalMinutes: raw.totalMinutes ?? raw.total_minutes ?? 0,
    currentStreak: raw.currentStreak ?? raw.current_streak ?? 0,
    longestStreak: raw.longestStreak ?? raw.longest_streak ?? 0,
    thisMonth: {
      workouts: raw.thisMonth?.workouts ?? raw.this_month?.workouts ?? 0,
      minutes: raw.thisMonth?.minutes ?? raw.this_month?.minutes ?? 0,
      feelingDistribution: raw.thisMonth?.feelingDistribution ?? raw.this_month?.feeling_distribution ?? {
        great: 0,
        okay: 0,
        tired: 0
      }
    },
    lastWorkout: raw.lastWorkout ?? raw.last_workout ?? null
  };
  
  return stats;
}

/**
 * 保存统计数据
 */
export function saveStats(stats: Stats): void {
  fs.writeFileSync(STATS_FILE, JSON.stringify(stats, null, 2), 'utf-8');
}

/**
 * 更新统计数据（打卡后调用）
 */
export function updateStats(record: WorkoutRecord): Stats {
  const stats = loadStats();
  const today = new Date().toISOString().split('T')[0];
  const currentMonth = today.substring(0, 7);
  const recordMonth = record.date.substring(0, 7);
  
  // 更新总计
  stats.totalWorkouts += 1;
  stats.totalMinutes += record.durationMinutes;
  stats.lastWorkout = record.date;
  
  // 更新连续天数
  stats.currentStreak = calculateCurrentStreak(record.date);
  if (stats.currentStreak > stats.longestStreak) {
    stats.longestStreak = stats.currentStreak;
  }
  
  // 更新本月统计
  if (recordMonth === currentMonth) {
    stats.thisMonth.workouts += 1;
    stats.thisMonth.minutes += record.durationMinutes;
    if (record.feeling) {
      stats.thisMonth.feelingDistribution[record.feeling] += 1;
    }
  }
  
  saveStats(stats);
  return stats;
}

/**
 * 计算当前连续天数
 */
function calculateCurrentStreak(lastDate: string): number {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  const last = new Date(lastDate);
  last.setHours(0, 0, 0, 0);
  
  const diffDays = Math.floor((today.getTime() - last.getTime()) / (1000 * 60 * 60 * 24));
  
  // 如果最后训练是今天或昨天，计算连续
  if (diffDays <= 1) {
    let streak = 0;
    let checkDate = new Date(today);
    
    while (true) {
      const dateStr = checkDate.toISOString().split('T')[0];
      const yearMonth = dateStr.substring(0, 7);
      const records = loadMonthRecords(yearMonth);
      
      if (records.some(r => r.date === dateStr)) {
        streak += 1;
        checkDate.setDate(checkDate.getDate() - 1);
      } else {
        break;
      }
    }
    
    return streak;
  }
  
  return 0;
}

/**
 * 重新计算所有统计数据
 */
export function recalculateStats(): Stats {
  const today = new Date().toISOString().split('T')[0];
  const currentMonth = today.substring(0, 7);
  
  let totalWorkouts = 0;
  let totalMinutes = 0;
  let thisMonthWorkouts = 0;
  let thisMonthMinutes = 0;
  const feelingDistribution = { great: 0, okay: 0, tired: 0 };
  let lastWorkout: string | null = null;
  
  // 遍历所有记录文件
  const recordsDir = path.join(BASE_DIR, 'records');
  if (fs.existsSync(recordsDir)) {
    const files = fs.readdirSync(recordsDir).filter(f => f.endsWith('.json'));
    
    for (const file of files) {
      const yearMonth = file.replace('.json', '');
      const records = loadMonthRecords(yearMonth);
      
      for (const record of records) {
        totalWorkouts += 1;
        totalMinutes += record.durationMinutes;
        
        if (record.feeling) {
          feelingDistribution[record.feeling] += 1;
        }
        
        if (!lastWorkout || record.date > lastWorkout) {
          lastWorkout = record.date;
        }
        
        if (yearMonth === currentMonth) {
          thisMonthWorkouts += 1;
          thisMonthMinutes += record.durationMinutes;
        }
      }
    }
  }
  
  const stats: Stats = {
    totalWorkouts,
    totalMinutes,
    currentStreak: lastWorkout ? calculateCurrentStreak(lastWorkout) : 0,
    longestStreak: 0, // 需要单独计算
    thisMonth: {
      workouts: thisMonthWorkouts,
      minutes: thisMonthMinutes,
      feelingDistribution
    },
    lastWorkout
  };
  
  // 计算最长连续
  stats.longestStreak = calculateLongestStreak();
  
  saveStats(stats);
  return stats;
}

/**
 * 计算最长连续天数
 */
function calculateLongestStreak(): number {
  const allDates: string[] = [];
  
  const recordsDir = path.join(BASE_DIR, 'records');
  if (fs.existsSync(recordsDir)) {
    const files = fs.readdirSync(recordsDir).filter(f => f.endsWith('.json'));
    
    for (const file of files) {
      const records = loadMonthRecords(file.replace('.json', ''));
      allDates.push(...records.map(r => r.date));
    }
  }
  
  if (allDates.length === 0) return 0;
  
  // 排序
  allDates.sort();
  
  let maxStreak = 1;
  let currentStreak = 1;
  
  for (let i = 1; i < allDates.length; i++) {
    const prev = new Date(allDates[i - 1]);
    const curr = new Date(allDates[i]);
    const diff = Math.floor((curr.getTime() - prev.getTime()) / (1000 * 60 * 60 * 24));
    
    if (diff === 1) {
      currentStreak += 1;
      if (currentStreak > maxStreak) {
        maxStreak = currentStreak;
      }
    } else if (diff > 1) {
      currentStreak = 1;
    }
    // diff === 0 是同一天，跳过
  }
  
  return maxStreak;
}

/**
 * 生成周总结
 */
export function generateWeeklySummary(weekStart: string): WeeklySummary {
  const plan = loadCurrentPlan();
  const records = getWeekRecords(weekStart);
  
  const weekEnd = addDays(weekStart, 6);
  const totalDays = plan ? plan.days.filter(d => d.exercises.length > 0).length : 0;
  const completedDays = records.length;
  const totalMinutes = records.reduce((sum, r) => sum + r.durationMinutes, 0);
  
  const feelingDistribution = { great: 0, okay: 0, tired: 0 };
  for (const r of records) {
    if (r.feeling) {
      feelingDistribution[r.feeling] += 1;
    }
  }
  
  // 找出跳过的天数
  const skippedDays: string[] = [];
  if (plan) {
    for (const day of plan.days) {
      if (day.exercises.length > 0 && !records.some(r => r.date === day.date)) {
        skippedDays.push(day.date);
      }
    }
  }
  
  // 生成建议
  const recommendations = generateRecommendations(
    completedDays,
    totalDays,
    feelingDistribution,
    skippedDays
  );
  
  return {
    weekStart,
    weekEnd,
    totalDays,
    completedDays,
    totalMinutes,
    feelingDistribution,
    skippedDays,
    recommendations
  };
}

/**
 * 生成调整建议
 */
function generateRecommendations(
  completedDays: number,
  totalDays: number,
  feelings: { great: number; okay: number; tired: number },
  skippedDays: string[]
): string[] {
  const recommendations: string[] = [];
  
  const completionRate = totalDays > 0 ? completedDays / totalDays : 0;
  
  if (completionRate < 0.5) {
    recommendations.push('本周完成率较低，考虑减少训练天数或调整训练时间');
  }
  
  if (feelings.tired > feelings.great) {
    recommendations.push('多次感到疲劳，建议增加休息日或降低训练强度');
  }
  
  if (feelings.great > feelings.okay + feelings.tired && completionRate >= 0.8) {
    recommendations.push('状态很好！下周可以考虑适当增加强度');
  }
  
  if (skippedDays.length > 0) {
    recommendations.push(`跳过了 ${skippedDays.length} 天训练，如果太忙可以调整计划`);
  }
  
  if (recommendations.length === 0) {
    recommendations.push('本周表现不错，继续保持！');
  }
  
  return recommendations;
}

// 日期工具
function addDays(dateStr: string, days: number): string {
  const date = new Date(dateStr);
  date.setDate(date.getDate() + days);
  return date.toISOString().split('T')[0];
}

/**
 * 格式化时长显示
 */
export function formatDuration(minutes: number): string {
  if (minutes < 60) return `${minutes} 分钟`;
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return mins > 0 ? `${hours} 小时 ${mins} 分钟` : `${hours} 小时`;
}
