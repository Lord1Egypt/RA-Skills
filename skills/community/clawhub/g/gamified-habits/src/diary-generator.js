/**
 * 日记生成器模块
 * 负责生成每日冒险日志
 */

const fs = require('fs');
const path = require('path');
const storage = require('./storage');

// 习惯类型对应的日记描述
const DIARY_TEMPLATES = {
  physical: {
    morning: "清晨，你战胜了困意，迎来了第一缕阳光 ☀️",
    action: "汗水见证了你的努力，身体变得更加强健 💪",
    evening: "一天的疲惫在运动后消散，身心舒畅 🌙"
  },
  intellectual: {
    morning: "晨光中，你翻开书页，智慧之光照亮心灵 📚",
    action: "知识的种子在心中生根发芽 🌱",
    evening: "夜幕降临，你回顾今日所学，收获满满 ✨"
  },
  wealth: {
    morning: "新的一天，你开始创造价值 💼",
    action: "每一份努力都在积累成财富 💰",
    evening: "回顾一天，你又创造了新的价值 🌟"
  },
  spiritual: {
    morning: "清晨冥想，内心如湖水般澄澈 🧘",
    action: "在宁静中，你找到了内心的平衡 ⚖️",
    evening: "夜晚反思，心灵得到净化与升华 🌙"
  },
  social: {
    morning: "新的一天，你准备传递温暖 💕",
    action: "真诚的交流让彼此更靠近 🤝",
    evening: "陪伴是最长情的告白，今天你做到了 👨‍👩‍👧"
  }
};

// 根据时间选择模板
function getTemplateByTime(type) {
  const hour = new Date().getHours();
  const templates = DIARY_TEMPLATES[type] || DIARY_TEMPLATES.physical;
  
  if (hour < 12) {
    return templates.morning;
  } else if (hour < 18) {
    return templates.action;
  } else {
    return templates.evening;
  }
}

/**
 * 生成每日冒险日志
 */
function generateDailyDiary(userData, habits) {
  const today = storage.getTodayStr();
  const checkinHistory = userData.checkinHistory || [];
  
  // 筛选今日打卡记录
  const todayCheckins = checkinHistory.filter(c => c.date === today);
  
  // 计算完成率
  const completionRate = habits.length > 0 
    ? Math.round((todayCheckins.length / habits.length) * 100) 
    : 0;
  
  // 构建日记内容
  let diary = `📖 ${today} 冒险日志\n\n`;
  diary += `━━━━━━━━━━━━━━━━━━━━━━\n\n`;
  
  // 开场白
  diary += `今天，你在自律的道路上继续前行...\n\n`;
  
  // 已完成的任务
  if (todayCheckins.length > 0) {
    diary += `✅ **今日战绩**\n\n`;
    todayCheckins.forEach((checkin, index) => {
      const habit = habits.find(h => h.id === checkin.habitId || h.name === checkin.habitName);
      const type = habit ? habit.type : 'physical';
      const template = getTemplateByTime(type);
      const customDesc = habit?.customDesc ? ` - ${habit.customDesc}` : '';
      
      diary += `${index + 1}. 「${checkin.habitName}」${customDesc}\n`;
      diary += `   ${template}\n`;
      diary += `   💫 +${checkin.xpGained} XP | 连击 ${checkin.streak} 天\n\n`;
    });
  }
  
  // 未完成的任务
  const completedHabitNames = todayCheckins.map(c => c.habitName);
  const incompleteHabits = habits.filter(h => !completedHabitNames.includes(h.name));
  
  if (incompleteHabits.length > 0) {
    diary += `❌ **待完成**\n\n`;
    incompleteHabits.forEach(habit => {
      diary += `• 「${habit.name}」- 下次继续加油！\n`;
    });
    diary += `\n`;
  }
  
  // 今日总结
  diary += `━━━━━━━━━━━━━━━━━━━━━━\n\n`;
  diary += `📊 **今日总结**\n\n`;
  diary += `• 完成率：${completionRate}% (${todayCheckins.length}/${habits.length})\n`;
  diary += `• 获得 XP：${todayCheckins.reduce((sum, c) => sum + c.xpGained, 0)}\n`;
  diary += `• 当前等级：Lv.${userData.user.level}\n`;
  
  // 评分
  const stars = getStarRating(completionRate);
  diary += `• 今日评分：${stars}\n\n`;
  
  // 明日预告
  diary += `🌅 **明日预告**\n\n`;
  if (completionRate === 100) {
    diary += `今天你击败了所有挑战！继续保持，你离"自律王者"又近了一步！\n`;
  } else if (completionRate >= 70) {
    diary += `今天表现不错！明天争取全部完成，加油！\n`;
  } else {
    diary += `明天是新的开始，相信自己能做到更好！\n`;
  }
  
  return {
    diary,
    date: today,
    completionRate,
    completedCount: todayCheckins.length,
    totalCount: habits.length
  };
}

/**
 * 获取评分星级
 */
function getStarRating(rate) {
  if (rate === 100) return "★★★★★";
  if (rate >= 80) return "★★★★☆";
  if (rate >= 60) return "★★★☆☆";
  if (rate >= 40) return "★★☆☆☆";
  return "★☆☆☆☆";
}

/**
 * 保存日记到文件
 */
function saveDiary(userId, diaryContent) {
  const dataDir = storage.DATA_DIR;
  const diaryDir = path.join(dataDir, 'diaries', userId);
  
  // 创建目录
  if (!fs.existsSync(diaryDir)) {
    fs.mkdirSync(diaryDir, { recursive: true });
  }
  
  // 保存文件
  const today = storage.getTodayStr();
  const filePath = path.join(diaryDir, `${today}.md`);
  
  try {
    fs.writeFileSync(filePath, diaryContent, 'utf8');
    return {
      success: true,
      path: filePath
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 读取指定日期的日记
 */
function readDiary(userId, date) {
  const dataDir = storage.DATA_DIR;
  const diaryDir = path.join(dataDir, 'diaries', userId);
  const filePath = path.join(diaryDir, `${date}.md`);
  
  try {
    if (fs.existsSync(filePath)) {
      const content = fs.readFileSync(filePath, 'utf8');
      return {
        success: true,
        content,
        path: filePath
      };
    }
    return {
      success: false,
      error: '日记不存在'
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

module.exports = {
  generateDailyDiary,
  saveDiary,
  readDiary,
  getStarRating,
  DIARY_TEMPLATES
};
