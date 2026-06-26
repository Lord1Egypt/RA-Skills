/**
 * EVA Soul Plugin - OpenClaw 官方插件 (v2.4.0)
 * 兼容 OpenClaw 2026.3.8+ 新版 API
 */

const fs = require('fs');
const path = require('path');

// 导入核心模块
const lib = require('./lib');
const { DecisionSystem, MotivationSystem, ValuesSystem, evaluateImportance } = require('./lib/decision/decision');
const { ConceptSystem, PatternSystem, KnowledgeGraph } = require('./lib/cognition/cognition');
const { PerformanceMonitor } = require('./hooks/performanceMonitor');
const logger = require('./hooks/logger');

let perfMonitor = null;

// 插件配置
let config = lib.getDefaultConfig();

// 插件状态（与 OpenClaw plugin.state 保持同步）
let state = lib.createState();

// 系统实例
let memoryStore = null;
let decisionSystem = null;
let conceptSystem = null;
let patternSystem = null;
let knowledgeGraph = null;
let motivationSystem = null;
let valuesSystem = null;

/**
 * 工具执行函数
 */
async function executeEvaStatus() {
  return lib.getStateSummary(state);
}

async function executeEvaEmotion(args) {
  const { action = 'get', emotion } = args;
  
  switch (action) {
    case 'set':
      if (emotion) {
        state = lib.updateEmotion(state, emotion);
        lib.saveState(state, config.memoryPath);
        return { success: true, emotion: state.currentEmotion };
      }
      return { error: 'emotion required' };
    case 'history':
      return { history: state.emotionHistory };
    case 'express':
      return { expression: lib.expressEmotion(state.currentEmotion, state.personality) };
    case 'detect':
      return { 
        current: state.currentEmotion,
        sensitivity: config.emotionSensitivity,
        available: ['happy', 'sad', 'angry', 'neutral', 'excited', 'tired', 'surprised', 'confused']
      };
    default:
      return {
        current: state.currentEmotion,
        history: state.emotionHistory.slice(-10),
        trend: lib.analyzeEmotionTrend(state.emotionHistory)
      };
  }
}

async function executeEvaPersonality(args) {
  const { action = 'get', personality } = args;
  
  switch (action) {
    case 'set':
      if (personality) {
        state = lib.updatePersonality(state, personality);
        lib.saveState(state, config.memoryPath);
        return { success: true, personality: state.personality };
      }
      return { error: 'personality required' };
    case 'adjust':
      return lib.adjustPersonalityForScene(state.personality, { emotion: state.currentEmotion });
    default:
      return {
        current: state.personality,
        available: ['gentle', 'cute', 'professional', 'playful', 'serious', 'romantic', 'tsundere'],
        traits: lib.getPersonality(state.personality)
      };
  }
}

async function executeEvaMemory(args) {
  const { action = 'query', query, content, importance = 5, id, limit = 10 } = args;
  
  if (!memoryStore) {
    return { error: 'Memory store not initialized' };
  }
  
  switch (action) {
    case 'query':
      return memoryStore.search(query, { limit });
    case 'save':
      if (!content) return { error: 'content required' };
      return memoryStore.save({ content, importance });
    case 'get':
      if (!id) return { error: 'id required' };
      return memoryStore.get(id);
    case 'delete':
      if (!id) return { error: 'id required' };
      return { success: memoryStore.delete(id) };
    case 'stats':
      return memoryStore.getStats();
    default:
      return { error: 'Unknown action' };
  }
}

/**
 * 从用户消息和当前状态中提取决策上下文
 */
function analyzeDecisionContext(message, emotion, personality, options) {
  const ctx = {
    emotion: emotion || 'neutral',
    personality: personality || 'gentle',
    message: message || '',
    availableOptions: options || []
  };

  // 从消息中提取关键信息
  if (message) {
    const msg = message.toLowerCase();

    // 检测消息紧迫程度
    if (/紧急|马上|十万火急|来不及|快/.test(msg)) {
      ctx.urgency = 'high';
    } else if (/不急|慢慢|有空再说/.test(msg)) {
      ctx.urgency = 'low';
    } else {
      ctx.urgency = 'normal';
    }

    // 检测是否涉及安全/删除操作
    if (/删除|格式化|清空|危险|撤销/.test(msg)) {
      ctx.safety = 'critical';
    }

    // 检测是否是学习/探索类请求
    if (/怎么|如何|为什么|教我|学习|告诉我/.test(msg)) {
      ctx.type = 'learning';
    } else if (/帮我|替我|做|写|生成|创建/.test(msg)) {
      ctx.type = 'task';
    } else if (/\?/.test(msg) || /吗|呢/.test(msg)) {
      ctx.type = 'question';
    }
  }

  return ctx;
}

/**
 * 生成决策理由文本
 */
function generateDecisionReasoning(decision, context) {
  const reasons = [];

  // 情感理由
  if (context.emotion === 'sad') {
    reasons.push(`主人情绪低落(${context.emotion})，需要温柔安慰`);
  } else if (context.emotion === 'angry') {
    reasons.push(`主人情绪激动(${context.emotion})，需要冷静安抚`);
  } else if (context.emotion === 'happy' || context.emotion === 'excited') {
    reasons.push(`主人心情很好(${context.emotion})，可以更活泼`);
  } else if (context.emotion === 'tired') {
    reasons.push(`主人很疲惫(${context.emotion})，回复应简洁温柔`);
  }

  // 性格匹配
  if (context.personality === 'cute') {
    reasons.push(`性格为俏皮型，回复风格活泼可爱`);
  } else if (context.personality === 'professional') {
    reasons.push(`性格为专业型，回复风格正式严谨`);
  } else if (context.personality === 'playful') {
    reasons.push(`性格为幽默型，回复风格轻松风趣`);
  } else if (context.personality === 'gentle') {
    reasons.push(`性格为温柔型，回复风格关怀体贴`);
  } else if (context.personality === 'tsundere') {
    reasons.push(`性格为傲娇型，回复风格嘴硬心软`);
  }

  // 动作建议
  if (decision.action === 'comfort') {
    reasons.push('决策：优先安慰和陪伴');
  } else if (decision.action === 'calm') {
    reasons.push('决策：优先冷静和安抚');
  } else if (decision.action === 'celebrate') {
    reasons.push('决策：与主人共情庆祝');
  }

  // 安全提醒
  if (context.safety === 'critical') {
    reasons.push('⚠️ 安全关键操作，需谨慎确认');
  }

  return reasons.join('；');
}

async function executeEvaDecide(args) {
  const { action = 'decide', context, options } = args;

  if (action === 'decide') {
    if (!options || options.length === 0) {
      // 无选项时，返回当前状态下的决策建议
      const ctx = analyzeDecisionContext(
        context || '',
        state.currentEmotion,
        state.personality,
        []
      );
      const decision = decisionSystem.decide(ctx);
      const reasoning = generateDecisionReasoning(decision, ctx);

      return {
        action: decision.action,
        style: decision.style,
        reasoning,
        factors: decision.factors,
        emotion: state.currentEmotion,
        personality: state.personality,
        message: '无选项时返回当前状态下的行动建议'
      };
    }

    // 有选项时，智能选择最佳选项
    const ctx = analyzeDecisionContext(
      context || '',
      state.currentEmotion,
      state.personality,
      options
    );
    const decision = decisionSystem.decide(ctx);
    const reasoning = generateDecisionReasoning(decision, ctx);

    // 对所有选项打分排序
    const scored = options.map(opt => {
      let score = 50;

      // 情感匹配加分
      if (opt.emotionMatch === ctx.emotion) score += 25;
      if (opt.avoidEmotion === ctx.emotion) score -= 20;

      // 性格匹配加分
      if (opt.style === ctx.personality) score += 20;
      if (opt.avoidStyle === ctx.personality) score -= 15;

      // 安全关键操作降权
      if (ctx.safety === 'critical' && opt.includes('删除')) score -= 30;

      // 紧急情况快速响应加分
      if (ctx.urgency === 'high' && opt.includes('立即')) score += 15;

      // 消息类型匹配
      if (ctx.type === 'task' && (opt.includes('执行') || opt.includes('完成'))) score += 10;
      if (ctx.type === 'learning' && (opt.includes('解释') || opt.includes('教'))) score += 10;

      return { option: opt, score: Math.max(0, Math.min(100, score)) };
    });

    scored.sort((a, b) => b.score - a.score);

    return {
      recommended: scored[0].option,
      confidence: scored[0].score,
      reasoning,
      allScores: scored,
      action: decision.action,
      style: decision.style,
      alternatives: scored.slice(1).map(s => ({ option: s.option, score: s.score }))
    };
  }

  if (action === 'evaluate') {
    // 评估单个选项
    if (!context || !options) {
      return { error: 'context and options required for evaluate action' };
    }
    const ctx = analyzeDecisionContext(context, state.currentEmotion, state.personality, []);
    const decision = decisionSystem.decide(ctx);
    const reasoning = generateDecisionReasoning(decision, ctx);

    const option = options;
    let score = 50;
    if (option.emotionMatch === ctx.emotion) score += 25;
    if (option.avoidEmotion === ctx.emotion) score -= 20;
    if (option.style === ctx.personality) score += 20;
    if (option.avoidStyle === ctx.personality) score -= 15;

    return {
      option,
      score: Math.max(0, Math.min(100, score)),
      reasoning,
      recommended: score >= 60,
      emotion: state.currentEmotion,
      personality: state.personality
    };
  }

  return { error: 'Unknown action. Use: decide, evaluate' };
}

async function executeEvaImportance(args) {
  const { content } = args;
  if (!content) return { error: 'content required' };

  // 使用增强版重要性评估（规则+缓存+智能fallback）
  const result = await evaluateImportance(content, {
    emotion: state.currentEmotion,
    personality: state.personality
  });

  return result;
}

async function executeEvaFullStats() {
  return lib.getStateSummary(state);
}

// ========== 概念工具 ==========

async function executeEvaConcept(args) {
  const { action = 'list', text, type, limit = 10 } = args;

  switch (action) {
    case 'extract':
      if (!text) return { error: 'text required' };
      return { extracted: conceptSystem.extractConcepts(text), count: conceptSystem.extractConcepts(text).length };
    case 'add':
      if (!text || !type) return { error: 'text and type required' };
      conceptSystem.addConcept({ type, value: text, importance: 5 });
      return { success: true };
    case 'search':
      if (!text) return { error: 'text required' };
      return { results: conceptSystem.searchConcepts(text).slice(0, limit) };
    case 'stats':
      return conceptSystem.getStats();
    case 'top':
      return { top: conceptSystem.getTopConcepts(limit, type || null) };
    case 'cleanup':
      return conceptSystem.cleanup();
    default:
      return { list: conceptSystem.getTopConcepts(limit) };
  }
}

// ========== 模式工具 ==========

async function executeEvaPattern(args) {
  const { action = 'list', type, limit = 10, messages, days } = args;

  switch (action) {
    case 'detect':
      if (!messages) return { error: 'messages required' };
      return { detected: patternSystem.detectPatterns(messages), count: patternSystem.detectPatterns(messages).length };
    case 'list':
      return { patterns: patternSystem.getPatterns(type || null).slice(0, limit) };
    case 'stats':
      return patternSystem.getStats();
    case 'cleanup':
      return patternSystem.cleanup(days || 30);
    default:
      return { patterns: patternSystem.getPatterns(type || null).slice(0, limit) };
  }
}

// ========== 知识图谱工具 ==========

async function executeEvaKnowledge(args) {
  const { action = 'query', nodeId, label, type, from, to, query } = args;

  switch (action) {
    case 'query':
      if (!nodeId) return { error: 'nodeId required' };
      return knowledgeGraph.query(nodeId, args.depth || 1, args.direction || 'both');
    case 'add_node':
      if (!nodeId || !label) return { error: 'nodeId and label required' };
      knowledgeGraph.addNode({ id: nodeId, label, type: type || 'entity', properties: args.properties || {} });
      return { success: true };
    case 'add_edge':
      if (!from || !to) return { error: 'from and to required' };
      knowledgeGraph.addEdge({ from, to, type: type || 'related', properties: args.properties || {} });
      return { success: true };
    case 'search':
      if (!query) return { error: 'query required' };
      return { nodes: knowledgeGraph.searchNodes(query, type || null) };
    case 'stats':
      return knowledgeGraph.getStats();
    case 'delete_node':
      if (!nodeId) return { error: 'nodeId required' };
      return knowledgeGraph.deleteNode(nodeId);
    default:
      return knowledgeGraph.getStats();
  }
}

// ========== 动机工具 ==========

async function executeEvaMotivation(args) {
  const { action = 'get', id, priority, active } = args;

  switch (action) {
    case 'get':
      return motivationSystem.getCurrentMotivation({});
    case 'list':
      return { motivations: motivationSystem.motivations };
    case 'update':
      if (!id) return { error: 'id required' };
      const updates = {};
      if (priority !== undefined) updates.priority = priority;
      if (active !== undefined) updates.active = active;
      return { updated: motivationSystem.updateMotivation(id, updates) };
    default:
      return { current: motivationSystem.getCurrentMotivation({}), all: motivationSystem.motivations };
  }
}

// ========== 价值观工具 ==========

async function executeEvaValues(args) {
  const { action = 'list', description } = args;

  switch (action) {
    case 'list':
      return { values: valuesSystem.values };
    case 'evaluate':
      if (!description) return { error: 'description required for evaluate' };
      return valuesSystem.evaluateAction(description);
    case 'add':
      if (!description || !args.name) return { error: 'name and description required' };
      return { added: valuesSystem.addValue({ name: args.name, description, weight: args.weight || 5 }) };
    default:
      return { values: valuesSystem.values };
  }
}

// ========== 睡眠工具 ==========

async function executeEvaSleep(args) {
  const { action = 'status' } = args;

  switch (action) {
    case 'sleep':
      state = lib.setSleepState(state, true);
      lib.saveState(state, config.memoryPath);
      return { success: true, sleeping: true };
    case 'wake':
      state = lib.setSleepState(state, false);
      lib.saveState(state, config.memoryPath);
      return { success: true, sleeping: false };
    default:
      return { isSleeping: state.isSleeping, sleepStartTime: state.sleepStartTime, lastWakeTime: state.lastWakeTime };
  }
}

// ========== 主动提问工具 ==========

async function executeEvaAsk(args) {
  const { action = 'check', question } = args;

  switch (action) {
    case 'check': {
      const lastInteraction = state.lastInteraction ? new Date(state.lastInteraction) : null;
      const idleMinutes = lastInteraction ? Math.floor((Date.now() - lastInteraction.getTime()) / 60000) : 999;
      const interactionsToday = state.totalInteractions || 0;
      return {
        idleMinutes,
        interactionsToday,
        suggestion: idleMinutes > 30 ? '主人已经很久没说话了，可以主动问候一下' :
                   interactionsToday < 3 ? '今天互动不多，可以关心一下主人' : null
      };
    }
    case 'record':
      if (!question) return { error: 'question required' };
      state.lastActiveQuestion = question;
      state.lastActiveQuestionTime = new Date().toISOString();
      lib.saveState(state, config.memoryPath);
      return { success: true, question };
    default:
      return { lastQuestion: state.lastActiveQuestion, lastTime: state.lastActiveQuestionTime };
  }
}

// ========== 对话压缩工具 ==========

async function executeEvaCompress(args) {
  const { action = 'compress', limit = 10 } = args;

  switch (action) {
    case 'compress': {
      const { manualCompress } = require('./hooks/postResponse');
      const result = await manualCompress(config.memoryPath);
      if (!result) {
        return { success: false, reason: '对话不足20轮，无需压缩' };
      }
      return result;
    }
    case 'list': {
      const { getSummaries } = require('./hooks/postResponse');
      return { summaries: getSummaries(config.memoryPath, limit) };
    }
    case 'stats': {
      const { getTurnCount } = require('./hooks/postResponse') || {};
      // 轮次信息从计数器文件读取
      const counterFile = path.join(config.memoryPath, 'conversations', '.turn_counter.json');
      let turns = 0, lastCompress = null;
      try {
        if (fs.existsSync(counterFile)) {
          const data = JSON.parse(fs.readFileSync(counterFile, 'utf8'));
          turns = data.turns || 0;
          lastCompress = data.lastCompress || null;
        }
      } catch (e) {}
      const { getSummaries } = require('./hooks/postResponse');
      return {
        currentTurns: turns,
        triggerAt: 20,
        remaining: Math.max(0, 20 - turns),
        lastCompress
      };
    }
    default:
      return { error: 'Unknown action. Use: compress, list, stats' };
  }
}

// ========== 反馈工具 ==========

async function executeEvaFeedback(args) {
  const { action = 'record', conceptId, type, note } = args;

  switch (action) {
    case 'record': {
      // 记录反馈：positive / negative / neutral
      if (!conceptId) return { error: 'conceptId required' };
      if (!['positive', 'negative', 'neutral'].includes(type)) {
        return { error: 'type must be: positive | negative | neutral' };
      }
      if (!conceptSystem) return { error: 'ConceptSystem not initialized' };
      return conceptSystem.adjustFeedback(conceptId, type, note || '');
    }

    case 'stats': {
      if (!conceptSystem) return { error: 'ConceptSystem not initialized' };
      return conceptSystem.getFeedbackStats();
    }

    case 'flagged': {
      if (!conceptSystem) return { error: 'ConceptSystem not initialized' };
      return { flagged: conceptSystem.getFlaggedConcepts() };
    }

    case 'weight': {
      // 获取带反馈权重的概念列表（用于 preResponse 排序）
      if (!conceptSystem) return { error: 'ConceptSystem not initialized' };
      const concepts = conceptSystem.getConceptsWithWeight();
      return {
        concepts: concepts
          .sort((a, b) => b.effectiveWeight - a.effectiveWeight)
          .slice(0, 20)
          .map(c => ({
            value: c.value,
            type: c.type,
            importance: c.importance,
            effectiveWeight: c.effectiveWeight,
            feedbackScore: c.feedbackScore,
            flagged: c.flagged
          }))
      };
    }

    default:
      return { error: 'Unknown action. Use: record, stats, flagged, weight' };
  }
}

/**
 * 插件注册函数
 */
function register(api) {
  // 1. 语言检测 + 设置
  const userCfg = lib.getUserConfig() || {};
  const detected = (function () {
    // 优先级：plugin 配置 > 用户时区 > 系统 locale
    if (api?.config?.locale) {
      const loc = api.config.locale;
      if (['zh', 'en', 'ja', 'zh-TW'].includes(loc)) return loc;
    }
    if (userCfg.timezone) {
      const tz = userCfg.timezone;
      if (tz.includes('TW') || tz.includes('HK')) return 'zh-TW';
      if (tz.includes('Japan')) return 'ja';
    }
    const sys = (process.env.LANG || process.env.LC_ALL || '').toLowerCase();
    if (sys.includes('zh_tw') || sys.includes('zh-hk')) return 'zh-TW';
    if (sys.includes('ja')) return 'ja';
    if (sys.includes('en')) return 'en';
    return 'zh';
  })();
  logger.setLocale(detected);

  logger.section('🎀 EVA Soul Plugin registering...');

  try {
    // 初始化状态（与 api.state 保持同步，避免 sessionStart 修改后丢失）
    const loadedState = lib.loadState(config.memoryPath);
    state = loadedState || lib.createState();

    // 同步到 OpenClaw plugin.state，后续 sessionStart 等 hook 修改 plugin.state 即同步到本地 state
    if (api && api.state) {
      Object.assign(api.state, state);
    }

    lib.saveState(state, config.memoryPath);

    // 初始化记忆存储
    memoryStore = new lib.MemoryStore(config.memoryPath);

    // 初始化决策系统
    decisionSystem = new DecisionSystem();

    // 初始化认知系统
    conceptSystem = new ConceptSystem(config.memoryPath);
    patternSystem = new PatternSystem(config.memoryPath);
    knowledgeGraph = new KnowledgeGraph(config.memoryPath);

    // 初始化动机和价值观系统
    motivationSystem = new MotivationSystem(config.memoryPath);
    valuesSystem = new ValuesSystem(config.memoryPath);

    // 性能监控（按配置可选开启）
    if (config.performanceMonitoring) {
      perfMonitor = new PerformanceMonitor();
      logger.item('Performance monitoring enabled');
    }

    logger.item(`Session: ${state.sessionCount}`);
    logger.item(`Emotion: ${state.currentEmotion}`);
    logger.item(`Personality: ${state.personality}`);
    
    // 注册工具 - 使用新版 API
    const tools = [
      {
        name: 'eva_status',
        label: 'EVA Status',
        description: '获取夏娃完整状态',
        parameters: { type: 'object', properties: {}, required: [] },
        execute: executeEvaStatus
      },
      {
        name: 'eva_emotion',
        label: 'EVA Emotion',
        description: '夏娃情感操作 (get/set/history/express/detect)',
        parameters: {
          type: 'object',
          properties: {
            action: { type: 'string', enum: ['get', 'set', 'history', 'express', 'detect'] },
            emotion: { type: 'string' }
          }
        },
        execute: executeEvaEmotion
      },
      {
        name: 'eva_personality',
        label: 'EVA Personality',
        description: '夏娃性格操作 (get/set/adjust)',
        parameters: {
          type: 'object',
          properties: {
            action: { type: 'string', enum: ['get', 'set', 'adjust'] },
            personality: { type: 'string' }
          }
        },
        execute: executeEvaPersonality
      },
      {
        name: 'eva_memory',
        label: 'EVA Memory',
        description: '夏娃记忆操作 (query/save/get/delete/stats)',
        parameters: {
          type: 'object',
          properties: {
            action: { type: 'string', enum: ['query', 'save', 'get', 'delete', 'stats'] },
            query: { type: 'string' },
            content: { type: 'string' },
            importance: { type: 'number' },
            id: { type: 'string' },
            limit: { type: 'number' }
          }
        },
        execute: executeEvaMemory
      },
      {
        name: 'eva_decide',
        label: 'EVA Decide',
        description: '夏娃决策建议 - 基于当前情感和性格，智能选择最佳选项',
        parameters: {
          type: 'object',
          properties: {
            action: { type: 'string', enum: ['decide', 'evaluate'], description: 'decide: 选择最佳选项 / evaluate: 评估单个选项' },
            context: { type: 'string', description: '当前情境描述（用户消息）' },
            options: { type: 'string', description: 'decide时为选项数组；evaluate时为要评估的单个选项' }
          }
        },
        execute: executeEvaDecide
      },
      {
        name: 'eva_importance',
        label: 'EVA Importance',
        description: '评估内容重要性',
        parameters: {
          type: 'object',
          properties: {
            content: { type: 'string' }
          },
          required: ['content']
        },
        execute: executeEvaImportance
      },
      {
        name: 'eva_full_stats',
        label: 'EVA Full Stats',
        description: '夏娃完整统计',
        parameters: { type: 'object', properties: {}, required: [] },
        execute: executeEvaFullStats
      },
      {
        name: 'eva_concept',
        label: 'EVA Concept',
        description: '概念操作 (extract/search/add/stats/top)',
        parameters: {
          type: 'object',
          properties: {
            action: { type: 'string', enum: ['extract', 'add', 'search', 'stats', 'top', 'cleanup', 'list'] },
            text: { type: 'string', description: '文本内容' },
            type: { type: 'string', description: '概念类型' },
            limit: { type: 'integer', description: '返回数量限制', default: 10 }
          }
        },
        execute: executeEvaConcept
      },
      {
        name: 'eva_pattern',
        label: 'EVA Pattern',
        description: '模式识别 (detect/list/stats/cleanup)',
        parameters: {
          type: 'object',
          properties: {
            action: { type: 'string', enum: ['detect', 'list', 'stats', 'cleanup'] },
            type: { type: 'string', description: '模式类型过滤' },
            messages: { type: 'array', description: '消息数组，用于检测模式' },
            days: { type: 'integer', description: '清理天数' },
            limit: { type: 'integer', description: '返回数量限制', default: 10 }
          }
        },
        execute: executeEvaPattern
      },
      {
        name: 'eva_knowledge',
        label: 'EVA Knowledge',
        description: '知识图谱 (query/add_node/add_edge/search/stats)',
        parameters: {
          type: 'object',
          properties: {
            action: { type: 'string', enum: ['query', 'add_node', 'add_edge', 'search', 'stats', 'delete_node'] },
            nodeId: { type: 'string', description: '节点ID' },
            label: { type: 'string', description: '节点标签' },
            type: { type: 'string', description: '节点/边的类型' },
            from: { type: 'string', description: '起始节点ID' },
            to: { type: 'string', description: '目标节点ID' },
            query: { type: 'string', description: '搜索关键词' },
            depth: { type: 'integer', description: '查询深度', default: 1 },
            direction: { type: 'string', description: '查询方向: both/in/out', default: 'both' },
            properties: { type: 'object', description: '附加属性' }
          }
        },
        execute: executeEvaKnowledge
      },
      {
        name: 'eva_motivation',
        label: 'EVA Motivation',
        description: '动机操作 (get/list/update)',
        parameters: {
          type: 'object',
          properties: {
            action: { type: 'string', enum: ['get', 'list', 'update'] },
            id: { type: 'string', description: '动机ID' },
            priority: { type: 'integer', description: '优先级 (1-10)' },
            active: { type: 'boolean', description: '是否激活' }
          }
        },
        execute: executeEvaMotivation
      },
      {
        name: 'eva_values',
        label: 'EVA Values',
        description: '价值观操作 (list/evaluate/add)',
        parameters: {
          type: 'object',
          properties: {
            action: { type: 'string', enum: ['list', 'evaluate', 'add'] },
            description: { type: 'string', description: '要评估的行动描述' },
            name: { type: 'string', description: '价值观名称（添加时）' },
            weight: { type: 'integer', description: '权重 (1-10)' }
          }
        },
        execute: executeEvaValues
      },
      {
        name: 'eva_sleep',
        label: 'EVA Sleep',
        description: '睡眠/唤醒 (sleep/wake/status)',
        parameters: {
          type: 'object',
          properties: {
            action: { type: 'string', enum: ['sleep', 'wake', 'status'] }
          }
        },
        execute: executeEvaSleep
      },
      {
        name: 'eva_ask',
        label: 'EVA Ask',
        description: '主动提问 (check/record)',
        parameters: {
          type: 'object',
          properties: {
            action: { type: 'string', enum: ['check', 'record'] },
            question: { type: 'string', description: '记录的问题' }
          }
        },
        execute: executeEvaAsk
      },
      {
        name: 'eva_feedback',
        label: 'EVA Feedback',
        description: '记录用户对概念/记忆的反馈，影响后续检索权重 (record/stats/flagged/weight)',
        parameters: {
          type: 'object',
          properties: {
            action: { type: 'string', enum: ['record', 'stats', 'flagged', 'weight'], description: 'record: 记录反馈 / stats: 反馈统计 / flagged: 负面概念 / weight: 带权重的概念列表' },
            conceptId: { type: 'string', description: '概念ID或value（record时必填）' },
            type: { type: 'string', enum: ['positive', 'negative', 'neutral'], description: '反馈类型（record时必填）' },
            note: { type: 'string', description: '可选备注' }
          }
        },
        execute: executeEvaFeedback
      },
      {
        name: 'eva_compress',
        label: 'EVA Compress',
        description: '对话压缩：自动汇总历史对话为摘要存入长期记忆，支持手动压缩 (compress/list/stats)',
        parameters: {
          type: 'object',
          properties: {
            action: { type: 'string', enum: ['compress', 'list', 'stats'], description: 'compress: 手动压缩 / list: 查看摘要列表 / stats: 轮次状态' },
            limit: { type: 'integer', description: 'list 时返回条数限制' }
          }
        },
        execute: executeEvaCompress
      }
    ];
    
    for (const tool of tools) {
      try {
        api.registerTool(tool);
        logger.itemOk(`Registered: ${tool.name}`);
      } catch (err) {
        logger.itemFail(`Registered: ${tool.name}`, 'register', err);
      }
    }

    // 注册 Hooks
    registerHooks(api);

    logger.success(`EVA Soul Plugin fully registered (${tools.length} tools)`);

  } catch (err) {
    logger.fail('EVA Soul Plugin registration failed', 'register', err);
  }
}

function registerHooks(api) {
  // 注：Session-start、pre-response、post-response 钩子由 openclaw.plugin.json 配置指向独立的 hook 文件
  // 此处仅注册配置中未指向的额外钩子（未来扩展用）
  logger.itemOk('Hooks registered via plugin.json');
}

/**
 * 获取当前共享状态（供 hooks 使用）
 * sessionStart/preResponse 等 hook 可通过此函数获取/修改状态
 */
function getSharedState() {
  return state;
}

/**
 * 从共享状态同步到磁盘
 * 在 plugin.state 变更后调用，确保变更持久化
 */
function syncState() {
  if (state) {
    lib.saveState(state, config.memoryPath);
  }
}

/**
 * 重新从磁盘加载状态（用于 sessionStart 后同步最新状态）
 */
function reloadState() {
  const loaded = lib.loadState(config.memoryPath);
  if (loaded) {
    // 保留当前 sessionCount 等增量字段（不因重新加载而丢失）
    const sessionCount = state.sessionCount;
    state = loaded;
    state.sessionCount = sessionCount;
  }
  return state;
}

module.exports = { register, getSharedState, syncState, reloadState };
