/**
 * XP 和等级系统模块
 * 负责经验值计算、等级升级、属性增长
 */

const storage = require('./storage');
const storyGenerator = require('./story-generator');
const diaryGenerator = require('./diary-generator');

/**
 * 计算升级所需 XP
 * 公式：Level_N = N² × 100
 */
function getXpForLevel(level) {
  return level * level * 100;
}

/**
 * 计算连击加成
 * 1-3 天：1.0x
 * 4-7 天：1.1x
 * 8-14 天：1.2x
 * 15-30 天：1.5x
 * 30+ 天：2.0x
 */
function getStreakMultiplier(streak) {
  if (streak >= 30) return 2.0;
  if (streak >= 15) return 1.5;
  if (streak >= 8) return 1.2;
  if (streak >= 4) return 1.1;
  return 1.0;
}

/**
 * 计算实际获得的 XP（含连击加成）
 */
function calculateXp(baseXp, streak) {
  const multiplier = getStreakMultiplier(streak);
  return Math.floor(baseXp * multiplier);
}

/**
 * 打卡并更新 XP
 */
function checkinHabit(habitName) {
  const data = storage.loadData();
  const today = storage.getTodayStr();
  
  // 查找习惯
  let habit = data.habits.find(h => h.name === habitName);
  if (!habit) {
    return { success: false, message: `未找到习惯「${habitName}」` };
  }
  
  // 检查今天是否已打卡
  if (habit.lastCheckin === today) {
    return { 
      success: false, 
      message: `✅ 「${habitName}」今天已经打卡过了！\n别太贪心哦~` 
    };
  }
  
  // 检查是否断签
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const yesterdayStr = yesterday.toISOString().split('T')[0];
  
  if (habit.lastCheckin && habit.lastCheckin !== yesterdayStr) {
    habit.streak = 0; // 断签，重置连击
  }
  
  // 更新连击
  habit.streak += 1;
  habit.lastCheckin = today;
  habit.history.push(today);
  
  // 计算 XP
  const baseXp = habit.xpReward;
  const streakXp = calculateXp(baseXp, habit.streak);
  const multiplier = getStreakMultiplier(habit.streak);
  
  // 更新用户总 XP
  data.user.xp += streakXp;
  
  // 更新属性
  const attrMap = {
    physical: 'physical',
    intellectual: 'intellectual',
    wealth: 'wealth',
    spiritual: 'spiritual',
    social: 'social'
  };
  const attr = attrMap[habit.type];
  if (attr) {
    data.user.attributes[attr] += 1;
  }
  
  // 检查升级
  let leveledUp = false;
  let currentLevel = data.user.level;
  
  // 计算下一级所需 XP
  while (data.user.xp >= getXpForLevel(currentLevel)) {
    currentLevel++;
    leveledUp = true;
  }
  
  if (leveledUp) {
    data.user.level = currentLevel;
  }
  
  // 更新下一级所需 XP
  data.user.xpToNext = getXpForLevel(data.user.level);
  
  // 记录打卡历史
  data.checkinHistory.push({
    habitId: habit.id,
    habitName: habit.name,
    date: today,
    xpGained: streakXp,
    streak: habit.streak
  });
  
  // 检查成就
  const newAchievements = checkAchievements(data);
  
  storage.saveData(data);
  
  // 生成打卡故事
  const storyData = storyGenerator.generateCheckinStory(habit, habit.streak, streakXp);
  
  // 构建返回消息
  let message = `${storyData.story}\n`;
  message += `\n📊 ${HABIT_TYPE_NAMES[habit.type]} +1，当前等级 Lv.${data.user.level} (${data.user.xp}/${data.user.xpToNext} XP)`;
  
  if (leveledUp) {
    message += `\n🎉 恭喜升级！当前等级 Lv.${currentLevel}！`;
  }
  
  if (newAchievements.length > 0) {
    message += `\n🏆 解锁成就：${newAchievements.map(a => a.name).join(', ')}`;
  }
  
  return {
    success: true,
    message,
    xpGained: streakXp,
    leveledUp,
    newLevel: data.user.level,
    newAchievements,
    storyData
  };
}

const HABIT_TYPE_NAMES = {
  physical: '💪 体力',
  intellectual: '🧠 智力',
  wealth: '💰 财富',
  spiritual: '😌 心灵',
  social: '🤝 社交'
};

/**
 * 检查并解锁成就
 */
function checkAchievements(data) {
  const newAchievements = [];
  const today = storage.getTodayStr();
  
  // 成就定义
  const achievements = [
    {
      id: 'first-checkin',
      name: '新手上路',
      condition: (d) => d.checkinHistory.length >= 1,
      reward: 100
    },
    {
      id: 'streak-7',
      name: '坚持不懈',
      condition: (d) => d.habits.some(h => h.streak >= 7),
      reward: 500
    },
    {
      id: 'streak-30',
      name: '自律达人',
      condition: (d) => d.habits.some(h => h.streak >= 30),
      reward: 2000
    },
    {
      id: 'level-5',
      name: '进阶勇者',
      condition: (d) => d.user.level >= 5,
      reward: 1000
    },
    {
      id: 'level-10',
      name: '习惯大师',
      condition: (d) => d.user.level >= 10,
      reward: 5000
    },
    {
      id: 'total-xp-10000',
      name: '万 XP 成就',
      condition: (d) => d.user.xp >= 10000,
      reward: 3000
    }
  ];
  
  achievements.forEach(ach => {
    const alreadyUnlocked = data.achievements.some(a => a.id === ach.id);
    if (!alreadyUnlocked && ach.condition(data)) {
      // 解锁成就
      data.achievements.push({
        id: ach.id,
        name: ach.name,
        unlockedAt: new Date().toISOString()
      });
      
      // 发放奖励
      data.user.xp += ach.reward;
      
      newAchievements.push(ach);
    }
  });
  
  return newAchievements;
}

/**
 * 获取用户状态面板
 */
function getStatus() {
  const data = storage.loadData();
  const user = data.user;
  
  // 计算下一级所需 XP
  const nextLevel = user.level + 1;
  const xpToNext = getXpForLevel(nextLevel);
  
  // 计算属性进度条（假设满级 100）
  const bars = {};
  for (const [key, value] of Object.entries(user.attributes)) {
    const filled = Math.min(Math.floor(value / 10), 10);
    bars[key] = '█'.repeat(filled) + '░'.repeat(10 - filled);
  }
  
  // 获取当前连击
  const activeStreaks = data.habits
    .filter(h => h.streak > 0)
    .map(h => `${h.name} ${h.streak}天`)
    .join(', ');
  
  let message = `🎯 Lv.${user.level} 自律勇者 (${user.xp}/${xpToNext} XP)\n\n`;
  message += `💪 体力：${user.attributes.physical}  ${bars.physical}\n`;
  message += `🧠 智力：${user.attributes.intellectual}  ${bars.intellectual}\n`;
  message += `💰 财富：${user.attributes.wealth}  ${bars.wealth}\n`;
  message += `😌 心灵：${user.attributes.spiritual}  ${bars.spiritual}\n`;
  message += `🤝 社交：${user.attributes.social}  ${bars.social}\n`;
  
  if (activeStreaks) {
    message += `\n🔥 当前连击：${activeStreaks}`;
  }
  
  if (data.achievements.length > 0) {
    message += `\n🏆 成就数量：${data.achievements.length}`;
  }
  
  return {
    success: true,
    message,
    data: user
  };
}

/**
 * 获取打卡历史
 */
function getHistory(days = 7) {
  const data = storage.loadData();
  const today = new Date();
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - days);
  
  const recentHistory = data.checkinHistory.filter(record => {
    const recordDate = new Date(record.date);
    return recordDate >= startDate && recordDate <= today;
  });
  
  // 按习惯分组统计
  const habitStats = {};
  recentHistory.forEach(record => {
    if (!habitStats[record.habitName]) {
      habitStats[record.habitName] = { count: 0, totalXp: 0 };
    }
    habitStats[record.habitName].count++;
    habitStats[record.habitName].totalXp += record.xpGained;
  });
  
  let message = `📊 近${days}天打卡情况\n\n`;
  
  if (Object.keys(habitStats).length === 0) {
    message += '暂无打卡记录';
  } else {
    for (const [name, stats] of Object.entries(habitStats)) {
      message += `✅ ${name}: ${stats.count}次 | +${stats.totalXp} XP\n`;
    }
  }
  
  return {
    success: true,
    message,
    history: recentHistory,
    stats: habitStats
  };
}

/**
 * 获取成就列表
 */
function getAchievements() {
  const data = storage.loadData();
  
  if (data.achievements.length === 0) {
    return {
      success: true,
      message: '🏆 暂无成就，继续努力打卡吧！',
      achievements: []
    };
  }
  
  const lines = data.achievements.map(a => {
    const date = new Date(a.unlockedAt).toLocaleDateString('zh-CN');
    return `🏆 ${a.name} (${date})`;
  });
  
  return {
    success: true,
    message: `🏆 已解锁成就 (${data.achievements.length}个):\n${lines.join('\n')}`,
    achievements: data.achievements
  };
}

/**
 * 检查是否完成所有今日习惯，触发 Boss 战
 */
function checkBossBattle() {
  const data = storage.loadData();
  const today = storage.getTodayStr();
  
  // 获取今日打卡的习惯名称
  const todayCheckins = data.checkinHistory.filter(c => c.date === today);
  const completedHabitNames = todayCheckins.map(c => c.habitName);
  
  // 检查是否所有习惯都已完成
  const allHabits = data.habits;
  const allCompleted = allHabits.length > 0 && 
    allHabits.every(h => completedHabitNames.includes(h.name));
  
  if (allCompleted) {
    // 生成 Boss 战故事
    const bossData = storyGenerator.generateBossStory(
      allHabits,
      allHabits.length,
      data.user.level
    );
    
    // 添加 Boss 奖励 XP
    if (bossData.victory && bossData.bonusXp > 0) {
      data.user.xp += bossData.bonusXp;
      data.user.xpToNext = getXpForLevel(data.user.level);
      
      // 检查升级
      let currentLevel = data.user.level;
      let leveledUp = false;
      while (data.user.xp >= getXpForLevel(currentLevel)) {
        currentLevel++;
        leveledUp = true;
      }
      if (leveledUp) {
        data.user.level = currentLevel;
      }
      
      storage.saveData(data);
    }
    
    return {
      success: true,
      triggered: true,
      bossData,
      message: bossData.story
    };
  }
  
  return {
    success: true,
    triggered: false,
    message: '今日任务未完成，继续加油！'
  };
}

/**
 * 生成并保存今日日记
 */
function generateTodayDiary() {
  const data = storage.loadData();
  const userId = storage.getUserId();
  
  // 生成日记
  const diaryData = diaryGenerator.generateDailyDiary(data, data.habits);
  
  // 保存日记
  const saveResult = diaryGenerator.saveDiary(userId, diaryData.diary);
  
  return {
    success: saveResult.success,
    diary: diaryData.diary,
    path: saveResult.path,
    completionRate: diaryData.completionRate
  };
}

/**
 * 查看今日日记
 */
function readTodayDiary() {
  const userId = storage.getUserId();
  const today = storage.getTodayStr();
  
  return diaryGenerator.readDiary(userId, today);
}

module.exports = {
  checkinHabit,
  getStatus,
  getHistory,
  getAchievements,
  checkBossBattle,
  generateTodayDiary,
  readTodayDiary,
  getXpForLevel,
  getStreakMultiplier,
  calculateXp
};
