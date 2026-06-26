/**
 * 故事生成器模块
 * 负责生成打卡时的战斗/冒险描述
 */

// 习惯类型对应的战斗场景模板
const SCENARIOS = {
  physical: {
    monsters: ["懒惰小怪", "疲惫兽", "虚弱史莱姆", "倦怠魔", "无力幽灵"],
    actions: ["训练", "挑战", "突破", "战胜", "征服"],
    descriptions: [
      "汗水顺着脸颊滑落，你感受到了力量的增长",
      "每一次坚持，都是对极限的突破",
      "身体在颤抖，但意志更加坚定",
      "你用实际行动证明了什么是毅力",
      "肌肉的酸痛是成长的勋章"
    ],
    rewards: ["体力成长", "耐力提升", "活力满满"]
  },
  intellectual: {
    monsters: ["无知幽灵", "困惑魔", "健忘怪", "迷茫灵", "愚昧兽"],
    actions: ["研习", "领悟", "探索", "启迪", "突破"],
    descriptions: [
      "知识的光芒照亮了你的心灵",
      "新的理解在脑海中浮现",
      "你感受到了智慧的成长",
      "思维的边界被拓宽了",
      "每一页都是通往智慧的阶梯"
    ],
    rewards: ["智慧提升", "思维敏捷", "洞察力强"]
  },
  wealth: {
    monsters: ["贫穷鬼", "浪费魔", "冲动怪", "挥霍灵", "贪婪兽"],
    actions: ["积累", "创造", "经营", "增值", "守护"],
    descriptions: [
      "价值在你的手中诞生",
      "每一份努力都在积累成财富",
      "你用实际行动创造了价值",
      "资源的种子正在发芽",
      "财富的基石又坚固了一分"
    ],
    rewards: ["财富增长", "价值提升", "资源丰富"]
  },
  spiritual: {
    monsters: ["焦虑魔", "浮躁怪", "混乱灵", "烦恼兽", "忧郁幽灵"],
    actions: ["净化", "平静", "修行", "沉淀", "升华"],
    descriptions: [
      "内心重归平静，如湖水般澄澈",
      "杂念消散，真我浮现",
      "你找到了内心的平衡点",
      "心灵在宁静中得到升华",
      "每一次呼吸都是与自己的对话"
    ],
    rewards: ["心灵成长", "内心平静", "精神饱满"]
  },
  social: {
    monsters: ["孤独怪", "社恐魔", "冷漠灵", "隔阂兽", "误解幽灵"],
    actions: ["连接", "陪伴", "守护", "沟通", "温暖"],
    descriptions: [
      "温暖的情感在心中流淌",
      "你用心守护着重要的羁绊",
      "爱的力量让彼此更靠近",
      "真诚的交流打开心灵",
      "陪伴是最长情的告白"
    ],
    rewards: ["羁绊加深", "人缘提升", "温暖满满"]
  }
};

// 连击称号
const STREAK_TITLES = {
  1: "新手冒险者",
  3: "熟练战士",
  7: "精英勇者",
  14: "传奇英雄",
  30: "不朽传说",
  100: "永恒神话"
};

/**
 * 获取连击称号
 */
function getStreakTitle(streak) {
  const thresholds = [100, 30, 14, 7, 3, 1];
  for (const threshold of thresholds) {
    if (streak >= threshold) {
      return STREAK_TITLES[threshold];
    }
  }
  return "见习冒险者";
}

/**
 * 生成打卡故事
 */
function generateCheckinStory(habit, streak, xpGained) {
  const scenario = SCENARIOS[habit.type] || SCENARIOS.physical;
  
  // 随机选择元素
  const monster = scenario.monsters[Math.floor(Math.random() * scenario.monsters.length)];
  const action = scenario.actions[Math.floor(Math.random() * scenario.actions.length)];
  const description = scenario.descriptions[Math.floor(Math.random() * scenario.descriptions.length)];
  const reward = scenario.rewards[Math.floor(Math.random() * scenario.rewards.length)];
  
  // 使用自定义描述（如果有）
  const habitName = habit.name;
  const customDesc = habit.customDesc ? ` - ${habit.customDesc}` : '';
  const customSuccess = habit.customSuccess || description;
  
  // 构建故事
  let story = `⚔️ 你完成了「${habitName}」${customDesc}！\n`;
  story += `🎯 面对"${monster}"，你选择了${action}\n`;
  story += `💫 ${customSuccess}\n`;
  story += `✨ +${xpGained} XP | ${reward}`;
  
  // 连击信息
  if (streak > 0) {
    const title = getStreakTitle(streak);
    story += `\n🔥 连击 ${streak} 天！称号：【${title}】`;
  }
  
  return {
    story,
    monster,
    action,
    reward,
    streakTitle: getStreakTitle(streak)
  };
}

/**
 * 生成 Boss 战描述
 */
function generateBossStory(completedHabits, totalHabits, userLevel) {
  // Boss 名称生成
  const bossNames = [
    "拖延魔王", "懒惰之王", "放弃恶魔", "借口领主", "怠惰君主",
    "明日怪", "逃避兽", "松懈幽灵", "散漫魔", "颓废领主"
  ];
  
  // 根据完成度选择 Boss
  const completionRate = completedHabits.length / totalHabits;
  let bossName;
  if (completionRate === 1) {
    bossName = bossNames[Math.floor(Math.random() * bossNames.length)];
  } else if (completionRate >= 0.7) {
    bossName = "拖延魔王";
  } else if (completionRate >= 0.5) {
    bossName = "懒惰之王";
  } else {
    bossName = "放弃恶魔";
  }
  
  // 生成参战英雄列表
  const heroList = completedHabits.map(h => {
    const xp = h.xpReward || 50;
    return `• 「${h.name}」⚔️ 造成 ${xp} 点伤害`;
  }).join('\n');
  
  // 总伤害
  const totalDamage = completedHabits.reduce((sum, h) => sum + (h.xpReward || 50), 0);
  
  // Boss 血量（根据等级调整）
  const bossHp = 100 + (userLevel * 50);
  
  // 战斗结果
  let result;
  if (completionRate === 1) {
    result = `🎉 Boss 被击败了！\n总伤害：${totalDamage}/${bossHp} 💥`;
  } else if (completionRate >= 0.7) {
    result = `⚔️ Boss 重伤逃跑了！\n总伤害：${totalDamage}/${bossHp} 💥\n还差一点就能彻底击败它！`;
  } else {
    result = `💪 Boss 还在猖狂！\n总伤害：${totalDamage}/${bossHp} 💥\n明天继续挑战！`;
  }
  
  // 奖励
  let rewards = '';
  if (completionRate === 1) {
    const bonusXp = Math.floor(totalDamage * 0.5);
    rewards = `\n\n🏆 胜利奖励：\n• 🎁 宝箱：+${bonusXp} XP\n• 🏅 成就：【今日勇者】\n• ✨ 明日士气 +10%`;
  }
  
  const story = `👹 Boss 战 - "${bossName}"！\n\n📊 今日参战英雄：\n${heroList}\n\n${result}${rewards}`;
  
  return {
    story,
    bossName,
    bossHp,
    totalDamage,
    victory: completionRate === 1,
    bonusXp: completionRate === 1 ? Math.floor(totalDamage * 0.5) : 0
  };
}

module.exports = {
  generateCheckinStory,
  generateBossStory,
  getStreakTitle,
  SCENARIOS,
  STREAK_TITLES
};
