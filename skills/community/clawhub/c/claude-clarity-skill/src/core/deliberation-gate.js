/**
 * DeliberationGate v1.0.0 — 思考门模块
 *
 * 在心虫思维链 PARSE 阶段之后插入，评估问题复杂度并决定是否进入深度思考。
 *
 * 三维评估：
 *   1. 复杂度（Complexity）     — 关键词覆盖面、问题模糊度、多问题检测
 *   2. 上下文完整性（Context）  — 信息是否充足，是否缺关键上下文
 *   3. 不确定性（Uncertainty）  — 问题本身是否模糊、主观、涉及预测
 *
 * 输出：
 *   needsPause: boolean        — 是否建议暂停思考
 *   reason: string             — 暂停/继续的原因
 *   estimatedComplexity: 1-4   — 估计复杂度（对应 REASONING_DEPTH）
 *   recommendedDepth: 1-4      — 推荐思考深度
 *
 * 集成到思维链：
 *   PARSE → DELIBERATE → HYPOTHESES | fastExit
 *
 * 设计原则：
 * - quickAssess: <0.5ms 纯模式匹配，零依赖
 * - deepAssess: 结合 PARSE 阶段的结构化输出做更准确评估
 * - 自动记录评估历史，支持查询统计
 */

// ═════════════════════════════════════════════════════════════════════════
// 常量
// ═════════════════════════════════════════════════════════════════════════

const REASONING_DEPTH = {
  SURFACE: 1,       // 表面：快速响应
  BASIC: 2,         // 基础：有限思考
  DEEP: 3,          // 深度：全流程思考
  COMPREHENSIVE: 4, // 综合：多路径深度推理
};

// 复杂度关键词模式
const COMPLEXITY_MARKERS = {
  high: [
    /为什么|原因|原理|机制|本质/m,
    /比较|对比|区别|优劣|权衡/m,
    /如果|假设|假如|假想/m,
    /预测|未来|趋势|走向/m,
    /设计|架构|方案|规划/m,
    /伦理|道德|价值观/m,
    /分析|评估|评价|批判/m,
    /系统|框架|体系/m,
  ],
  medium: [
    /如何|怎么|怎样/m,
    /解释|说明|描述/m,
    /建议|推荐|选择/m,
    /问题|bug|错误|异常/m,
    /优化|改进|提升/m,
    /证明|论证|推导/m,
  ],
  low: [
    /是什么|定义|概念/m,
    /多少|数字|数量/m,
    /对错|对不对|是否/m,
    /确认|验证|检查/m,
    /有没有|在不在/m,
  ],
};

// 模糊度指标
const AMBIGUITY_INDICATORS = [
  /大概|可能|也许|或许/m,
  /或者|还是|或是/m,
  /一般|通常|有时候/m,
  /根据情况|看情况/m,
  /某种程度|某种意义上/m,
];

// 上下文不完整指标
const INCOMPLETE_INDICATORS = [
  /如果.*就/m,
  /假设.*会/m,
  /缺少|没有.*信息/m,
  /不知道|不清楚/m,
  /给我[^。]*?$/,          // 以"给我…"结尾，缺少前置上下文
];

// 任务类型到推荐深度的映射
const TYPE_DEPTH_MAP = {
  judgment: REASONING_DEPTH.COMPREHENSIVE,
  explanation: REASONING_DEPTH.DEEP,
  creative: REASONING_DEPTH.DEEP,
  calculation: REASONING_DEPTH.BASIC,
  retrieval: REASONING_DEPTH.SURFACE,
  general: REASONING_DEPTH.BASIC,
};

// ═════════════════════════════════════════════════════════════════════════
// DeliberationGate 类
// ═════════════════════════════════════════════════════════════════════════

class DeliberationGate {
  constructor() {
    /** @type {Array<{timestamp: number, result: object}>} */
    this.assessmentHistory = [];
  }

  /**
   * 快速评估入口（<0.5ms）
   * 基于纯文本特征的模式匹配，不做深度分析
   *
   * @param {string} input — 用户输入
   * @returns {{
   *   needsPause: boolean,
   *   reason: string,
   *   estimatedComplexity: number,
   *   recommendedDepth: number,
   *   detail?: object
   * }}
   */
  quickAssess(input) {
    if (!input || typeof input !== 'string' || input.trim().length === 0) {
      const result = {
        needsPause: false,
        reason: '空输入，无需思考',
        estimatedComplexity: REASONING_DEPTH.SURFACE,
        recommendedDepth: REASONING_DEPTH.SURFACE,
        detail: null,
      };
      this._record(result);
      return result;
    }

    const complexity = this._assessComplexity(input);
    const contextCompleteness = this._assessContextCompleteness(input);
    const uncertainty = this._assessUncertainty(input);

    const result = this._synthesize(complexity, contextCompleteness, uncertainty);
    this._record(result);
    return result;
  }

  /**
   * 深度评估（结合 PARSE 阶段的结构化输出）
   * 用 PARSE 结果的变量数、约束条件、任务类型校准 quickAssess
   *
   * @param {string} input — 用户输入
   * @param {object} [parseResult] — PARSE 阶段的输出
   * @param {object} [parseResult.variables]
   * @param {object} [parseResult.constraints]
   * @param {string} [parseResult.type]
   * @returns {object}
   */
  deepAssess(input, parseResult = {}) {
    const quick = this.quickAssess(input);

    if (!parseResult || Object.keys(parseResult).length === 0) {
      return quick;
    }

    const { variables = {}, constraints = [], type } = parseResult;

    // 变量数量加权
    const totalVars = (variables.numbers?.length || 0) + (variables.entities?.length || 0);
    if (totalVars > 5) {
      quick.estimatedComplexity = Math.max(quick.estimatedComplexity, REASONING_DEPTH.COMPREHENSIVE);
    } else if (totalVars > 3) {
      quick.estimatedComplexity = Math.max(quick.estimatedComplexity, REASONING_DEPTH.DEEP);
    }

    // 约束条件加权
    if (Array.isArray(constraints) && constraints.length > 2) {
      quick.estimatedComplexity = Math.max(quick.estimatedComplexity, REASONING_DEPTH.DEEP);
    }

    // 任务类型校准（覆盖低模式匹配高）
    if (type && TYPE_DEPTH_MAP[type]) {
      quick.estimatedComplexity = Math.max(quick.estimatedComplexity, TYPE_DEPTH_MAP[type]);
    }

    // 重新合成
    quick.recommendedDepth = this._clampDepth(quick.estimatedComplexity);
    quick.needsPause = quick.estimatedComplexity >= REASONING_DEPTH.DEEP;
    if (quick.needsPause) {
      const typeLabel = type || '未知';
      quick.reason = `复杂度高（${quick.estimatedComplexity}级/${typeLabel}），建议暂停深度思考`;
    }
    if (quick.detail) {
      quick.detail.typeOverride = type || null;
      quick.detail.variableCount = totalVars;
    }

    return quick;
  }

  /**
   * 是否可以快速退出（跳过 HYPOTHESES/INVERT 等深度阶段）
   * 复杂度 <= BASIC 且不确定性低 且 上下文完整
   *
   * @param {object} assessResult — quickAssess 或 deepAssess 的输出
   * @returns {{ canFastExit: boolean, reason: string }}
   */
  canFastExit(assessResult) {
    if (!assessResult) {
      return { canFastExit: false, reason: '无评估结果' };
    }
    if (assessResult.estimatedComplexity <= REASONING_DEPTH.BASIC) {
      const detail = assessResult.detail;
      if (detail && detail.uncertainty && detail.uncertainty.score < 0.3) {
        return {
          canFastExit: true,
          reason: `简单问题（复杂度${assessResult.estimatedComplexity}），不确定性低，快速响应`,
        };
      }
      return {
        canFastExit: false,
        reason: `复杂度低但存在不确定性（${detail?.uncertainty?.score?.toFixed(2) || '未知'}）`,
      };
    }
    return {
      canFastExit: false,
      reason: `复杂度 ${assessResult.estimatedComplexity}，需要深度思考`,
    };
  }

  // ─── 内部评估方法 ─────────────────────────────────────────────────────

  /**
   * 复杂度评估
   */
  _assessComplexity(input) {
    let score = 0;
    const matches = [];

    for (const pattern of COMPLEXITY_MARKERS.high) {
      if (pattern.test(input)) {
        score += 2;
        matches.push({ pattern: 'high', match: pattern.source });
      }
    }
    for (const pattern of COMPLEXITY_MARKERS.medium) {
      if (pattern.test(input)) {
        score += 1;
        matches.push({ pattern: 'medium', match: pattern.source });
      }
    }
    for (const pattern of COMPLEXITY_MARKERS.low) {
      if (pattern.test(input)) {
        score -= 0.5;
      }
    }

    // 模糊度加成
    for (const pattern of AMBIGUITY_INDICATORS) {
      if (pattern.test(input)) {
        score += 1;
      }
    }

    // 长度因子（长文本通常更复杂）
    if (input.length > 200) score += 1;
    if (input.length > 500) score += 1.5;

    // 多问题检测
    const questionCount = (input.match(/[？?]/g) || []).length;
    if (questionCount >= 3) score += 1;
    if (questionCount >= 6) score += 1.5;

    // 多句子复杂度
    const sentenceCount = (input.match(/[。.!！\n]/g) || []).length;
    if (sentenceCount >= 5) score += 1;

    return {
      score: Math.max(0, score),
      matches,
      questionCount,
      sentenceCount,
      level: score <= 1 ? 'simple' : score <= 3 ? 'moderate' : score <= 6 ? 'complex' : 'very_complex',
    };
  }

  /**
   * 上下文完整性评估
   */
  _assessContextCompleteness(input) {
    let incompleteness = 0;
    const reasons = [];

    for (const pattern of INCOMPLETE_INDICATORS) {
      if (pattern.test(input)) {
        incompleteness += 1;
        reasons.push(`触发不完整模式: ${pattern.source}`);
      }
    }

    // 缺少具体信息（短文本且无数字）
    if (input.length < 100 && !/\d+/.test(input)) {
      incompleteness += 1;
      reasons.push('文本短且缺少具体数据');
    }

    // 条件语句数量
    const conditionalCount = (input.match(/如果|当|假如|要是/gi) || []).length;
    incompleteness += conditionalCount * 0.5;

    const score = Math.min(1, incompleteness / 5);
    return {
      score,
      complete: score < 0.3,
      incomplete: score >= 0.3,
      reasons: reasons.slice(0, 3),
    };
  }

  /**
   * 不确定性评估
   */
  _assessUncertainty(input) {
    let uncertainty = 0;
    const reasons = [];

    for (const pattern of AMBIGUITY_INDICATORS) {
      if (pattern.test(input)) {
        uncertainty += 0.5;
        reasons.push(`模糊表述: ${pattern.source}`);
      }
    }

    // 主观问题
    if (/你觉得|你认为|你感觉|你觉得呢|你的看法/.test(input)) {
      uncertainty += 1;
      reasons.push('主观问题');
    }

    // 未来预测
    if (/将来|未来|以后|会怎样|会变成/.test(input)) {
      uncertainty += 1;
      reasons.push('涉及未来预测');
    }

    // 开放性问题
    if (/怎么样|怎么看|如何看|什么看法|有何见解/.test(input)) {
      uncertainty += 1;
      reasons.push('开放性问题');
    }

    const score = Math.min(1, uncertainty / 4);
    return {
      score,
      certain: score < 0.3,
      uncertain: score >= 0.3,
      reasons: reasons.slice(0, 3),
    };
  }

  /**
   * 合成三维评估结果
   */
  _synthesize(complexity, contextCompleteness, uncertainty) {
    // 加权合成：复杂度50% + 上下文完整性25% + 不确定性25%
    const compositeScore = (
      (complexity.score / 10) * 0.5 +
      (contextCompleteness.score) * 0.25 +
      (uncertainty.score) * 0.25
    );

    const estimatedComplexity = this._compositeToDepth(compositeScore);
    const recommendedDepth = estimatedComplexity;

    const reasons = [];
    if (complexity.level === 'complex' || complexity.level === 'very_complex') {
      reasons.push(`问题复杂度高（${complexity.level}）`);
    }
    if (!contextCompleteness.complete) {
      reasons.push('上下文不够完整');
    }
    if (!uncertainty.certain) {
      reasons.push('问题存在不确定性');
    }

    const needsPause = estimatedComplexity >= REASONING_DEPTH.DEEP;

    return {
      needsPause,
      reason: needsPause
        ? reasons.join('；') || `综合复杂度 ${estimatedComplexity} 级，建议暂停思考`
        : `问题简单（${complexity.level}），无需暂停，快速响应`,
      estimatedComplexity,
      recommendedDepth,
      detail: {
        complexity,
        contextCompleteness,
        uncertainty,
        compositeScore: compositeScore.toFixed(3),
      },
    };
  }

  /**
   * 合成分数 → 思考深度
   */
  _compositeToDepth(score) {
    if (score <= 0.2) return REASONING_DEPTH.SURFACE;
    if (score <= 0.4) return REASONING_DEPTH.BASIC;
    if (score <= 0.65) return REASONING_DEPTH.DEEP;
    return REASONING_DEPTH.COMPREHENSIVE;
  }

  /**
   * 深度值裁剪到有效范围
   */
  _clampDepth(d) {
    return Math.max(REASONING_DEPTH.SURFACE, Math.min(REASONING_DEPTH.COMPREHENSIVE, d));
  }

  /**
   * 记录评估结果到历史
   */
  _record(result) {
    this.assessmentHistory.push({
      timestamp: Date.now(),
      result: {
        needsPause: result.needsPause,
        estimatedComplexity: result.estimatedComplexity,
        recommendedDepth: result.recommendedDepth,
        reason: result.reason,
      },
    });
    // 只保留最近 200 条
    if (this.assessmentHistory.length > 200) {
      this.assessmentHistory = this.assessmentHistory.slice(-200);
    }
  }

  // ─── 查询 ────────────────────────────────────────────────────────────

  getHistory(limit = 50) {
    return this.assessmentHistory.slice(-limit);
  }

  getStats() {
    const total = this.assessmentHistory.length;
    if (total === 0) {
      return { totalAssessments: 0, pauseRate: 0, avgComplexity: 0 };
    }
    const paused = this.assessmentHistory.filter(a => a.result.needsPause).length;
    const avgComplexity = this.assessmentHistory.reduce(
      (s, a) => s + a.result.estimatedComplexity, 0
    ) / total;
    return {
      totalAssessments: total,
      pauseRate: Math.round((paused / total) * 100),
      avgComplexity: avgComplexity.toFixed(2),
    };
  }
}

module.exports = { DeliberationGate, REASONING_DEPTH };