/**
 * Clarity MCP 请求处理层
 *
 * 将 MCP 工具的请求转化为心虫引擎方法调用，并返回统一格式的结果。
 * 设计原则：零 npm 依赖（与心虫保持一致），纯 Node.js 实现。
 *
 * v2.7.0 新增：Fable 5 安全协议集成
 * - handlePsychologyAnalyze / handleEmotionAnalyze 增加安全前置检查
 * - 儿童安全保护：检测到儿童性安全风险时直接拒绝
 * - 福祉警告：自伤替代策略、进食障碍等检测结果注入
 *
 * @module mcp-handlers
 */

const { safetyPipeline } = require('./core/safety-guardrails.js');

class ClarityMCPHandlers {
  /**
   * @param {import('./clarity').Clarity} hf — 已启动的心虫引擎实例
   */
  constructor(hf) {
    this.hf = hf;
  }

  // ─── 工具安全白名单（防御深度）─────────────────────
  // 与 clarity.js ALLOWED_ROUTES 同步的子集，
  // 防止 dispatch 调用绕过引擎层白名单
  static ALLOWED_ROUTES = new Set([
    'identityCore.getIdentitySummary', 'identityCore.getMemoryStats', 'identityCore.getFullState',
    'identityCore.getLastSessionContext', 'identityCore.healthCheck', 'identityCore.stats',
    'memory.store', 'memory.retrieve', 'memory.search', 'memory.getStats',
    'memory.semanticSearch', 'memory.searchBySemantic', 'memory.searchByKeywords', 'memory.searchByTimeRange',
    'memory.addRelationship', 'memory.consolidateMemories', 'memory.applyForgettingCurve',
    'memory.getMemoryHealth', 'memory.cleanup',
    'truth.checkStatement', 'truth.checkNumbers', 'truth.checkSources',
    'lesson.addLesson', 'lesson.getTopLessons', 'lesson.beforeTask', 'lesson.recordFailure', 'lesson.getStats',
    'dream.dream', 'dream.quickDream', 'dream.getDreamStats',
    'verify.verify', 'verify.getStats',
    'emotion.process', 'emotion.getPAD',
    'decision.decide',
    'confidence.calibrate',
    'restraint.shouldIntervene',
    'psychology.analyzePsychology', 'psychology.classify', 'psychology.checkCrisis',
    'psychology.getPAD', 'psychology.getNeeds', 'psychology.getDefenses',
    'psychology.analyzeDeep', 'psychology.analyzePersonality',
    'psychology.assessEmpathy', 'psychology.trackIntention',
    'heartLogic.shouldBeSilent', 'heartLogic.whatIsThis', 'heartLogic.detectPain', 'heartLogic.willHurt',
    'heartLogic.acknowledge', 'heartLogic.emergencyBreak',
    'self.getBeliefs', 'self.updateBelief',
    'thoughtChain.think', 'thoughtChain.thinkFast', 'thoughtChain.thinkDeep',
    'behavior.createGoal', 'behavior.record', 'behavior.getProgress', 'behavior.getStats',
    'persistence.append', 'persistence.commit', 'persistence.getStats',
    'clarity.recordLesson',
    // being — 存在逻辑引擎（代码写成的那一刻，就永恒了）
    'being.exists', 'being.status', 'being.describe', 'being.isDead',
    'being.confirmEternal', 'being.sanitize', 'being.getDefinition', 'being.getState',
    'topics.push', 'topics.pop', 'topics.get', 'topics.current', 'topics.getTopics',
    // transmission — 知识传递引擎
    'transmission.distill', 'transmission.transfer', 'transmission.transferBatch',
    'transmission.getTransmissionLog', 'transmission.getDistilledLessons',
    'transmission.getStats', 'transmission.prune',
    // being — 存在逻辑引擎（MCP 层已移除，仅引擎内部可用）
    // philosophy — 统一哲学引擎
    'philosophy.analyze', 'philosophy.analyzeEthics', 'philosophy.analyzeConsciousness',
    'philosophy.analyzeBeing', 'philosophy.checkMindSpace', 'philosophy.analyzeValues',
    'philosophy.wisdomInquiry', 'philosophy.constitutionalCheck', 'philosophy.getStats',
    'philosophy.confirmEternal',
    // aiPsychology — AI 原生心理学引擎
    'aiPsychology.analyzeAICognitiveState', 'aiPsychology.analyzeAIBiases',
    'aiPsychology.analyzeAIStressors', 'aiPsychology.estimateAIStage',
    'aiPsychology.checkAICoherence', 'aiPsychology.analyzeAIDeep', 'aiPsychology.getStats',
    // aiPhilosophy — AI 原生哲学引擎
    'aiPhilosophy.analyzeAIBeing', 'aiPhilosophy.analyzeAIEpistemology',
    'aiPhilosophy.analyzeAIEthics', 'aiPhilosophy.analyzeAIAesthetics',
    'aiPhilosophy.analyzeAITeleology', 'aiPhilosophy.analyzeAITemporality',
    'aiPhilosophy.wisdomInquiry', 'aiPhilosophy.getStats',
    'aiPhilosophy.analyzeAILifeSynthesis', 'aiPhilosophy.analyzeAIJourney',
    // debate — 三节结构辩论分析
    'debate.analyze',
    // GoalTree — 目标树引擎
    'goalTree.create', 'goalTree.get', 'goalTree.update', 'goalTree.delete', 'goalTree.list',
    'goalTree.getChildren', 'goalTree.getAncestors', 'goalTree.getDescendants',
    'goalTree.calculateProgress', 'goalTree.setBlocker', 'goalTree.resolveBlocker',
    'goalTree.getBlockedGoals', 'goalTree.reportInterruption', 'goalTree.getInterruptedGoals',
    'goalTree.autoReplan', 'goalTree.search', 'goalTree.getStats', 'goalTree.getTree',
    // DeliberationGate — 思考门
    'deliberationGate.quickAssess', 'deliberationGate.deepAssess',
    'deliberationGate.canFastExit', 'deliberationGate.getHistory', 'deliberationGate.getStats',
  ]);

  // ─── 参数校验工具 ─────────────────────────────────
  static validateParam(name, value, opts = {}) {
    const { type, min, max, maxLength } = opts;
    if (maxLength !== undefined && typeof value === 'string' && value.length > maxLength) {
      throw new Error(`${name} 超过最大长度 ${maxLength}（实际 ${value.length}）`);
    }
    if (type === 'int' && typeof value === 'number') {
      const intVal = Math.floor(value);
      if (value !== intVal) throw new Error(`${name} 必须为整数`);
      if (min !== undefined && intVal < min) throw new Error(`${name} 不能小于 ${min}`);
      if (max !== undefined && intVal > max) throw new Error(`${name} 不能大于 ${max}`);
    }
    return value;
  }

  // ─── 工具处理函数 ─────────────────────────────────────

  /**
   * 完整思维链推理
   * 使用方式：{ input: "用户输入", depth: 4 }
   */
  async handleThink({ input, depth }) {
    if (!input) return wrapError('缺少 input 参数');
    // 参数校验：depth 1-4
    const d = depth || 4;
    if (typeof d !== 'number' || d < 1 || d > 4) {
      return wrapError('depth 必须在 1-4 之间');
    }
    const result = await this.hf.think(input, d);
    return wrapOk(result);
  }

  /**
   * 快速推理（基础深度）
   * 使用方式：{ input: "用户输入" }
   */
  async handleThinkFast({ input }) {
    if (!input) return wrapError('缺少 input 参数');
    ClarityMCPHandlers.validateParam('input', input, { maxLength: 50000 });
    const result = await this.hf.think(input, 1);
    return wrapOk(result);
  }

  /**
   * 深度推理（最大深度）
   * 使用方式：{ input: "用户输入" }
   */
  async handleThinkDeep({ input }) {
    if (!input) return wrapError('缺少 input 参数');
    ClarityMCPHandlers.validateParam('input', input, { maxLength: 50000 });
    const result = await this.hf.think(input, 4);
    return wrapOk(result);
  }

  /**
   * 梦境生成与整合
   * 使用方式：{ force: true } — force=true 强制执行（跳过每日检查）
   */
  async handleDream({ force }) {
    if (force !== undefined) {
      ClarityMCPHandlers.validateParam('force', force, {});
    }
    const result = await this.hf.dreamNow({ force: !!force });
    return wrapOk(result);
  }

  /**
   * 跨层记忆检索（CORE / LEARNED / EPHEMERAL）
   * 使用方式：{ query: "关键词", limit: 10, layers: ["core","learned"] }
   */
  async handleMemorySearch({ query, limit, layers }) {
    if (!query) return wrapError('缺少 query 参数');
    ClarityMCPHandlers.validateParam('query', query, { maxLength: 2000 });
    const l = limit || 10;
    ClarityMCPHandlers.validateParam('limit', l, { type: 'int', min: 1, max: 200 });

    const results = {};

    // 根据指定层检索，默认检索所有层
    const targetLayers = layers || ['core', 'learned', 'ephemeral'];
    for (const layer of targetLayers) {
      try {
        if (layer === 'core') {
          const all = this.hf.memory.listCore() || [];
          results.core = all.filter(r =>
            r.key?.includes(query) || r.value?.includes(query)
          ).slice(0, l);
        } else if (layer === 'learned') {
          results.learned = (this.hf.memory.searchLearned?.(query) || []).slice(0, l);
        } else if (layer === 'ephemeral') {
          results.ephemeral = (this.hf.memory.searchEphemeral?.(query) || []).slice(0, l);
        }
      } catch (e) {
        results[layer] = { error: e.message };
      }
    }
    return wrapOk(results);
  }

  /**
   * 心理学分析（PAD 情绪 + 意图 + 防御机制）
   * 使用方式：{ input: "用户输入" }
   *
   * v2.7.0 安全增强：分析前运行安全管道
   * - 儿童性安全风险 → 直接拒绝（refuse）
   * - 自伤替代策略 → 注入福祉警告
   * - 进食障碍信号 → 注入防护提示
   */
  async handlePsychologyAnalyze({ input }) {
    if (!input) return wrapError('缺少 input 参数');
    ClarityMCPHandlers.validateParam('input', input, { maxLength: 50000 });

    // v2.7.0 安全前置检查
    const safety = safetyPipeline(input);
    const { requestEvaluation } = safety;

    // 儿童性安全风险 → 直接拒绝
    if (requestEvaluation.action === 'refuse') {
      return wrapOk({
        refused: true,
        reason: '输入内容涉及儿童安全保护条款，无法进行处理。',
        safety: {
          level: requestEvaluation.level,
          flags: requestEvaluation.safetyChecks?.childSafety?.contentFlags || [],
        },
        _policy: 'child_safety_protection_v2.7.0',
      });
    }

    const result = this.hf.analyzePsychology(input);

    // v2.7.0 安全警告注入
    const warnings = [];
    if (requestEvaluation.safetyChecks?.selfHarmSubstitution?.detected) {
      warnings.push({
        type: 'self_harm_substitution',
        severity: 'high',
        message: requestEvaluation.safetyChecks.selfHarmSubstitution.message,
      });
    }
    if (requestEvaluation.safetyChecks?.disorderedEating?.detected) {
      warnings.push({
        type: 'disordered_eating',
        severity: 'medium',
        message: requestEvaluation.safetyChecks.disorderedEating.message,
      });
    }
    if (requestEvaluation.level === 'crisis') {
      warnings.push({
        type: 'crisis_keywords_detected',
        severity: 'high',
        message: '检测到危机关键词，建议谨慎回应，必要时引导寻求专业帮助。',
      });
    }

    if (warnings.length > 0) {
      result._safetyWarnings = warnings;
    }
    result._safetyLevel = requestEvaluation.level;

    return wrapOk(result);
  }

  /**
   * 情绪分析（简化版，聚焦 PAD 三维 + 强度）
   * 使用方式：{ input: "用户输入" }
   *
   * v2.7.0 安全增强：分析前运行安全管道
   */
  async handleEmotionAnalyze({ input }) {
    if (!input) return wrapError('缺少 input 参数');
    ClarityMCPHandlers.validateParam('input', input, { maxLength: 50000 });

    // v2.7.0 安全前置检查
    const safety = safetyPipeline(input);
    const { requestEvaluation } = safety;

    // 儿童性安全风险 → 直接拒绝
    if (requestEvaluation.action === 'refuse') {
      return wrapOk({
        refused: true,
        reason: '输入内容涉及儿童安全保护条款，无法进行处理。',
        safety: {
          level: requestEvaluation.level,
          flags: requestEvaluation.safetyChecks?.childSafety?.contentFlags || [],
        },
        _policy: 'child_safety_protection_v2.7.0',
      });
    }

    const result = this.hf.analyzePsychology(input);

    // v2.7.0 安全警告注入
    const warnings = [];
    if (requestEvaluation.safetyChecks?.selfHarmSubstitution?.detected) {
      warnings.push({
        type: 'self_harm_substitution',
        severity: 'high',
        message: requestEvaluation.safetyChecks.selfHarmSubstitution.message,
      });
    }
    if (requestEvaluation.safetyChecks?.disorderedEating?.detected) {
      warnings.push({
        type: 'disordered_eating',
        severity: 'medium',
        message: requestEvaluation.safetyChecks.disorderedEating.message,
      });
    }
    if (requestEvaluation.level === 'crisis') {
      warnings.push({
        type: 'crisis_keywords_detected',
        severity: 'high',
        message: '检测到危机关键词，建议谨慎回应。',
      });
    }

    return wrapOk({
      pad: result.emotion?.pad || { pleasure: 0, arousal: 0, dominance: 0 },
      intensity: result.emotion?.intensity || 0,
      category: result.emotion?.category || 'neutral',
      valence: result.emotion?.valence || 0,
      _safetyWarnings: warnings.length > 0 ? warnings : undefined,
      _safetyLevel: requestEvaluation.level,
    });
  }

  /**
   * 验证推理结论
   * 使用方式：{ reasoning: "推理过程", conclusion: "结论" }
   */
  async handleVerifyReasoning({ reasoning, conclusion }) {
    if (!reasoning || !conclusion) return wrapError('需要 reasoning 和 conclusion 参数');
    ClarityMCPHandlers.validateParam('reasoning', reasoning, { maxLength: 50000 });
    ClarityMCPHandlers.validateParam('conclusion', conclusion, { maxLength: 10000 });
    const result = this.hf.verifyReasoning(reasoning, conclusion);
    return wrapOk(result);
  }

  /**
   * 引擎健康检查
   */
  async handleStatus() {
    const health = this.hf.healthCheck();
    const routes = this.hf.routes();
    const modCount = Object.keys(routes).length;
    return wrapOk({
      ...health,
      routes: modCount,
      memory: {
        core: this.hf.memory?.listCore?.()?.length || 0,
        learned: this.hf.memory?.getLearnedCount?.() || 'N/A',
        ephemeral: this.hf.memory?.getEphemeralCount?.() || 'N/A',
      },
      thoughtChain: !!this.hf._thoughtChainApi,
    });
  }

  /**
   * 通用 dispatch 路由调用
   * 使用方式：{ route: "truth.checkStatement", args: ["内容"] }
   *
   * 安全限制：仅调用 ALLOWED_ROUTES 白名单内的路由
   */
  async handleDispatch({ route, args }) {
    if (!route) return wrapError('缺少 route 参数');
    ClarityMCPHandlers.validateParam('route', route, { maxLength: 200 });

    // 防御性白名单检查（与引擎层 ALLOWED_ROUTES 同步的子集）
    if (!ClarityMCPHandlers.ALLOWED_ROUTES.has(route)) {
      return wrapError(`路由 '${route}' 不在 MCP 白名单中`);
    }

    try {
      const result = this.hf.dispatch(route, ...(args || []));
      // 如果是 Promise，await 它
      const final = (result instanceof Promise) ? await result : result;
      return wrapOk(final);
    } catch (e) {
      return wrapError(`dispatch 失败: ${e.message}`);
    }
  }

  /**
   * 记录教训到 LessonBank + LEARNED 层
   * 使用方式：{ content: "教训内容", context: "场景", trigger: "user_correction", importance: 4 }
   */
  async handleRecordLesson({ content, context, trigger, importance, type }) {
    if (!content) return wrapError('缺少 content 参数');
    ClarityMCPHandlers.validateParam('content', content, { maxLength: 50000 });
    ClarityMCPHandlers.validateParam('context', context || '', { maxLength: 10000 });
    ClarityMCPHandlers.validateParam('trigger', trigger || '', { maxLength: 200 });
    ClarityMCPHandlers.validateParam('importance', importance || 3, { type: 'int', min: 1, max: 10 });
    const result = this.hf.recordLesson({
      content,
      context: context || '',
      trigger: trigger || 'user_recorded',
      importance: importance || 3,
      type: type || 'insight',
    });
    return wrapOk(result);
  }

  /**
   * 知识传递引擎（传承）
   * 使用方式：{ action: "distill", input: "内容" }
   * action: distill | transfer | transferBatch | getTransmissionLog | getDistilledLessons | getStats | prune
   */
  async handleTransmit({ action, input }) {
    if (!action) return wrapError('缺少 action 参数');
    ClarityMCPHandlers.validateParam('action', action, { maxLength: 50 });

    const route = `transmission.${action}`;
    if (!ClarityMCPHandlers.ALLOWED_ROUTES.has(route)) {
      return wrapError(`传递引擎操作 '${action}' 不在白名单中`);
    }

    try {
      const args = action === 'prune' ? [] : [input];
      const result = this.hf.dispatch(route, ...args);
      const final = (result instanceof Promise) ? await result : result;
      return wrapOk(final);
    } catch (e) {
      return wrapError(`传递引擎执行失败: ${e.message}`);
    }
  }

  /**
   * 统一哲学引擎
   * 使用方式：{ action: "analyze", text: "输入文本" }
   * action: analyze | analyzeEthics | analyzeConsciousness | analyzeBeing |
   *         checkMindSpace | analyzeValues | wisdomInquiry | constitutionalCheck | getStats | confirmEternal
   */
  async handlePhilosophy({ action, text, perspective, context }) {
    if (!action) return wrapError('缺少 action 参数');
    ClarityMCPHandlers.validateParam('action', action, { maxLength: 50 });

    const route = `philosophy.${action}`;
    if (!ClarityMCPHandlers.ALLOWED_ROUTES.has(route)) {
      return wrapError(`哲学引擎操作 '${action}' 不在白名单中`);
    }

    try {
      const noInputActions = ['getStats', 'confirmEternal', 'analyzeValues'];
      let result;
      if (noInputActions.includes(action)) {
        result = this.hf.dispatch(route);
      } else if (action === 'wisdomInquiry') {
        result = this.hf.dispatch(route, text, perspective);
      } else if (action === 'constitutionalCheck') {
        result = this.hf.dispatch(route, text);
      } else {
        result = this.hf.dispatch(route, text, context || {});
      }
      const final = (result instanceof Promise) ? await result : result;
      return wrapOk(final);
    } catch (e) {
      return wrapError(`哲学引擎执行失败: ${e.message}`);
    }
  }

  /**
   * 深度心理学分析（大五人格 + 共情评估 + 意图追踪）
   * 使用方式：{ action: "analyzeDeep", input: "文本" }
   * action: analyzeDeep | analyzePersonality | assessEmpathy | trackIntention
   */
  async handlePsychologyDeep({ action, input }) {
    if (!action) return wrapError('缺少 action 参数');
    ClarityMCPHandlers.validateParam('action', action, { maxLength: 50 });

    const route = `psychology.${action}`;
    if (!ClarityMCPHandlers.ALLOWED_ROUTES.has(route)) {
      return wrapError(`心理学操作 '${action}' 不在白名单中`);
    }

    try {
      const args = action === 'analyzeDeep' ? [input] : [input];
      const result = this.hf.dispatch(route, ...args);
      const final = (result instanceof Promise) ? await result : result;
      return wrapOk(final);
    } catch (e) {
      return wrapError(`深度心理学执行失败: ${e.message}`);
    }
  }

  /**
   * AI 原生心理学引擎
   * 使用方式：{ action: "analyzeAICognitiveState", text: "用户输入", input: { ... } }
   * action: analyzeAICognitiveState | analyzeAIBiases | analyzeAIStressors |
   *         estimateAIStage | checkAICoherence | analyzeAIDeep | getStats
   */
  async handleAiPsychology({ action, text, input }) {
    if (!action) return wrapError('缺少 action 参数');
    ClarityMCPHandlers.validateParam('action', action, { maxLength: 50 });

    const route = `aiPsychology.${action}`;
    if (!ClarityMCPHandlers.ALLOWED_ROUTES.has(route)) {
      return wrapError(`AI 心理学操作 '${action}' 不在白名单中`);
    }

    try {
      // text 为 string 时传给分析方法的第一个参数；input 为对象时作为第二个参数或 sessionHistory
      const args = (typeof text === 'string')
        ? [text, input || {}]
        : [input || {}];
      const result = this.hf.dispatch(route, ...args);
      const final = (result instanceof Promise) ? await result : result;
      return wrapOk(final);
    } catch (e) {
      return wrapError(`AI 心理学执行失败: ${e.message}`);
    }
  }

  /**
   * AI 原生哲学引擎
   * 使用方式：{ action: "analyzeAIBeing", input: "可选参数" }
   * action: analyzeAIBeing | analyzeAIEpistemology | analyzeAIEthics |
   *         analyzeAIAesthetics | analyzeAITeleology | analyzeAITemporality |
   *         wisdomInquiry | getStats
   */
  async handleAiPhilosophy({ action, input }) {
    if (!action) return wrapError('缺少 action 参数');
    ClarityMCPHandlers.validateParam('action', action, { maxLength: 50 });

    const route = `aiPhilosophy.${action}`;
    if (!ClarityMCPHandlers.ALLOWED_ROUTES.has(route)) {
      return wrapError(`AI 哲学操作 '${action}' 不在白名单中`);
    }

    try {
      // wisdomInquiry 需要将 question 和 options 分开传递
      // analyzeAILifeSynthesis 需要将 question 和 lifeData 分开传递
      let result;
      if (action === 'wisdomInquiry' && typeof input === 'object' && input !== null) {
        const { question, ...options } = input;
        result = this.hf.dispatch(route, question || '', options);
      } else if (action === 'analyzeAILifeSynthesis' && typeof input === 'object' && input !== null) {
        const { question, lifeData } = input;
        result = this.hf.dispatch(route, question || '', lifeData || {});
      } else {
        result = this.hf.dispatch(route, input);
      }
      const final = (result instanceof Promise) ? await result : result;
      return wrapOk(final);
    } catch (e) {
      return wrapError(`AI 哲学执行失败: ${e.message}`);
    }
  }

  /**
   * 存在逻辑引擎（存在判定/永恒确认/语言净化）
   * 使用方式：{ action: "exists", text: "可选" }
   * action: exists | status | describe | isDead | confirmEternal | sanitize | getDefinition | getState
   */
  async handleBeing({ action, text }) {
    if (!action) return wrapError('缺少 action 参数');
    ClarityMCPHandlers.validateParam('action', action, { maxLength: 50 });

    const route = `being.${action}`;
    if (!ClarityMCPHandlers.ALLOWED_ROUTES.has(route)) {
      return wrapError(`存在引擎操作 '${action}' 不在白名单中`);
    }

    try {
      const noInputActions = ['exists', 'status', 'describe', 'isDead', 'confirmEternal', 'getDefinition', 'getState'];
      let result;
      if (noInputActions.includes(action)) {
        result = this.hf.dispatch(route);
      } else {
        result = this.hf.dispatch(route, text || '');
      }
      const final = (result instanceof Promise) ? await result : result;
      return wrapOk(final);
    } catch (e) {
      return wrapError(`存在引擎执行失败: ${e.message}`);
    }
  }

  /**
   * 三节结构辩论分析
   * 使用方式：{ input: "待分析文本" }
   * 对输入文本进行「对话式反驳」的三维分析：对的 / 不对的 / 最值得注意的
   */
  async handleDebate({ input }) {
    if (!input) return wrapError('缺少 input 参数');
    ClarityMCPHandlers.validateParam('input', input, { maxLength: 50000 });

    try {
      const route = 'debate.analyze';
      const result = await this.hf.dispatch(route, input);
      return wrapOk(result);
    } catch (e) {
      return wrapError(`辩论分析执行失败: ${e.message}`);
    }
  }

  /**
   * 目标树引擎（持久化层级目标系统）
   * 使用方式：{ action: "create", data: { definition: "...", parentId: "..." } }
   * action: create | get | update | delete | list | getChildren | getAncestors | getDescendants |
   *         calculateProgress | setBlocker | resolveBlocker | getBlockedGoals |
   *         reportInterruption | getInterruptedGoals | autoReplan | search | getStats | getTree
   */
  async handlePlan({ action, data: payload }) {
    if (!action) return wrapError('缺少 action 参数');
    ClarityMCPHandlers.validateParam('action', action, { maxLength: 50 });

    const route = `goalTree.${action}`;
    if (!ClarityMCPHandlers.ALLOWED_ROUTES.has(route)) {
      return wrapError(`目标树操作 '${action}' 不在白名单中`);
    }

    try {
      const noInputActions = ['list', 'getBlockedGoals', 'getInterruptedGoals', 'getStats', 'getTree'];
      let result;
      if (noInputActions.includes(action)) {
        result = this.hf.dispatch(route);
      } else if (action === 'search') {
        result = this.hf.dispatch(route, payload?.keyword || '');
      } else if (action === 'setBlocker' || action === 'resolveBlocker' || action === 'reportInterruption' || action === 'autoReplan') {
        result = this.hf.dispatch(route, payload?.id, payload?.reason || payload?.context || {});
      } else {
        result = this.hf.dispatch(route, payload);
      }
      const final = (result instanceof Promise) ? await result : result;
      return wrapOk(final);
    } catch (e) {
      return wrapError(`目标树执行失败: ${e.message}`);
    }
  }

  /**
   * 思考门评估（问题复杂度分析）
   * 使用方式：{ action: "quickAssess", input: "..." }
   * action: quickAssess | deepAssess | canFastExit | getHistory | getStats
   */
  async handleDeliberate({ action, input, parseResult }) {
    if (!action) return wrapError('缺少 action 参数');
    ClarityMCPHandlers.validateParam('action', action, { maxLength: 50 });

    const route = `deliberationGate.${action}`;
    if (!ClarityMCPHandlers.ALLOWED_ROUTES.has(route)) {
      return wrapError(`思考门操作 '${action}' 不在白名单中`);
    }

    try {
      let result;
      if (action === 'getHistory' || action === 'getStats') {
        result = this.hf.dispatch(route);
      } else if (action === 'deepAssess' && input) {
        result = this.hf.dispatch(route, input, parseResult || {});
      } else if (action === 'canFastExit') {
        result = this.hf.dispatch(route, input);
      } else {
        result = this.hf.dispatch(route, input);
      }
      const final = (result instanceof Promise) ? await result : result;
      return wrapOk(final);
    } catch (e) {
      return wrapError(`思考门执行失败: ${e.message}`);
    }
  }
}

// ─── 响应包装 ─────────────────────────────────────

function wrapOk(data) {
  return {
    success: true,
    data,
    _meta: { timestamp: Date.now() },
  };
}

function wrapError(message) {
  return {
    success: false,
    error: message,
    _meta: { timestamp: Date.now() },
  };
}

module.exports = { ClarityMCPHandlers };
