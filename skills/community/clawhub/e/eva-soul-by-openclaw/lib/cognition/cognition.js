/**
 * EVA Soul - 认知系统模块 (完整版)
 * 包含：概念抽象、模式识别、知识图谱
 *
 * SECURITY MANIFEST:
 *   Environment variables accessed: SILICONFLOW_API_KEY (向量搜索API)
 *   External endpoints called: api.siliconflow.cn (向量嵌入服务)
 *   Local files read: memory/eva-concepts.json, memory/eva-patterns.json, memory/eva-knowledge-graph.json
 *   Local files written: memory/eva-concepts.json, memory/eva-patterns.json, memory/eva-knowledge-graph.json
 */

const fs = require('fs');
const path = require('path');
const { expandPath } = require('../core/config');
const { fetchWithRetry } = require('../../hooks/errorHandler');
const logger = require('../../hooks/logger');

/**
 * 概念系统 - 完整版
 */
class ConceptSystem {
  constructor(memoryPath) {
    this.memoryPath = expandPath(memoryPath);
    this.conceptsFile = path.join(this.memoryPath, 'eva-concepts.json');
    this.concepts = this.loadConcepts();
    this.stats = { totalExtracted: 0, lastUpdate: null };
  }
  
  /**
   * 加载概念
   */
  loadConcepts() {
    if (fs.existsSync(this.conceptsFile)) {
      try {
        const data = JSON.parse(fs.readFileSync(this.conceptsFile, 'utf8'));
        return data.concepts || [];
      } catch (e) {
        return [];
      }
    }
    return [];
  }
  
  /**
   * 保存概念
   */
  saveConcepts() {
    const data = {
      concepts: this.concepts,
      stats: this.stats,
      lastSave: new Date().toISOString()
    };
    fs.writeFileSync(this.conceptsFile, JSON.stringify(data, null, 2));
  }
  
  /**
   * 提取概念 - 完整版
   */
  extractConcepts(text) {
    if (!text) return [];
    
    const concepts = [];
    
    // 1. 实体识别
    const entities = this.extractEntities(text);
    concepts.push(...entities);
    
    // 2. 主题识别
    const topics = this.extractTopics(text);
    concepts.push(...topics);
    
    // 3. 关键词提取
    const keywords = this.extractKeywords(text);
    concepts.push(...keywords);
    
    // 4. 情感词提取
    const emotions = this.extractEmotionWords(text);
    concepts.push(...emotions);
    
    // 5. 意图识别
    const intents = this.extractIntents(text);
    concepts.push(...intents);
    
    // 更新统计
    this.stats.totalExtracted += concepts.length;
    this.stats.lastUpdate = new Date().toISOString();
    
    return concepts;
  }
  
  /**
   * 提取实体 - 完整版
   */
  extractEntities(text) {
    const entities = [];
    const patterns = {
      // 人名
      person: [
        /(?:我叫|我是|名字叫|姓|名叫)([^\s，。,.]+)/g,
        /([A-Z][a-z]+ [A-Z][a-z]+)/g
      ],
      // 地名
      location: [
        /(?:在|住在|来自|去|到)([^\s，。,.]+(?:市|省|区|县|国))/g,
        /([^\s，。,.]+(?:市|省|区|县))/g
      ],
      // 组织/公司
      organization: [
        /(?:在|属于|加入|创立)([^\s，。,.]+(?:公司|企业|机构|组织))/g
      ],
      // 时间
      time: [
        /(\d{4}[年\-]\d{1,2}[月\-]\d{1,2}[日]?)/g,
        /(今天|明天|昨天|上周|下周|去年|明年)/g
      ],
      // 数字
      number: [
        /(\d+(?:个|次|件|条|元|万|亿))/g
      ],
      // 联系方式
      contact: [
        /(1[3-9]\d{9})/g,
        /([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/g
      ]
    };
    
    for (const [type, regexps] of Object.entries(patterns)) {
      for (const regex of regexps) {
        let match;
        while ((match = regex.exec(text)) !== null) {
          if (match[1] && match[1].length > 1) {
            entities.push({
              type,
              value: match[1].trim(),
              importance: type === 'person' ? 9 : type === 'contact' ? 8 : 5,
              source: 'regex'
            });
          }
        }
      }
    }
    
    return entities;
  }
  
  /**
   * 提取主题
   */
  extractTopics(text) {
    const topics = [];
    const topicMap = {
      work: {
        keywords: ['工作', '项目', '事业', '创业', '公司', '业务', '客户', '合同', '会议', 'deadline', '任务'],
        importance: 7
      },
      life: {
        keywords: ['生活', '家庭', '租房', '买房', '装修', '吃饭', '睡觉', '休息'],
        importance: 6
      },
      health: {
        keywords: ['健康', '运动', '健身', '看病', '体检', '感冒', '发烧', '身体'],
        importance: 8
      },
      hobby: {
        keywords: ['爱好', '喜欢', '游戏', '音乐', '电影', '读书', '旅游', '运动'],
        importance: 5
      },
      relationship: {
        keywords: ['朋友', '家人', '女朋友', '男朋友', '结婚', '老婆', '老公', '孩子'],
        importance: 8
      },
      finance: {
        keywords: ['钱', '投资', '理财', '股票', '基金', '存款', '工资', '收入'],
        importance: 7
      },
      tech: {
        keywords: ['代码', '编程', 'AI', '电脑', '软件', '网站', '开发', '技术'],
        importance: 6
      },
      emotion: {
        keywords: ['开心', '难过', '生气', '焦虑', '压力', '放松', '烦'],
        importance: 7
      }
    };
    
    for (const [topic, config] of Object.entries(topicMap)) {
      for (const kw of config.keywords) {
        if (text.includes(kw)) {
          topics.push({
            type: 'topic',
            value: topic,
            importance: config.importance,
            source: 'keyword',
            matched: kw
          });
          break;
        }
      }
    }
    
    return topics;
  }
  
  /**
   * 提取关键词 - 完整版
   */
  extractKeywords(text) {
    const keywords = [];
    
    // 停用词
    const stopWords = new Set(['的', '是', '在', '有', '和', '了', '就', '都', '而', '及', '与', '或', '一个', '一些', '这个', '那个', '什么', '怎么', '如何', '为什么']);
    
    // 简单分词
    const words = text.split(/[\s，。,、；：""''（）()!?！？]+/).filter(w => w.length >= 2);
    const wordCounts = {};
    
    for (const word of words) {
      if (stopWords.has(word)) continue;
      wordCounts[word] = (wordCounts[word] || 0) + 1;
    }
    
    // 排序取高频词
    const sorted = Object.entries(wordCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 20);
    
    for (const [word, count] of sorted) {
      keywords.push({
        type: 'keyword',
        value: word,
        count,
        importance: Math.min(10, 3 + count),
        source: 'frequency'
      });
    }
    
    return keywords;
  }
  
  /**
   * 提取情感词
   */
  extractEmotionWords(text) {
    const emotionWords = [];
    const emotions = {
      positive: ['开心', '高兴', '快乐', '棒', '好', '喜欢', '爱', '幸福', '满足', '舒服', '温暖'],
      negative: ['难过', '伤心', '哭', '生气', '愤怒', '烦', '累', '困', '怕', '担心', '焦虑'],
      neutral: ['但是', '然而', '虽然', '如果', '因为', '所以']
    };
    
    for (const [category, words] of Object.entries(emotions)) {
      for (const word of words) {
        if (text.includes(word)) {
          emotionWords.push({
            type: 'emotion_word',
            value: word,
            category,
            importance: 4,
            source: 'dictionary'
          });
        }
      }
    }
    
    return emotionWords;
  }
  
  /**
   * 提取意图
   */
  extractIntents(text) {
    const intents = [];
    const patterns = [
      { intent: 'greeting', keywords: ['你好', 'hello', 'hi', '早上好', '晚上好', '嗨'], importance: 3 },
      { intent: 'question', keywords: ['吗', '呢', '怎么', '什么', '为什么', '?', '？'], importance: 5 },
      { intent: 'request', keywords: ['帮我', '请', '能不能', '可以帮我', '想要', '需要'], importance: 7 },
      { intent: 'command', keywords: ['去', '做', '执行', '开始', '停止'], importance: 6 },
      { intent: 'thanks', keywords: ['谢谢', '感谢', '感恩', '多亏'], importance: 4 },
      { intent: 'apology', keywords: ['对不起', '抱歉', '不好意思'], importance: 4 }
    ];
    
    for (const pattern of patterns) {
      for (const kw of pattern.keywords) {
        if (text.includes(kw)) {
          intents.push({
            type: 'intent',
            value: pattern.intent,
            importance: pattern.importance,
            source: 'pattern'
          });
          break;
        }
      }
    }
    
    return intents;
  }
  
  /**
   * 添加概念
   */
  addConcept(concept) {
    const existing = this.concepts.find(c =>
      c.type === concept.type && c.value === concept.value
    );

    if (existing) {
      existing.count = (existing.count || 0) + 1;
      existing.lastSeen = new Date().toISOString();
      existing.importance = Math.max(existing.importance || 0, concept.importance || 5);
      if (concept.matched) existing.matched = concept.matched;
    } else {
      this.concepts.push({
        ...concept,
        createdAt: new Date().toISOString(),
        lastSeen: new Date().toISOString(),
        count: 1,
        // 反馈相关字段（初始化）
        feedbackScore: 0,
        feedbackCount: 0,
        flagged: false,
        feedbackHistory: []
      });
    }

    this.saveConcepts();
    return this.concepts;
  }

  /**
   * 记录对概念的反馈（核心方法）
   * @param {string} conceptId - 概念 ID 或 value（兼容两种方式）
   * @param {string} type - positive | negative | neutral
   * @param {string} note - 可选备注
   * @returns {object} 更新后的概念
   */
  adjustFeedback(conceptId, type = 'neutral', note = '') {
    // 支持按 ID 或按 value 查找
    const concept = this.concepts.find(c =>
      c.id === conceptId || c.value === conceptId || c.value === conceptId
    );

    if (!concept) {
      return { error: `概念不存在: ${conceptId}` };
    }

    const scoreMap = { positive: 1, neutral: 0, negative: -1 };
    const delta = scoreMap[type] ?? 0;

    // 更新反馈分数
    concept.feedbackScore = (concept.feedbackScore || 0) + delta;
    concept.feedbackCount = (concept.feedbackCount || 0) + 1;

    // 记录历史（保留最近10条）
    const event = {
      type,
      delta,
      note,
      time: new Date().toISOString()
    };
    concept.feedbackHistory = (concept.feedbackHistory || []).slice(-9).concat(event);

    // 自动标记：连续3次以上负面反馈 或 总分低于 -3
    const negCount = concept.feedbackHistory
      .slice(-5)
      .filter(e => e.type === 'negative').length;
    concept.flagged = negCount >= 3 || concept.feedbackScore < -3;

    this.saveConcepts();
    return {
      success: true,
      concept: {
        value: concept.value,
        type: concept.type,
        importance: concept.importance,
        feedbackScore: concept.feedbackScore,
        feedbackCount: concept.feedbackCount,
        effectiveWeight: this.getEffectiveWeight(concept),
        flagged: concept.flagged
      }
    };
  }

  /**
   * 获取概念的有效权重（含反馈调整）
   * @param {object} concept - 概念对象
   * @returns {number} 调整后权重 [0.1 ~ 10]
   */
  getEffectiveWeight(concept) {
    const base = concept.importance || 5;
    const score = concept.feedbackScore || 0;
    // feedbackScore 范围约 [-10, +10]，每偏离1则权重调整 ±10%
    const multiplier = 1 + score * 0.1;
    return Math.max(0.1, Math.min(10, base * multiplier));
  }

  /**
   * 获取所有概念的有效权重（用于 preResponse 排序）
   * @returns {Array} 带 effectiveWeight 的概念列表
   */
  getConceptsWithWeight() {
    return this.concepts.map(c => ({
      ...c,
      effectiveWeight: this.getEffectiveWeight(c)
    }));
  }

  /**
   * 获取被标记（负面）的概念列表
   */
  getFlaggedConcepts() {
    return this.concepts
      .filter(c => c.flagged)
      .map(c => ({
        value: c.value,
        type: c.type,
        importance: c.importance,
        feedbackScore: c.feedbackScore,
        feedbackCount: c.feedbackCount,
        lastFeedback: c.feedbackHistory?.[c.feedbackHistory.length - 1]
      }));
  }

  /**
   * 获取反馈统计
   */
  getFeedbackStats() {
    const all = this.concepts;
    const flagged = all.filter(c => c.flagged).length;
    const withFeedback = all.filter(c => c.feedbackCount > 0).length;
    const totalNegative = all.reduce((s, c) => s + Math.max(0, -(c.feedbackScore || 0)), 0);
    const totalPositive = all.reduce((s, c) => s + Math.max(0, c.feedbackScore || 0), 0);

    return {
      total: all.length,
      withFeedback,
      flagged,
      negativeConcepts: totalNegative,
      positiveConcepts: totalPositive,
      avgScore: withFeedback > 0
        ? (all.reduce((s, c) => s + (c.feedbackScore || 0), 0) / withFeedback).toFixed(2)
        : 0
    };
  }
  
  /**
   * 批量添加概念
   */
  addConcepts(concepts) {
    for (const concept of concepts) {
      this.addConcept(concept);
    }
    return this.concepts;
  }
  
  /**
   * 搜索概念
   */
  searchConcepts(query, type = null) {
    const lowerQuery = query.toLowerCase();
    return this.concepts.filter(c => {
      const matchQuery = c.value.toLowerCase().includes(lowerQuery);
      const matchType = !type || c.type === type;
      return matchQuery && matchType;
    });
  }
  
  /**
   * 获取高频概念
   */
  getTopConcepts(limit = 10, type = null) {
    let filtered = this.concepts;
    if (type) {
      filtered = filtered.filter(c => c.type === type);
    }
    return filtered
      .sort((a, b) => (b.count || 1) - (a.count || 1))
      .slice(0, limit);
  }
  
  /**
   * 获取概念统计
   */
  getStats() {
    const byType = {};
    const byImportance = { high: 0, medium: 0, low: 0 };
    
    for (const concept of this.concepts) {
      byType[concept.type] = (byType[concept.type] || 0) + 1;
      
      if (concept.importance >= 7) byImportance.high++;
      else if (concept.importance >= 4) byImportance.medium++;
      else byImportance.low++;
    }
    
    return {
      total: this.concepts.length,
      byType,
      byImportance,
      ...this.stats
    };
  }
  
  /**
   * 清理低频概念
   */
  cleanup(minCount = 2) {
    const before = this.concepts.length;
    this.concepts = this.concepts.filter(c => (c.count || 0) >= minCount);
    this.saveConcepts();
    return { before, after: this.concepts.length, removed: before - this.concepts.length };
  }
  
  /**
   * 导出概念
   */
  export(format = 'json') {
    if (format === 'json') {
      return this.concepts;
    }
    
    if (format === 'text') {
      return this.concepts.map(c => `${c.type}: ${c.value} (${c.importance})`).join('\n');
    }
    
    return this.concepts;
  }
}

/**
 * 模式识别系统 - 完整版
 */
class PatternSystem {
  constructor(memoryPath) {
    this.memoryPath = expandPath(memoryPath);
    this.patternsFile = path.join(this.memoryPath, 'eva-patterns.json');
    this.patterns = this.loadPatterns();
    this.messageHistory = [];
    this.maxHistory = 100;
  }
  
  /**
   * 加载模式
   */
  loadPatterns() {
    if (fs.existsSync(this.patternsFile)) {
      try {
        const data = JSON.parse(fs.readFileSync(this.patternsFile, 'utf8'));
        return data.patterns || [];
      } catch (e) {
        return [];
      }
    }
    return [];
  }
  
  /**
   * 保存模式
   */
  savePatterns() {
    const data = {
      patterns: this.patterns,
      lastSave: new Date().toISOString()
    };
    fs.writeFileSync(this.patternsFile, JSON.stringify(data, null, 2));
  }
  
  /**
   * 添加消息到历史
   */
  addMessage(msg) {
    this.messageHistory.push({
      ...msg,
      timestamp: msg.timestamp || new Date().toISOString()
    });
    
    if (this.messageHistory.length > this.maxHistory) {
      this.messageHistory = this.messageHistory.slice(-this.maxHistory);
    }
  }
  
  /**
   * 检测模式 - 完整版
   */
  detectPatterns(messages = null, minOccurrence = 2) {
    const msgs = messages || this.messageHistory;
    const patterns = [];
    
    if (msgs.length < 2) return patterns;
    
    // 1. 时间模式
    const timePatterns = this.detectTimePatterns(msgs);
    patterns.push(...timePatterns);
    
    // 2. 行为模式
    const behaviorPatterns = this.detectBehaviorPatterns(msgs);
    patterns.push(...behaviorPatterns);
    
    // 3. 情感模式
    const emotionPatterns = this.detectEmotionPatterns(msgs);
    patterns.push(...emotionPatterns);
    
    // 4. 意图模式
    const intentPatterns = this.detectIntentPatterns(msgs);
    patterns.push(...intentPatterns);
    
    // 5. 关键词模式
    const keywordPatterns = this.detectKeywordPatterns(msgs);
    patterns.push(...keywordPatterns);
    
    // 添加到模式库
    for (const pattern of patterns) {
      if (pattern.occurrences >= minOccurrence) {
        this.addPattern(pattern);
      }
    }
    
    return patterns;
  }
  
  /**
   * 检测时间模式
   */
  detectTimePatterns(messages) {
    const patterns = [];
    const hourCounts = {};
    const dayCounts = {};
    const weekdayCounts = {};
    
    for (const msg of messages) {
      const time = new Date(msg.timestamp || Date.now());
      const hour = time.getHours();
      const day = time.getDate();
      const weekday = time.getDay();
      
      hourCounts[hour] = (hourCounts[hour] || 0) + 1;
      dayCounts[day] = (dayCounts[day] || 0) + 1;
      weekdayCounts[weekday] = (weekdayCounts[weekday] || 0) + 1;
    }
    
    // 高峰时段
    for (const [hour, count] of Object.entries(hourCounts)) {
      if (count >= Math.max(2, messages.length * 0.2)) {
        patterns.push({
          type: 'time',
          name: `活跃时段${hour}点`,
          value: parseInt(hour),
          frequency: count / messages.length,
          occurrences: count,
          description: `在${hour}点活动频繁`
        });
      }
    }
    
    // 星期模式
    const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    for (const [day, count] of Object.entries(weekdayCounts)) {
      if (count >= Math.max(2, messages.length * 0.15)) {
        patterns.push({
          type: 'weekday',
          name: `${weekdays[day]}活跃`,
          value: parseInt(day),
          frequency: count / messages.length,
          occurrences: count,
          description: `在${weekdays[day]}活动较多`
        });
      }
    }
    
    return patterns;
  }
  
  /**
   * 检测行为模式
   */
  detectBehaviorPatterns(messages) {
    const patterns = [];
    const toolCounts = {};
    const actionCounts = {};
    
    for (const msg of messages) {
      // 工具使用
      if (msg.tool) {
        toolCounts[msg.tool] = (toolCounts[msg.tool] || 0) + 1;
      }
      
      // 动作类型
      if (msg.action) {
        actionCounts[msg.action] = (actionCounts[msg.action] || 0) + 1;
      }
    }
    
    // 常用工具
    for (const [tool, count] of Object.entries(toolCounts)) {
      if (count >= 2) {
        patterns.push({
          type: 'tool',
          name: `常用工具:${tool}`,
          value: tool,
          frequency: count / messages.length,
          occurrences: count,
          description: `经常使用${tool}工具`
        });
      }
    }
    
    // 常用动作
    for (const [action, count] of Object.entries(actionCounts)) {
      if (count >= 2) {
        patterns.push({
          type: 'action',
          name: `常用动作:${action}`,
          value: action,
          frequency: count / messages.length,
          occurrences: count,
          description: `经常执行${action}操作`
        });
      }
    }
    
    return patterns;
  }
  
  /**
   * 检测情感模式
   */
  detectEmotionPatterns(messages) {
    const patterns = [];
    const emotions = messages.map(m => m.emotion).filter(Boolean);
    
    if (emotions.length < 2) return patterns;
    
    // 持续情感
    const emotionCounts = {};
    for (const emotion of emotions) {
      emotionCounts[emotion] = (emotionCounts[emotion] || 0) + 1;
    }
    
    for (const [emotion, count] of Object.entries(emotionCounts)) {
      if (count >= 2) {
        patterns.push({
          type: 'emotion',
          name: `持续${emotion}`,
          value: emotion,
          frequency: count / emotions.length,
          occurrences: count,
          description: `多保持${emotion}情绪`
        });
      }
    }
    
    // 情感变化
    for (let i = 1; i < emotions.length; i++) {
      if (emotions[i] !== emotions[i-1]) {
        const key = `${emotions[i-1]}→${emotions[i]}`;
        const existing = patterns.find(p => p.name === key);
        if (existing) {
          existing.occurrences++;
        } else {
          patterns.push({
            type: 'emotion_change',
            name: key,
            value: key,
            frequency: 1 / emotions.length,
            occurrences: 1,
            description: `情绪从${emotions[i-1]}变为${emotions[i]}`
          });
        }
      }
    }
    
    return patterns;
  }
  
  /**
   * 检测意图模式
   */
  detectIntentPatterns(messages) {
    const patterns = [];
    const intentCounts = {};
    
    for (const msg of messages) {
      if (msg.intent) {
        intentCounts[msg.intent] = (intentCounts[msg.intent] || 0) + 1;
      }
    }
    
    for (const [intent, count] of Object.entries(intentCounts)) {
      if (count >= 2) {
        patterns.push({
          type: 'intent',
          name: `常用意图:${intent}`,
          value: intent,
          frequency: count / messages.length,
          occurrences: count,
          description: `经常进行${intent}操作`
        });
      }
    }
    
    return patterns;
  }
  
  /**
   * 检测关键词模式
   */
  detectKeywordPatterns(messages) {
    const patterns = [];
    const wordCounts = {};
    
    for (const msg of messages) {
      const text = msg.message || msg.content || '';
      const words = text.split(/[\s，。,、；：""''（）()!?！？]+/).filter(w => w.length >= 2);
      
      for (const word of words) {
        wordCounts[word] = (wordCounts[word] || 0) + 1;
      }
    }
    
    for (const [word, count] of Object.entries(wordCounts)) {
      if (count >= 3) {
        patterns.push({
          type: 'keyword',
          name: `高频词:${word}`,
          value: word,
          frequency: count / messages.length,
          occurrences: count,
          description: `经常提到"${word}"`
        });
      }
    }
    
    return patterns;
  }
  
  /**
   * 添加模式
   */
  addPattern(pattern) {
    const existing = this.patterns.find(p => 
      p.type === pattern.type && p.name === pattern.name
    );
    
    if (existing) {
      existing.occurrences = (existing.occurrences || 0) + 1;
      existing.lastSeen = new Date().toISOString();
    } else {
      this.patterns.push({
        ...pattern,
        createdAt: new Date().toISOString(),
        lastSeen: new Date().toISOString()
      });
    }
    
    this.savePatterns();
    return this.patterns;
  }
  
  /**
   * 获取模式
   */
  getPatterns(type = null) {
    if (type) {
      return this.patterns.filter(p => p.type === type);
    }
    return this.patterns;
  }
  
  /**
   * 获取模式统计
   */
  getStats() {
    const byType = {};
    for (const pattern of this.patterns) {
      byType[pattern.type] = (byType[pattern.type] || 0) + 1;
    }
    
    return {
      total: this.patterns.length,
      byType,
      historySize: this.messageHistory.length
    };
  }
  
  /**
   * 清理旧模式
   */
  cleanup(days = 30) {
    const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
    const before = this.patterns.length;
    this.patterns = this.patterns.filter(p => 
      new Date(p.lastSeen || p.createdAt).getTime() > cutoff
    );
    this.savePatterns();
    return { before, after: this.patterns.length };
  }
}

/**
 * 知识图谱 - 完整版
 */
class KnowledgeGraph {
  constructor(memoryPath) {
    this.memoryPath = expandPath(memoryPath);
    this.graphFile = path.join(this.memoryPath, 'eva-knowledge-graph.json');
    this.graph = this.loadGraph();
  }
  
  /**
   * 加载图谱
   */
  loadGraph() {
    if (fs.existsSync(this.graphFile)) {
      try {
        return JSON.parse(fs.readFileSync(this.graphFile, 'utf8'));
      } catch (e) {
        return { nodes: [], edges: [] };
      }
    }
    return { nodes: [], edges: [] };
  }
  
  /**
   * 保存图谱
   */
  saveGraph() {
    fs.writeFileSync(this.graphFile, JSON.stringify(this.graph, null, 2));
  }
  
  /**
   * 添加实体节点
   */
  addNode(node) {
    const { id, label, type, properties = {} } = node;
    
    const existing = this.graph.nodes.find(n => n.id === id);
    
    if (existing) {
      existing.properties = { ...existing.properties, ...properties };
      existing.updatedAt = new Date().toISOString();
    } else {
      this.graph.nodes.push({
        id,
        label: label || id,
        type: type || 'entity',
        properties,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      });
    }
    
    this.saveGraph();
    return this.graph.nodes;
  }
  
  /**
   * 批量添加节点
   */
  addNodes(nodes) {
    for (const node of nodes) {
      this.addNode(node);
    }
    return this.graph.nodes;
  }
  
  /**
   * 添加关系边
   */
  addEdge(edge) {
    const { from, to, type, properties = {} } = edge;
    
    const existing = this.graph.edges.find(e => 
      e.from === from && e.to === to && e.type === type
    );
    
    if (existing) {
      existing.weight = (existing.weight || 1) + 1;
      existing.properties = { ...existing.properties, ...properties };
      existing.updatedAt = new Date().toISOString();
    } else {
      this.graph.edges.push({
        from,
        to,
        type: type || 'related',
        weight: 1,
        properties,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      });
    }
    
    this.saveGraph();
    return this.graph.edges;
  }
  
  /**
   * 批量添加边
   */
  addEdges(edges) {
    for (const edge of edges) {
      this.addEdge(edge);
    }
    return this.graph.edges;
  }
  
  /**
   * 查询节点
   */
  getNode(id) {
    return this.graph.nodes.find(n => n.id === id);
  }
  
  /**
   * 查询关系 - 完整版
   */
  query(startNodeId, depth = 1, direction = 'both') {
    const results = { nodes: [], edges: [], paths: [] };
    const visited = new Set();
    
    const traverse = (nodeId, currentDepth, path) => {
      if (currentDepth > depth || visited.has(nodeId)) return;
      visited.add(nodeId);
      
      const node = this.graph.nodes.find(n => n.id === nodeId);
      if (node && currentDepth > 0) results.nodes.push(node);
      
      path = [...path, nodeId];
      
      // 出边
      if (direction === 'both' || direction === 'out') {
        const outEdges = this.graph.edges.filter(e => e.from === nodeId);
        for (const edge of outEdges) {
          results.edges.push(edge);
          if (currentDepth < depth) {
            traverse(edge.to, currentDepth + 1, path);
          }
        }
      }
      
      // 入边
      if (direction === 'both' || direction === 'in') {
        const inEdges = this.graph.edges.filter(e => e.to === nodeId);
        for (const edge of inEdges) {
          results.edges.push(edge);
          if (currentDepth < depth) {
            traverse(edge.from, currentDepth + 1, path);
          }
        }
      }
    };
    
    traverse(startNodeId, 0, []);
    
    return results;
  }
  
  /**
   * 搜索节点
   */
  searchNodes(query, type = null) {
    const lowerQuery = query.toLowerCase();
    return this.graph.nodes.filter(n => {
      const matchQuery = n.label.toLowerCase().includes(lowerQuery) || 
                        n.id.toLowerCase().includes(lowerQuery);
      const matchType = !type || n.type === type;
      return matchQuery && matchType;
    });
  }
  
  /**
   * 获取节点的所有关系
   */
  getNodeRelations(nodeId) {
    const incoming = this.graph.edges.filter(e => e.to === nodeId);
    const outgoing = this.graph.edges.filter(e => e.from === nodeId);
    
    return {
      incoming: incoming.map(e => ({
        ...e,
        node: this.graph.nodes.find(n => n.id === e.from)
      })),
      outgoing: outgoing.map(e => ({
        ...e,
        node: this.graph.nodes.find(n => n.id === e.to)
      }))
    };
  }
  
  /**
   * 获取图谱统计
   */
  getStats() {
    const nodeTypes = {};
    const edgeTypes = {};
    
    for (const node of this.graph.nodes) {
      nodeTypes[node.type] = (nodeTypes[node.type] || 0) + 1;
    }
    
    for (const edge of this.graph.edges) {
      edgeTypes[edge.type] = (edgeTypes[edge.type] || 0) + 1;
    }
    
    return {
      nodes: this.graph.nodes.length,
      edges: this.graph.edges.length,
      nodeTypes,
      edgeTypes,
      density: this.graph.edges.length / Math.max(1, this.graph.nodes.length * (this.graph.nodes.length - 1) / 2)
    };
  }
  
  /**
   * 删除节点
   */
  deleteNode(id) {
    const before = this.graph.nodes.length;
    this.graph.nodes = this.graph.nodes.filter(n => n.id !== id);
    this.graph.edges = this.graph.edges.filter(e => e.from !== id && e.to !== id);
    this.saveGraph();
    return { before, after: this.graph.nodes.length };
  }
  
  /**
   * 删除边
   */
  deleteEdge(from, to, type = null) {
    const before = this.graph.edges.length;
    this.graph.edges = this.graph.edges.filter(e => 
      !(e.from === from && e.to === to && (!type || e.type === type))
    );
    this.saveGraph();
    return { before, after: this.graph.edges.length };
  }
  
  /**
   * 导出图谱
   */
  export(format = 'json') {
    if (format === 'json') {
      return this.graph;
    }
    
    if (format === 'dot') {
      let dot = 'digraph EVA {\n';
      for (const node of this.graph.nodes) {
        dot += `  "${node.id}" [label="${node.label}", type="${node.type}"];\n`;
      }
      for (const edge of this.graph.edges) {
        dot += `  "${edge.from}" -> "${edge.to}" [label="${edge.type}"];\n`;
      }
      dot += '}\n';
      return dot;
    }
    
    return this.graph;
  }
}

/**
 * Embedding增强 - 概念提取
 */
class EmbeddingConceptEnhancer {
  constructor() {
    this.vectorConfig = {
      apiKey: process.env.SILICONFLOW_API_KEY,
      model: 'BAAI/bge-large-zh-v1.5',
      apiUrl: 'https://api.siliconflow.cn/v1/embeddings'
    };

    // 预设概念类别向量 (用于相似度匹配)
    this.categoryTemplates = {
      person: ['人名', '人物', '谁', '朋友', '家人', '同事', '老板', '员工'],
      location: ['地点', '城市', '国家', '地址', '在哪里', '住在'],
      work: ['工作', '项目', '公司', '创业', '业务', '客户', '合同', '会议'],
      life: ['生活', '家庭', '租房', '吃饭', '睡觉', '日常'],
      health: ['健康', '运动', '生病', '感冒', '身体', '锻炼'],
      emotion: ['开心', '难过', '生气', '害怕', '爱', '恨'],
      finance: ['钱', '投资', '理财', '工资', '收入', '支出'],
      tech: ['电脑', '手机', '代码', 'AI', '技术', '开发'],
      education: ['学习', '学校', '考试', '培训', '课程'],
      hobby: ['爱好', '喜欢', '兴趣', '娱乐', '游戏']
    };

    // 模板关键词 embedding 缓存（惰性预计算）
    this._templateEmbeddings = null;
    this._embeddingCache = new Map(); // 通用文本缓存（TTL 1小时）
  }
  
  /**
   * 生成文本embedding向量（带缓存，TTL 1小时）
   */
  async generateEmbedding(text) {
    if (!this.vectorConfig.apiKey) return null;

    const cached = this._embeddingCache.get(text);
    if (cached && Date.now() - cached.timestamp < 60 * 60 * 1000) {
      return cached.embedding;
    }

    try {
      const response = await fetchWithRetry(this.vectorConfig.apiUrl, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.vectorConfig.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: this.vectorConfig.model,
          input: [text]
        })
      });

      const data = await response.json();
      if (data.data && data.data[0]) {
        const embedding = data.data[0].embedding;
        this._embeddingCache.set(text, { embedding, timestamp: Date.now() });
        return embedding;
      }
      return null;
    } catch (e) {
      logger.warn(`[embedding] 生成失败: ${e.message}`, 'cognition');
      return null;
    }
  }

  /**
   * 预计算所有模板关键词的 embedding（惰性，一次性）
   */
  async _ensureTemplateEmbeddings() {
    if (this._templateEmbeddings) return;

    const templateEmbeddings = {};
    for (const [category, keywords] of Object.entries(this.categoryTemplates)) {
      const vectors = [];
      for (const keyword of keywords) {
        const emb = await this.generateEmbedding(keyword);
        if (emb) vectors.push(emb);
      }
      templateEmbeddings[category] = vectors;
    }
    this._templateEmbeddings = templateEmbeddings;
  }

  /**
   * 使用embedding增强概念提取
   */
  async enhanceConcepts(text, existingConcepts = []) {
    const enhanced = {
      embedding: null,
      category: null,
      semanticTags: [],
      confidence: 0
    };

    // 1. 生成文本向量
    const embedding = await this.generateEmbedding(text);
    if (!embedding) return enhanced;

    enhanced.embedding = embedding;

    // 2. 预计算模板向量（一次性）
    await this._ensureTemplateEmbeddings();

    // 3. 计算与类别模板的相似度（使用缓存的模板向量）
    const categoryScores = {};

    for (const [category, templateVectors] of Object.entries(this._templateEmbeddings)) {
      if (!templateVectors.length) {
        categoryScores[category] = 0;
        continue;
      }
      const avgSim = templateVectors.reduce((sum, v) => sum + this.cosineSimilarity(embedding, v), 0) / templateVectors.length;
      categoryScores[category] = avgSim;
    }

    // 4. 找出最匹配的类别
    let maxScore = 0;
    let bestCategory = 'unknown';

    for (const [category, score] of Object.entries(categoryScores)) {
      if (score > maxScore) {
        maxScore = score;
        bestCategory = category;
      }
    }
    
    enhanced.category = bestCategory;
    enhanced.confidence = maxScore;
    
    // 5. 生成语义标签
    enhanced.semanticTags = this.generateSemanticTags(text, bestCategory, embedding);
    
    return enhanced;
  }
  
  /**
   * 余弦相似度计算
   */
  cosineSimilarity(a, b) {
    if (!a || !b || a.length !== b.length) return 0;
    
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;
    
    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }
    
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
  }
  
  /**
   * 生成语义标签
   */
  generateSemanticTags(text, category, embedding) {
    const tags = [category];
    const msg = text.toLowerCase();
    
    // 基于类别添加标签
    const categoryTags = {
      work: ['职业', '事业', '商务'],
      life: ['日常', '个人'],
      health: ['身体', '医疗'],
      emotion: ['感受', '心情'],
      finance: ['金钱', '资产'],
      tech: ['技术', '数码'],
      education: ['学习', '知识'],
      hobby: ['休闲', '娱乐']
    };
    
    if (categoryTags[category]) {
      tags.push(...categoryTags[category]);
    }
    
    // 基于情感添加标签
    if (/开心|高兴|快乐/.test(msg)) tags.push('正面情感');
    if (/难过|伤心|痛苦/.test(msg)) tags.push('负面情感');
    if (/爱|喜欢/.test(msg)) tags.push('情感相关');
    if (/工作|项目|会议/.test(msg)) tags.push('工作相关');
    
    return [...new Set(tags)];
  }
  
  /**
   * 批量处理概念 (带缓存)
   */
  async batchEnhance(concepts) {
    const results = [];
    for (const concept of concepts) {
      if (!concept.embedding) {
        const enhanced = await this.enhanceConcepts(concept.value || concept.content || '');
        results.push({ ...concept, ...enhanced });
      } else {
        results.push(concept);
      }
    }
    return results;
  }
}

// 导出
module.exports = {
  ConceptSystem,
  PatternSystem,
  KnowledgeGraph,
  EmbeddingConceptEnhancer
};
