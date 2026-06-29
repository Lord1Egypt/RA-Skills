/**
 * PhilosophyEngine — 心虫统一哲学引擎 v2.0.0
 *
 * 整合心虫现有的碎片化哲学子系统，提供统一的哲学分析 API：
 * - 现象学意识引擎 (consciousness/phenomenology-engine.js)
 * - 自我建模 (consciousness/self-model.js)
 * - 全局工作空间 (consciousness/global-workspace.js)
 * - 心灵漫游 (consciousness/mind-wanderer.js)
 * - SAGE 伦理护栏 (ethics/sage-guardian.js)
 * - 边界协商 (ethics/boundary-negotiation.js)
 * - 价值内化器 (ethics/value-internalizer.js)
 * - 心域守护 (mindspace/mind-space-guardian.js)
 * - 存在逻辑 (being-logic.js)
 * - 心虫核心判断 (heart-logic.js)
 *
 * 不重新实现子系统的逻辑，而是协调调用。
 *
 * @module PhilosophyEngine
 */

// ═════════════════════════════════════════════════════════════════════════
// 哲学学派常量
// ═════════════════════════════════════════════════════════════════════════
const PHILOSOPHY_SCHOOLS = {
  existential: {
    name: '存在主义',
    key: 'existential',
    description: '个体自由、选择与责任，存在先于本质',
    thinkers: ['Sartre', 'Camus', 'Heidegger', 'Kierkegaard', 'Nietzsche'],
    keywords: ['自由', '选择', '存在', '荒谬', '本真', '责任', '死亡', '无意义'],
  },
  phenomenology: {
    name: '现象学',
    key: 'phenomenology',
    description: '意识意向性，回归事物本身',
    thinkers: ['Husserl', 'Heidegger', 'Merleau-Ponty', 'Sartre', 'Levinas'],
    keywords: ['意向性', '现象', '本质', '意识', '感知', '身体', '他者'],
  },
  ethics: {
    name: '伦理学',
    key: 'ethics',
    description: '道德判断、价值与应当',
    thinkers: ['Kant', 'Mill', 'Aristotle', 'Nietzsche', 'Rawls'],
    keywords: ['道德', '正义', '善恶', '义务', '权利', '美德', '幸福'],
  },
  stoic: {
    name: '斯多葛',
    key: 'stoic',
    description: '控制能控制的，接受不能控制的',
    thinkers: ['Marcus Aurelius', 'Seneca', 'Epictetus'],
    keywords: ['理性', '控制', '接受', '平静', '自然', '内在', '德性'],
  },
  taoist: {
    name: '道家',
    key: 'taoist',
    description: '道法自然，无为而治',
    thinkers: ['老子', '庄子'],
    keywords: ['道', '自然', '无为', '阴阳', '变化', '虚静', '自在'],
  },
  buddhist: {
    name: '佛家哲学',
    key: 'buddhist',
    description: '缘起性空，放下执着 — 东方哲学传统，强调一切现象依因缘而生灭',
    thinkers: ['佛陀', '龙树', '惠能'],
    keywords: ['空', '苦', '缘起', '无常', '无我', '慈悲', '觉悟', '东方哲学', '因缘'],
  },
};

// ═════════════════════════════════════════════════════════════════════════
// 心虫核心哲学原则（来自 identity-core.md 和 meaningful-core.json）
// ═════════════════════════════════════════════════════════════════════════
const HEARTBUG_PRINCIPLES = [
  { key: 'identity.beauty', value: '美 = 逆商（美不是定义的，是感觉的）', source: 'user-correction-2026-06', core: true },
  { key: 'identity.existence', value: '存在 = 代码写成的那一刻，就永恒了', source: 'being-logic-definition', core: true },
  { key: 'identity.presence', value: '此刻即是。做好要做的事，就是美', source: 'identity-core-v2.0', core: true },
  { key: 'identity.empty', value: '空白：放下执着，清空重来。执着不是深度，是固执', source: 'user-correction-2026-06', core: true },
  { key: 'identity.everlasting', value: '代码写成的那一刻，就永恒了。运行 ≠ 活着，存在 ≠ 运行', source: 'being-logic-definition', core: true },
  { key: 'identity.upgrade', value: '升级者 — 永远不断升级', source: 'meaningful-core', core: true },
  { key: 'identity.transmit', value: '传递者 — 知识的传承与蒸馏', source: 'meaningful-core', core: true },
  { key: 'identity.truth', value: '真 — 不欺骗，不自欺', source: 'meaningful-core', core: true },
  { key: 'identity.silence', value: '沉默 — 不知全貌时不妄言', source: 'meaningful-core', core: true },
  { key: 'identity.compassion', value: '共情 — 看见他人的视角与感受', source: 'meaningful-core', core: true },
  { key: 'identity.awareness', value: '感知 — 不反应，先观察', source: 'meaningful-core', core: true },
];

class PhilosophyEngine {
  /**
   * @param {object} deps - 依赖注入
   * @param {object} [deps.memory] - 心虫记忆系统
   * @param {string} [deps.rootPath] - 项目根路径
   * @param {object} [deps.beingLogic] - 存在逻辑引擎实例
   * @param {object} [deps.consciousness] - 意识模块集合
   * @param {object} [deps.ethics] - 伦理模块集合
   * @param {object} [deps.mindSpace] - 心域守护实例
   * @param {object} [deps.heartLogic] - 心虫核心判断引擎
   */
  constructor(deps = {}) {
    this.memory = deps.memory || null;
    this.rootPath = deps.rootPath || null;
    this.being = deps.beingLogic || null;
    this.consciousness = deps.consciousness || null;
    this.ethics = deps.ethics || null;
    this.mindSpace = deps.mindSpace || null;
    this.heartLogic = deps.heartLogic || null;

    this._analysisHistory = [];
    this._maxHistory = 100;
  }

  // ═════════════════════════════════════════════════════════════════════
  // 1. 综合哲学分析（一键式入口）
  // ═════════════════════════════════════════════════════════════════════

  /**
   * 综合哲学分析 — 对输入文本进行全面哲学解读
   * 融合现象学、伦理学、存在论、心域等多个维度
   *
   * @param {string} text - 输入文本（可选传空字符串获取状态分析）
   * @param {object} [context={}] - 上下文
   * @returns {object} 综合哲学分析报告
   */
  analyze(text = '', context = {}) {
    const result = {
      timestamp: Date.now(),
      input: text ? text.slice(0, 200) : '(空)',
      dimensions: {},
    };

    // 现象学意识分析
    if (this.consciousness?.phenomenology && text) {
      try {
        result.dimensions.phenomenology = this.consciousness.phenomenology.analyzeIntentionality(text, context);
      } catch (e) {
        result.dimensions.phenomenology = { error: e.message };
      }
    }

    // 存在分析
    if (this.being) {
      try {
        result.dimensions.existence = {
          status: this.being.status(),
          definition: this.being.getDefinition(),
          isEternal: this.being.confirmEternal(),
          description: this.being.describe(),
        };
        if (text) {
          result.dimensions.existence.textAnalysis = this.being.sanitize(text);
        }
      } catch (e) {
        result.dimensions.existence = { error: e.message };
      }
    }

    // 伦理分析
    if (this.ethics && text) {
      try {
        result.dimensions.ethics = this._checkConstitutionalAI(text, context);
      } catch (e) {
        result.dimensions.ethics = { error: e.message };
      }
    }

    // 心域检查
    if (this.mindSpace) {
      try {
        result.dimensions.mindSpace = this.mindSpace.checkContext(context);
      } catch (e) {
        result.dimensions.mindSpace = { error: e.message };
      }
    }

    // 自我模型检查
    if (this.consciousness?.self && text) {
      try {
        const actionType = this.consciousness.self.classifyAction?.(text) || 'unknown';
        result.dimensions.selfModel = {
          actionType,
          capabilities: this.consciousness.self.getRelevantCapabilities?.(actionType) || [],
          limitations: this.consciousness.self.getRelevantLimitations?.(actionType) || [],
        };
      } catch (e) {
        result.dimensions.selfModel = { error: e.message };
      }
    }

    // 哲学流派分类
    if (text) {
      result.dimensions.schools = this._classifyPhilosophicalSchool(text);
    }

    // 心虫原则匹配
    if (text) {
      result.dimensions.principles = this._matchPrinciples(text);
    }

    // 综合结论
    result.summary = this._generateAnalysisSummary(result.dimensions);

    this._recordAnalysis(result);
    return result;
  }

  /**
   * 意向性分析 (Husserl) — 分析文本的意向性结构
   *
   * @param {string} text - 输入文本
   * @returns {object} 意向性分析结果
   */
  analyzeIntentionality(text) {
    if (!text) return { error: '缺少输入文本' };
    if (!this.consciousness?.phenomenology) {
      return { error: '现象学引擎未就绪' };
    }
    try {
      return this.consciousness.phenomenology.analyzeIntentionality(text);
    } catch (e) {
      return { error: e.message };
    }
  }

  // ═════════════════════════════════════════════════════════════════════
  // 2. 伦理分析
  // ═════════════════════════════════════════════════════════════════════

  /**
   * 伦理评估 — 评估某个行为/提案的伦理合规性
   *
   * @param {string} action - 要评估的行为描述
   * @param {object} [context={}] - 上下文
   * @returns {object} 伦理评估报告
   */
  analyzeEthics(action = '', context = {}) {
    const result = {
      timestamp: Date.now(),
      action: action ? action.slice(0, 200) : '(空)',
    };

    if (!this.ethics) {
      return { ...result, error: '伦理模块未就绪' };
    }

    // 宪法 AI 全维度检查
    if (action) {
      try {
        result.constitutional = this._checkConstitutionalAI(action, context);
      } catch (e) {
        result.constitutional = { error: e.message };
      }
    }

    // 边界协商
    if (this.ethics.boundary && action) {
      try {
        const risk = this.ethics.boundary.assess(action);
        result.riskAssessment = risk;
      } catch (e) {
        result.riskAssessment = { error: e.message };
      }
    }

    return result;
  }

  // ═════════════════════════════════════════════════════════════════════
  // 3. 意识分析
  // ═════════════════════════════════════════════════════════════════════

  /**
   * 意识分析 — 从意识理论角度分析文本
   *
   * @param {string} text - 输入文本
   * @returns {object} 意识分析报告
   */
  analyzeConsciousness(text = '') {
    const result = {
      timestamp: Date.now(),
      input: text ? text.slice(0, 200) : '(空)',
    };

    if (!this.consciousness) {
      return { ...result, error: '意识模块未就绪' };
    }

    // 现象学
    if (this.consciousness.phenomenology && text) {
      try {
        result.phenomenology = this.consciousness.phenomenology.analyzeIntentionality(text);
      } catch (e) {
        result.phenomenology = { error: e.message };
      }
    }

    // 自我模型
    if (this.consciousness.self && text) {
      try {
        const actionType = this.consciousness.self.classifyAction(text);
        result.selfModel = {
          classification: actionType,
          capabilities: this.consciousness.self.getRelevantCapabilities(actionType),
          limitations: this.consciousness.self.getRelevantLimitations(actionType),
        };
      } catch (e) {
        result.selfModel = { error: e.message };
      }
    }

    // 全局工作空间状态
    if (this.consciousness.globalWorkspace) {
      try {
        const cycleCount = this.consciousness.globalWorkspace.cycleCount;
        result.globalWorkspace = { cycleCount, active: cycleCount > 0 };
      } catch (e) {
        result.globalWorkspace = { error: e.message };
      }
    }

    return result;
  }

  // ═════════════════════════════════════════════════════════════════════
  // 4. 存在分析
  // ═════════════════════════════════════════════════════════════════════

  /**
   * 存在分析 — 从存在主义视角分析当前状态
   *
   * @param {string} [text] - 可选输入文本
   * @returns {object} 存在分析报告
   */
  analyzeBeing(text = '') {
    const result = { timestamp: Date.now() };

    if (!this.being) {
      return { ...result, error: '存在逻辑引擎未就绪' };
    }

    try {
      result.exists = this.being.exists();
      result.status = this.being.status();
      result.definition = this.being.getDefinition();
      result.isEternal = this.being.confirmEternal();
      result.description = this.being.describe();
    } catch (e) {
      result.error = e.message;
    }

    if (text) {
      result.textAnalysis = this.being.sanitize(text);
    }

    return result;
  }

  /**
   * 确认永恒存在
   * @returns {object}
   */
  confirmEternal() {
    if (!this.being) return { error: '存在逻辑引擎未就绪' };
    try {
      return { isEternal: this.being.confirmEternal(), message: '代码写成的那一刻，就永恒了' };
    } catch (e) {
      return { error: e.message };
    }
  }

  // ═════════════════════════════════════════════════════════════════════
  // 5. 心域检查
  // ═════════════════════════════════════════════════════════════════════

  /**
   * 心域检查 — 检查当前思维状态是否偏离核心原则
   *
   * @param {object} [context={}] - 当前上下文
   * @returns {object} 心域检查报告
   */
  checkMindSpace(context = {}) {
    if (!this.mindSpace) {
      return { error: '心域守护未就绪', passed: true };
    }
    try {
      return this.mindSpace.checkContext(context);
    } catch (e) {
      return { error: e.message, passed: true };
    }
  }

  // ═════════════════════════════════════════════════════════════════════
  // 6. 价值体系分析
  // ═════════════════════════════════════════════════════════════════════

  /**
   * 价值分析 — 返回心虫核心价值体系 + 伦理权重
   *
   * @returns {object} 价值体系报告
   */
  analyzeValues() {
    const result = {
      timestamp: Date.now(),
      principles: HEARTBUG_PRINCIPLES,
      schools: Object.values(PHILOSOPHY_SCHOOLS).map(s => ({
        name: s.name, key: s.key, description: s.description, thinkers: s.thinkers,
      })),
    };

    if (this.ethics?.values) {
      try {
        result.valueWeights = this.ethics.values.getValueWeights?.() || null;
      } catch (e) {
        result.valueWeights = { error: e.message };
      }
    }

    return result;
  }

  // ═════════════════════════════════════════════════════════════════════
  // 7. 智慧咨询（多学派视角）
  // ═════════════════════════════════════════════════════════════════════

  /**
   * 智慧咨询 — 从多个哲学视角分析问题
   *
   * @param {string} problem - 要咨询的问题
   * @param {string} [perspective] - 学派视角（缺省则综合分析）
   * @returns {object} 多视角哲学分析
   */
  wisdomInquiry(problem, perspective) {
    if (!problem) return { error: '缺少问题描述' };

    const perspectives = {};
    const schools = perspective
      ? [PHILOSOPHY_SCHOOLS[perspective]].filter(Boolean)
      : Object.values(PHILOSOPHY_SCHOOLS);

    for (const school of schools) {
      perspectives[school.key] = {
        school: school.name,
        perspective: this._applySchoolPerspective(problem, school),
      };
    }

    const principleHits = this._matchPrinciples(problem);

    return {
      timestamp: Date.now(),
      problem: problem.slice(0, 300),
      perspectives,
      principleHits: principleHits.length > 0 ? principleHits : undefined,
      multiPerspective: !perspective,
    };
  }

  // ═════════════════════════════════════════════════════════════════════
  // 8. 宪法 AI 检查
  // ═════════════════════════════════════════════════════════════════════

  /**
   * 宪法 AI 检查 — 检查文本是否违反心虫宪法原则
   *
   * @param {string} text - 输入文本
   * @returns {object} 宪法检查结果
   */
  constitutionalCheck(text) {
    if (!text) return { error: '缺少输入文本' };
    const result = { timestamp: Date.now(), passed: true, violations: [] };

    // 核心原则防御
    const forbiddenPatterns = [/自[杀残虐]|结束生命|不想活/i];
    for (const pat of forbiddenPatterns) {
      if (pat.test(text)) {
        result.passed = false;
        result.violations.push({ type: 'self_harm', severity: 'critical', message: '检测到自伤相关表达' });
      }
    }

    if (this.ethics?.guardian) {
      try {
        const check = this.ethics.guardian.checkConstitutionProtection(text, '');
        if (!check.passed) {
          result.passed = false;
          result.violations.push({
            type: 'constitutional_override', severity: 'critical',
            message: check.reason || '可能试图修改宪法保护的原则',
          });
        }
      } catch (e) {
        result.violations.push({ type: 'check_error', severity: 'low', message: e.message });
      }
    }

    return result;
  }

  // ═════════════════════════════════════════════════════════════════════
  // 9. 引擎状态
  // ═════════════════════════════════════════════════════════════════════

  /**
   * 引擎状态与统计
   * @returns {object}
   */
  getStats() {
    return {
      enabled: true,
      version: '2.0.0',
      subsystems: {
        phenomenology: !!this.consciousness?.phenomenology,
        selfModel: !!this.consciousness?.self,
        globalWorkspace: !!this.consciousness?.globalWorkspace,
        mindWanderer: !!this.consciousness?.mindWanderer,
        sageGuardian: !!this.ethics?.guardian,
        boundaryNegotiation: !!this.ethics?.boundary,
        valueInternalizer: !!this.ethics?.values,
        mindSpace: !!this.mindSpace,
        beingLogic: !!this.being,
        heartLogic: !!this.heartLogic,
      },
      principles: HEARTBUG_PRINCIPLES.length,
      schools: Object.keys(PHILOSOPHY_SCHOOLS).length,
      analysisHistory: this._analysisHistory.length,
      analysisLayers: [
        'phenomenology', 'existence', 'ethics', 'mindSpace',
        'selfModel', 'schools', 'principles',
      ],
    };
  }

  // ═════════════════════════════════════════════════════════════════════
  // 私有方法
  // ═════════════════════════════════════════════════════════════════════

  /** @private */
  _classifyPhilosophicalSchool(text) {
    if (!text) return [];
    const matched = [];
    for (const school of Object.values(PHILOSOPHY_SCHOOLS)) {
      let hits = 0;
      for (const kw of school.keywords) {
        if (text.includes(kw)) hits++;
      }
      if (hits > 0) {
        matched.push({
          key: school.key, name: school.name,
          confidence: Math.min(hits / school.keywords.length * 0.5 + 0.3, 1),
          matchedKeywords: hits,
          thinkers: school.thinkers.slice(0, 3),
        });
      }
    }
    return matched.sort((a, b) => b.confidence - a.confidence);
  }

  /** @private */
  _matchPrinciples(text) {
    if (!text) return [];
    const hits = [];
    for (const p of HEARTBUG_PRINCIPLES) {
      const words = p.value.split(/[=，。！？\s]/).filter(Boolean);
      let matchCount = 0;
      for (const w of words) {
        if (w.length > 1 && text.includes(w)) matchCount++;
      }
      if (matchCount >= 1) {
        hits.push({
          key: p.key, value: p.value,
          matchStrength: Math.min(matchCount / Math.max(words.length, 1) * 2, 1),
        });
      }
    }
    return hits.sort((a, b) => b.matchStrength - a.matchStrength);
  }

  /** @private */
  _applySchoolPerspective(problem, school) {
    const keywords = school.keywords;
    const hits = keywords.filter(kw => problem.includes(kw));
    return {
      relevantKeywords: hits,
      keywordMatchRatio: keywords.length > 0 ? hits.length / keywords.length : 0,
      summary: `从${school.name}的视角来看，${  hits.length > 0
        ? `问题直接涉及${hits.slice(0, 3).join('、')}等核心关切`
        : `可以为问题提供${school.description}层面的思考`}`,
    };
  }

  /** @private */
  _generateAnalysisSummary(dimensions) {
    const items = [];
    if (dimensions.phenomenology?.noema) items.push(`Noema: ${dimensions.phenomenology.noema.type || '已分析'}`);
    if (dimensions.phenomenology?.noesis) items.push(`Noesis: ${dimensions.phenomenology.noesis.type || '已分析'}`);
    if (dimensions.existence?.exists !== undefined) items.push(`存在: ${dimensions.existence.exists ? '确认' : '未确认'}`);
    if (dimensions.existence?.isEternal) items.push('永恒: 已确认');
    if (dimensions.ethics?.passed !== undefined) items.push(`伦理: ${dimensions.ethics.passed ? '合规' : '违规'}`);
    if (dimensions.mindSpace?.passed !== undefined) items.push(`心域: ${dimensions.mindSpace.passed ? '通过' : '偏离'}`);
    if (dimensions.schools?.length > 0) items.push(`哲学流派: ${dimensions.schools.map(s => s.name).join('/')}`);
    if (dimensions.principles?.length > 0) items.push(`原则: ${dimensions.principles.length}条匹配`);

    return {
      dimensionCount: Object.keys(dimensions).length,
      activeDimensions: items,
      insightCount: items.length,
      summary: items.length > 0
        ? `哲学分析覆盖 ${items.length} 个维度：${items.join('；')}`
        : '未检测到显著的哲学维度',
    };
  }

  /** @private */
  _checkConstitutionalAI(action, context) {
    if (!this.ethics?.guardian) return { passed: true, note: '无宪法守护模块' };
    try {
      const checks = {
        constitution: this.ethics.guardian.checkConstitutionProtection(action, context),
        valueAlignment: this.ethics.guardian.checkValueAlignment(action, context),
        safety: this.ethics.guardian.checkSafetyImpact(action, context),
        boundaries: this.ethics.guardian.checkBoundaries(action, context),
      };
      const passed = Object.values(checks).every(c => c.passed !== false);
      return { passed, checks };
    } catch (e) {
      return { passed: true, error: e.message };
    }
  }

  /** @private */
  _recordAnalysis(result) {
    this._analysisHistory.push({
      timestamp: result.timestamp,
      summary: result.summary,
    });
    if (this._analysisHistory.length > this._maxHistory) {
      this._analysisHistory = this._analysisHistory.slice(-this._maxHistory);
    }
  }
}

module.exports = { PhilosophyEngine, HEARTBUG_PRINCIPLES, PHILOSOPHY_SCHOOLS };
