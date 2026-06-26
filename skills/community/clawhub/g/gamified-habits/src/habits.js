/**
 * 习惯管理模块
 * 负责习惯的创建、删除、查询等操作
 */

const storage = require('./storage');

// 习惯类型映射
const HABIT_TYPES = {
  physical: '体力',
  intellectual: '智力',
  wealth: '财富',
  spiritual: '心灵',
  social: '社交'
};

// 默认 XP 奖励
const DEFAULT_XP = {
  physical: 50,
  intellectual: 60,
  wealth: 40,
  spiritual: 30,
  social: 35
};

/**
 * 创建习惯
 */
function createHabit(name, type = 'physical', frequency = 'daily', xpReward = null, customDesc = null, customSuccess = null) {
  const data = storage.loadData();
  
  // 检查是否已存在同名习惯
  const existing = data.habits.find(h => h.name === name);
  if (existing) {
    return { success: false, message: `习惯「${name}」已存在` };
  }
  
  // 确定 XP 奖励
  const xp = xpReward || DEFAULT_XP[type] || 50;
  
  const habit = {
    id: storage.generateId(),
    name,
    type,
    typeName: HABIT_TYPES[type] || '体力',
    frequency,
    xpReward: xp,
    streak: 0,
    lastCheckin: null,
    history: [],
    createdAt: new Date().toISOString()
  };
  
  // 可选的自定义描述
  if (customDesc) {
    habit.customDesc = customDesc;
  }
  if (customSuccess) {
    habit.customSuccess = customSuccess;
  }
  
  data.habits.push(habit);
  storage.saveData(data);
  
  return {
    success: true,
    message: `✅ 已创建习惯「${name}」\n类型：${habit.typeName} | 频率：${frequency === 'daily' ? '每日' : '每周'} | 奖励：${xp} XP${customDesc ? ` | 描述：${customDesc}` : ''}`,
    habit
  };
}

/**
 * 删除习惯
 */
function deleteHabit(name) {
  const data = storage.loadData();
  const index = data.habits.findIndex(h => h.name === name);
  
  if (index === -1) {
    return { success: false, message: `未找到习惯「${name}」` };
  }
  
  const deleted = data.habits.splice(index, 1)[0];
  storage.saveData(data);
  
  return {
    success: true,
    message: `🗑️ 已删除习惯「${name}」`,
    habit: deleted
  };
}

/**
 * 获取习惯列表
 */
function listHabits() {
  const data = storage.loadData();
  
  if (data.habits.length === 0) {
    return {
      success: true,
      message: '📋 暂无习惯，快创建一个吧！\n使用：habits create <名称> [类型]',
      habits: []
    };
  }
  
  const lines = data.habits.map(h => {
    const streak = h.streak > 0 ? ` 🔥${h.streak}天` : '';
    return `• ${h.name} (${h.typeName})${streak} - ${h.xpReward} XP/次`;
  });
  
  return {
    success: true,
    message: `📋 习惯列表 (${data.habits.length}个):\n${lines.join('\n')}`,
    habits: data.habits
  };
}

/**
 * 根据名称查找习惯
 */
function findHabitByName(name) {
  const data = storage.loadData();
  return data.habits.find(h => h.name === name);
}

/**
 * 根据模糊匹配查找习惯
 */
function findHabitByKeyword(keyword) {
  const data = storage.loadData();
  
  // 精确匹配
  const exact = data.habits.find(h => h.name === keyword);
  if (exact) return exact;
  
  // 包含匹配
  const partial = data.habits.find(h => h.name.includes(keyword));
  if (partial) return partial;
  
  // 类型匹配（如"跑步"匹配"体力"类型）
  const typeMap = {
    '跑': 'physical',
    '跳': 'physical',
    '健身': 'physical',
    '运动': 'physical',
    '读': 'intellectual',
    '学': 'intellectual',
    '写': 'intellectual',
    '储蓄': 'wealth',
    '记账': 'wealth',
    '冥想': 'spiritual',
    '日记': 'spiritual',
    '聚会': 'social',
    '聊天': 'social'
  };
  
  const targetType = typeMap[keyword];
  if (targetType) {
    return data.habits.find(h => h.type === targetType);
  }
  
  return null;
}

module.exports = {
  createHabit,
  deleteHabit,
  listHabits,
  findHabitByName,
  findHabitByKeyword,
  HABIT_TYPES,
  DEFAULT_XP
};
