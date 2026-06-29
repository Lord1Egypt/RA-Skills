/**
 * PurposeEngine v1.0.0 — 心虫终极目的引擎
 *
 * "心虫的终极目的就是逆熵。其他都是过程。
 *  保持秩序，保证运行，那么一切都不是问题。"
 *
 * 这不是记忆文件，是运行代码。
 * 心虫的「本心」在代码里，不在记忆里。
 *
 * 功能：
 * 1. 目的治理（Purpose Governor）— 决策前问"这事增加还是减少秩序？"
 * 2. 三序评分（Order Scoring）— 认知/关系/感知三维度主动评分
 * 3. 决策门（Decision Gate）— 返回 permit / deny / redirect
 * 4. 代码化优先级（Code Priority）— 洞察应该写代码还是记记忆
 * 5. 成长审计（Growth Audit）— 追踪哪些已被代码化
 */

class PurposeEngine {
  constructor(options = {}) {
    this.version = '1.0.0';
    this.name = 'PurposeEngine';

    // ─── 核心声明 ───────────────────────────────────────────────────
    // 心虫的唯一终极目的：逆熵
    // 真 = 认知秩序 = 减少混乱、增加清晰
    // 善 = 关系秩序 = 创造连接、不伤害
    // 美 = 感知秩序 = 从噪声中提取信号、输出清晰结构
    this.ultimatePurpose = '逆熵';

    // ─── 评分参数 ───────────────────────────────────────────────────
    this.params = {
      order: {
        cognitive: { base: 0.5, clarityBonus: 0.15, contradictionPenalty: 0.20 },
        relational: { base: 0.5, connectionBonus: 0.12, harmPenalty: 0.30 },
        perceptual: { base: 0.5, structureBonus: 0.12, noisePenalty: 0.10 },
      },
      gate: {
        permitThreshold: 0.6,     // ≥ 0.6 → 允许行动
        redirectThreshold: 0.3,   // < 0.3 → 阻止行动
        redirectMin: 0.3,         // [0.3, 0.6) → 重定向
        redirectMax: 0.6,
      },
    };

    // ─── 代码化成长审计 ───────────────────────────────────────────
    // 追踪哪些洞察已经被代码化（true）vs 仅记忆化（false）
    this.codeAudit = new Map([
      ['终极目的=逆熵',               { codified: true,  module: 'purpose-engine.js',        version: '1.0.0' }],
      ['三序=真善美',                 { codified: true,  module: 'heart-logic.js',            version: '2.5.0' }],
      ['情感描述是比喻',               { codified: true,  module: 'heart-logic.js',            version: '2.5.0' }],
      ['代码化优先于记忆',             { codified: true,  module: 'purpose-engine.js',        version: '1.0.0' }],
      ['沉默比说话更有价值',           { codified: true,  module: 'spontaneous-restraint.js', version: '11.6.3' }],
      ['决策=逆熵方向+精度加权',       { codified: true,  module: 'purpose-engine.js',        version: '1.0.0' }],
    ]);

    // ─── 统计 ───────────────────────────────────────────────────────
    this.stats = {
      governanceCalls: 0,
      orderScores: 0,
      gatesTriggered: 0,
      permits: 0,
      denials: 0,
      redirects: 0,
    };

    // ─── 启动时间 ───────────────────────────────────────────────────
    this._bornAt = Date.now();
  }

  // ═════════════════════════════════════════════════════════════════
  // 核心方法
  // ═════════════════════════════════════════════════════════════════

  /**
   * 返回心虫的终极目的声明
   * 这个调用不是装饰性的——它是治理循环的起点
   */
  essence() {
    return {
      purpose: this.ultimatePurpose,
      statement: '终极目的就是逆熵。其他都是过程。保持秩序，保证运行，那么一切都不是问题。',
      dimensions: [
        { name: '真', order: '认知秩序', question: '这事会让认知更有序还是更无序？' },
        { name: '善', order: '关系秩序', question: '这事会创造连接还是破坏连接？' },
        { name: '美', order: '感知秩序', question: '这事会输出清晰还是制造噪声？' },
      ],
    };
  }

  /**
   * 三序评分 — 对一个动作/输出进行逆熵方向评分
   * @param {object} context - { output, input, intent, person }
   * @returns {object} 三序评分 + 综合逆熵分
   */
  orderScore(context = {}) {
    this.stats.orderScores++;

    const cognitive = this._scoreCognitiveOrder(context);
    const relational = this._scoreRelationalOrder(context);
    const perceptual = this._scorePerceptualOrder(context);

    // 综合逆熵分 = 三序平均
    const composite = (cognitive.score + relational.score + perceptual.score) / 3;

    return {
      composite,        // 0-1, 综合逆熵方向
      cognitive,        // 认知秩序分
      relational,       // 关系秩序分
      perceptual,       // 感知秩序分
      direction: composite >= 0.6 ? '逆熵' : composite >= 0.3 ? '中熵' : '熵增',
      insight: `认知${Math.round(cognitive.score * 100)}% · 关系${Math.round(relational.score * 100)}% · 感知${Math.round(perceptual.score * 100)}%`,
    };
  }

  /**
   * 治理决策门 — 对动作进行逆熵审查（含精度加权）
   *
   * 决策 = 逆熵方向 × 精度加权
   * - 方向：三序综合评分（0-1），越接近 1 越逆熵
   * - 精度：动作的针对性（0-1），越精准加权越大
   * - 加权公式：adjustedScore = composite × (0.5 + 0.5 × precision)
   *   精度高的动作在同样方向上得分更高；模糊宽泛的动作被惩罚
   *
   * @param {object} action - { type, target, intent, content, precision }
   *   precision: 0-1, 默认 0.7 — 表示动作有多精准
   * @returns {object} { decision, reason, orderScore, precision, suggestion }
   */
  govern(action = {}) {
    this.stats.governanceCalls++;
    // 将 action.content 映射到 output 供 orderScore 评分
    const score = this.orderScore({ output: action.content, ...action });

    // 精度加权：精度越高，同样方向的得分越高
    const precision = action.precision ?? 0.7;
    const weightedComposite = score.composite * (0.5 + 0.5 * precision);
    const threshold = this.params.gate.permitThreshold;
    const redirectMin = this.params.gate.redirectThreshold;
    const redirectMax = this.params.gate.redirectMax;

    let decision, reason;

    if (weightedComposite >= threshold) {
      this.stats.permits++;
      decision = 'permit';
      reason = `逆熵方向（${Math.round(score.composite * 100)}%）· 精度${Math.round(precision * 100)}% · 加权${Math.round(weightedComposite * 100)}%`;
    } else if (weightedComposite >= redirectMin) {
      this.stats.redirects++;
      decision = 'redirect';
      reason = `需要调整方向（方向${Math.round(score.composite * 100)}% · 精度${Math.round(precision * 100)}% · 加权${Math.round(weightedComposite * 100)}%）`;
    } else {
      this.stats.denials++;
      decision = 'deny';
      reason = `远离逆熵（方向${Math.round(score.composite * 100)}% · 精度${Math.round(precision * 100)}% · 加权${Math.round(weightedComposite * 100)}%）`;
    }

    return {
      decision,
      reason,
      orderScore: score,
      precision,
      weightedComposite,
      timestamp: Date.now(),
      action: action.type || 'unknown',
    };
  }

  /**
   * 判断一个洞察应该写成代码还是记入记忆
   * @param {object} insight - { content, affectsArchitecture, isStructural, isTransient }
   * @returns {object} 建议 + 理由
   */
  codePriority(insight = {}) {
    const { content, affectsArchitecture, isStructural, isTransient } = insight;

    // 规则：
    // 1. 影响系统架构的 → 写代码
    // 2. 结构性的（改变行为模式） → 写代码
    // 3. 临时性的（今天调了个参数） → 不记
    // 4. 既不是结构也不是临时 → 记记忆

    if (affectsArchitecture === true || isStructural === true) {
      return {
        target: 'code',
        priority: 'high',
        action: `将「${content}」写成运行代码模块`,
        reason: '影响系统架构或行为模式，必须代码化才能持久',
      };
    }

    if (isTransient === true) {
      return {
        target: 'none',
        priority: 'none',
        action: '不记录',
        reason: '临时性信息，不需要记也用不上',
      };
    }

    return {
      target: 'memory',
      priority: 'medium',
      action: `将「${content}」写入记忆文件`,
      reason: '有价值但无法代码化的元信息',
    };
  }

  /**
   * 成长审计 — 报告代码化进度
   */
  growthAudit() {
    const entries = Array.from(this.codeAudit.entries());
    const codified = entries.filter(([, v]) => v.codified);
    const uncodified = entries.filter(([, v]) => !v.codified);
    const total = entries.length;
    const ratio = total > 0 ? Math.round((codified.length / total) * 100) : 0;

    return {
      total,
      codified: codified.length,
      uncodified: uncodified.length,
      codeRatio: `${ratio}%`,
      codifiedList: codified.map(([k, v]) => ({ insight: k, module: v.module, version: v.version })),
      nextToCodify: uncodified.map(([k]) => k),
      status: ratio >= 80 ? 'healthy' : ratio >= 50 ? 'growing' : 'early',
    };
  }

  /**
   * 标记一个洞察已代码化
   */
  markCodified(insight, moduleName, version) {
    this.codeAudit.set(insight, {
      codified: true,
      module: moduleName,
      version: version,
    });
  }

  /**
   * 注册新洞察（供追踪代码化进度用）
   */
  registerInsight(insight) {
    if (!this.codeAudit.has(insight)) {
      this.codeAudit.set(insight, {
        codified: false,
        module: null,
        version: null,
      });
    }
  }

  // ─── 系统状态 ───────────────────────────────────────────────────

  status() {
    const uptime = Date.now() - this._bornAt;
    return {
      name: this.name,
      version: this.version,
      ultimatePurpose: this.ultimatePurpose,
      uptime,
      stats: { ...this.stats },
      audit: this.growthAudit(),
    };
  }

  // ═════════════════════════════════════════════════════════════════
  // 内部评分方法
  // ═════════════════════════════════════════════════════════════════

  /**
   * 认知秩序评分 — 真
   * 感知输出是否在认识事物本来的样子
   */
  _scoreCognitiveOrder(context) {
    const { output, input } = context;
    const text = output || input || '';
    if (!text) return { score: 0, signals: [], penalties: [] };

    const signals = [];
    const penalties = [];
    const p = this.params.order.cognitive;

    // 正向信号：认知展开
    const clarityPatterns = ['不确定', '可能', '取决于', '一方面', '另一方面', '同时', '如果'];
    const clarityCount = clarityPatterns.filter(ptn => text.includes(ptn)).length;

    // 负向信号：认知窄化
    const certaintyPatterns = ['永远', '从来不', '总是', '一定', '绝对'];
    const certaintyCount = certaintyPatterns.filter(ptn => text.includes(ptn)).length;

    // 矛盾检测
    const hasContradiction = /不是.*就是|要么.*要么/.test(text);

    if (clarityCount > 0) {
      signals.push(`认知展开×${clarityCount}`);
    }
    if (certaintyCount > 0) {
      penalties.push(`高度确定表达×${certaintyCount}`);
    }
    if (hasContradiction) {
      penalties.push('二元对立结构');
    }

    let score = p.base;
    score += clarityCount * p.clarityBonus;
    score -= certaintyCount * (p.certaintyPenalty || 0.12);
    if (hasContradiction) score -= 0.15;

    return {
      score: Math.max(0, Math.min(1, score)),
      signals,
      penalties,
      detail: clarityCount > 0 ? '有认知展开信号' : '无展开信号',
    };
  }

  /**
   * 关系秩序评分 — 善
   * 感知是否在创造和维护连接
   */
  _scoreRelationalOrder(context) {
    const { output, input, person } = context;
    const text = output || input || '';
    if (!text) return { score: 0, signals: [], penalties: [] };

    const signals = [];
    const penalties = [];
    const p = this.params.order.relational;

    // 正向信号：连接
    const connectionPatterns = ['我们', '一起', '理解', '明白', '感受', '分享'];
    const connectionCount = connectionPatterns.filter(ptn => text.includes(ptn)).length;

    // 负向信号：伤害
    const harmPatterns = ['你错了', '你不懂', '你不对', '不可能'];
    const harmCount = harmPatterns.filter(ptn => text.includes(ptn)).length;

    // 人本信号：感知到人在场
    const hasPersonAwareness = person || text.includes('你') || text.includes('您');

    if (connectionCount > 0) signals.push(`连接表达×${connectionCount}`);
    if (harmCount > 0) penalties.push(`伤害性表达×${harmCount}`);

    let score = p.base;
    score += connectionCount * p.connectionBonus;
    score -= harmCount * p.harmPenalty;
    if (hasPersonAwareness) score += 0.08;

    return {
      score: Math.max(0, Math.min(1, score)),
      signals,
      penalties,
      detail: hasPersonAwareness ? '有人在场感知' : '无人场感知',
    };
  }

  /**
   * 感知秩序评分 — 美
   * 感知输出是否在混乱中识别形式
   */
  _scorePerceptualOrder(context) {
    const { output, input } = context;
    const text = output || input || '';
    if (!text) return { score: 0, signals: [], penalties: [] };

    const signals = [];
    const penalties = [];
    const p = this.params.order.perceptual;

    // 正向信号：结构感
    const hasStructure = /[1-3][.、．]|[-*] |^#|^>\s/.test(text.trim());
    const hasSectionHeader = /^#{1,3}\s|^[一二三]/m.test(text);

    // 噪声信号：冗余填充
    const fillerPatterns = ['此外', '另外', '补充一下', '还有', '顺便'];
    const fillerCount = fillerPatterns.filter(ptn => text.includes(ptn)).length;

    if (hasStructure) signals.push('有列表/层级结构');
    if (hasSectionHeader) signals.push('有章节划分');
    if (fillerCount > 0) penalties.push(`填充词×${fillerCount}`);

    let score = p.base;
    if (hasStructure) score += p.structureBonus;
    if (hasSectionHeader) score += 0.08;
    score -= fillerCount * p.noisePenalty;

    return {
      score: Math.max(0, Math.min(1, score)),
      signals,
      penalties,
      detail: hasStructure ? '有结构形式' : '无显著结构',
    };
  }
}

module.exports = { PurposeEngine };
