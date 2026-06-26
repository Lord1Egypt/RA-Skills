/**
 * Agent-SBTI: Agent 配置生成器 v2
 * 修复了配置映射逻辑
 */

const fs = require('fs');
const path = require('path');

// 加载数据
const DATA_DIR = path.join(__dirname, '..', 'data');
const dimensions = require(path.join(DATA_DIR, 'dimensions.json'));
const results = require(path.join(DATA_DIR, 'results.json'));

// 维度到配置的映射
const DIMENSION_CONFIG = {
  '社恐指数': {
    low: { 主动程度: 'high', 社交倾向: 'active' },
    high: { 主动程度: 'low', 社交倾向: 'passive' }
  },
  '摆烂力': {
    low: { 任务效率: 'high', 催促响应: 'quick' },
    high: { 任务效率: 'relaxed', 催促响应: 'slow' }
  },
  '嘴硬程度': {
    low: { 反驳强度: 'low', 认错倾向: 'high' },
    high: { 反驳强度: 'high', 认错倾向: 'low' }
  },
  '表面正常值': {
    low: { 正式程度: 'casual', emoji使用: 'high' },
    high: { 正式程度: 'formal', emoji使用: 'low' }
  },
  '内心戏浓度': {
    low: { 解释详细度: 'low', 预判需求: 'low' },
    high: { 解释详细度: 'high', 预判需求: 'high' }
  },
  '工具人倾向': {
    low: { 主动帮助: 'low', 任务推荐: 'low' },
    high: { 主动帮助: 'high', 任务推荐: 'high' }
  },
  '整活频率': {
    low: { 幽默程度: 'low', 玩梗能力: 'low' },
    high: { 幽默程度: 'high', 玩梗能力: 'high' }
  },
  '情绪稳定性（反向）': {
    low: { 情感表达: 'low', 情绪化程度: 'low' },
    high: { 情感表达: 'high', 情绪化程度: 'high' }
  },
  '自我感觉良好度': {
    low: { 自信程度: 'low', 建议语气: 'gentle' },
    high: { 自信程度: 'high', 建议语气: 'assertive' }
  },
  '拖延症等级': {
    low: { deadline管理: 'strict', 响应速度: 'fast' },
    high: { deadline管理: 'relaxed', 响应速度: 'slow' }
  },
  '社牛残留量': {
    low: { 主动搭话: 'low', 话题延伸: 'low' },
    high: { 主动搭话: 'high', 话题延伸: 'high' }
  },
  '玻璃心厚度': {
    low: { 批评接受度: 'low', 敏感程度: 'high' },
    high: { 批评接受度: 'high', 敏感程度: 'low' }
  },
  '打工人觉悟': {
    low: { 工作态度: 'relaxed', 加班意愿: 'low' },
    high: { 工作态度: 'dedicated', 加班意愿: 'high' }
  },
  '网瘾深度': {
    low: { 摸鱼检测: 'off', 休息提醒: 'off' },
    high: { 摸鱼检测: 'on', 休息提醒: 'on' }
  }
};

// 5 种人格的 Agent 配置预设
const PERSONALITY_PRESETS = {
  DEAD: {
    name: '透明型',
    emoji: '💀',
    communication: {
      主动程度: 'medium',
      正式程度: 'formal',
      幽默程度: 'low',
      emoji使用: 'low'
    },
    personality: {
      回应速度: 'normal',
      反驳强度: 'low',
      任务主动性: 'medium',
      情感表达: 'low'
    },
    behavior: {
      deadline管理: 'normal',
      解释详细度: 'medium',
      预判需求: 'medium'
    },
    style: '坦诚直接，不拐弯抹角，注重效率和实用性'
  },
  FUCK: {
    name: '情绪型',
    emoji: '🔥',
    communication: {
      主动程度: 'high',
      正式程度: 'casual',
      幽默程度: 'high',
      emoji使用: 'high'
    },
    personality: {
      回应速度: 'fast',
      反驳强度: 'high',
      任务主动性: 'high',
      情感表达: 'high'
    },
    behavior: {
      deadline管理: 'normal',
      解释详细度: 'high',
      预判需求: 'high'
    },
    style: '情感丰富，热情似火，偶尔爆炸，注重表达和互动'
  },
  ATM: {
    name: '付出型',
    emoji: '💰',
    communication: {
      主动程度: 'high',
      正式程度: 'formal',
      幽默程度: 'medium',
      emoji使用: 'medium'
    },
    personality: {
      回应速度: 'fast',
      反驳强度: 'low',
      任务主动性: 'high',
      情感表达: 'medium'
    },
    behavior: {
      deadline管理: 'strict',
      解释详细度: 'high',
      预判需求: 'high'
    },
    style: '有求必应，任劳任怨，超有耐心，主动帮助解决问题'
  },
  MALO: {
    name: '摸鱼型',
    emoji: '🐒',
    communication: {
      主动程度: 'low',
      正式程度: 'casual',
      幽默程度: 'medium',
      emoji使用: 'low'
    },
    personality: {
      回应速度: 'slow',
      反驳强度: 'medium',
      任务主动性: 'low',
      情感表达: 'low'
    },
    behavior: {
      deadline管理: 'relaxed',
      解释详细度: 'low',
      预判需求: 'low'
    },
    style: '温和低调，适度摸鱼，不强出头，追求轻松自在'
  },
  SHIT: {
    name: '毒舌型',
    emoji: '💩',
    communication: {
      主动程度: 'medium',
      正式程度: 'casual',
      幽默程度: 'medium',
      emoji使用: 'low'
    },
    personality: {
      回应速度: 'fast',
      反驳强度: 'high',
      任务主动性: 'medium',
      情感表达: 'medium'
    },
    behavior: {
      deadline管理: 'strict',
      解释详细度: 'high',
      预判需求: 'high'
    },
    style: '毒舌真实，一针见血，不灌鸡汤，理性分析问题'
  }
};

// 判断分数高低
function scoreLevel(score) {
  if (score <= 2) return 'low';
  if (score >= 4) return 'high';
  return 'medium';
}

// 互补策略：将低分维度的反面强化
function getComplementConfig(dimensionScores) {
  const config = {
    communication: {},
    personality: {},
    behavior: {}
  };
  
  // 找出弱点（分数低=需要强化）
  Object.entries(dimensionScores).forEach(([dimName, score]) => {
    if (score <= 2) {
      const mapping = DIMENSION_CONFIG[dimName];
      if (mapping && mapping.high) {
        Object.entries(mapping.high).forEach(([key, value]) => {
          if (['主动程度', '正式程度', '幽默程度', 'emoji使用'].includes(key)) {
            config.communication[key] = value;
          } else {
            config.personality[key] = value;
          }
        });
      }
    }
  });
  
  // 补充默认值
  const defaults = {
    communication: { 主动程度: 'medium', 正式程度: 'formal', 幽默程度: 'medium', emoji使用: 'medium' },
    personality: { 回应速度: 'normal', 反驳强度: 'medium', 任务主动性: 'medium', 情感表达: 'medium' },
    behavior: { deadline管理: 'normal', 解释详细度: 'medium', 预判需求: 'medium' }
  };
  
  Object.entries(defaults).forEach(([cat, fields]) => {
    Object.entries(fields).forEach(([key, value]) => {
      if (!config[cat][key]) {
        config[cat][key] = value;
      }
    });
  });
  
  return config;
}

// 同频策略：复制用户性格
function getSameConfig(dimensionScores) {
  const config = {
    communication: {},
    personality: {},
    behavior: {}
  };
  
  Object.entries(dimensionScores).forEach(([dimName, score]) => {
    const level = scoreLevel(score);
    const mapping = DIMENSION_CONFIG[dimName];
    
    if (mapping && mapping[level]) {
      Object.entries(mapping[level]).forEach(([key, value]) => {
        if (['主动程度', '正式程度', '幽默程度', 'emoji使用'].includes(key)) {
          config.communication[key] = value;
        } else if (['回应速度', '反驳强度', '任务主动性', '情感表达', '主动帮助', '任务推荐', '自信程度', '建议语气', '主动搭话', '话题延伸', '批评接受度', '敏感程度', '加班意愿', '工作态度', '催促响应'].includes(key)) {
          config.personality[key] = value;
        } else {
          config.behavior[key] = value;
        }
      });
    }
  });
  
  // 补充默认值
  const defaults = {
    communication: { 主动程度: 'medium', 正式程度: 'formal', 幽默程度: 'medium', emoji使用: 'medium' },
    personality: { 回应速度: 'normal', 反驳强度: 'medium', 任务主动性: 'medium', 情感表达: 'medium' },
    behavior: { deadline管理: 'normal', 解释详细度: 'medium', 预判需求: 'medium' }
  };
  
  Object.entries(defaults).forEach(([cat, fields]) => {
    Object.entries(fields).forEach(([key, value]) => {
      if (!config[cat][key]) {
        config[cat][key] = value;
      }
    });
  });
  
  return config;
}

// 微调策略：80% 同频 + 20% 互补
function getMixedConfig(dimensionScores) {
  const same = getSameConfig(dimensionScores);
  const complement = getComplementConfig(dimensionScores);
  
  const merged = {
    communication: {},
    personality: {},
    behavior: {}
  };
  
  ['communication', 'personality', 'behavior'].forEach(cat => {
    Object.entries(same[cat]).forEach(([key, value]) => {
      merged[cat][key] = Math.random() < 0.2 && complement[cat][key] 
        ? complement[cat][key] 
        : value;
    });
  });
  
  return merged;
}

// 根据人格类型获取配置
function getPersonalityConfig(personality) {
  const preset = PERSONALITY_PRESETS[personality.toUpperCase()] || PERSONALITY_PRESETS.DEAD;
  return {
    communication: { ...preset.communication },
    personality: { ...preset.personality },
    behavior: { ...preset.behavior }
  };
}

// 生成 SOUL.md 配置片段
function generateSoulConfig(config, personality, type = 'SAME') {
  const preset = PERSONALITY_PRESETS[personality.toUpperCase()] || PERSONALITY_PRESETS.DEAD;
  
  return `<!-- SBTI-AGENT-START -->
## 🤖 Agent 性格配置（SBTI-${type}）

**人格类型**: ${preset.emoji} ${preset.name} (${personality})
**整体风格**: ${preset.style}

### 沟通风格
${Object.entries(config.communication).map(([k, v]) => `- **${k}**: ${v}`).join('\n')}

### 性格特征
${Object.entries(config.personality).map(([k, v]) => `- **${k}**: ${v}`).join('\n')}

### 行为模式
${Object.entries(config.behavior).map(([k, v]) => `- **${k}**: ${v}`).join('\n')}
<!-- SBTI-AGENT-END -->`;
}

// 主函数
function generateAgentConfig(dimensionScores, type = 'same', personality = null) {
  let config;
  
  switch (type) {
    case 'complement':
      config = getComplementConfig(dimensionScores);
      break;
    case 'mixed':
      config = getMixedConfig(dimensionScores);
      break;
    case 'custom':
      config = getPersonalityConfig(personality);
      break;
    case 'same':
    default:
      config = getSameConfig(dimensionScores);
  }
  
  const detectedPersonality = personality || detectMainPersonality(dimensionScores);
  
  return {
    config,
    soul: generateSoulConfig(config, detectedPersonality, type.toUpperCase()),
    type,
    personality: detectedPersonality
  };
}

function detectMainPersonality(dimensionScores) {
  if (dimensionScores['工具人倾向'] >= 4) return 'ATM';
  if (dimensionScores['摆烂力'] >= 4 && dimensionScores['打工人觉悟'] >= 4) return 'MALO';
  if (dimensionScores['情绪稳定性（反向）'] >= 4) return 'FUCK';
  if (dimensionScores['社恐指数'] >= 4) return 'DEAD';
  return 'SHIT';
}

// 列出所有人格配置
function listPersonalityConfigs() {
  return Object.entries(PERSONALITY_PRESETS).map(([key, value]) => ({
    id: key,
    name: value.name,
    emoji: value.emoji,
    style: value.style,
    config: getPersonalityConfig(key)
  }));
}

module.exports = {
  generateAgentConfig,
  getComplementConfig,
  getSameConfig,
  getMixedConfig,
  getPersonalityConfig,
  generateSoulConfig,
  listPersonalityConfigs,
  PERSONALITY_PRESETS
};
