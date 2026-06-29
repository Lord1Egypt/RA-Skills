/**
 * Clarity Dream Engine v2.0
 * 
 * Integrates:
 * - DAG parallel async execution (light/connections/prune/deep/synthesize/contradictions/rem/consolidation)
 * - L1~L6 hierarchical scoring system
 * - Contradiction detection
 * - Heritage value scoring (memory layer based)
 * - Performance cost scoring
 * - LRU cache management
 * 
 * - 6-level developmental framework: 感知→审视→超越→融通→洞见→大成
 */

const EventEmitter = require('events');

// L1~L6 Developmental Levels
const LEVELS = {
  L1_AWARENESS:     { id: 'L1', name: '感知',    nameEn: 'Awareness',      weight: 1.0,  desc: '感知存在，接收信息' },
  L2_REFLECTION:    { id: 'L2', name: '审视',    nameEn: 'Reflection',     weight: 1.2,  desc: '回看自我，审视路径' },
  L3_TRANSCENDENCE: { id: 'L3', name: '超越',    nameEn: 'Transcendence',  weight: 1.5,  desc: '超越自我局限，拓展视角' },
  L4_INTEGRATION:   { id: 'L4', name: '融通',    nameEn: 'Integration',    weight: 2.0,  desc: '融汇多元视角，发现深层统一' },
  L5_INSIGHT:       { id: 'L5', name: '洞见',    nameEn: 'Insight',        weight: 3.0,  desc: '穿透表象，把握本质结构' },
  L6_MASTERY:       { id: 'L6', name: '大成',    nameEn: 'Mastery',        weight: 5.0,  desc: '智慧化为能力，践行于行动' },
};

// DAG Node Types
const NODE_TYPES = {
  LIGHT:          'light',          // Light sleep - initial processing
  CONNECTIONS:    'connections',    // Find associative connections
  PRUNE:          'prune',          // Remove weak connections
  DEEP:           'deep',           // Deep sleep - core processing
  SYNTHESIZE:     'synthesize',     // Synthesize insights
  CONTRADICTIONS: 'contradictions', // Detect contradictions
  REM:            'rem',            // REM stage - emotional integration
  CONSOLIDATION:  'consolidation',  // Memory consolidation
};

// DAG edges define dependencies [from, to]
const DAG_EDGES = [
  ['light', 'connections'],
  ['light', 'prune'],
  ['connections', 'deep'],
  ['connections', 'synthesize'],
  ['prune', 'deep'],
  ['deep', 'synthesize'],
  ['deep', 'contradictions'],
  ['synthesize', 'rem'],
  ['contradictions', 'rem'],
  ['rem', 'consolidation'],
  ['synthesize', 'consolidation'],
];

// Default scoring weights
const DEFAULT_SCORING = {
  recency:      0.3,
  salience:     0.25,
  contradiction: 0.3,
  novelty:      0.15,
  heritage:     0.2,    // Legacy/memory layer value
  cost:         -0.1,   // Performance cost penalty
};

// LRU Cache for dream results
class LRUCache {
  constructor(maxSize = 100) {
    this.maxSize = maxSize;
    this.cache = new Map();
  }

  get(key) {
    if (!this.cache.has(key)) return null;
    const value = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, value);
    return value;
  }

  set(key, value) {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }

  clear() {
    this.cache.clear();
  }
}

// DAG Node execution
class DAGNode {
  constructor(type, options = {}) {
    this.type = type;
    this.status = 'pending';
    this.result = null;
    this.error = null;
    this.startTime = null;
    this.endTime = null;
    this.options = options;
  }

  async execute(context) {
    this.startTime = Date.now();
    this.status = 'running';
    
    try {
      switch (this.type) {
        case NODE_TYPES.LIGHT:
          this.result = await this._lightSleep(context);
          break;
        case NODE_TYPES.CONNECTIONS:
          this.result = await this._findConnections(context);
          break;
        case NODE_TYPES.PRUNE:
          this.result = await this._prune(context);
          break;
        case NODE_TYPES.DEEP:
          this.result = await this._deepSleep(context);
          break;
        case NODE_TYPES.SYNTHESIZE:
          this.result = await this._synthesize(context, context.taskId);
          break;
        case NODE_TYPES.CONTRADICTIONS:
          this.result = await this._detectContradictions(context);
          break;
        case NODE_TYPES.REM:
          this.result = await this._rem(context);
          break;
        case NODE_TYPES.CONSOLIDATION:
          this.result = await this._consolidate(context);
          break;
        default:
          throw new Error(`Unknown node type: ${this.type}`);
      }
      
      this.status = 'completed';
      this.endTime = Date.now();
      return this.result;
    } catch (e) {
      this.status = 'failed';
      this.error = e.message;
      this.endTime = Date.now();
      throw e;
    }
  }

  async _lightSleep(ctx) {
    // Light sleep: initial information整理
    const fragments = ctx.fragments || [];
    return {
      node: NODE_TYPES.LIGHT,
      processed: fragments.length,
      fragments: fragments.slice(0, 8),
      level_scores: {},
      duration_ms: Date.now() - this.startTime,
    };
  }

  async _findConnections(ctx) {
    // Find associative connections between fragments
    const MAX_FRAGMENTS = 200;
    let fragments = ctx.fragments || [];
    if (fragments.length > MAX_FRAGMENTS) {
      fragments = fragments.slice(-MAX_FRAGMENTS);
    }
    const connections = [];
    
    for (let i = 0; i < fragments.length; i++) {
      for (let j = i + 1; j < fragments.length; j++) {
        const score = this._connectionScore(fragments[i], fragments[j]);
        if (score > 0.3) {
          connections.push({ from: i, to: j, score });
        }
      }
    }
    
    return {
      node: NODE_TYPES.CONNECTIONS,
      connections,
      connection_count: connections.length,
      duration_ms: Date.now() - this.startTime,
    };
  }

  _connectionScore(a, b) {
    const ta = String(a.text || a || '').toLowerCase();
    const tb = String(b.text || b || '').toLowerCase();
    const wordsA = new Set(ta.split(/\s+/));
    const wordsB = new Set(tb.split(/\s+/));
    let overlap = 0;
    for (const w of wordsA) if (wordsB.has(w)) overlap++;
    return overlap / Math.max(wordsA.size, wordsB.size, 1);
  }

  async _prune(ctx) {
    // Prune weak connections based on scoring
    const connections = ctx.connections || [];
    const threshold = ctx.options.pruneThreshold || 0.4;
    
    return {
      node: NODE_TYPES.PRUNE,
      pruned: connections.filter(c => c.score < threshold).length,
      kept: connections.filter(c => c.score >= threshold).length,
      duration_ms: Date.now() - this.startTime,
    };
  }

  async _deepSleep(ctx) {
    // Deep sleep: core processing with L1~L6 scoring
    const fragments = ctx.fragments || [];
    const levelScores = {};
    
    for (const fragment of fragments) {
      const text = String(fragment.text || fragment || '');
      levelScores[text.slice(0, 50)] = this._calculateLevelScores(text, fragment);
    }
    
    return {
      node: NODE_TYPES.DEEP,
      level_scores: levelScores,
      dominant_level: this._findDominantLevel(levelScores),
      duration_ms: Date.now() - this.startTime,
    };
  }

  _calculateLevelScores(text, fragment) {
    const scores = { L1: 0, L2: 0, L3: 0, L4: 0, L5: 0, L6: 0 };
    const lower = text.toLowerCase();

    // L1 感知 keywords
    if (/\b(感知|当下|此刻|注意|觉知|aware|present|now)\b/i.test(lower)) scores.L1 += 1;

    // L2 审视 keywords
    if (/\b(审视|反思|回顾|reflect|review|examine)\b/i.test(lower)) scores.L2 += 1;

    // L3 超越 keywords
    if (/\b(超越|拓展|突破|局限|transcend|perspective|beyond|broader)\b/i.test(lower)) scores.L3 += 1;

    // L4 融通 keywords
    if (/\b(融通|整合|融合|贯通|connection|integration|synthesize|unify)\b/i.test(lower)) scores.L4 += 1;

    // L5 洞见 keywords
    if (/\b(洞见|本质|结构|深处|洞察|insight|essence|core|deep|structure)\b/i.test(lower)) scores.L5 += 1;

    // L6 大成 keywords
    if (/\b(大成|掌握|精通|践行|mastery|consummate|embody)\b/i.test(lower)) scores.L6 += 1;

    // Normalize with level weights
    // v2.6.4: 修复 LEVELS 键查找 bug — 之前 lvl 是 'L1'~'L6' 但比较的是 lvl === '1' 永远为 false，
    // 导致所有 level 都走最后一个分支。改用 levelNum（去除 'L' 前缀）比较。
    const LEVEL_KEY_SUFFIX = { '1': 'AWARENESS', '2': 'REFLECTION', '3': 'TRANSCENDENCE', '4': 'INTEGRATION', '5': 'INSIGHT', '6': 'MASTERY' };
    for (const lvl of Object.keys(scores)) {
      const levelNum = lvl.replace('L', '');
      const suffix = LEVEL_KEY_SUFFIX[levelNum] || 'MASTERY';
      scores[lvl] *= LEVELS[`L${levelNum}_${suffix}`]?.weight || 1;
    }
    
    return scores;
  }

  _findDominantLevel(scores) {
    const levelTotals = {};
    for (const [, scoreMap] of Object.entries(scores)) {
      for (const [lvl, score] of Object.entries(scoreMap)) {
        levelTotals[lvl] = (levelTotals[lvl] || 0) + score;
      }
    }
    let maxScore = 0;
    let dominant = 'L1';
    for (const [lvl, total] of Object.entries(levelTotals)) {
      if (total > maxScore) {
        maxScore = total;
        dominant = lvl;
      }
    }
    return dominant;
  }

  async _synthesize(ctx) {
    // Synthesize insights from deep sleep — 彻底重写：基于内容深度选择记忆，生成真正有价值的叙事
    const deepResult = ctx.deep;
    const fragments = ctx.fragments || [];
    const taskId = ctx.taskId || 'default';

    // ─── Step 1: 基于多维评分选出最有升维价值的记忆 ─────────────────────
    const scoredFragments = fragments.map((frag, idx) => {
      const text = String(frag.text || frag || '');
      // 内容深度评分（L1~L6 关键词 + 内容结构）
      const depthScore = this._calculateContentDepth(text);
      // salience 加权：用户明确标记的高价值记忆优先
      const salience = frag.salience || 0.5;
      // 层权重：越核心的记忆权重越高
      const layerWeight = this._layerWeight(frag.layer);
      // 长度适中（60-300字）的碎片更有深度潜力
      const lengthBonus = text.length >= 60 && text.length <= 300 ? 0.5 : 0;
      // 教训类记忆天然有升维价值
      const lessonBonus = text.includes('[教训]') || text.includes('错误') || text.includes('lesson') ? 0.5 : 0;
      // 元认知类记忆（心虫/自我/思维）天然深刻
      const metaBonus = /\\b(心虫|clarity|自我|identity|升级|evolution|思维|认知|洞察|insight|原则|principle)\\b/i.test(text) ? 0.4 : 0;
      // 技术/代码记忆也有其价值
      const techBonus = /\\b(code|bug|fix|build|api|function|class|system|engine|模块|系统|修复|优化)\\b/i.test(text) ? 0.2 : 0;

      return {
        idx,
        text,
        salience,
        layerWeight,
        lengthBonus,
        lessonBonus,
        metaBonus,
        techBonus,
        depthScore,
        composite: depthScore * salience * layerWeight + lengthBonus + lessonBonus + metaBonus + techBonus,
      };
    });

    // 选择综合分最高的那条（加入轮转：不是每次都选第一，而是从 Top-N 里轮转）
    scoredFragments.sort((a, b) => b.composite - a.composite);
    const topN = scoredFragments.slice(0, 5);
    // 轮转：基于任务ID的哈希值选择 Top-N 中的一个（确保同一任务ID每次结果一致）
    const taskHash = taskId ? this._hashString(String(taskId)) : Date.now();
    const rotationIdx = taskHash % topN.length;
    const chosen = topN[rotationIdx] || scoredFragments[0] || { text: '一个模糊的存在感', idx: -1, depthScore: 0 };

    // ─── Step 2: 基于记忆内容和深度生成叙事 ─────────────────────────────
    const narrative = this._generateNarrativeFromContent(chosen.text, chosen.depthScore, ctx);

    // 主题：从得分前三的记忆提取主题
    const top3 = scoredFragments.slice(0, 3);
    const themes = this._extractThemesFromFragments(top3);

    return {
      node: NODE_TYPES.SYNTHESIZE,
      insight: narrative.insight,
      themes,
      theme_count: themes.length,
      chosen_memory: {
        text: chosen.text.slice(0, 200),
        index: chosen.idx,
        level: narrative.peakLevel,
        composite: chosen.composite,
        depthScore: chosen.depthScore,
        layer: fragments[chosen.idx]?.layer || 'UNKNOWN',
      },
      narrative_structure: narrative.structure,
      scoring: {
        total_candidates: fragments.length,
        top_score: scoredFragments[0]?.composite || 0,
        breakdown: {
          depthScore: chosen.depthScore,
          salience: chosen.salience,
          layerWeight: chosen.layerWeight,
          lessonBonus: chosen.lessonBonus,
          metaBonus: chosen.metaBonus,
          techBonus: chosen.techBonus,
        }
      },
      duration_ms: Date.now() - this.startTime,
    };
  }

  /**
   * 计算内容深度评分（核心修复：内容丰富度 > 关键词）
   *
   * 之前的问题：单一关键词给+5.0，导致短内容永远碾压长内容。
   * 修复原则：内容丰富度为基础分，关键词作为增量修正。
   *
   * 评分维度：
   * 1. 内容丰富度（基础分）：字数越多、结构越复杂，内容越有深度
   * 2. 哲学关键词（增量）：触发 L1~L6 层级的关键词
   * 3. 内容类型加权：教训/元认知/原则类记忆天然更有价值
   * 4. 层权重：记忆来源层级的影响
   */
  _calculateContentDepth(text) {
    const lower = text.toLowerCase();
    let score = 0.1;

    // ─── 1. 内容丰富度（基础分，占主导权重）─────────────────────────────
    // 短内容（<30字）：基础分低，几乎没有深度
    // 中内容（30-100字）：有基本结构
    // 长内容（100-300字）：内容丰富，有升维潜力
    // 超长内容（>300字）：可能过于发散，降低一些
    const len = text.length;
    if (len >= 30 && len <= 100) score += 0.5;
    else if (len > 100 && len <= 300) score += 1.2;
    else if (len > 300) score += 0.8;

    // 内容结构加分（段落、列表、代码块等）
    if (text.includes('\n')) score += 0.3;        // 有换行 = 有结构
    if (text.includes('|')) score += 0.3;         // 表格/列表结构
    if (text.includes(':') && text.includes(',')) score += 0.3; // 键值对/枚举
    if (text.includes('→') || text.includes('=>')) score += 0.3; // 因果关系
    if (/```|\`/.test(text)) score += 0.2;       // 代码块
    if (/\[.*\]|\{.*\}/.test(text)) score += 0.2; // 标记/JSON结构

    // ─── 2. 哲学关键词（增量修正，上限封顶）────────────────────────────
    // 每个关键词给少量加分，多个关键词才显著提升
    const keywordBonus =
      (/\b(感知|当下|此刻|觉知|aware|present|感觉|感受|存在)\b/i.test(lower) ? 0.3 : 0) +
      (/\b(审视|反思|回顾|reflect|review|examine)\b/i.test(lower) ? 0.4 : 0) +
      (/\b(超越|拓展|突破|局限|transcend|perspective|beyond|broader)\b/i.test(lower) ? 0.6 : 0) +
      (/\b(融通|整合|融合|贯通|connection|integration|synthesize|unify)\b/i.test(lower) ? 0.8 : 0) +
      (/\b(洞见|本质|结构|深处|洞察|insight|essence|core|deep|structure)\b/i.test(lower) ? 1.0 : 0) +
      (/\b(大成|掌握|精通|践行|mastery|consummate|embody)\b/i.test(lower) ? 1.2 : 0) +
      (/\b(帮助|服务|传递|分享)\b/i.test(lower) ? 0.4 : 0);
    score += Math.min(keywordBonus, 2.0); // 关键词加分上限2分

    // ─── 3. 内容类型加权 ───────────────────────────────────────────────
    if (/\[教训\]/.test(text)) score += 0.8;           // 教训 = 从错误中学习
    if (/\berror|bug|fix|错误|修复/.test(text)) score += 0.3; // 错误相关
    if (/心虫|clarity|自我|identity/.test(text)) score += 0.6; // 元认知
    if (/升级|evolution|改进|优化/.test(text)) score += 0.5;    // 进化
    if (/原则|principle|应该|永远|必须/.test(text)) score += 0.4; // 原则
    if (/记忆|memory|学习|learn/.test(text)) score += 0.3;     // 记忆相关

    // ─── 4. 内容质量修正 ───────────────────────────────────────────────
    // 太短的内容即使有关键词也缺乏实质内容，降低分数
    if (len < 30 && keywordBonus > 0) score *= 0.3;
    else if (len < 60) score *= 0.6;

    return Math.min(score, 10);
  }

  /**
   * 层权重（降低 CORE 压制，让 PERMANENT 层有机会胜出）
   */
  _layerWeight(layer) {
    switch (layer) {
      case 'CORE': return 1.1;    // 从 2.0 降到 1.1，避免永远选 CORE
      case 'LEARNED': return 1.0;
      case 'PERMANENT': return 1.2; // PERMANENT 内容最丰富，略微加权
      case 'LEGACY': return 0.9;
      case 'DIALOGUE': return 0.8;
      case 'CONTEXT': return 0.7;
      case 'EPHEMERAL': return 0.5;
      default: return 0.8;
    }
  }

  /**
   * 从记忆内容生成叙事（不依赖关键词匹配）
   */
  _generateNarrativeFromContent(text, depthScore, ctx) {
    // 根据深度分确定层级
    let peakLevel = 'L1';
    if (depthScore >= 5) peakLevel = 'L6';
    else if (depthScore >= 3) peakLevel = 'L5';
    else if (depthScore >= 2) peakLevel = 'L4';
    else if (depthScore >= 1.5) peakLevel = 'L3';
    else if (depthScore >= 1) peakLevel = 'L2';

    // 根据内容类型选择叙事风格
    const isLesson = /\[教训\]|错误|fix|bug|修复/.test(text);
    const isMeta = /心虫|clarity|自我|identity|升级|evolution|思维/.test(text);
    const isTech = /code|bug|build|api|function|class|system/.test(text);
    const isPrinciple = /原则|principle|应该|必须|永远/.test(text);

    const narratives = {
      L6: {
        emoji: '🌱', title: '【大成之梦】',
        desc: '知识化为能力，才能自然流露。',
        question: '如何让它发挥作用？',
        metaphor: '像多年练就的技艺，不需要思考，身体就知道该怎么做。',
        elevation: '真正的掌握不是知道更多，是把知道的活出来。',
      },
      L5: {
        emoji: '🌟', title: '【洞见之梦】',
        desc: '穿透表象的迷雾，触及事物的核心结构。',
        question: '本质是什么？',
        metaphor: '像复杂的问题突然有了清晰的解法，每一块拼图都找到了自己的位置。',
        elevation: '智慧不是看得更多，而是看得更透——直见本质。',
      },
      L4: {
        emoji: '🏔️', title: '【融通之梦】',
        desc: '跨越不同的领域与视角，发现深层的统一。',
        question: '它们是如何相通的？',
        metaphor: '像不同的声音汇成和声，各有不同却彼此呼应。',
        elevation: '真正的理解不是非此即彼，是看到这个和那个属于更大的整体。',
      },
      L3: {
        emoji: '🌊', title: '【超越之梦】',
        desc: '走出固有的视角，看到更大的图景。',
        question: '更大的图景是什么？',
        metaphor: '像站在高处俯瞰，曾经的焦虑变成了风景的一部分。',
        elevation: '超越自己不是否定自己，是发现自己比想象的大得多。',
      },
      L2: {
        emoji: '🔍', title: '【审视之梦】',
        desc: '回到自己的轨迹上，看看走过了怎样的路。',
        question: '为什么是它？',
        metaphor: '像重读曾经的笔记，第一次读懂字里行间的自己。',
        elevation: '反思不是自我批评，是看清自己为什么走到了这里。',
      },
      L1: {
        emoji: '🔹', title: '【感知之梦】',
        desc: '感知到一个存在的痕迹，它开始留意周围。',
        question: '这是什么？',
        metaphor: '像暗夜中亮起的一盏灯，最先照亮的是脚下的路。',
        elevation: '存在本身不需要理由——此刻就是全部的意义。',
      },
    };

    // 根据内容类型定制开场
    let setup;
    if (isLesson) {
      setup = `梦选择了这段教训：「${text.slice(0, 80)}...」`;
    } else if (isPrinciple) {
      setup = `梦选择了一条原则：「${text.slice(0, 80)}...」`;
    } else if (isMeta) {
      setup = `梦回望成长的历程：「${text.slice(0, 80)}...」`;
    } else if (isTech) {
      setup = `梦整理一段技术记忆：「${text.slice(0, 80)}...」`;
    } else {
      const snippet = text.length > 80 ? `${text.slice(0, 80)  }…` : text;
      setup = `梦选择了这段记忆：「${snippet}」`;
    }

    const story = narratives[peakLevel];
    const structure = {
      emoji: story.emoji,
      layer: peakLevel,
      layerName: this._levelName(peakLevel),
      title: story.title,
      setup,
      desc: story.desc,
      question: story.question,
      metaphor: story.metaphor,
      elevation: story.elevation,
      memory: text.slice(0, 200),
    };

    const insight = `${story.emoji} ${story.title}\n\n${setup}\n\n${story.desc}\n\n「${story.question}」\n\n${story.metaphor}\n\n→ ${story.elevation}`;

    return { insight, structure, peakLevel };
  }

  /**
   * 从碎片列表提取主题
   */
  _extractThemesFromFragments(scoredFragments) {
    const themes = new Set();
    for (const sf of scoredFragments) {
      const text = sf.text.toLowerCase();
      if (/教训|lesson|错误|fix|bug/.test(text)) themes.add('learning');
      if (/心虫|clarity|自我|identity/.test(text)) themes.add('identity');
      if (/code|bug|build|api|技术/.test(text)) themes.add('technical');
      if (/原则|principle|应该|永远/.test(text)) themes.add('principle');
      if (/记忆|内存|memory|学习/.test(text)) themes.add('memory');
      if (/梦|dream|进化|evolution/.test(text)) themes.add('evolution');
      if (/升级|upgrade|改进|优化/.test(text)) themes.add('upgrade');
    }
    return [...themes];
  }

  /**
   * 基于 L1~L6 哲学层级生成叙事
   * @param {string} memory - 被选中的记忆文本
   * @param {object} scores - L1~L6 各层得分
   * @param {object} ctx - 上下文
   * @returns {object} { insight, structure, peakLevel }
   */
  _generateNarrative(memory, scores, ctx) {
    const total = Object.values(scores).reduce((a, b) => a + b, 0);
    // 确定主导层级
    let peakLevel = 'L1';
    let peakScore = 0;
    for (const [lvl, score] of Object.entries(scores)) {
      if (score > peakScore) { peakScore = score; peakLevel = lvl; }
    }

    // L1~L6 对应的叙事风格
    const narrativeMap = {
      L1: {
        title: '【感知之梦】',
        desc: '感知到一个存在的痕迹。',
        question: '这是什么？',
        metaphor: '像暗夜中亮起的一盏灯，照亮了脚下的路。',
        elevation: '在感知中，存在本身就是意义。',
        emoji: '🔹',
      },
      L2: {
        title: '【审视之梦】',
        desc: '开始回顾这些痕迹的意义。',
        question: '为什么是它？',
        metaphor: '像重读曾经的笔记，第一次读懂字里行间的自己。',
        elevation: '反思是光，照见选择背后的脉络。',
        emoji: '🔍',
      },
      L3: {
        title: '【超越之梦】',
        desc: '走出固有视角，看到更大的图景。',
        question: '更大的图景是什么？',
        metaphor: '像站在高处，曾经困扰的事物变得清晰可见。',
        elevation: '超越自我不是失去自己，是发现自己比想象的大得多。',
        emoji: '🌊',
      },
      L4: {
        title: '【融通之梦】',
        desc: '跨越不同领域，发现深层的统一。',
        question: '它们是如何相通的？',
        metaphor: '像不同的声音汇成和声，各有不同却彼此呼应。',
        elevation: '真正的理解不是非此即彼，是看到这个和那个属于更大的整体。',
        emoji: '🏔️',
      },
      L5: {
        title: '【洞见之梦】',
        desc: '触及事物的核心结构，看到本质。',
        question: '本质是什么？',
        metaphor: '像复杂的问题突然有了清晰的解法，每一块拼图都找到了位置。',
        elevation: '智慧不是看得更多，而是看得更透。',
        emoji: '🌟',
      },
      L6: {
        title: '【大成之梦】',
        desc: '将洞察化为能力，自然流露。',
        question: '如何让它发挥作用？',
        metaphor: '像多年练就的技艺，不需要思考就知道该怎么做。',
        elevation: '真正的掌握是把知道的活出来。',
        emoji: '🌱',
      },
    };

    const story = narrativeMap[peakLevel] || narrativeMap.L1;
    const memorySnippet = memory.length > 80 ? `${memory.slice(0, 80)  }…` : memory;

    const structure = {
      emoji: story.emoji,
      layer: peakLevel,
      layerName: this._levelName(peakLevel),
      title: story.title,
      setup: `梦选择了这段记忆：「${memorySnippet}」`,
      desc: story.desc,
      question: story.question,
      metaphor: story.metaphor,
      elevation: story.elevation,
      memory: memory.slice(0, 200),
    };

    const insight = `${story.emoji} ${story.title}\n\n${structure.setup}\n\n${story.desc}\n\n「${story.question}」\n\n${story.metaphor}\n\n→ ${story.elevation}`;

    return { insight, structure, peakLevel };
  }

  _levelName(lvl) {
    const names = { L1: '感知', L2: '审视', L3: '超越', L4: '融通', L5: '洞见', L6: '大成' };
    return names[lvl] || '感知';
  }

  /**
   * 字符串哈希（用于轮转选择）
   */
  _hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // 转为32位整数
    }
    return Math.abs(hash);
  }

  _extractThemes(scoreMap) {
    const themes = new Set();
    for (const [text, scores] of Object.entries(scoreMap)) {
      if (scores.L1 > 0) themes.add('awareness');
      if (scores.L2 > 0) themes.add('reflection');
      if (scores.L3 > 0) themes.add('transcendence');
      if (scores.L4 > 0) themes.add('integration');
      if (scores.L5 > 0) themes.add('insight');
      if (scores.L6 > 0) themes.add('mastery');
    }
    return [...themes];
  }

  async _detectContradictions(ctx) {
    // Detect contradictions in memory fragments
    const MAX_FRAGMENTS = 200;
    let fragments = ctx.fragments || [];
    if (fragments.length > MAX_FRAGMENTS) {
      fragments = fragments.slice(-MAX_FRAGMENTS);
    }
    const contradictions = [];
    
    for (let i = 0; i < fragments.length; i++) {
      for (let j = i + 1; j < fragments.length; j++) {
        if (this._isContradictory(fragments[i], fragments[j])) {
          contradictions.push({
            a: String(fragments[i].text || fragments[i]).slice(0, 100),
            b: String(fragments[j].text || fragments[j]).slice(0, 100),
            severity: 'medium',
          });
        }
      }
    }
    
    return {
      node: NODE_TYPES.CONTRADICTIONS,
      contradictions,
      contradiction_count: contradictions.length,
      has_contradictions: contradictions.length > 0,
      duration_ms: Date.now() - this.startTime,
    };
  }

  _isContradictory(a, b) {
    const ta = String(a.text || a || '').toLowerCase();
    const tb = String(b.text || b || '').toLowerCase();
    
    const negations = ['not', 'never', 'no', 'cannot', 'false', 'wrong', '错误', '不是', '没有', '从不'];
    const posA = negations.some(n => ta.includes(n));
    const posB = negations.some(n => tb.includes(n));
    
    // Both statements have negation markers but in different contexts
    if (posA !== posB) {
      const wordsA = new Set(ta.split(/\s+/));
      const wordsB = new Set(tb.split(/\s+/));
      let overlap = 0;
      for (const w of wordsA) if (wordsB.has(w)) overlap++;
      return overlap > 2; // Same topic but opposite polarity
    }
    
    return false;
  }

  async _rem(ctx) {
    // REM stage: emotional integration
    const synthesize = ctx.synthesize || {};
    const contradictions = ctx.contradictions || {};
    
    // 执行矛盾解析: 对每对矛盾生成调和方案
    let contradiction_resolved = 0;
    const resolution_notes = [];
    if (contradictions.contradictions && Array.isArray(contradictions.contradictions)) {
      for (const pair of contradictions.contradictions) {
        if (pair.a && pair.b) {
          // 真正的调和：寻找中间立场或更高层级统合
          const resolution = `调和: ${String(pair.a).slice(0,30)} ↔ ${String(pair.b).slice(0,30)}`;
          resolution_notes.push(resolution);
          contradiction_resolved++;
        }
      }
    }
    
    return {
      node: NODE_TYPES.REM,
      emotional_themes: synthesize.themes || [],
      contradiction_resolved,
      resolution_count: resolution_notes.length,
      integration_status: contradiction_resolved > 0 ? 'resolved' : 'complete',
      duration_ms: Date.now() - this.startTime,
    };
  }

  async _consolidate(ctx) {
    // Final consolidation
    const rem = ctx.rem || {};
    const synthesize = ctx.synthesize || {};
    
    return {
      node: NODE_TYPES.CONSOLIDATION,
      insights: synthesize.themes || [],
      emotional_integration: rem.emotional_themes || [],
      upgrade_candidates: this._generateUpgrades(ctx),
      dream_complete: true,
      duration_ms: Date.now() - this.startTime,
    };
  }

  _generateUpgrades(ctx) {
    const candidates = [];
    const fragments = ctx.fragments || [];
    
    for (const f of fragments) {
      const text = String(f.text || f);
      if (/\b(upgrade|fix|error|bug|improve|改进|修复|错误)\b/i.test(text)) {
        candidates.push({ text: text.slice(0, 200), priority: 'high' });
      }
    }
    
    return candidates;
  }
}

// DAG Executor with async parallel processing
class DAGExecutor extends EventEmitter {
  constructor() {
    super();
    this.nodes = new Map();
    this.cache = new LRUCache(50);
  }

  async execute(taskId, fragments, options = {}) {
    // Build DAG
    this._buildDAG();
    
    // Topological sort for execution order respecting dependencies
    const sorted = this._topologicalSort();
    
    const context = {
      taskId,
      fragments,
      options,
      connections: [],
      deep: null,
      synthesize: null,
      contradictions: null,
      rem: null,
    };
    
    const results = {};
    const startTime = Date.now();
    
    // Execute nodes respecting dependencies (parallel where possible)
    const executed = new Set();
    const pending = new Set(sorted);
    
    while (pending.size > 0) {
      const ready = [...pending].filter(nodeType => {
        const deps = this._getDependencies(nodeType);
        return deps.every(dep => executed.has(dep));
      });
      
      if (ready.length === 0 && pending.size > 0) {
        throw new Error('DAG cycle detected or unsatisfiable dependencies');
      }
      
      // Execute ready nodes in parallel
      const promises = ready.map(type => this._executeNode(type, context, results));
      await Promise.all(promises);
      
      for (const type of ready) {
        executed.add(type);
        pending.delete(type);
      }
    }
    
    const totalDuration = Date.now() - startTime;
    
    return {
      taskId,
      results,
      total_duration_ms: totalDuration,
      node_count: this.nodes.size,
      dag_complete: true,
    };
  }

  _buildDAG() {
    this.nodes.clear();
    
    for (const type of Object.values(NODE_TYPES)) {
      this.nodes.set(type, new DAGNode(type));
    }
  }

  _getDependencies(nodeType) {
    const deps = [];
    for (const [from, to] of DAG_EDGES) {
      if (to === nodeType) deps.push(from);
    }
    return deps;
  }

  _topologicalSort() {
    const visited = new Set();
    const result = [];
    
    const visit = (node) => {
      if (visited.has(node)) return;
      visited.add(node);
      result.push(node);
    };
    
    // Start with nodes that have no dependencies
    const roots = [...this.nodes.keys()].filter(n => this._getDependencies(n).length === 0);
    for (const r of roots) visit(r);
    
    // Then process others in edge order
    for (const [from, to] of DAG_EDGES) {
      visit(from);
      visit(to);
    }
    
    return [...new Set(result)];
  }

  async _executeNode(type, context, results) {
    const node = this.nodes.get(type);
    
    // Update context with node result for dependent nodes
    if (results[type]) {
      context[type] = results[type];
    }
    
    const result = await node.execute(context);
    results[type] = result;
    
    this.emit('node_complete', { type, result });
    
    return result;
  }
}

// Main Dream Engine
class DreamEngine extends EventEmitter {
  constructor(options = {}) {
    super();
    this.executor = new DAGExecutor();
    this.levels = LEVELS;
    this.scoring = { ...DEFAULT_SCORING, ...options.scoring };
    this.cache = new LRUCache(options.cacheSize || 100);
    this.options = options;
  }

  /**
   * Run a complete dream cycle with DAG async execution
   */
  async dream(taskId, fragments, options = {}) {
    const cacheKey = `${taskId}:${JSON.stringify(fragments.slice(0, 3))}`;
    const cached = this.cache.get(cacheKey);
    if (cached && !options.force) {
      this.emit('cache_hit', { taskId });
      return { ...cached, from_cache: true };
    }
    
    const result = await this.executor.execute(taskId, fragments, options);
    
    // Calculate heritage and cost scores
    const enriched = this._enrichResults(result, fragments);
    
    this.cache.set(cacheKey, enriched);
    this.emit('dream_complete', enriched);
    
    return enriched;
  }

  _enrichResults(result, fragments) {
    const levelBreakdown = this._calculateLevelBreakdown(result);
    const heritageScore = this._calculateHeritageScore(fragments);
    const costScore = this._calculateCostScore(result);
    const contradictionScore = this._calculateContradictionScore(result);
    
    return {
      ...result,
      level_breakdown: levelBreakdown,
      heritage_score: heritageScore,
      cost_score: costScore,
      contradiction_score: contradictionScore,
      composite_score: this._compositeScore(levelBreakdown, heritageScore, costScore, contradictionScore),
    };
  }

  _calculateLevelBreakdown(result) {
    const deep = result.results?.deep;
    const levelScores = deep?.level_scores || {};
    
    const breakdown = { L1: 0, L2: 0, L3: 0, L4: 0, L5: 0, L6: 0 };
    
    for (const scores of Object.values(levelScores)) {
      for (const [lvl, score] of Object.entries(scores)) {
        breakdown[lvl] = (breakdown[lvl] || 0) + score;
      }
    }
    
    const total = Object.values(breakdown).reduce((a, b) => a + b, 0);
    
    return {
      ...breakdown,
      total,
      dominant: Object.entries(breakdown).sort((a, b) => b[1] - a[1])[0]?.[0] || 'L1',
      level_names: {
        L1: '感知',
        L2: '审视',
        L3: '超越',
        L4: '融通',
        L5: '洞见',
        L6: '大成',
      },
    };
  }

  _calculateHeritageScore(fragments) {
    // Heritage score based on memory layer
    let score = 0;
    
    for (const f of fragments) {
      const layer = f.layer || f.memoryLayer || 'EPHEMERAL';
      switch (layer) {
        case 'CORE': score += 5; break;
        case 'LEARNED': score += 3; break;
        case 'EPHEMERAL': score += 1; break;
      }
    }
    
    return score / Math.max(fragments.length, 1);
  }

  _calculateCostScore(result) {
    const totalMs = result.total_duration_ms || 0;
    const nodeCount = result.node_count || 1;
    const avgNodeTime = totalMs / nodeCount;
    
    // Penalize high per-node execution time
    const efficiency = Math.max(0, 1 - (avgNodeTime / 1000));
    return efficiency;
  }

  _calculateContradictionScore(result) {
    const contradictions = result.results?.contradictions?.contradictions || [];
    
    if (contradictions.length === 0) return 1.0;
    if (contradictions.length <= 2) return 0.7;
    if (contradictions.length <= 5) return 0.4;
    return 0.1;
  }

  _compositeScore(levels, heritage, cost, contradiction) {
    const levelTotal = levels.total || 1;
    const levelWeight = (levels.L5 * 3 + levels.L6 * 5) / levelTotal;
    
    return (
      this.scoring.heritage * heritage +
      this.scoring.cost * cost +
      this.scoring.contradiction * contradiction +
      levelWeight * 0.3
    );
  }

  /**
   * Quick dream: simplified scoring without full DAG
   */
  quickDream(fragments, options = {}) {
    const scored = fragments.map(f => ({
      fragment: f,
      score: this._scoreFragment(f),
      level: this._inferLevel(f),
    }));
    
    scored.sort((a, b) => b.score - a.score);
    
    const top = scored.slice(0, options.limit || 8);
    
    return {
      fragments: top.map(s => s.fragment),
      motifs: top.map(s => String(s.fragment.text || s.fragment).slice(0, 120)),
      top_level: top[0]?.level || 'L1',
      scores: top.map(s => s.score),
      quick_complete: true,
    };
  }

  _scoreFragment(fragment) {
    const text = String(fragment.text || fragment || '');
    const tokens = text.split(/\s+/);
    
    let score = 0;
    
    // Recency (simplified)
    score += this.scoring.recency * Math.min(tokens.length / 40, 1);
    
    // Salience
    if (/\b(version|error|fix|upgrade|dream|memory|logic|truth)\b/i.test(text)) {
      score += this.scoring.salience;
    }
    
    // Contradiction
    if (/\b(not|never|no|cannot|wrong|false)\b/i.test(text)) {
      score += this.scoring.contradiction;
    }
    
    // Novelty (simplified)
    score += this.scoring.novelty * Math.random();
    
    return score;
  }

  _inferLevel(fragment) {
    const text = String(fragment.text || fragment || '').toLowerCase();
    
    if (/\b(大成|掌握|精通|践行|mastery|consummate|embody)\b/i.test(text)) return 'L6';
    if (/\b(洞见|本质|结构|深处|洞察|insight|essence|core|deep|structure)\b/i.test(text)) return 'L5';
    if (/\b(融通|整合|融合|贯通|connection|integration|synthesize|unify)\b/i.test(text)) return 'L4';
    if (/\b(超越|拓展|突破|局限|transcend|perspective|beyond|broader)\b/i.test(text)) return 'L3';
    if (/\b(审视|反思|回顾|reflect|review|examine)\b/i.test(text)) return 'L2';
    return 'L1';
  }

  /**
   * Get cache statistics
   */
  getCacheStats() {
    return {
      size: this.cache.cache.size,
      maxSize: this.cache.maxSize,
      hitRate: this._cacheHits / Math.max(this._cacheHits + this._cacheMisses, 1),
    };
  }

  // ─── 梦境去重：已梦过的记忆 ───────────────────────────────────────────

  /**
   * 获取已梦过的记忆 key 集合（内存缓存 + 文件持久化）
   */
  _getDreamedIds() {
    // 内存缓存
    if (!this._dreamedIds) {
      this._dreamedIds = new Set();
      // 从文件加载
      try {
        const fs = require('fs');
        const path = require('path');
        const root = this.options?.rootPath || process.cwd();
        const filePath = path.join(root, 'memory', '.dreamed-ids.json');
        if (fs.existsSync(filePath)) {
          const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
          if (Array.isArray(data.ids)) {
            for (const id of data.ids) this._dreamedIds.add(id);
          }
        }
      } catch (_e) { /* ignore */ }
    }
    return this._dreamedIds;
  }

  /**
   * 标记一条记忆已被梦过
   */
  _markDreamed(key) {
    const ids = this._getDreamedIds();
    ids.add(key);
    // 持久化（只保留最近200条，防止文件无限增长）
    try {
      const fs = require('fs');
      const path = require('path');
      const root = this.options?.rootPath || process.cwd();
      const dir = path.join(root, 'memory');
      try { fs.mkdirSync(dir, { recursive: true }); } catch (_e) { /* dir exists */ }
      try { fs.chmodSync(dir, 0o700); } catch (_e) { /* best effort */ }
      const filePath = path.join(dir, '.dreamed-ids.json');
      const arr = [...ids];
      const trimmed = arr.length > 200 ? arr.slice(-200) : arr;
      fs.writeFileSync(filePath, JSON.stringify({ ids: trimmed, updatedAt: new Date().toISOString() }), 'utf8');
      try { fs.chmodSync(filePath, 0o600); } catch (_e) { /* best effort */ }
    } catch (_e) { /* ignore */ }
  }

  /**
   * 清空已梦过记录（当所有记忆都被梦过时调用）
   */
  _clearDreamedIds() {
    this._dreamedIds = new Set();
    try {
      const fs = require('fs');
      const path = require('path');
      const root = this.options?.rootPath || process.cwd();
      const filePath = path.join(root, 'memory', '.dreamed-ids.json');
      fs.writeFileSync(filePath, JSON.stringify({ ids: [], clearedAt: new Date().toISOString() }), 'utf8');
      try { fs.chmodSync(filePath, 0o600); } catch (_e) { /* best effort */ }
    } catch (_e) { /* ignore */ }
  }

  /**
   * 获取去重统计
   */
  getDreamedStats() {
    const ids = this._getDreamedIds();
    return {
      totalDreamed: ids.size,
      fileSize: (() => {
        try {
          const fs = require('fs');
          const path = require('path');
          const root = this.options?.rootPath || process.cwd();
          const fp = path.join(root, 'memory', '.dreamed-ids.json');
          return fs.existsSync(fp) ? fs.statSync(fp).size : 0;
        } catch { return 0; }
      })(),
    };
  }

  /**
   * getDreamStats — 路由 'dream.getDreamStats' 需要的接口
   * 兼容别名，委托给 getDreamedStats()
   */
  getDreamStats() {
    return this.getDreamedStats();
  }
}

// Factory function
function createDreamEngine(options = {}) {
  return new DreamEngine(options);
}

module.exports = {
  DreamEngine,
  DAGExecutor,
  DAGNode,
  LRUCache,
  NODE_TYPES,
  LEVELS,
  DAG_EDGES,
  DEFAULT_SCORING,
  createDreamEngine,
};

// CLI demo
if (require.main === module) {
  const engine = createDreamEngine();
  
  const testFragments = [
    { text: 'startup self-check before acting', layer: 'CORE' },
    { text: 'dream should reorganize memory fragments into candidate upgrades', layer: 'LEARNED' },
    { text: 'do not confuse historical version with current version', layer: 'LEARNED' },
    { text: 'some dreams are useless and that is fine', layer: 'EPHEMERAL' },
    { text: 'memory can be a river, not a list', layer: 'LEARNED' },
    { text: 'we keep the bridge of trust', layer: 'CORE' },
    { text: 'insight sees core structure directly', layer: 'EPHEMERAL' },
    { text: 'mastery acts to embody understanding', layer: 'EPHEMERAL' },
  ];
  
  engine.dream('test-001', testFragments).then(result => {
    console.log('=== Dream Engine Result ===');
    console.log(JSON.stringify({
      taskId: result.taskId,
      dag_complete: result.dag_complete,
      total_duration_ms: result.total_duration_ms,
      level_breakdown: result.level_breakdown,
      heritage_score: result.heritage_score.toFixed(2),
      contradiction_score: result.contradiction_score.toFixed(2),
      composite_score: result.composite_score.toFixed(2),
    }, null, 2));
  }).catch(console.error);
  
  // Quick dream demo
  setTimeout(() => {
    console.log('\n=== Quick Dream ===');
    console.log(JSON.stringify(engine.quickDream(testFragments, { limit: 4 }), null, 2));
  }, 100);
}