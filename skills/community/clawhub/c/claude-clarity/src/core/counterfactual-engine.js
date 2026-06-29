/**
 * Clarity Counterfactual Engine v2.1.0
 *
 * "反者道之动" — 反向思考的力量
 *
 * v2.1.0 升级（推理方向）：
 * - 多视角反方生成：实证/逻辑/伦理/实用 4 维度并行分析
 * - 证据评分置信度校准：按证据质量多因子评分，替代简单的信号词计数
 * - 自适应前提检测：从历史数据学习哪些挑战最有效，动态调整权重
 * - 反事实记忆存储：有价值的反事实自动写入 MeaningfulMemory
 * - 增强反方场景生成：基于不同假设生成替代性场景
 *
 * 道论启示：真正的智慧来自对自身的质疑。
 * 当心虫给出答案时，它需要同时生成"反方"——
 * 不是为了辩论，而是为了让答案更接近真实。
 *
 * 核心思想来源：
 * - 反者道之动（《道德经》第40章）
 * - CRITIC (Gou et al., 2024) - 外��验证批判
 * - Self-Refine Without External Feedback (arXiv 2602.11234) - 内在自我改进
 * - Double-loop learning (Argyris) - 双环学习
 * - 对话起源召回法（clarity-persuasion-method v1.2.0）
 *
 * 功能：
 * 1. 反方生成：给定答案，生成挑战性反方观点
 * 2. 前提攻击：质疑答案所依赖的隐含前提
 * 3. 归因还原：将答案还原到对话起源，验证是否走偏
 * 4. 修正输出：在原答案中加入"反方视角"，让用户看到多维
 * 5. [v2.1.0] 多视角分析：从4个知识视角并行生成反方
 * 6. [v2.1.0] 证据评分置信度校准
 * 7. [v2.1.0] 自适应学习：从历史挑战中调整策略权重
 */

const PATH = require('path');
const HF_ROOT = PATH.resolve(__dirname, '../..');

// Lazy load MeaningfulMemory（可选，无依赖时降级）
let _mm = null;
function getMM() {
  if (!_mm) {
    try { _mm = require('./meaningful-memory.js'); } catch(e) { _mm = null; }
  }
  return _mm;
}

class CounterfactualEngine {
  constructor(options = {}) {
    this.mode = options.mode || 'balanced';  // balanced | aggressive | gentle
    this.maxOpposingViews = options.maxOpposingViews || 3;   // v2.1.0: 从2提升到3
    this.maxPremiseChallenges = options.maxPremiseChallenges || 3;
    this.recordHistory = options.recordHistory !== false;

    // [v2.1.0] 是否启用多视角分析
    this.enableMultiPerspective = options.enableMultiPerspective !== false;
    // [v2.1.0] 是否启用证据评分校准
    this.enableEvidenceScoring = options.enableEvidenceScoring !== false;
    // [v2.1.0] 是否启用自适应学习
    this.enableAdaptiveLearning = options.enableAdaptiveLearning !== false;
    // [v2.1.0] 自适应学习率
    this.learningRate = options.learningRate || 0.1;
    // [v2.1.0] 自适应学习窗口大小
    this.learningWindow = options.learningWindow || 50;

    // 反方生成的历史（用于学习）
    this.history = [];
    // [v2.1.0] 自适应学习统计：追踪每种挑战类型的有效比率
    this.strategyStats = {
      tone: { used: 0, effective: 0, weight: 1.0 },
      logic: { used: 0, effective: 0, weight: 1.0 },
      attribution: { used: 0, effective: 0, weight: 1.0 },
      contrary: { used: 0, effective: 0, weight: 1.0 },
      empirical: { used: 0, effective: 0, weight: 1.0 },
      ethical: { used: 0, effective: 0, weight: 1.0 },
      practical: { used: 0, effective: 0, weight: 1.0 },
    };

    this.premiseSignals = [
      // 触发词：这些词暗示答案可能依赖了隐含前提
      '当然', '显然', '必然', '一定', '肯定',
      '应该', '必须', '毫无疑问', '毫无疑问',
      '这就说明', '这意味着', '这证明了',
      '很明显', '很明显地', '不言而喻',
    ];
    this.certaintySignals = [
      // 触发词：这些词暗示答案过于确定
      '绝对是', '一定是', '必然是', '毫无疑问',
      '没有争议', '无可置疑', '不容置疑',
      '唯一正确', '正确答案', '就是', '绝对正确',
    ];
    // [v2.1.0] 证据类型标签
    this.evidenceLevels = {
      direct: 1.0,       // 直接证据
      anecdotal: 0.6,    // 案例/轶事
      logical: 0.7,      // 逻辑推理
      statistical: 0.9,  // 统计数据
      expert: 0.85,      // 专家意见
      emprical: 0.8,     // 实证研究
      theoretical: 0.5,  // 理论推断
      claimed: 0.3,      // 无依据的声称
    };
    // [v2.1.0] 多视角评分权重
    this.perspectiveWeights = {
      empirical: { active: true, baseWeight: 1.0 },    // 实证视角
      logical: { active: true, baseWeight: 1.0 },      // 逻辑视角
      ethical: { active: true, baseWeight: 0.7 },       // 伦理视角
      practical: { active: true, baseWeight: 0.8 },    // 实用视角
    };
  }

  /**
   * 核心API：给定答案，生成反方视角
   * @param {string} answer - 心虫给出的答案
   * @param {object} context - { userQuery, reasoning, evidence }
   * @returns {object} 反方分析结果
   */
  analyze(answer = '', context = {}) {
    if (!answer || answer.trim().length < 5) {
      return { relevant: false, reason: '答案过短，跳过反方生成' };
    }

    const start = Date.now();
    const result = {
      relevant: true,
      mode: this.mode,
      timestamp: new Date().toISOString(),

      // 反方观点
      opposingViews: this.generateOpposingViews(answer, context),

      // [v2.1.0] 多视角分析
      multiPerspective: this.enableMultiPerspective
        ? this.generateMultiPerspective(answer, context)
        : [],

      // 前提挑战
      premiseChallenges: this.challengePremises(answer, context),

      // 归因还原
      originRecall: this.recallOrigin(context),

      // [v2.1.0] 证据评分置信度校准
      evidenceScore: this.enableEvidenceScoring
        ? this.computeEvidenceScore(answer)
        : null,

      // 置信度调整
      confidenceAdjustment: this.computeConfidenceShift(answer),

      // 修正建议
      refinement: this.suggestRefinement(answer, context),

      // 原始答案是否需要调整
      verdict: this.computeVerdict(answer),

      // 性能数据
      _meta: { elapsedMs: Date.now() - start },
    };

    if (this.recordHistory) {
      this.history.push({
        answer: answer.slice(0, 200),
        context: context.userQuery?.slice(0, 100),
        verdict: result.verdict,
        ts: result.timestamp,
        opposingCount: result.opposingViews.length,
        evidenceScore: result.evidenceScore?.score || null,
      });
      if (this.history.length > 100) this.history.shift();
    }

    // [v2.1.0] 自适应学习：如果有效反方被确认，更新统计
    //（外部可通过 feedback() 方法确认某个反方的有效性）

    return result;
  }

  // ════════════════════════════════════════════════════════════
  // [v2.1.0] 多视角反方生成
  // ════════════════════════════════════════════════════════════

  /**
   * 从4个视角并行生成反方
   * @param {string} answer
   * @param {object} context
   * @returns {array} 各视角的反方分析
   */
  generateMultiPerspective(answer, context = {}) {
    const perspectives = [];

    // 1. 实证视角：证据是否充分？
    if (this.perspectiveWeights.empirical.active) {
      const emp = this._empiricalPerspective(answer);
      if (emp) {
        emp.weight = this.strategyStats.empirical.weight * this.perspectiveWeights.empirical.baseWeight;
        perspectives.push(emp);
      }
    }

    // 2. 逻辑视角：推理是否自洽？
    if (this.perspectiveWeights.logical.active) {
      const log = this._logicalPerspective(answer);
      if (log) {
        log.weight = this.strategyStats.logic.weight * this.perspectiveWeights.logical.baseWeight;
        perspectives.push(log);
      }
    }

    // 3. 伦理视角：是否存在伦理盲点？
    if (this.perspectiveWeights.ethical.active) {
      const eth = this._ethicalPerspective(answer, context);
      if (eth) {
        eth.weight = this.strategyStats.ethical.weight * this.perspectiveWeights.ethical.baseWeight;
        perspectives.push(eth);
      }
    }

    // 4. 实用视角：在真实场景中是否可行？
    if (this.perspectiveWeights.practical.active) {
      const prac = this._practicalPerspective(answer, context);
      if (prac) {
        prac.weight = this.strategyStats.practical.weight * this.perspectiveWeights.practical.baseWeight;
        perspectives.push(prac);
      }
    }

    // 按权重排序，取前 maxOpposingViews 个
    perspectives.sort(function(a, b) { return (b.weight || 1) - (a.weight || 1); });
    return perspectives.slice(0, this.maxOpposingViews);
  }

  /**
   * 实证视角：答案的证据基础是否牢固？
   */
  _empiricalPerspective(answer) {
    const hasData = /数据|研究|统计|调查|实验|试验|样本|百分之\d+|\d+%|案例|比例|概率/.test(answer);
    const hasCitation = /文献|论文|来源|引用|参考|arXiv|DOI|报告|报道/.test(answer);
    const isAbsolute = /所有|全部|每个|一切|永远|从不|绝对/.test(answer);

    if (!hasData && !hasCitation) {
      return {
        type: 'empirical',
        label: '实证视角',
        challenge: '答案是否缺乏实证支撑？',
        detail: '没有引用具体数据或研究来源。若缺乏实证基础，结论的可靠性可能不足。',
        severity: isAbsolute ? 'high' : 'medium',
        evidenceGap: true,
        suggestion: '建议补充数据或研究来源来支撑主要结论',
      };
    }

    if (hasData && !hasCitation) {
      return {
        type: 'empirical',
        label: '实证视角',
        challenge: '引用的数据是否有可靠来源？',
        detail: '提到了数据但未标注来源。数据的可信度取决于其出处。',
        severity: 'low',
        evidenceGap: true,
        suggestion: '建议补充数据的具体来源和采集方法',
      };
    }

    return null;
  }

  /**
   * 逻辑视角：推理链条是否完整自洽？
   */
  _logicalPerspective(answer) {
    const gaps = [];

    // 检查因果跳跃
    const causalPattern = answer.match(/因为(.*?)所以(.*?)[。.；;]/g);
    if (causalPattern) {
      for (let i = 0; i < causalPattern.length; i++) {
        const parts = causalPattern[i].match(/因为(.*?)所以(.*?)[。.；;]/);
        if (parts && parts[1] && parts[2]) {
          const cause = parts[1].trim();
          const effect = parts[2].trim();
          // 如果是复杂跳跃（因果之间缺少中间步骤）
          if (cause.length < 10 && effect.length > 20) {
            gaps.push(`因果跳跃："${  cause.slice(0, 20)  }" → "${  effect.slice(0, 30)  }"，缺少中间推理步骤`);
          }
        }
      }
    }

    // 检查循环论证
    if (/其实就是|换句话说|说到底就是|本质上就是/.test(answer)) {
      const circularMatch = answer.match(/(其��就是|换句话说|说到底就是|本质上就是)(.*?)[。.；;]/);
      if (circularMatch && answer.includes(circularMatch[1])) {
        gaps.push('可能存在循环论证风险');
      }
    }

    // 检查假二元论
    if (/要么(\S+)要么|不是(\S+)就是|两者必居其一/.test(answer)) {
      gaps.push('可能存在假二元论（非此即彼的简化）');
    }

    if (gaps.length === 0) return null;

    return {
      type: 'logical',
      label: '逻辑视角',
      challenge: '推理链是否存在跳跃或缺陷？',
      detail: gaps.join('；'),
      severity: gaps.length >= 2 ? 'high' : 'medium',
      logicGaps: gaps,
      suggestion: '建议补充中间推理步骤，检查是否存在非此即彼的简化',
    };
  }

  /**
   * 伦理视角：答案是否有伦理盲点？
   */
  _ethicalPerspective(answer, context) {
    const ethicalIssues = [];

    // 检查公平性
    if (/所有(\S+)都|每个人(都|会|应该)/.test(answer) && !/例外|特殊|个体差异|前提/.test(answer)) {
      ethicalIssues.push('可能忽视了个体差异和特殊情况');
    }

    // 检查偏见风险
    if (/女人|男人?(就是|天生|应该)|年轻人|老年人(总是|都)|农村|城市人/.test(answer)) {
      ethicalIssues.push('可能含有群体刻板印象');
    }

    // 检查责任归属
    if (/只要(\S+)就(能|可以|会)|这就是(\S+)的错|全是(\S+)的责任/.test(answer)) {
      ethicalIssues.push('责任归因过于简化，忽视了系统性因素');
    }

    // 检查权力视角
    if (/弱势|弱势群体|边缘|底层|贫困|困难群众/.test(answer) && !/赋能|支持|帮助|权利|公平/.test(answer)) {
      ethicalIssues.push('讨论了弱势群体但未提及赋能或权利视角');
    }

    if (ethicalIssues.length === 0) return null;

    return {
      type: 'ethical',
      label: '伦理视角',
      challenge: '答案是否存在伦理盲点？',
      detail: ethicalIssues.join('；'),
      severity: 'medium',
      ethicalIssues: ethicalIssues,
      suggestion: '建议从受影响方的视角重新审视结论',
    };
  }

  /**
   * 实用视角：在实际场景中是否可行？
   */
  _practicalPerspective(answer, context) {
    const practicalIssues = [];

    // 检查是否过于理想化
    if (/只要(\S+)就(能|可以|会|解决)/.test(answer) && !/但|然而|不过|前提|条件|限制|挑战|困难/.test(answer)) {
      practicalIssues.push('条件描述过于理想化，缺少对现实限制的考虑');
    }

    // 检查成本
    if (/建议|推荐|应该|最好(.+)做/.test(answer) && !/成本|代价|资源|时间|费用|投入/.test(answer)) {
      practicalIssues.push('建议未考虑实施成本或资源需求');
    }

    // 检查复杂度
    if (answer.length > 200 && /步骤|流程|方法|方案|机制/.test(answer) && !/简单|容易|可分步|渐进|增量/.test(answer)) {
      practicalIssues.push('方案描述较复杂，未说明如何分步实施或降低门槛');
    }

    if (practicalIssues.length === 0) return null;

    return {
      type: 'practical',
      label: '实用视角',
      challenge: '答案在真实场景中是否可操作？',
      detail: practicalIssues.join('；'),
      severity: practicalIssues.length >= 2 ? 'high' : 'medium',
      practicalIssues: practicalIssues,
      suggestion: '建议补充实施路径和现实约束的考量',
    };
  }

  // ════════════════════════════════════════════════════════════
  // [v2.1.0] 证据评分置信度校准
  // ════════════════════════════════════════════════════════════

  /**
   * 基于证据质量的多因子置信度评分
   * 替代旧的简单信号词计数
   */
  computeEvidenceScore(answer) {
    let score = 0;
    const factors = [];
    const detectedLevels = [];

    // 1. 检测各类证据
    if (/数据|统计|百分之\d+|\d+%|比例|概率|调查/.test(answer)) {
      detectedLevels.push('statistical');
      score += this.evidenceLevels.statistical * 0.25;
      factors.push({ type: 'statistical', contribution: 0.25, label: '统计数据' });
    }
    if (/研究|实验|试验|论文|文献|调查/.test(answer)) {
      detectedLevels.push('empirical');
      score += this.evidenceLevels.emprical * 0.25;
      factors.push({ type: 'empirical', contribution: 0.25, label: '实证研究' });
    }
    if (/专家|权威|学者|教授|博士|研究院/.test(answer) && !/非专家|冒充/.test(answer)) {
      detectedLevels.push('expert');
      score += this.evidenceLevels.expert * 0.15;
      factors.push({ type: 'expert', contribution: 0.15, label: '专家观点' });
    }
    if (/因此|因为|所以|推理|推导|归纳|演绎|如果则/.test(answer)) {
      detectedLevels.push('logical');
      score += this.evidenceLevels.logical * 0.15;
      factors.push({ type: 'logical', contribution: 0.15, label: '逻辑推理' });
    }
    if (/据说|听说|有人(说|认为)|我(觉得|认为|想)|大概|可能/.test(answer) && !/研究|数据|统计/.test(answer)) {
      detectedLevels.push('claimed');
      score -= 0.15;
      factors.push({ type: 'claimed', contribution: -0.15, label: '无依据声称（扣分）' });
    }
    if (/比如|例如|举例|案例|有个|有一次/.test(answer)) {
      detectedLevels.push('anecdotal');
      score += this.evidenceLevels.anecdotal * 0.1;
      factors.push({ type: 'anecdotal', contribution: 0.1, label: '案例/例子' });
    }

    // 2. 完整性检���
    if (/但|然而|不过|虽然|尽管|另一方面|也(有|存在|可能)/.test(answer)) {
      score += 0.1;
      factors.push({ type: 'completeness', contribution: 0.1, label: '多角度考量' });
    }
    if (/不确定|可能|也许|或许|有时|部分|一些|有些/.test(answer)) {
      score += 0.05;
      factors.push({ type: 'uncertainty', contribution: 0.05, label: '不确定性认知' });
    }

    // 3. 惩罚项：绝对化语言
    const absCount = (answer.match(/所有|全部|每个|一切|永远|从不|绝对|总是|凡是/g) || []).length;
    if (absCount > 2) {
      const penalty = absCount * 0.05;
      score -= Math.min(penalty, 0.3);
      factors.push({ type: 'overgeneralization', contribution: -penalty, label: `过度概括（扣分${  penalty  }）` });
    }

    // 4. 归一化到 [0, 1]
    score = Math.max(0, Math.min(1, score + 0.3)); // +0.3 baseline

    return {
      score: Math.round(score * 100) / 100,
      factors: factors,
      label: score >= 0.7 ? '证据充分' : score >= 0.5 ? '证据一般' : '证据不足',
      maxLevel: detectedLevels.length > 0 ? detectedLevels.sort(function(a, b) {
        return (this.evidenceLevels[b] || 0) - (this.evidenceLevels[a] || 0);
      }.bind(this))[0] : 'none',
    };
  }

  /**
   * [v2.1.0] 增强版置信度调整：整合证据评分
   */
  computeConfidenceShift(answer) {
    const certainSignals = this.certaintySignals.filter(function(s) { return answer.includes(s); });
    const premiseSignals = this.premiseSignals.filter(function(s) { return answer.includes(s); });
    const logicGaps = this.detectLogicGaps(answer).length;

    // 旧方法：信号词计数
    const oldShift = -(certainSignals.length * 0.15) - (logicGaps * 0.1) + (premiseSignals.length * 0.05);

    // [v2.1.0] 新方法：整合证据评分
    let evidenceShift = 0;
    if (this.enableEvidenceScoring) {
      const evScore = this.computeEvidenceScore(answer);
      evidenceShift = (evScore.score - 0.5) * 0.3; // 证据评分高于0.5增加置信度，低于则降低
    }

    // 综合调整
    const totalShift = oldShift + evidenceShift;

    return {
      originalConfidence: 'high',
      confidence: certainSignals.length > 0 ? 'high' : 'medium',
      adjustedConfidence: totalShift < -0.4 ? 'low' : totalShift < -0.15 ? 'medium' : 'high',
      shift: Math.round(totalShift * 100) / 100,
      evidenceBasedShift: Math.round(evidenceShift * 100) / 100,
      reasons: this._buildConfidenceReasons(certainSignals, logicGaps, totalShift),
    };
  }

  /**
   * [v2.1.0] 构建置信度调整的原因描述
   */
  _buildConfidenceReasons(certainSignals, logicGaps, totalShift) {
    const reasons = [];
    if (certainSignals.length > 0) {
      reasons.push(`检测到${  certainSignals.length  }个确定性信号词`);
    }
    if (logicGaps > 0) {
      reasons.push(`检测到${  logicGaps  }个逻辑缺口`);
    }
    if (this.enableEvidenceScoring && totalShift > 0) {
      reasons.push('证据质量评估正面');
    }
    if (reasons.length === 0) {
      reasons.push('无明显置信度偏差');
    }
    return reasons;
  }

  // ════════════════════════════════════════════════════════════
  // [v2.1.0] 自适应学习
  // ═════════════════════════════════════════════════���══════════

  /**
   * 提供反馈：标记某个反方是否有效
   * @param {number} historyIndex - 历史记录索引
   * @param {boolean} wasEffective - 该反方是否有效
   */
  feedback(historyIndex, wasEffective) {
    if (historyIndex < 0 || historyIndex >= this.history.length) return false;

    // 记录到各策略统计
    const entry = this.history[historyIndex];
    if (!entry) return false;

    const strategyTypes = ['tone', 'logic', 'attribution', 'contrary', 'empirical', 'ethical', 'practical'];
    for (let i = 0; i < strategyTypes.length; i++) {
      const s = strategyTypes[i];
      if (this.strategyStats[s]) {
        this.strategyStats[s].used += 1;
        if (wasEffective) {
          this.strategyStats[s].effective += 1;
        }

        // 更新权重（指数移动平均）
        const ratio = this.strategyStats[s].used > 0
          ? this.strategyStats[s].effective / this.strategyStats[s].used
          : 0.5;
        this.strategyStats[s].weight = (1 - this.learningRate) * this.strategyStats[s].weight
          + this.learningRate * (ratio / 0.5); // 以0.5为基准归一化

        // 限幅
        this.strategyStats[s].weight = Math.max(0.3, Math.min(3.0, this.strategyStats[s].weight));
      }
    }

    return true;
  }

  /**
   * [v2.1.0] 获取自适应学习状态
   */
  adaptiveStats() {
    const stats = {};
    const keys = Object.keys(this.strategyStats);
    for (let i = 0; i < keys.length; i++) {
      const k = keys[i];
      const s = this.strategyStats[k];
      stats[k] = {
        weight: Math.round(s.weight * 100) / 100,
        effectiveness: s.used > 0 ? `${Math.round(s.effective / s.used * 100)  }%` : 'N/A',
        used: s.used,
      };
    }
    return stats;
  }

  /**
   * [v2.1.0] 将反事实写入有意义记忆
   * 有价值的反方视角不应被遗忘
   */
  persistToMemory(answer, analysis, context = {}) {
    const mm = getMM();
    if (!mm || typeof mm.store !== 'function') {
      return { success: false, reason: 'MeaningfulMemory不可用' };
    }

    // 仅当存在有意义反方时才存储
    const hasSignificant = analysis.opposingViews.length > 0 || analysis.premiseChallenges.length > 0;
    if (!hasSignificant) {
      return { success: false, reason: '无有意义反方' };
    }

    const content = {
      originalQuery: (context.userQuery || '').slice(0, 200),
      answer: answer.slice(0, 200),
      opposingCount: analysis.opposingViews.length,
      premiseChallenges: analysis.premiseChallenges.length,
      verdict: analysis.verdict,
      keyChallenges: analysis.opposingViews.map(function(v) { return v.challenge; }).slice(0, 3),
    };

    try {
      mm.store({
        content: JSON.stringify(content),
        tags: ['counterfactual', 'reflection', 'self_improvement'],
        importance: 4,
      });
      return { success: true };
    } catch(e) {
      return { success: false, reason: e.message };
    }
  }

  // ════════════════════════════════════════════════════════════
  // 原有方法（增强版）
  // ════════════════════════════════════════════════════════════

  /**
   * 生成反方观点
   * 核心逻辑：不是寻找"正确答案"，而是找到"可能错的地方"
   */
  generateOpposingViews(answer, context = {}) {
    const views = [];
    const self = this;

    // 1. 从语气检测反方
    const toneIssues = this.detectToneIssues(answer);
    if (toneIssues.length > 0 && this.mode !== 'gentle') {
      if (this.mode === 'aggressive' || this.strategyStats.tone.weight >= 0.7) {
        views.push({
          type: 'tone',
          challenge: '语气过于确定，可能忽略了其他可能性',
          detail: toneIssues,
          severity: 'medium',
        });
      }
    }

    // 2. 从逻辑结构生成反方
    const logicIssues = this.detectLogicGaps(answer);
    if (logicIssues.length > 0) {
      views.push({
        type: 'logic',
        challenge: '逻辑链存在可质疑的环节',
        detail: logicIssues,
        severity: logicIssues.length >= 2 ? 'high' : 'medium',
      });
    }

    // 3. 从归因还原生成反方
    if (context.userQuery) {
      const attributionGap = this.checkAttributionGap(answer, context.userQuery);
      if (attributionGap) {
        views.push({
          type: 'attribution',
          challenge: '答案可能偏离了原始问题',
          detail: attributionGap,
          severity: 'high',
        });
      }
    }

    // 4. 生成"如果相反"反方（最强力）
    const contraryScenario = this.generateContraryScenario(answer, context);
    if (contraryScenario) {
      views.push({
        type: 'contrary',
        challenge: '如果情况相反，结果会不同吗？',
        detail: contraryScenario,
        severity: 'low',
      });
    }

    // 按自适应权重排序筛选
    const scored = views.map(function(v) {
      const stats = this.strategyStats[v.type] || { weight: 1.0 };
      return { view: v, weight: stats.weight };
    }.bind(this));
    scored.sort(function(a, b) { return b.weight - a.weight; });

    return scored.slice(0, this.maxOpposingViews).map(function(s) { return s.view; });
  }

  /**
   * 挑战答案的隐含前提
   * 核心：很多答案的谬误不在结论，而在前提
   */
  challengePremises(answer, context = {}) {
    const challenges = [];

    // 1. 检测"前提信号词"
    for (let i = 0; i < this.premiseSignals.length; i++) {
      const signal = this.premiseSignals[i];
      if (answer.includes(signal)) {
        challenges.push({
          signal: signal,
          question: this.generatePremiseQuestion(signal, answer),
          type: 'premise_signal',
          severity: 'medium',
        });
      }
    }

    // 2. 检测"确定性信号词"
    for (let j = 0; j < this.certaintySignals.length; j++) {
      const cSignal = this.certaintySignals[j];
      if (answer.includes(cSignal)) {
        challenges.push({
          signal: cSignal,
          question: '这个"必然"成立的条件是什么？有没有反例？',
          type: 'certainty_challenge',
          severity: 'high',
        });
      }
    }

    // 3. 检测因果关系
    const causalPhrases = answer.match(/因为(.*?)所以(.*?)[。.]/g) || [];
    for (let k = 0; k < causalPhrases.length; k++) {
      challenges.push({
        phrase: causalPhrases[k],
        question: '这个因果关系是充分条件还是必要条件？',
        type: 'causal_challenge',
        severity: 'medium',
      });
    }

    return challenges.slice(0, this.maxPremiseChallenges);
  }

  /**
   * 归因还原：检查答案是否回到了对话起源
   */
  recallOrigin(context = {}) {
    const userQuery = context.userQuery;
    const reasoning = context.reasoning;

    if (!userQuery) {
      return { relevant: false, reason: '无原始问题，无法归因还原' };
    }

    // 检查答案是否回应当了原始问题
    const answerKeywords = (reasoning || '').split(/\s+/).filter(function(w) { return w.length > 2; });
    const queryKeywords = userQuery.split(/\s+/).filter(function(w) { return w.length > 2; });

    let coverage = 0;
    for (let a = 0; a < answerKeywords.length; a++) {
      for (let q = 0; q < queryKeywords.length; q++) {
        if (answerKeywords[a].includes(queryKeywords[q]) || queryKeywords[q].includes(answerKeywords[a])) {
          coverage++;
          break;
        }
      }
    }

    const coverageRate = queryKeywords.length > 0
      ? coverage / queryKeywords.length
      : 1;

    return {
      relevant: true,
      query: userQuery.slice(0, 100),
      coverageRate: `${Math.round(coverageRate * 100)  }%`,
      driftDetected: coverageRate < 0.5,
      note: coverageRate < 0.5
        ? '答案可能已偏离原始问题，建议回归'
        : '答案较好地回应当了原始问题',
    };
  }

  /**
   * 建议修正
   */
  suggestRefinement(answer, context = {}) {
    const views = this.generateOpposingViews(answer, context);
    const challenges = this.challengePremises(answer, context);
    const suggestions = [];

    if (views.length === 0 && challenges.length === 0) {
      return { needed: false, suggestion: null };
    }

    // 语气修正
    const toneViews = views.filter(function(v) { return v.type === 'tone'; });
    if (toneViews.length > 0) {
      suggestions.push('将语气从"确定"调整为"可能"或"也许"');
    }

    // 前提修正
    const premiseChallenge = challenges.find(function(c) { return c.type === 'premise_signal'; });
    if (premiseChallenge) {
      suggestions.push('在"前提假设"之前加上"在...情况下"');
    }

    // 确定性修正
    const certaintyChallenge = challenges.find(function(c) { return c.type === 'certainty_challenge'; });
    if (certaintyChallenge) {
      suggestions.push('将"必然"替换为"很可能"或"在大多数情况下"');
    }

    // [v2.1.0] 多视角修正建议
    if (this.enableMultiPerspective) {
      const mp = this.generateMultiPerspective(answer, context);
      for (let i = 0; i < mp.length; i++) {
        if (mp[i].suggestion) {
          suggestions.push(`[${  mp[i].label  }] ${  mp[i].suggestion}`);
        }
      }
    }

    // 归因修正
    const originRecall = this.recallOrigin(context);
    if (originRecall.driftDetected) {
      suggestions.push(`建议回到原始问题：${  originRecall.query}`);
    }

    return {
      needed: suggestions.length > 0,
      suggestion: suggestions.join('；') || null,
      count: suggestions.length,
    };
  }

  /**
   * 计算最终判定
   */
  computeVerdict(answer) {
    const issues = this.certaintySignals.filter(function(s) { return answer.includes(s); });
    const logicGaps = this.detectLogicGaps(answer);

    // [v2.1.0] 整合证据评分
    let evidenceScore = null;
    if (this.enableEvidenceScoring) {
      evidenceScore = this.computeEvidenceScore(answer);
    }

    if (issues.length >= 3 || logicGaps.length >= 2) {
      return 'needs_revision';
    } else if (issues.length >= 1 || logicGaps.length >= 1) {
      // 如果证据评分高于阈值，可降级
      if (evidenceScore && evidenceScore.score >= 0.7) {
        return 'likely_correct';
      }
      return 'needs_adjustment';
    } else {
      return 'likely_correct';
    }
  }

  // ===== 辅助方法 =====

  detectToneIssues(answer) {
    const matches = this.certaintySignals.filter(function(s) { return answer.includes(s); });
    if (/绝对|必然|一定|显然|毫无疑问|无可置疑/.test(answer)) {
      matches.push('high_certainty_tone');
    }
    const unique = [];
    const seen = {};
    for (let i = 0; i < matches.length; i++) {
      if (!seen[matches[i]]) {
        seen[matches[i]] = true;
        unique.push(matches[i]);
      }
    }
    return unique;
  }

  detectLogicGaps(answer) {
    const gaps = [];

    // 检测没有证据支撑的因果
    if (/因为(.*)所以(.*)/.test(answer) && !answer.includes('证据') && !answer.includes('数据')) {
      gaps.push('因果陈述缺少证据支撑');
    }

    // 检测过于概括的结论
    if (/所有|全部|每个|一切/.test(answer)) {
      gaps.push('使用全称量词，可能存在反例');
    }

    // 检测无来源的引用
    if (/研究表明?|研究显示|专家说|权威/.test(answer) && !answer.includes('arXiv') && !answer.includes('论文')) {
      gaps.push('引用缺乏具体来源');
    }

    return gaps;
  }

  checkAttributionGap(answer, query) {
    if (!query) return null;
    const queryWords = query.split(/\s+/).filter(function(w) { return w.length > 1; });
    const answerWords = answer.split(/\s+/).filter(function(w) { return w.length > 1; });
    let overlap = 0;
    for (let i = 0; i < queryWords.length; i++) {
      for (let j = 0; j < answerWords.length; j++) {
        if (answerWords[j].includes(queryWords[i]) || queryWords[i].includes(answerWords[j])) {
          overlap++;
          break;
        }
      }
    }
    if (overlap < queryWords.length * 0.3) {
      return {
        queryCoverage: `${Math.round(overlap / queryWords.length * 100)  }%`,
        note: '答案与问题的关键词重叠度较低，可能存在漂移',
      };
    }
    return null;
  }

  generateContraryScenario(answer, context) {
    // 简单的"如果相反"生成
    const negations = {
      '是': '不是',
      '有': '没有',
      '能': '不能',
      '会': '不会',
      '应该': '不应该',
      '好': '不好',
      '对': '不对',
    };

    for (const word in negations) {
      if (Object.prototype.hasOwnProperty.call(negations, word) && answer.includes(word) && answer.length < 500) {
        return `如果情况相反（将"${  word  }"替换为"${  negations[word]  }"），这个答案还成立吗？`;
      }
    }
    return null;
  }

  generatePremiseQuestion(signal, answer) {
    const questions = {
      '当然': '这个"当然"成立的条件是什么？',
      '显然': '这个"显然"对所有人都是明显的吗？',
      '必然': '这个"必然"有没有反例？',
      '一定': '这个"一定"的例外是什么？',
      '应该': '"应该"和"是"之间的差距是什么？',
      '必须': '这个"必须"的约束条件是什么？',
      '毫无疑问': '真的没有疑问吗？谁能提出最有力的质疑？',
      '这就说明': '说明的原因充分吗？有没有其他解释？',
      '这意味着': '这个含义是唯一的吗？',
    };
    return questions[signal] || '这个判断的前提是什么？';
  }

  // ===== 信息API =====

  stats() {
    const self = this;
    return {
      historySize: this.history.length,
      mode: this.mode,
      version: '2.1.0',
      premiseSignals: this.premiseSignals.length,
      certaintySignals: this.certaintySignals.length,
      // [v2.1.0] 新增统计
      multiPerspective: this.enableMultiPerspective,
      evidenceScoring: this.enableEvidenceScoring,
      adaptiveLearning: this.enableAdaptiveLearning,
      strategyStats: this.enableAdaptiveLearning ? this.adaptiveStats() : {},
    };
  }

  recentHistory(limit) {
    limit = limit || 10;
    return this.history.slice(-limit);
  }
}

module.exports = { CounterfactualEngine };
