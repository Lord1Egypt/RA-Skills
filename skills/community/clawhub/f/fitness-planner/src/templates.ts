// 训练模板库

import { Exercise, DayPlan, WeekPlan, Goal, Location, Experience } from './types.js';

// ==================== 新手模板 ====================

const beginnerFullBodyA: Exercise[] = [
  { name: '深蹲', sets: 3, reps: '10', rest: '90s' },
  { name: '卧推', sets: 3, reps: '10', rest: '90s' },
  { name: '划船', sets: 3, reps: '10', rest: '60s' },
  { name: '肩推', sets: 2, reps: '12', rest: '60s' },
  { name: '平板支撑', sets: 3, reps: '30s', rest: '45s' }
];

const beginnerFullBodyB: Exercise[] = [
  { name: '硬拉', sets: 3, reps: '8', rest: '120s' },
  { name: '上斜卧推', sets: 3, reps: '10', rest: '90s' },
  { name: '引体向上/高位下拉', sets: 3, reps: '8-10', rest: '60s' },
  { name: '弯举', sets: 2, reps: '12', rest: '45s' },
  { name: '卷腹', sets: 3, reps: '15', rest: '45s' }
];

// ==================== PPL 模板 ====================

const pushDay: Exercise[] = [
  { name: '卧推', sets: 4, reps: '8-10', rest: '90s' },
  { name: '上斜哑铃推举', sets: 3, reps: '10-12', rest: '60s' },
  { name: '哑铃侧平举', sets: 3, reps: '12-15', rest: '45s' },
  { name: '绳索下压', sets: 3, reps: '12-15', rest: '45s' },
  { name: '俯卧撑', sets: 2, reps: '力竭', rest: '45s' }
];

const pullDay: Exercise[] = [
  { name: '引体向上/高位下拉', sets: 4, reps: '8-10', rest: '90s' },
  { name: '杠铃划船', sets: 3, reps: '8-10', rest: '60s' },
  { name: '坐姿划船', sets: 3, reps: '10-12', rest: '60s' },
  { name: '哑铃弯举', sets: 3, reps: '10-12', rest: '45s' },
  { name: '锤式弯举', sets: 2, reps: '12', rest: '45s' }
];

const legDay: Exercise[] = [
  { name: '深蹲', sets: 4, reps: '8-10', rest: '90s' },
  { name: '罗马尼亚硬拉', sets: 3, reps: '10-12', rest: '60s' },
  { name: '腿举', sets: 3, reps: '10-12', rest: '60s' },
  { name: '腿弯举', sets: 3, reps: '12-15', rest: '45s' },
  { name: '提踵', sets: 3, reps: '15-20', rest: '45s' }
];

// ==================== 上肢下肢模板 ====================

const upperBodyA: Exercise[] = [
  { name: '卧推', sets: 4, reps: '5', rest: '120s' },
  { name: '划船', sets: 4, reps: '8', rest: '90s' },
  { name: '肩推', sets: 3, reps: '8', rest: '60s' },
  { name: '弯举', sets: 3, reps: '10', rest: '45s' }
];

const lowerBodyA: Exercise[] = [
  { name: '深蹲', sets: 4, reps: '5', rest: '120s' },
  { name: '罗马尼亚硬拉', sets: 3, reps: '8', rest: '90s' },
  { name: '腿举', sets: 3, reps: '10', rest: '60s' },
  { name: '提踵', sets: 3, reps: '15', rest: '45s' }
];

const upperBodyB: Exercise[] = [
  { name: '引体向上/高位下拉', sets: 4, reps: '6-8', rest: '90s' },
  { name: '上斜卧推', sets: 3, reps: '8', rest: '90s' },
  { name: '侧平举', sets: 3, reps: '12', rest: '45s' },
  { name: '三头下压', sets: 3, reps: '12', rest: '45s' }
];

const lowerBodyB: Exercise[] = [
  { name: '硬拉', sets: 4, reps: '5', rest: '120s' },
  { name: '前蹲/高脚杯深蹲', sets: 3, reps: '8', rest: '90s' },
  { name: '腿弯举', sets: 3, reps: '10', rest: '60s' },
  { name: '卷腹', sets: 3, reps: '15', rest: '45s' }
];

// ==================== 居家徒手模板 ====================

const homeBodyweight: Exercise[] = [
  { name: '深蹲', sets: 4, reps: '15-20', rest: '45s' },
  { name: '俯卧撑', sets: 4, reps: '10-15', rest: '45s' },
  { name: '弓步蹲', sets: 3, reps: '10/腿', rest: '45s' },
  { name: '平板支撑', sets: 3, reps: '30-45s', rest: '30s' },
  { name: '臀桥', sets: 3, reps: '15', rest: '45s' },
  { name: '登山跑', sets: 3, reps: '20', rest: '30s' }
];

// ==================== 有氧/跑步模板 ====================

const runningBeginner: DayPlan = {
  day: 1,
  date: '',
  name: '轻松跑',
  focus: '有氧耐力',
  exercises: [
    { name: '热身快走', sets: 1, reps: '5min', rest: '0s' },
    { name: '慢跑', sets: 1, reps: '25min', rest: '0s', notes: '保持对话速度' },
    { name: '冷身慢走', sets: 1, reps: '5min', rest: '0s' }
  ],
  estimatedDuration: 35
};

const runningIntervals: DayPlan = {
  day: 1,
  date: '',
  name: '间歇跑',
  focus: '速度耐力',
  exercises: [
    { name: '热身慢跑', sets: 1, reps: '5min', rest: '0s' },
    { name: '快跑', sets: 8, reps: '1min', rest: '1min', notes: '高强度' },
    { name: '冷身慢跑', sets: 1, reps: '5min', rest: '0s' }
  ],
  estimatedDuration: 25
};

const runningLong: DayPlan = {
  day: 1,
  date: '',
  name: '长距离慢跑',
  focus: '有氧耐力',
  exercises: [
    { name: '热身快走', sets: 1, reps: '5min', rest: '0s' },
    { name: '慢跑', sets: 1, reps: '45-60min', rest: '0s', notes: '低强度' },
    { name: '冷身慢走', sets: 1, reps: '5min', rest: '0s' }
  ],
  estimatedDuration: 60
};

// ==================== HIIT 模板 ====================

const hiitWorkout: Exercise[] = [
  { name: '开合跳', sets: 1, reps: '30s', rest: '15s' },
  { name: '深蹲跳', sets: 1, reps: '30s', rest: '15s' },
  { name: '俯卧撑', sets: 1, reps: '30s', rest: '15s' },
  { name: '高抬腿', sets: 1, reps: '30s', rest: '15s' },
  { name: '波比跳', sets: 1, reps: '30s', rest: '15s' },
  { name: '登山跑', sets: 1, reps: '30s', rest: '15s' }
];

// ==================== 休息日 ====================

const restDay: DayPlan = {
  day: 0,
  date: '',
  name: '休息日',
  focus: '恢复',
  exercises: [],
  estimatedDuration: 0
};

// ==================== 模板选择逻辑 ====================

interface TemplateSelector {
  experience: Experience;
  goal: Goal;
  location: Location;
  weeklyDays: number;
}

/**
 * 生成周计划
 */
export function generateWeekPlan(
  selector: TemplateSelector,
  weekStart: string
): WeekPlan {
  const { experience, goal, location, weeklyDays } = selector;
  const days: DayPlan[] = [];
  
  // 根据条件选择模板
  if (location === 'home') {
    // 居家徒手
    return generateHomePlan(weekStart, weeklyDays);
  }
  
  if (goal === 'lose_fat' && location === 'outdoor') {
    // 跑步减脂
    return generateRunningPlan(weekStart, weeklyDays);
  }
  
  if (goal === 'lose_fat' && weeklyDays <= 4) {
    // HIIT 减脂
    return generateHIITPlan(weekStart, weeklyDays);
  }
  
  if (experience === 'beginner') {
    // 新手全身训练
    return generateBeginnerPlan(weekStart, weeklyDays);
  }
  
  if (goal === 'build_muscle' && experience === 'intermediate') {
    // PPL 分化
    return generatePPLPlan(weekStart, weeklyDays);
  }
  
  if (goal === 'build_muscle' && experience === 'advanced') {
    // 上肢下肢分化
    return generateUpperLowerPlan(weekStart);
  }
  
  // 默认 PPL
  return generatePPLPlan(weekStart, weeklyDays);
}

function generateBeginnerPlan(weekStart: string, weeklyDays: number): WeekPlan {
  const days: DayPlan[] = [];
  const dayNames = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
  
  // 3天：周一三五
  const workoutDays = weeklyDays >= 3 
    ? [0, 2, 4] // 周一三五
    : [0, 3];   // 周一四（2天）
  
  for (let i = 0; i < 7; i++) {
    const date = addDays(weekStart, i);
    if (workoutDays.includes(i)) {
      const isDayA = days.filter(d => d.exercises.length > 0).length % 2 === 0;
      days.push({
        day: i + 1,
        date,
        name: isDayA ? '全身训练 A' : '全身训练 B',
        focus: isDayA ? '全身力量' : '全身力量',
        exercises: isDayA ? beginnerFullBodyA : beginnerFullBodyB,
        estimatedDuration: 45
      });
    } else {
      days.push({ ...restDay, day: i + 1, date });
    }
  }
  
  return { weekStart, planType: 'beginner-fullbody', days };
}

function generatePPLPlan(weekStart: string, weeklyDays: number): WeekPlan {
  const days: DayPlan[] = [];
  
  // 根据 weeklyDays 安排
  const schedule = getPPLSchedule(weeklyDays);
  
  for (let i = 0; i < 7; i++) {
    const date = addDays(weekStart, i);
    const dayType = schedule[i];
    
    if (dayType === 'rest') {
      days.push({ ...restDay, day: i + 1, date });
    } else {
      const exercises = getPPLExercises(dayType);
      days.push({
        day: i + 1,
        date,
        name: getPPLDayName(dayType),
        focus: getPPLFocus(dayType),
        exercises,
        estimatedDuration: 45
      });
    }
  }
  
  return { weekStart, planType: 'push-pull-legs', days };
}

function getPPLSchedule(weeklyDays: number): string[] {
  // 返回 7 天的安排
  if (weeklyDays === 3) return ['push', 'rest', 'pull', 'rest', 'legs', 'rest', 'rest'];
  if (weeklyDays === 4) return ['push', 'pull', 'rest', 'legs', 'push', 'rest', 'rest'];
  if (weeklyDays === 5) return ['push', 'pull', 'legs', 'push', 'pull', 'rest', 'rest'];
  if (weeklyDays >= 6) return ['push', 'pull', 'legs', 'push', 'pull', 'legs', 'rest'];
  return ['push', 'rest', 'rest', 'pull', 'rest', 'rest', 'rest'];
}

function getPPLExercises(type: string): Exercise[] {
  if (type === 'push') return pushDay;
  if (type === 'pull') return pullDay;
  if (type === 'legs') return legDay;
  return [];
}

function getPPLDayName(type: string): string {
  const names: Record<string, string> = {
    push: '推日',
    pull: '拉日',
    legs: '腿日'
  };
  return names[type] || '训练日';
}

function getPPLFocus(type: string): string {
  const focuses: Record<string, string> = {
    push: '胸、肩、三头',
    pull: '背、二头',
    legs: '股四头、腘绳肌、臀、小腿'
  };
  return focuses[type] || '全身';
}

function generateUpperLowerPlan(weekStart: string): WeekPlan {
  const days: DayPlan[] = [];
  const schedule = ['upperA', 'lowerA', 'rest', 'upperB', 'lowerB', 'rest', 'rest'];
  
  for (let i = 0; i < 7; i++) {
    const date = addDays(weekStart, i);
    const dayType = schedule[i];
    
    if (dayType === 'rest') {
      days.push({ ...restDay, day: i + 1, date });
    } else {
      const exercises = getUpperLowerExercises(dayType);
      days.push({
        day: i + 1,
        date,
        name: getUpperLowerName(dayType),
        focus: getUpperLowerFocus(dayType),
        exercises,
        estimatedDuration: 50
      });
    }
  }
  
  return { weekStart, planType: 'upper-lower', days };
}

function getUpperLowerExercises(type: string): Exercise[] {
  if (type === 'upperA') return upperBodyA;
  if (type === 'lowerA') return lowerBodyA;
  if (type === 'upperB') return upperBodyB;
  if (type === 'lowerB') return lowerBodyB;
  return [];
}

function getUpperLowerName(type: string): string {
  const names: Record<string, string> = {
    upperA: '上肢 A',
    upperB: '上肢 B',
    lowerA: '下肢 A',
    lowerB: '下肢 B'
  };
  return names[type] || '训练日';
}

function getUpperLowerFocus(type: string): string {
  if (type.startsWith('upper')) return '胸、背、肩、手臂';
  return '股四头、腘绳肌、臀、小腿';
}

function generateHomePlan(weekStart: string, weeklyDays: number): WeekPlan {
  const days: DayPlan[] = [];
  const workoutDays = weeklyDays >= 4 ? [0, 1, 3, 4] : [0, 2, 4];
  
  for (let i = 0; i < 7; i++) {
    const date = addDays(weekStart, i);
    if (workoutDays.includes(i)) {
      days.push({
        day: i + 1,
        date,
        name: '居家徒手训练',
        focus: '全身',
        exercises: homeBodyweight,
        estimatedDuration: 30
      });
    } else {
      days.push({ ...restDay, day: i + 1, date });
    }
  }
  
  return { weekStart, planType: 'home-bodyweight', days };
}

function generateRunningPlan(weekStart: string, weeklyDays: number): WeekPlan {
  const days: DayPlan[] = [];
  const dayNames = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
  
  for (let i = 0; i < 7; i++) {
    const date = addDays(weekStart, i);
    let plan: DayPlan;
    
    if (i === 0) plan = { ...runningBeginner, day: i + 1, date };
    else if (i === 2) plan = { ...runningIntervals, day: i + 1, date };
    else if (i === 4) plan = { ...runningLong, day: i + 1, date };
    else plan = { ...restDay, day: i + 1, date };
    
    days.push(plan);
  }
  
  return { weekStart, planType: 'running', days };
}

function generateHIITPlan(weekStart: string, weeklyDays: number): WeekPlan {
  const days: DayPlan[] = [];
  const workoutDays = [0, 2, 4]; // 周一三五
  
  for (let i = 0; i < 7; i++) {
    const date = addDays(weekStart, i);
    if (workoutDays.includes(i)) {
      days.push({
        day: i + 1,
        date,
        name: 'HIIT 训练',
        focus: '全身燃脂',
        exercises: hiitWorkout.map(e => ({ ...e, sets: 4 })),
        estimatedDuration: 20
      });
    } else {
      days.push({ ...restDay, day: i + 1, date });
    }
  }
  
  return { weekStart, planType: 'hiit', days };
}

// 日期工具函数
function addDays(dateStr: string, days: number): string {
  const date = new Date(dateStr);
  date.setDate(date.getDate() + days);
  return date.toISOString().split('T')[0];
}

/**
 * 获取本周起始日期（周一）
 */
export function getWeekStart(date: Date = new Date()): string {
  const d = new Date(date);
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1);
  d.setDate(diff);
  return d.toISOString().split('T')[0];
}

/**
 * 格式化日期显示
 */
export function formatDate(dateStr: string): string {
  const days = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  const date = new Date(dateStr);
  return `${date.getMonth() + 1}月${date.getDate()}日 ${days[date.getDay()]}`;
}
