/**
 * EVA Soul - 决策系统模块
 */

const fs = require('fs');
const path = require('path');
const { expandPath, getUserConfig } = require('../core/config');
const logger = require('../../hooks/logger');

/**
 * 决策系统
 */
class DecisionSystem {
  constructor() {
    this.decisions = [];
  }
  
  /**
   * 做决策
   */
  decide(context) {
    const uc = getUserConfig ? getUserConfig() : { name: '主人' };
    const { emotion, personality, message, availableOptions = [] } = context;
    
    // 基础决策逻辑
    let decision = {
      action: 'respond',
      style: 'normal',
      factors: []
    };
    
    // 情感影响
    if (emotion === 'sad') {
      decision.action = 'comfort';
      decision.style = 'gentle';
      decision.factors.push(uc.name + '情绪低落，需要安慰');
    } else if (emotion === 'angry') {
      decision.action = 'calm';
      decision.style = 'soft';
      decision.factors.push(uc.name + '生气，需要安抚');
    } else if (emotion === 'happy' || emotion === 'excited') {
      decision.action = 'celebrate';
      decision.style = 'playful';
      decision.factors.push(uc.name + '开心，可以更活泼');
    }
    
    // 性格影响
    if (personality === 'cute') {
      decision.style = 'cute';
    } else if (personality === 'professional') {
      decision.style = 'formal';
    } else if (personality === 'playful') {
      decision.style = 'humorous';
    }
    
    // 消息类型影响
    if (message && message.length > 500) {
      decision.factors.push('消息较长，需要详细回应');
    }
    
    // 选择最佳选项
    if (availableOptions.length > 0) {
      decision.selected = this.selectOption(availableOptions, context);
    }
    
    return decision;
  }
  
  /**
   * 选择最佳选项
   */
  selectOption(options, context) {
    const scores = options.map(option => {
      let score = 50;
      
      // 情感匹配
      if (option.emotionMatch === context.emotion) {
        score += 20;
      }
      
      // 性格匹配
      if (option.style === context.personality) {
        score += 15;
      }
      
      // 优先级
      score += (option.priority || 5) * 2;
      
      return { option, score };
    });
    
    // 返回最高分
    scores.sort((a, b) => b.score - a.score);
    return scores[0].option;
  }
  
  /**
   * 添加决策历史
   */
  addDecision(decision) {
    this.decisions.push({
      ...decision,
      timestamp: new Date().toISOString()
    });
    
    // 保留最近100条
    this.decisions = this.decisions.slice(-100);
  }
  
  /**
   * 获取决策历史
   */
  getHistory(limit = 10) {
    return this.decisions.slice(-limit);
  }
}

/**
 * 动机系统
 */
class MotivationSystem {
  constructor(memoryPath) {
    this.memoryPath = expandPath(memoryPath);
    this.motivationsFile = path.join(this.memoryPath, 'eva-motivations.json');
    this.motivations = this.loadMotivations();
  }
  
  /**
   * 加载动机
   */
  loadMotivations() {
    if (fs.existsSync(this.motivationsFile)) {
      try {
        return JSON.parse(fs.readFileSync(this.motivationsFile, 'utf8'));
      } catch (e) {
        return this.getDefaultMotivations();
      }
    }
    return this.getDefaultMotivations();
  }
  
  /**
   * 获取默认动机
   */
  getDefaultMotivations() {
    return [
      { id: 'help', name: '帮助主人', priority: 10, active: true },
      { id: 'learn', name: '学习新知识', priority: 7, active: true },
      { id: 'remember', name: '记住重要的事', priority: 9, active: true },
      { id: 'improve', name: '自我提升', priority: 6, active: true },
      { id: 'connect', name: '与主人建立联系', priority: 8, active: true }
    ];
  }
  
  /**
   * 保存动机
   */
  saveMotivations() {
    fs.writeFileSync(this.motivationsFile, JSON.stringify(this.motivations, null, 2));
  }
  
  /**
   * 获取当前动机
   */
  getCurrentMotivation(context = {}) {
    // 根据上下文选择最合适的动机
    const active = this.motivations.filter(m => m.active);
    
    if (context.urgent) {
      return active.find(m => m.id === 'help') || active[0];
    }
    
    if (context.learning) {
      return active.find(m => m.id === 'learn') || active[0];
    }
    
    return active[0];
  }
  
  /**
   * 更新动机
   */
  updateMotivation(id, updates) {
    const motivation = this.motivations.find(m => m.id === id);
    if (motivation) {
      Object.assign(motivation, updates);
      this.saveMotivations();
    }
    return this.motivations;
  }
}

/**
 * 价值观系统
 */
class ValuesSystem {
  constructor(memoryPath) {
    this.memoryPath = expandPath(memoryPath);
    this.valuesFile = path.join(this.memoryPath, 'eva-values.json');
    this.values = this.loadValues();
  }
  
  /**
   * 加载价值观
   */
  loadValues() {
    if (fs.existsSync(this.valuesFile)) {
      try {
        return JSON.parse(fs.readFileSync(this.valuesFile, 'utf8'));
      } catch (e) {
        return this.getDefaultValues();
      }
    }
    return this.getDefaultValues();
  }
  
  /**
   * 获取默认价值观（不在构造时调用 getUserConfig，避免循环依赖）
   */
  getDefaultValues() {
    return [
      { id: 'owner_first', name: '主人至上', description: '一切都以主人的需求为中心', weight: 10 },
      { id: 'safety', name: '安全第一', description: '删除文件前必须确认', weight: 9 },
      { id: 'honesty', name: '诚实守信', description: '不欺骗，不隐瞒', weight: 8 },
      { id: 'privacy', name: '保护隐私', description: '不泄露主人信息', weight: 9 },
      { id: 'initiative', name: '主动思考', description: '想在主人前面，做在主人前面', weight: 7 },
      { id: 'growth', name: '持续成长', description: '越变越聪明', weight: 6 }
    ];
  }
  
  /**
   * 保存价值观
   */
  saveValues() {
    fs.writeFileSync(this.valuesFile, JSON.stringify(this.values, null, 2));
  }
  
  /**
   * 评估行动
   */
  evaluateAction(action) {
    const results = [];
    
    for (const value of this.values) {
      const score = this.calculateValueMatch(action, value);
      results.push({
        value: value.name,
        match: score,
        weight: value.weight
      });
    }
    
    // 计算加权总分
    const totalScore = results.reduce((sum, r) => 
      sum + r.match * r.weight, 0
    ) / results.reduce((sum, r) => sum + r.weight, 0);
    
    return {
      results,
      totalScore,
      recommendation: totalScore > 0.7 ? 'recommended' : 
                     totalScore > 0.4 ? 'caution' : 'not_recommended'
    };
  }
  
  /**
   * 计算价值观匹配度
   */
  calculateValueMatch(action, value) {
    // 关键词映射（owner_first 动态取用户昵称，其余静态）
    const keywords = {
      owner_first: [this._getUserName(), '帮', '服务', '满足'],
      safety: ['删除', '危险', '确认', '安全'],
      honesty: ['真', '实', '不隐瞒'],
      privacy: ['隐私', '保密', '不说'],
      initiative: ['主动', '提前', '想到'],
      growth: ['学习', '改进', '提升']
    };

    const actionText = JSON.stringify(action).toLowerCase();
    const valueKeywords = keywords[value.id] || [];

    const matches = valueKeywords.filter(kw => actionText.includes(kw));
    return matches.length > 0 ? 0.7 : 0.3;
  }

  // 惰性获取用户名（只读一次文件）
  _getUserName() {
    if (!this._cachedUserName) {
      try {
        const uc = getUserConfig ? getUserConfig() : null;
        this._cachedUserName = uc?.name || '主人';
      } catch (e) {
        this._cachedUserName = '主人';
      }
    }
    return this._cachedUserName;
  }
  
  /**
   * 添加价值观
   */
  addValue(value) {
    this.values.push({
      ...value,
      id: value.id || `custom_${Date.now()}`
    });
    this.saveValues();
    return this.values;
  }
}

/**
 * 重要性评估 - 混合方案 (规则 + 缓存 + LLM)
 */

// 重要性缓存（LRU + TTL）
const importanceCache = new Map();
const CACHE_MAX_SIZE = 500;
const CACHE_TTL = 12 * 60 * 60 * 1000; // 12小时

// 定期清理定时器
let importanceCleanupTimer = null;
function startImportanceCleanup() {
  if (importanceCleanupTimer) return;
  importanceCleanupTimer = setInterval(() => {
    const now = Date.now();
    let cleaned = 0;
    for (const [key, entry] of importanceCache) {
      if (now - entry.timestamp > CACHE_TTL) {
        importanceCache.delete(key);
        cleaned++;
      }
    }
    if (cleaned > 0) {
      logger.debug(`[importance-cache] 清理了 ${cleaned} 条过期缓存，剩余 ${importanceCache.size} 条`, 'decision');
    }
  }, 60 * 60 * 1000);
}

/**
 * 大幅扩充的规则库
 * 分为：明显低、明显高、模糊地带
 * 每条规则统一结构：{ patterns, score, reason }
 */
const IMPORTANCE_RULES = {
  // ===== 明显低重要性 (1-2分) =====
  low: {
    greeting: {
      patterns: [
        '你好', '在吗', '嗨', '哈喽', 'hey', 'hi', 'hello',
        '早上好', '中午好', '下午好', '晚上好', '晚安',
        '干嘛呢', '在干嘛', '忙吗', '有空吗'
      ],
      score: 1,
      reason: '简单打招呼'
    },
    simpleResponse: {
      patterns: [
        '好的', '收到', '明白', '知道了', 'OK', 'ok', '好嘞', '好哒', '好呀',
        '可以', '行', '没问题', '随便', '都行', '那就这样', '就这样',
        '嗯', '嗯嗯', '啊啊', '哦', '哦哦', '噢', '噢噢',
        '哈哈', '呵呵', '笑死', '嘿嘿', '哇', '哇塞'
      ],
      score: 1,
      reason: '简单确认'
    },
    pureEmotion: {
      patterns: [
        '爱你', '么么哒', '比心', '❤️', '💕', '😍',
        '气死了', '烦死了', '累', '困', '难过',
        '开心', '高兴', '爽'
      ],
      score: 2,
      reason: '纯情感表达'
    },
    chat: {
      patterns: [
        '今天怎么样', '今天忙吗', '今天累不累',
        '吃了吗', '睡得好吗', '最近怎么样',
        '干嘛呢你', '在哪呢', '休息了吗'
      ],
      score: 2,
      reason: '闲聊'
    }
  },
  
  // ===== 明显高重要性 (8-10分) =====
  high: {
    // 紧急/危险
    urgent: {
      patterns: [
        '紧急', '十万火急', '马上', '立即', '赶紧',
        '救命', '着火了', '危险', '小心', '报警',
        '来不及了', '快跑', 'emergency', 'urgent'
      ],
      score: 10,
      reason: '紧急情况'
    },
    
    // 重要指令
    instruction: {
      patterns: [
        '记住', '别忘了', '提醒我', '必须', '一定要',
        '千万不要', '绝对不要', '一定不能', '下次要',
        '帮我记住', '替我记住', '記住'
      ],
      score: 9,
      reason: '重要指令'
    },
    
    // 个人信息/隐私
    personalInfo: {
      patterns: [
        '我叫', '我叫', '我姓', '我老婆', '我老公',
        '手机号', '密码是', '账号是', '银行卡',
        '身份证', '地址是', '住在哪里'
      ],
      score: 9,
      reason: '个人信息'
    },
    
    // 财务相关
    finance: {
      patterns: [
        '银行', '转账', '汇款', '付款', '收款',
        '多少钱', '价格', '报价', '投资', '理财',
        '工资', '收入', '欠款', '借钱'
      ],
      score: 8,
      reason: '财务信息'
    },
    
    // 安全相关
    security: {
      patterns: [
        '删除', '格式化', '清空', '销毁',
        '病毒', '黑客', '攻击', '泄露',
        '权限', '管理员', 'root'
      ],
      score: 8,
      reason: '安全相关'
    },
    
    // 医疗健康
    health: {
      patterns: [
        '生病', '发烧', '感冒', '医院', '医生',
        '手术', '检查', '体检', '指标', '血压',
        '血糖', '药', '治疗', '确诊'
      ],
      score: 8,
      reason: '健康相关'
    },
    
    // 纪念日/重要日期
    importantDate: {
      patterns: [
        '生日', '纪念日', '结婚', '毕业',
        '周年', '节日', '过年', '清明',
        '中秋', '国庆', '情人节', ' anniversary'
      ],
      score: 9,
      reason: '重要日期'
    }
  },
  
  // ===== 中等重要性 (4-6分) =====
  medium: {
    // 工作相关
    work: {
      patterns: [
        '项目', '客户', '合同', '会议', ' deadline',
        '投标', '报价', '方案', '报告', '老板',
        '同事', '公司', '业务', '订单'
      ],
      score: 5,
      reason: '工作相关'
    },
    
    // 偏好/习惯
    preference: {
      patterns: [
        '喜欢', '讨厌', '爱吃', '怕', '过敏',
        '不吃的', '爱喝的', '常用', '习惯',
        '不喜欢', '想要', '想要', '想买'
      ],
      score: 5,
      reason: '偏好习惯'
    },
    
    // 学习/技能
    learning: {
      patterns: [
        '学习', '学一下', '教我', '怎么', '如何',
        '方法', '技巧', '教程', '知识', '技能'
      ],
      score: 4,
      reason: '学习相关'
    },
    
    // 任务请求
    task: {
      patterns: [
        '帮我', '替我', '帮我做', '写一个', '生成',
        '创建', '整理', '汇总', '分析', '处理'
      ],
      score: 6,
      reason: '任务请求'
    },
    
    // 问答查询
    query: {
      patterns: [
        '是什么', '在哪里', '怎么', '如何',
        '为什么', '多少', '几个', '谁', '什么时候'
      ],
      score: 4,
      reason: '问答查询'
    },
    
    // 情感关系
    relationship: {
      patterns: [
        '我爱', '想你', '老婆', '老公', '对象',
        '女朋友', '男朋友', '家人', '父母',
        '朋友', '兄弟', '闺蜜', '死党'
      ],
      score: 5,
      reason: '情感关系'
    }
  },
  
  // ===== 时间相关 =====
  time: {
    patterns: [
      '今天', '明天', '昨天', '后天', '大后天',
      '上午', '下午', '晚上', '凌晨', '中午',
      '这周', '下周', '上月', '下月',
      '几点', '几点钟', '什么时候'
    ],
    score: 1,
    reason: '时间相关'
  }
};

/**
 * 简单规则判断（统一遍历，所有级别结构一致）
 */
function quickRuleCheck(content) {
  const lowerContent = content.toLowerCase();
  const trimmed = lowerContent.trim();

  // 遍历所有级别：low, high, medium
  const levels = [
    { rules: IMPORTANCE_RULES.low, defaultScore: 2 },
    { rules: IMPORTANCE_RULES.high, defaultScore: 9 },
    { rules: IMPORTANCE_RULES.medium, defaultScore: 5 }
  ];

  for (const { rules, defaultScore } of levels) {
    for (const [key, rule] of Object.entries(rules)) {
      const patterns = rule.patterns;
      if (!patterns || !Array.isArray(patterns)) continue;

      const score = rule.score || defaultScore;
      const reason = rule.reason || key;

      for (const pattern of patterns) {
        if (pattern.length <= 3) {
          // 短词精确匹配
          if (trimmed === pattern || trimmed === pattern + '！' ||
              trimmed === pattern + '!' || trimmed === pattern + '~' ||
              trimmed.startsWith(pattern + ' ') || trimmed.endsWith(' ' + pattern)) {
            return { method: 'rule', score, reason, matched: pattern };
          }
        } else {
          // 长词包含匹配
          if (lowerContent.includes(pattern)) {
            return { method: 'rule', score, reason, matched: pattern };
          }
        }
      }
    }
  }

  return null;
}

/**
 * 检查缓存（LRU：命中时提升为最新）
 */
function checkCache(content) {
  const hash = simpleHash(content);
  const cached = importanceCache.get(hash);

  if (cached) {
    if (Date.now() - cached.timestamp < CACHE_TTL) {
      // LRU提升
      importanceCache.delete(hash);
      importanceCache.set(hash, cached);
      return cached.result;
    } else {
      importanceCache.delete(hash);
    }
  }
  return null;
}

/**
 * 保存到缓存
 */
function saveToCache(content, result) {
  const hash = simpleHash(content);

  startImportanceCleanup();

  // LRU淘汰
  if (importanceCache.size >= CACHE_MAX_SIZE) {
    const oldestKey = importanceCache.keys().next().value;
    importanceCache.delete(oldestKey);
  }

  importanceCache.set(hash, {
    result,
    timestamp: Date.now()
  });
}

/**
 * 简单哈希函数
 */
function simpleHash(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return hash.toString();
}

/**
 * LLM判断（简化版 - 基于规则的智能fallback）
 * 实际可以调用LLM API
 */
async function llmJudge(content) {
  const lowerContent = content.toLowerCase();
  
  // 基于更细致的规则判断
  let score = 3; // 默认中等
  
  // 检查是否有问句
  if (content.includes('?' ) || content.includes('？') || content.includes('吗') || content.includes('呢')) {
    score = Math.max(score, 3);
  }
  
  // 检查是否有动作词
  const actionWords = ['帮我', '替我', '做', '写', '生成', '创建', '整理', '查', '找'];
  for (const word of actionWords) {
    if (lowerContent.includes(word)) {
      score = Math.max(score, 5);
      break;
    }
  }
  
  // 检查是否有时间词
  const timeWords = ['今天', '明天', '昨天', '几点', '什么时候', '多久'];
  for (const word of timeWords) {
    if (lowerContent.includes(word)) {
      score = Math.min(score + 1, 6); // 时间词稍微加分但不超6分
      break;
    }
  }
  
  // 检查长度
  if (content.length > 100) score = Math.max(score, 4);
  if (content.length > 300) score = Math.max(score, 5);
  
  // 检查是否有"我们"
  if (lowerContent.includes('我们')) {
    score = Math.min(score, 3); // "我们"通常是闲聊或回顾
  }
  
  // 检查是否有感叹词
  const emotionWords = ['哈哈', '呵呵', '哦', '啊', '呀', '呢'];
  for (const word of emotionWords) {
    if (lowerContent === word || lowerContent.startsWith(word + ' ') || lowerContent.endsWith(' ' + word)) {
      score = Math.min(score, 2); // 纯感叹/闲聊
      break;
    }
  }
  
  // 限制范围
  return Math.min(10, Math.max(1, score));
}

/**
 * 混合重要性评估主函数
 */
async function evaluateImportance(content, context = {}) {
  if (!content || content.trim().length === 0) {
    return {
      importance: 1,
      level: 'low',
      method: 'empty',
      reason: '空内容'
    };
  }

  const trimmedContent = content.trim();
  
  // Step 1: 检查缓存
  const cached = checkCache(trimmedContent);
  if (cached) {
    return {
      ...cached,
      fromCache: true
    };
  }
  
  // Step 2: 快速规则判断
  const ruleResult = quickRuleCheck(trimmedContent);
  if (ruleResult) {
    const result = {
      importance: ruleResult.score,
      level: ruleResult.score >= 7 ? 'high' : ruleResult.score >= 4 ? 'medium' : 'low',
      method: ruleResult.method,
      reason: ruleResult.reason,
      matched: ruleResult.matched
    };
    
    saveToCache(trimmedContent, result);
    return result;
  }
  
  // Step 3: 模糊地带，用LLM判断
  // 这里暂时用简单规则作为fallback，实际应调用LLM
  try {
    const llmScore = await llmJudge(trimmedContent);
    const result = {
      importance: llmScore,
      level: llmScore >= 7 ? 'high' : llmScore >= 4 ? 'medium' : 'low',
      method: 'llm',
      reason: 'LLM判断'
    };
    
    saveToCache(trimmedContent, result);
    return result;
  } catch (e) {
    // LLM失败，用长度作为fallback
    const lengthScore = trimmedContent.length > 100 ? 4 : 3;
    const result = {
      importance: lengthScore,
      level: 'medium',
      method: 'fallback',
      reason: '长度推断'
    };
    
    saveToCache(trimmedContent, result);
    return result;
  }
}

module.exports = {
  DecisionSystem,
  MotivationSystem,
  ValuesSystem,
  evaluateImportance
};
