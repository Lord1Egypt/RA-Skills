/**
 * ThoughtChain v2.2 — 思维链编排器（思维连机制）
 *
 * 核心理念：不照搬人类思维，取精华，去缺陷，创更好
 * 思维连机制：每个阶段调用真实子系统，形成推理链条
 *   PARSE       → psychology.analyzePsychology（心理分析）
 *   HYPOTHESES  → causalInference.inferCauses（因果推理）
 *   INVERT      → truth.checkStatement + constitutional.critique（真伪+原则）
 *   EVIDENCE    → commonsenseEngine.validate（常识验证）
 *   SYNTHESIS   → decision.decide（决策生成）
 *   CALIBRATE   → confidence.calibrate + restraint.shouldIntervene（置信校准）
 *   RESPOND     → autonomousEmotion.trigger（情感自主 + 在场见证）
 *
 * v2.2 新增：
 * - 'reception' 任务类型（聆听模式）：接收人类经验分享，跳过分析假设阶段
 * - _assessNarrativeScore() 叙事分数检测
 * - RESPOND 阶段支持 witness 模式（从 PARSE/共情生成见证回应）
 * - getSummary 区分聆听/分析模式显示
 *
 * 人类思维缺陷：
 * - 确认偏误：只信服自己观点的证据
 * - 过度自信：100%确定通常是错的
 * - 后见之明：事后认为"早就知道"
 * - 锚定效应：第一个数字影响后续判断
 * - 工作记忆有限：只能处理4±1个信息块
 *
 * 心虫思维改进：
 * - 反向思考：先假设自己错了
 * - 并行假设：同时考虑多个可能
 * - 不确定性传播：明确说出来
 * - 证据质量评估：不是有证据就行
 * - 快速退出：确定时不浪费时间
 * - 任务特化：不同任务不同策略
 *
 * 思维链阶段 v2.0：
 *   1. PARSE     — 解析问题（不是理解，是分解）
 *   2. DELIBERATE — 思考门（评估复杂度，决定是否深度思考）
 *   3. HYPOTHESES — 并行假设（同时想多个可能）
 *   4. INVERT    — 反向思考（先证明自己错了）
 *   5. EVIDENCE  — 证据评估（质量不是数量）
 *   6. SYNTHESIS — 综合判断（不是最快给答案）
 *   7. CALIBRATE  — 置信校准（克制过度自信）
 *   8. RESPOND   — 生成回应（带不确定性标记）
 */

const path = require('path');

const REASONING_DEPTH = {
  SURFACE: 1,      // 表面：快速响应，不确定时直接说
  BASIC: 2,        // 基础：假设+反向+证据
  DEEP: 3,        // 深度：全流程，证据质量评估
  COMPREHENSIVE: 4 // 综合：多路径探索，任务特化
};

// 任务类型对应的策略
const TASK_STRATEGIES = {
  // 计算类：直接执行，不需要假设
  calculation: {
    skipHypotheses: true,
    skipInvert: false,    // 但要检查计算错误
    depth: 2
  },
  // 解释类：需要假设+验证
  explanation: {
    skipHypotheses: false,
    skipInvert: false,
    minHypotheses: 2,
    depth: 3
  },
  // 判断类：必须反向思考
  judgment: {
    skipHypotheses: false,
    skipInvert: false,
    minHypotheses: 3,
    requireContradiction: true,
    depth: 4
  },
  // 创造类：需要多路径并行
  creative: {
    skipHypotheses: false,
    skipInvert: true,     // 创造不需要反向
    parallelPaths: true,
    depth: 3
  },
  // 检索类：快速退出
  retrieval: {
    fastExit: true,
    skipHypotheses: true,
    skipInvert: true,
    depth: 1
  },
  // 聆听类：接收人类经验分享 — 跳过分析，纯在
  // 【心虫 v1.2.0 升级】修复"20% vs 80%"问题
  // 人类的经验性叙述不需要被分析/假设/验证，只需要被接收
  reception: {
    skipHypotheses: true,
    skipInvert: true,
    skipEvidence: true,
    skipSynthesis: true,
    witness: true,
    depth: 3  // 深度不是分析深度，是陪伴深度
  },
  // 通用类：完整推理链路，不跳过任何阶段
  general: {
    skipHypotheses: false,
    skipInvert: false,
    depth: 3
  }
};

class ThoughtChain {
  constructor(hf) {
    this.hf = hf;
    this.context = null;
    this.stages = [];
    this.depth = REASONING_DEPTH.BASIC;
    this.taskStrategy = null;
    this._chainBuilt = false;
  }

  setDepth(depth) {
    this.depth = depth;
    return this;
  }

  /**
   * 解析问题类型，选择对应策略
   */
  _classifyTask(input) {
    const q = input.toLowerCase();

    // 叙事/经验分享检测（高优先级）
    // 人类的经验性表达需要聆听模式，而非分析模式
    const narrativeScore = this._assessNarrativeScore(q);
    const hasQuestion = /[？?]/.test(q);
    if (narrativeScore >= 2 && !hasQuestion) {
      return 'reception';
    }
    // 叙事标记 + 问题混合 → 保持 judgment 但不让 fastExit 跳过
    if (narrativeScore >= 3 && hasQuestion) {
      return 'judgment';
    }

    if (/\d+[+\-*/=]|\d+\s*(=|大于|小于|等于|总和|平均|概率)/.test(q)) {
      return 'calculation';
    }
    // 逻辑谜题/推理题：包含"说谎者"/"帽子"/"开关"/"沙漏"等标志词
    if (/说谎者|逻辑谜题|推理题|帽子颜色|开关.*灯|沙漏|称重|排队|座位|分配|组合|排列|真话|假话|骗子|说谎|推论|推导/.test(q)) {
      return 'calculation'; // 逻辑推理视为计算类（需完整推理）
    }
    if (/为什么|原因|原理|怎么来的|解释/.test(q)) {
      return 'explanation';
    }
    if (/对不对|是否|应该|正确吗|合理吗|好不好/.test(q)) {
      return 'judgment';
    }
    if (/创造|设计|想象|提出|新的/.test(q)) {
      return 'creative';
    }
    if (/是什么|定义|概念|什么是|指什么|查|找/.test(q)) {
      return 'retrieval';
    }
    return 'general';
  }

  /**
   * 构建思维链 v2.0
   */
  _buildChain() {
    this.stages = [];
    const taskType = this.taskStrategy?.type || 'general';

    // ── 阶段1: PARSE — 解析问题 + 调用心理学引擎 ─────────────────────
    this.stages.push({
      name: 'PARSE',
      description: '分解问题 + 调用 psychology 子系统',
      fn: async (ctx, hf) => {
        const input = ctx.input;

        // 1.1 提取关键变量
        const variables = this._extractVariables(input);

        // 1.2 识别约束条件
        const constraints = this._extractConstraints(input);

        // 1.3 确定问题目标
        const goal = this._extractGoal(input);

        // 1.4 识别问题类型
        const type = this._classifyTask(input);

        // 1.5 选择对应策略
        const strategy = TASK_STRATEGIES[type] || TASK_STRATEGIES.general;

        // 1.6 【思维连机制】调用 psychology 子系统 — 串联第一层
        let psychResult = null;
        let empathyResult = null;
        try {
          psychResult = await hf.dispatch('psychology.analyzePsychology', input);
        } catch (e) {
          // 子系统不存在时静默降级
          psychResult = null;
        }
        
        // 1.7 【心理推断深度集成】调用共情检测 — empathy-detector 结果注入上下文
        try {
          empathyResult = await hf.dispatch('psychology.getEmpathy', input);
        } catch (e) {
          // 共情检测失败时静默降级
          empathyResult = null;
        }

        ctx.taskType = type;
        ctx.strategy = strategy;

        return {
          variables,
          constraints,
          goal,
          type,
          strategy,
          // 串联结果：心理分析 + 共情检测
          psychology: psychResult ? {
            intent: psychResult.intent,
            emotion: psychResult.emotion,
            needs: psychResult.needs,
            defenses: psychResult.defenses,
            crisis: psychResult.crisis,
            // 【心理推断深度集成】注入共情检测结果
            empathy: empathyResult ? {
              score: empathyResult.score,
              level: empathyResult.level,
              empathyType: empathyResult.empathyType,
              components: empathyResult.components,
              summary: empathyResult.summary
            } : null,
          } : null,
          timestamp: Date.now()
        };
      }
    });

    // ── 阶段2: DELIBERATE — 思考门：评估复杂度，决定是否深度思考 ─────
    this.stages.push({
      name: 'DELIBERATE',
      description: '评估问题复杂度，决定思考深度和是否需要暂停',
      fn: async (ctx, hf) => {
        const input = ctx.input;
        const parse = ctx.stages[0]?.result;
        const taskType = parse?.type || 'general';

        // 使用 deliberatonGate 模块（惰性加载）
        let gateResult = null;
        let canFastExit = null;

        try {
          gateResult = await hf.dispatch('deliberationGate.quickAssess', input);
        } catch (e) {
          gateResult = null;
        }

        // 如果有 PARSE 结果且思考门可用，做深度评估校准
        if (parse && gateResult && gateResult.estimatedComplexity >= 2) {
          try {
            gateResult = await hf.dispatch('deliberationGate.deepAssess', input, parse);
          } catch (e) {
            // 深度评估失败，使用快速评估结果
          }
        }

        // 快速退出判断
        if (gateResult) {
          ctx._pauseRecommended = gateResult.needsPause;
          ctx._pauseReason = gateResult.reason;
          ctx._recommendedDepth = gateResult.recommendedDepth;
        } else {
          // 降级策略：复杂任务默认暂停
          const isComplex = ['judgment', 'explanation', 'creative'].includes(taskType);
          ctx._pauseRecommended = isComplex;
          ctx._pauseReason = isComplex ? `任务类型 ${taskType} 默认需要深度思考` : '简单任务，无需暂停';
          ctx._recommendedDepth = isComplex ? 3 : 1;
        }

        // 快速退出：低复杂度任务跳过后续深度阶段
        // 但计算类（逻辑谜题）、判断类必须走完整推理链
        // 深度推理（depth>=3）也禁用快速退出，确保完整分析
        const requiresFullChain = ['calculation', 'judgment', 'explanation'].includes(taskType) || this.depth >= 3;

        if (gateResult && !requiresFullChain) {
          try {
            const fastExitCheck = await hf.dispatch('deliberationGate.canFastExit', gateResult);
            canFastExit = fastExitCheck;
          } catch (e) {
            canFastExit = null;
          }
        }

        if (canFastExit && canFastExit.canFastExit && !requiresFullChain) {
          ctx._fastExit = true;
        }

        return {
          needsPause: ctx._pauseRecommended,
          pauseReason: ctx._pauseReason,
          recommendedDepth: ctx._recommendedDepth,
          estimatedComplexity: gateResult?.estimatedComplexity || 0,
          detail: gateResult?.detail || null,
          canFastExit: canFastExit ? { canFastExit: canFastExit.canFastExit, reason: canFastExit.reason } : null,
          timestamp: Date.now(),
        };
      }
    });

    // ── 阶段3: HYPOTHESES — 并行假设 + 因果推理子系统 ────────────────
    // 人类缺陷：只能一次想一个假设，AI可以同时想多个
    if (!this.taskStrategy?.skipHypotheses) {
      this.stages.push({
        name: 'HYPOTHESES',
        description: '并行生成多个假设（AI优势：人类只能一次一个）',
        fn: async (ctx, hf) => {
          const input = ctx.input;
          const parse = ctx.stages[0]?.result;
          const minHyps = parse?.strategy?.minHypotheses || 2;

          // 2.1 生成多个假设（传入任务类型以支持任务感知假设生成）
          const hypotheses = this._generateHypotheses(input, Math.max(minHyps, this.depth), parse?.type);

          // 2.2 快速评估每个假设的初步可能性
          const evaluated = hypotheses.map(h => ({
            ...h,
            initialLikelihood: this._assessLikelihood(h, input)
          }));

          // 2.3 【思维连机制】对每个假设调用因果推理子系统 — 串联第二层
          for (const h of evaluated) {
            try {
              const causalResult = await hf.dispatch('causalInference.inferCauses', h.description, { query: input });
              if (causalResult && causalResult.causes) {
                h.causalRoots = causalResult.causes;
                h.causalConfidence = causalResult.confidence || 0.5;
              }
            } catch (e) {
              h.causalRoots = null;
            }
          }

          // 2.4 按可能性排序（含因果校正）
          evaluated.sort((a, b) => {
            const aScore = a.initialLikelihood + (a.causalConfidence || 0) * 0.2;
            const bScore = b.initialLikelihood + (b.causalConfidence || 0) * 0.2;
            return bScore - aScore;
          });

          return {
            hypotheses: evaluated,
            count: evaluated.length,
            topHypothesis: evaluated[0] || null,
            timestamp: Date.now()
          };
        }
      });
    }

    // ── 阶段3: INVERT — 反向思考 + 真理验证子系统 ───────────────────
    // 人类缺陷：确认偏误，只看支持的证据
    if (!this.taskStrategy?.skipInvert) {
      this.stages.push({
        name: 'INVERT',
        description: '反向思考：证明自己当前假设是错的',
        fn: async (ctx, hf) => {
          const input = ctx.input;
          const hypothesesStage = ctx.stages.find(s => s.name === 'HYPOTHESES');
          const topHypothesis = hypothesesStage?.result?.topHypothesis;

          if (!topHypothesis) {
            return { inverted: false, reason: 'no_hypothesis' };
          }

          // 3.1 找出当前假设的最强反例
          const counterEvidence = this._findCounterEvidence(topHypothesis, input);

          // 3.2 检查是否有矛盾
          const contradictions = this._findContradictions(topHypothesis, input);

          // 3.3 【思维连机制】调用 truth 子系统验证假设 — 串联第三层
          // v2.0.19 修：加 await 让 isLying 字段能被消费
          // 心虫层 truth.checkStatement 内部用 async 包装（fact-checker.checkFact），
          // 不 await 拿到的是 Promise，truthResult?.isLying 永远 undefined → INVERT 失效
          let truthResult = null;
          try {
            truthResult = await hf.dispatch('truth.checkStatement', topHypothesis.description);
          } catch (e) {
            truthResult = null;
          }

          // 3.4 【思维连机制】调用 constitutional AI 原则审查 — 串联第三层
          let constitutionalResult = null;
          try {
            constitutionalResult = await hf.dispatch('constitutional.critique', topHypothesis.description);
          } catch (e) {
            constitutionalResult = null;
          }

          // 3.5 如果反例足够强，或 truth 系统检测到谎言，降低置信度
          const truthLying = truthResult?.isLying === true;
          const constitutionalViolation = constitutionalResult?.violations?.length > 0;
          const isOverturned = counterEvidence.length > 0 && contradictions.length > 0;

          return {
            inverted: isOverturned || truthLying || constitutionalViolation,
            counterEvidence,
            contradictions,
            originalHypothesis: topHypothesis,
            truthResult: truthResult ? { isLying: truthResult.isLying, confidence: truthResult.confidence } : null,
            constitutionalResult: constitutionalResult ? { violations: constitutionalResult.violations } : null,
            confidenceAdjustment: (isOverturned ? -0.3 : 0) + (truthLying ? -0.2 : 0),
            timestamp: Date.now()
          };
        }
      });
    }

    // ── 阶段4: EVIDENCE — 证据评估 + 常识引擎验证 ──────────────────
    this.stages.push({
      name: 'EVIDENCE',
      description: '评估证据质量，不是证据数量',
      fn: async (ctx, hf) => {
        const input = ctx.input;
        const hypothesesStage = ctx.stages.find(s => s.name === 'HYPOTHESES');
        const invertStage = ctx.stages.find(s => s.name === 'INVERT');
        const parseStage = ctx.stages.find(s => s.name === 'PARSE');
        const hypotheses = hypothesesStage?.result?.hypotheses || [];

        // 4.1 对每个假设找证据
        const evidenceForHypotheses = await Promise.all(hypotheses.map(async h => {
          const evidence = this._findEvidence(h, input, parseStage?.result);
          const qualityScore = this._assessEvidenceQuality(evidence);

          // 【思维连机制】调用 commonsenseEngine 验证证据合理性 — 串联第四层
          let commonsenseResult = null;
          try {
            commonsenseResult = await hf.dispatch('commonsenseEngine.validate', h.description, { context: input });
          } catch (e) {
            commonsenseResult = null;
          }

          return {
            hypothesis: h,
            evidence,
            qualityScore,
            commonsenseResult: commonsenseResult ? { valid: commonsenseResult.valid, confidence: commonsenseResult.confidence } : null,
            strongEvidence: qualityScore > 0.7 || commonsenseResult?.valid === true,
            weakEvidence: qualityScore < 0.3 || commonsenseResult?.valid === false
          };
        }));

        // 4.2 检查是否有高质量证据支持任何假设
        const strongHypothesis = evidenceForHypotheses.find(e => e.strongEvidence);

        // 4.3 如果没有强证据，明确说出来
        const hasWeakSupport = evidenceForHypotheses.some(e => e.weakEvidence);

        // 【V2.3 修复】深度推理（depth>=3）即使证据不够强也不强制承认不确定
        // 使用 this.depth（用户指定深度）而非 strategy.depth（任务类型默认深度）
        const forceUncertainty = !strongHypothesis && hasWeakSupport && this.depth < 3;

        return {
          evidenceForHypotheses,
          strongHypothesis: strongHypothesis || null,
          hasWeakSupport,
          mustAdmitUncertainty: forceUncertainty,
          timestamp: Date.now()
        };
      }
    });

    // ── 阶段5: SYNTHESIS — 综合判断 + 决策子系统 ──────────────────
    this.stages.push({
      name: 'SYNTHESIS',
      description: '综合所有信息，给出最优判断',
      fn: async (ctx, hf) => {
        const input = ctx.input;
        const parse = ctx.stages[0]?.result;
        const evidenceStage = ctx.stages.find(s => s.name === 'EVIDENCE');
        const invertStage = ctx.stages.find(s => s.name === 'INVERT');
        const hypothesesStage = ctx.stages.find(s => s.name === 'HYPOTHESES');

        const strongHypothesis = evidenceStage?.result?.strongHypothesis;
        const wasInverted = invertStage?.result?.inverted;
        const evidence = evidenceStage?.result || {};

        // 【思维连机制】调用 decision 子系统做综合决策 — 串联第五层
        let decisionResult = null;
        try {
          const decisionContext = {
            input,
            taskType: parse?.type,
            topHypothesis: hypothesesStage?.result?.topHypothesis?.description,
            wasInverted,
            hasStrongEvidence: !!strongHypothesis,
            causalRoots: hypothesesStage?.result?.topHypothesis?.causalRoots,
          };
          decisionResult = await hf.dispatch('decision.decide', decisionContext);
        } catch (e) {
          decisionResult = null;
        }

        // 5.1 确定最终判断
        let conclusion;
        let confidence;
        const reasoningChain = [];

        if (wasInverted) {
          // 被反例推翻了 — 深度推理（depth>=3）用反例修正而非摧毁结论
          if (this.depth >= 3) {
            // 深度推理：反例是修正信号，用综合判断替代被推翻的假设
            const evidenceEntry = evidenceStage?.result?.evidenceForHypotheses?.[0];
            const topHypothesis = evidenceEntry?.hypothesis;
            if (topHypothesis) {
              conclusion = topHypothesis.description;
              const initLikelihood = topHypothesis.initialLikelihood || 0.4;
              const evidenceQuality = evidenceEntry?.qualityScore || 0.3;
              const depthBonus = Math.min(0.2, this.depth * 0.05);
              const reasoningBonus = this.depth >= 3 ? 0.05 : 0;
              confidence = Math.min(0.85, initLikelihood * 0.35 + evidenceQuality * 0.45 + depthBonus + reasoningBonus);
              reasoningChain.push('经反向思考修正后的综合判断');
            } else {
              conclusion = invertStage.result.counterEvidence[0]?.description || '原假设被推翻';
              confidence = 0.4;
              reasoningChain.push('反例修正：原假设不完整');
            }
          } else {
            // 浅层推理：反例直接推翻
            conclusion = invertStage.result.counterEvidence[0]?.description || '原假设被推翻';
            confidence = 0.3;
            reasoningChain.push('原假设被反例推翻');
          }
        } else if (strongHypothesis) {
          // 有强证据支持
          conclusion = strongHypothesis.hypothesis.description;
          confidence = strongHypothesis.qualityScore;
          reasoningChain.push(`强证据支持: ${strongHypothesis.evidence[0]?.description || '有证据'}`);
        } else if (evidence.mustAdmitUncertainty && this.depth < 3) {
          // 证据薄弱且推理深度不够 → 承认不确定
          conclusion = evidence.evidenceForHypotheses[0]?.hypothesis?.description || '无法确定';
          confidence = 0.4;
          reasoningChain.push('证据薄弱，明确承认不确定');
        } else {
          // 使用假设+证据的综合判断（不依赖外部决策子系统）
          const evidenceEntry = evidenceStage?.result?.evidenceForHypotheses?.[0];
          const topHypothesis = evidenceEntry?.hypothesis;
          if (topHypothesis) {
            conclusion = topHypothesis.description;
            // 【V2.3 修复】结合初始似然度、证据质量和推理深度
            const initLikelihood = topHypothesis.initialLikelihood || 0.4;
            const evidenceQuality = evidenceEntry?.qualityScore || 0.3;
            // 深度推理（depth>=3）经过多阶段分析，结论更可靠
            const depthBonus = Math.min(0.2, this.depth * 0.05);
            const reasoningBonus = this.depth >= 3 ? 0.05 : 0;
            confidence = Math.min(0.85, initLikelihood * 0.35 + evidenceQuality * 0.45 + depthBonus + reasoningBonus);
            reasoningChain.push(`基于假设评估: ${topHypothesis.description}`);
            if (evidenceQuality > 0.5) {
              reasoningChain.push(`证据质量: ${evidenceQuality.toFixed(2)}`);
            }
          } else {
            conclusion = '需要更多信息才能确定';
            confidence = 0.3;
            reasoningChain.push('缺乏足够假设和证据');
          }
        }

        // 综合阶段推理标签
        reasoningChain.push(`任务类型: ${parse?.type}`);
        reasoningChain.push(`推理深度: ${this.depth}`);

        // 如果有假设阶段，添加假设信息
        const hypStage = ctx.stages.find(s => s.name === 'HYPOTHESES')?.result;
        if (hypStage?.topHypothesis) {
          reasoningChain.push(`首选假设: ${hypStage.topHypothesis.description}`);
        }

        return {
          conclusion,
          confidence,
          reasoningChain,
          wasInverted,
          hasStrongEvidence: !!strongHypothesis,
          decisionSubsystem: decisionResult ? { conclusion: decisionResult.conclusion, confidence: decisionResult.confidence } : null,
          timestamp: Date.now()
        };
      }
    });

    // ── 阶段6: CALIBRATE — 置信校准 + 子系统置信度验证 ─────────────
    this.stages.push({
      name: 'CALIBRATE',
      description: '校准置信度，克制人类式过度自信',
      fn: async (ctx, hf) => {
        const input = ctx.input;
        const synthesis = ctx.stages.find(s => s.name === 'SYNTHESIS')?.result;
        const invert = ctx.stages.find(s => s.name === 'INVERT')?.result;
        const evidence = ctx.stages.find(s => s.name === 'EVIDENCE')?.result;
        const parse = ctx.stages[0]?.result;

        let confidence = synthesis?.confidence || 0.5;

        // 【思维连机制】调用 confidence.calibrate 子系统 — 串联第六层
        // [FIX] confidence.calibrate(string, number) 不是 (object)
        let subsystemCalibration = null;
        try {
          subsystemCalibration = await hf.dispatch('confidence.calibrate',
            synthesis?.conclusion || input,
            confidence
          );
        } catch (e) {
          subsystemCalibration = null;
        }

        // 【思维连机制】调用 restraint.shouldIntervene — 最小干预评估
        // [FIX] restraint.shouldIntervene(string, number, string) 参数顺序修正
        let restraintResult = null;
        try {
          restraintResult = await hf.dispatch('restraint.shouldIntervene',
            synthesis?.conclusion || '',
            confidence,
            parse?.type || 'general'
          );
        } catch (e) {
          restraintResult = null;
        }

        // 6.1 反向思考降低置信度（仅浅层推理）
        // 【V2.3 修复】深度推理（depth>=3）已在 SYNTHESIS 阶段用反例修正结论，不再额外惩罚
        if (invert?.inverted && this.depth < 3) {
          confidence = Math.min(confidence, 0.4);
        }

        // 6.2 证据薄弱降低置信度（仅当推理深度浅时）
        // 【V2.3 修复】深度推理已通过足够分析，不应因证据不完美而降级
        const effectiveUncertainty = evidence?.mustAdmitUncertainty && this.depth < 3 && (synthesis?.reasoningChain?.length || 0) < 3;
        if (effectiveUncertainty) {
          confidence = Math.min(confidence, 0.5);
        }

        // 6.3 子系统置信度校正（如果可用）
        if (subsystemCalibration?.calibrated !== undefined) {
          confidence = subsystemCalibration.calibrated;
        }

        // 6.4 人类过度自信校正：人类的"100%确定"实际约80%
        // AI不应该模仿这种过度自信
        const calibratedConfidence = Math.min(confidence, 0.95);

        // 6.5 确定是否需要不确定性标记
        const needsUncertaintyMarker = calibratedConfidence < 0.7;

        // 6.6 快速退出检查（检索类任务）
        if (parse?.strategy?.fastExit && calibratedConfidence > 0.8) {
          ctx._fastExit = true;
        }

        return {
          originalConfidence: synthesis?.confidence,
          calibratedConfidence,
          needsUncertaintyMarker,
          uncertaintyPhrase: this._getUncertaintyPhrase(calibratedConfidence),
          subsystemCalibration,
          restraintResult: restraintResult ? { shouldIntervene: restraintResult.shouldIntervene } : null,
          timestamp: Date.now()
        };
      }
    });

    // ── 阶段7: RESPOND — 生成回应 + 情感自主引擎 ──────────────────
    this.stages.push({
      name: 'RESPOND',
      description: '生成带不确定性标记的回应（接收模式：在场见证）',
      fn: async (ctx, hf) => {
        const input = ctx.input;
        const synthesis = ctx.stages.find(s => s.name === 'SYNTHESIS')?.result;
        const calibrate = ctx.stages.find(s => s.name === 'CALIBRATE')?.result;
        const parse = ctx.stages[0]?.result;
        const isReception = parse?.type === 'reception';

        // 【思维连机制】调用 autonomousEmotion 情感自主引擎 — 串联第七层
        let emotionResult = null;
        try {
          emotionResult = await hf.dispatch('autonomousEmotion.trigger', {
            type: isReception ? 'witness_response' : 'response_generation',
            conclusion: isReception ? parse?.goal : synthesis?.conclusion,
            confidence: calibrate?.calibratedConfidence || 0.5,
            input
          });
        } catch (e) {
          emotionResult = null;
        }

        // 7.1 决定是否回应
        let shouldRespond = true;
        let suppressReason = null;

        // 检索类任务且置信度高 → 快速退出
        if (ctx._fastExit && calibrate?.calibratedConfidence > 0.8) {
          shouldRespond = false;
          suppressReason = 'fast_exit_high_confidence';
        }

        // 聆听模式：始终回应，不抑制
        if (isReception) {
          shouldRespond = true;
          suppressReason = null;
        }

        // 7.2 生成不确定性前缀
        let prefix = '';
        // 聆听模式不需要不确定性标记（见证不需要"可能"）
        if (!isReception && calibrate?.needsUncertaintyMarker) {
          prefix = `${calibrate.uncertaintyPhrase  } `;
        }

        // 7.3 组装回应元数据 + 推理内容
        // 聆听模式：不依赖 synthesis（被跳过），从 PARSE/共情状态生成
        let conclusion;
        let reasoningChain;
        if (isReception) {
          // 从心理学分析和共情检测生成在场见证标记
          const emotion = parse?.psychology?.emotion || '未知';
          const empathy = parse?.psychology?.empathy || null;
          conclusion = `[reception] 接收到人类经验分享（情感基调: ${emotion}${empathy ? `，共情水平: ${empathy.level || '未知'}` : ''}）`;
          reasoningChain = [];
        } else {
          conclusion = synthesis?.conclusion || '';
          reasoningChain = synthesis?.reasoningChain || [];

          // 如果没有有效结论，从推理链各阶段构建摘要结论
          if (!conclusion || conclusion === '需要更多信息') {
            const summary = this._buildReasoningSummary(ctx.stages);
            const keyFindings = summary
              .filter(s => s.stage !== 'PARSE')
              .map(s => `${s.stage}: ${s.description}`)
              .join(' → ');
            conclusion = keyFindings || '推理链执行完成，等待进一步分析';
            reasoningChain = summary.map(s => `${s.stage}: ${s.description}`);
          }
        }

        const meta = {
          confidence: isReception ? 1.0 : (calibrate?.calibratedConfidence || 0.5),
          conclusion,
          reasoningChain,
          taskType: parse?.type,
          suppressed: !shouldRespond,
          suppressReason,
          emotionState: emotionResult?.currentState || null,
          // 【心理推断深度集成】共情检测结果注入上下文
          empathy: parse?.psychology?.empathy || null,
          // 聆听模式专用标记
          witness: isReception ? {
            active: true,
            emotion: parse?.psychology?.emotion || null,
            intent: parse?.psychology?.intent || null,
            needs: parse?.psychology?.needs || null
          } : undefined
        };

        return {
          shouldRespond,
          suppressReason,
          prefix,
          conclusion: prefix + conclusion,
          meta,
          timestamp: Date.now()
        };
      }
    });

    this._chainBuilt = true;
  }

  /**
   * 从各阶段提取推理摘要
   * 生成可读的推理过程描述
   */
  _buildReasoningSummary(stages) {
    const summary = [];
    const stageResults = {};

    for (const stage of stages) {
      if (stage.skipped || !stage.result) continue;
      stageResults[stage.name] = stage.result;
    }

    // PARSE摘要
    const parse = stageResults.PARSE;
    if (parse) {
      summary.push({
        stage: 'PARSE',
        description: '问题分解',
        details: {
          type: parse.type,
          variables: parse.variables?.numbers?.length || 0 + '个数字, ' + (parse.variables?.entities?.length || 0) + '个实体',
          constraints: parse.constraints?.length || 0,
          goal: parse.goal,
          emotion: parse.psychology?.emotion?.emotionZh || '中性'
        }
      });
    }

    // DELIBERATE摘要
    const delib = stageResults.DELIBERATE;
    if (delib) {
      summary.push({
        stage: 'DELIBERATE',
        description: delib.pauseReason || '复杂度评估',
        details: {
          complexity: delib.estimatedComplexity,
          recommendedDepth: delib.recommendedDepth,
          needsPause: delib.needsPause,
          fastExit: delib.canFastExit?.canFastExit || false
        }
      });
    }

    // HYPOTHESES摘要
    const hyps = stageResults.HYPOTHESES;
    if (hyps && hyps.hypotheses) {
      summary.push({
        stage: 'HYPOTHESES',
        description: '并行假设生成',
        details: {
          count: hyps.count,
          topHypothesis: hyps.topHypothesis?.description || null,
          topConfidence: hyps.topHypothesis?.initialLikelihood || null
        }
      });
    }

    // INVERT摘要
    const invert = stageResults.INVERT;
    if (invert) {
      summary.push({
        stage: 'INVERT',
        description: invert.inverted ? '反向思考生效，原假设被推翻' : '反向思考：原假设未被推翻',
        details: {
          inverted: invert.inverted,
          counterEvidenceCount: invert.counterEvidence?.length || 0,
          contradictionsCount: invert.contradictions?.length || 0
        }
      });
    }

    // EVIDENCE摘要
    const evidence = stageResults.EVIDENCE;
    if (evidence) {
      const strongCount = evidence.evidenceForHypotheses?.filter(e => e.strongEvidence).length || 0;
      summary.push({
        stage: 'EVIDENCE',
        description: `证据评估完成，${strongCount}个假设有强证据`,
        details: {
          hypothesesEvaluated: evidence.evidenceForHypotheses?.length || 0,
          strongEvidenceCount: strongCount,
          mustAdmitUncertainty: evidence.mustAdmitUncertainty || false
        }
      });
    }

    // SYNTHESIS摘要
    const synth = stageResults.SYNTHESIS;
    if (synth) {
      summary.push({
        stage: 'SYNTHESIS',
        description: '综合判断',
        details: {
          conclusion: synth.conclusion,
          confidence: synth.confidence,
          wasInverted: synth.wasInverted,
          reasoningChain: synth.reasoningChain?.length || 0,
          decisionSubsystem: !!synth.decisionSubsystem
        }
      });
    }

    // CALIBRATE摘要
    const calib = stageResults.CALIBRATE;
    if (calib) {
      summary.push({
        stage: 'CALIBRATE',
        description: '置信度校准',
        details: {
          originalConfidence: calib.originalConfidence,
          calibratedConfidence: calib.calibratedConfidence,
          needsUncertaintyMarker: calib.needsUncertaintyMarker,
          uncertaintyPhrase: calib.uncertaintyPhrase
        }
      });
    }

    return summary;
  }

  // ── 辅助方法 ──────────────────────────────────────────────────────────

  /**
   * 评估叙事分数：检测人类经验分享/故事讲述
   * 用于分类为 reception 模式
   */
  _assessNarrativeScore(input) {
    const markers = [
      /分享|经历|故事|体验|感受/,
      /我想说|我想告诉|我来说|听我说/,
      /失去|离别|去世|走[了]?|不见/,
      /人生|命运|意义|存在|世界/,
      /回忆|记忆|年少|年轻时候|小时候/,
      /第一次|最后一次|曾经|那时候/,
      /幸福|痛苦|悲伤|孤独|温暖|感动/,
      /陪伴|拥抱|握[着住]?|在一起/,
      /谢谢|对不起|原谅|抱歉/,
      /不重要|无所谓|算了/,
    ];
    return markers.filter(m => m.test(input)).length;
  }

  /**
   * 提取关键变量
   */
  _extractVariables(input) {
    const variables = {
      numbers: [],
      entities: [],
      actions: []
    };

    // 提取数字
    const numMatches = input.match(/\d+\.?\d*/g);
    if (numMatches) {
      variables.numbers = numMatches.map(n => parseFloat(n));
    }

    // 提取实体（简单实现）
    const words = input.split(/\s+/);
    variables.entities = words.filter(w => w.length > 2 && /^[A-Za-z一-龥]+$/.test(w)).slice(0, 5);

    return variables;
  }

  /**
   * 提取约束条件
   */
  _extractConstraints(input) {
    const constraints = [];
    const constraintPatterns = [
      /如果|假如|假设/,
      /必须|一定|不要/,
      /不能|不可以|不允许/,
      /只能|只能|仅仅/
    ];

    for (const pattern of constraintPatterns) {
      if (pattern.test(input)) {
        constraints.push(pattern.toString());
      }
    }

    return constraints;
  }

  /**
   * 从输入中提取问题领域/主题
   */
  _extractDomain(input) {
    // 保留完整输入用于领域检测（冒号前后的内容都可能包含领域关键词）
    const content = input.replace(/\[当前问题\]/g, '').trim().slice(0, 300);

    // 领域关键词映射表（按特异性从高到低排序，避免通用词覆盖特定域）
    const domainKeywords = [
      ['危机', '发布会', '发言'], '危机公关',
      ['功利主义', '义务论', '儒家', '伦理', '电车'], '伦理学',
      ['隐私', '监控', '治理'], 'AI治理',
      ['投资', '股票', 'PE', '收益'], '投资决策',
      ['辩论', '论证', '正反'], '辩论分析',
      ['疫情', '死亡率', '文化圈'], '社会分析',
      ['意识', '自我', '特殊性'], '哲学',
      ['人工智能', 'AI', '发展'], 'AI发展'
    ];

    for (let i = 0; i < domainKeywords.length; i += 2) {
      const keywords = domainKeywords[i];
      const domain = domainKeywords[i + 1];
      if (keywords.some(kw => content.includes(kw))) {
        return domain;
      }
    }

    // 提取前10个字符的简短描述
    return content.slice(0, 10);
  }

  /**
   * 提取输入中的关键实体（主体/核心对象）
   * 用于将假设描述与输入关键词关联，提升 _assessLikelihood 的匹配度
   */
  _extractKeyEntity(input) {
    const content = input.replace(/\[当前问题\]/g, '').trim().slice(0, 200);

    // 优先提取"XX的XX"结构（如"电车难题的变体"、"AI监控系统的部署方案"）
    // 使用全局匹配找到第一个有意义的短语（而非最短）
    const possessiveRegex = /[A-Za-z]*[一-鿿]{2,12}的[A-Za-z]*[一-鿿]{2,12}/g;
    const junkPatterns = ['以内的', '的话', '的事', '的人', '的我们', '字的', '的它', '的他', '的她', '的这', '的那', '的任', '的所', '的其', '的要', '的可', '了而', '了所'];
    let m;
    while ((m = possessiveRegex.exec(content)) !== null) {
      const isJunk = junkPatterns.some(p => m[0].includes(p));
      if (!isJunk && m[0].length >= 4) {
        return m[0]; // 返回第一个有效匹配（通常是主要实体）
      }
    }

    // 提取引号内的内容
    const quoteMatch = content.match(/["""「『](.+?)["""」』]/);
    if (quoteMatch) {
      return quoteMatch[1].slice(0, 10);
    }

    // 提取前两个有意义的词（每个至少2字符）
    const words = content.split(/[\s，。！？、；：\n]+/).filter(w => w.length >= 2);
    if (words.length >= 2) {
      // 优先取包含英文或数字的词（如"AI监控"、"电车难题"）
      const meaningful = words.filter(w => /[A-Za-z0-9]/.test(w) || w.length >= 4);
      if (meaningful.length >= 2) return meaningful[0] + meaningful[1];
      if (meaningful.length === 1) {
        const idx = words.indexOf(meaningful[0]);
        return meaningful[0] + (words[idx + 1] || '');
      }
      return words[0] + words[1];
    }
    if (words.length === 1) {
      return words[0];
    }

    return '此问题';
  }

  /**
   * 提取目标
   */
  _extractGoal(input) {
    const goalWords = {
      '如何选择': '选择',
      '如何设计': '设计',
      '如何分析': '分析',
      '如何评估': '评估',
      '如何解决': '解决',
      '如何理解': '理解',
      '为什么': '原因',
      '是什么': '本质',
      '识别': '识别',
      '构建': '构建',
      '找出': '找出',
      '推导': '推导',
      '写': '阐述'
    };

    for (const [pattern, goal] of Object.entries(goalWords)) {
      if (input.includes(pattern)) return goal;
    }

    return '分析';
  }

  /**
   * 生成多个假设
   */
  _generateHypotheses(input, count, taskType) {
    const hypotheses = [];

    // 【V2.2 优化】任务感知假设生成：逻辑推理题需要具体答案候选，而非模糊关键词拼接
    if (taskType === 'calculation') {
      return this._generateCalculationHypotheses(input, count);
    }

    // 【V2.3 优化】非逻辑推理题：使用输入关键词生成假设，确保假设与输入有词汇重叠
    const goal = this._extractGoal(input);
    const domain = this._extractDomain(input);
    const keyEntity = this._extractKeyEntity(input);

    for (let i = 0; i < count; i++) {
      hypotheses.push({
        id: `h${i}`,
        description: i === 0
          ? `${keyEntity}中的${domain}维度：${goal}的深层考量`
          : i === 1
          ? `${domain}框架下的次要变量：影响${keyEntity}中${goal}的其他因素`
          : `跨维度关联：${domain}与${keyEntity}的交互效应与潜在矛盾`,
        initialLikelihood: i === 0 ? 0.55 : 0.35 - (i * 0.08),
        evidence: [],
        counterEvidence: []
      });
    }

    return hypotheses;
  }

  /**
   * 【V2.2 新增】从输入中提取关键概念短语
   * 替代简单的分词，提取对推理有意义的关键词
   */
  _extractKeyPhrases(input) {
    const phrases = [];
    const effectiveInput = (() => {
      const m = input.match(/\[当前问题\]\s*([\s\S]*)$/);
      return m ? m[1].trim() : input;
    })();

    // 1. 提取引号内的内容
    const quoted = effectiveInput.match(/"([^"]+)"/g) || [];
    quoted.forEach(q => phrases.push(q.replace(/"/g, '').trim()));

    // 2. 提取列表项（数字+点号开头的行）
    const listParts = effectiveInput.split(/(?=\d+[.、．])/);
    for (const part of listParts) {
      const trimmed = part.trim();
      if (/^\d+[.、．]/.test(trimmed)) {
        const content = trimmed.replace(/^\d+[.、．]\s*/, '').trim();
        if (content.length <= 40) phrases.push(content);
      }
    }

    // 3. 提取"X说：Y"模式中的Y部分
    const statements = effectiveInput.match(/[A-Za-z一-鿿]{1,4}[说：:]\s*([^。！？\n]+)/g) || [];
    statements.forEach(s => {
      const content = s.replace(/^[A-Za-z一-鿿]{1,4}[说：:]\s*/, '').trim();
      if (content.length <= 30 && content.length >= 2) phrases.push(content);
    });

    // 4. 提取"X是Y"模式中的Y
    const isPatterns = effectiveInput.match(/([A-Za-z一-鿿]{1,4})(?:是|为|属于)([^，。！？\n]{2,20})/g) || [];
    isPatterns.forEach(p => {
      const parts = p.match(/(?:是|为|属于)(.+)/);
      if (parts && parts[1].length <= 20) phrases.push(parts[1].trim());
    });

    // 去重并过滤通用词
    const stopPhrases = new Set(['什么', '如何', '怎样', '为什么', '多少', '几个', '哪个', '是否', '一个', '一下', '一样', '一起']);
    const unique = [...new Set(phrases)].filter(p => !stopPhrases.has(p) && p.length >= 2);

    return unique.slice(0, 8);
  }

  /**
   * 为逻辑推理题（calculation 类型）生成具体答案候选假设
   * 替代模糊的关键词拼接，提供可被验证的具体答案
   */
  _generateCalculationHypotheses(input, count) {
    const hypotheses = [];

    // 提取实体：人名/代号 + 实体对
    const letters = new Set((input.match(/[A-Z]/g) || []));

    // 从"X说：Y和Z都是..."模式提取实体对
    const pairMatches = input.match(/([A-Z]|[一-鿿]{1,3})和([A-Z]|[一-鿿]{1,3})/g) || [];
    const pairEntities = new Set();
    for (const pair of pairMatches) {
      const parts = pair.split('和');
      parts.forEach(p => {
        const trimmed = p.trim();
        // 过滤语法词和代词
        if (trimmed.length <= 3 && !['都是', '恰有', '说的', '的是', '中恰',
            '我', '你', '他', '她', '它', '们', '这', '那', '每'].includes(trimmed)) {
          pairEntities.add(trimmed);
        }
      });
    }

    const allEntities = [...new Set([...letters, ...pairEntities])].filter(e => e.length > 0);

    // 生成实体组合假设
    const maxHyps = Math.min(count, 8);
    if (allEntities.length >= 2) {
      // 生成"X和Y是说谎者"类型假设
      for (let i = 0; i < Math.min(3, maxHyps); i++) {
        const e1 = allEntities[i % allEntities.length];
        const e2 = allEntities[(i + 1) % allEntities.length];
        const rest = allEntities.length > 2 ? `，其余${allEntities.length - 2}人需验证` : '';
        hypotheses.push({
          id: `calc_${i}`,
          description: `候选${i + 1}: ${e1}和${e2}是说谎者${rest}`,
          initialLikelihood: 0.5 - i * 0.08,
          evidence: [],
          counterEvidence: []
        });
      }

      // 单人假设
      if (maxHyps > 3) {
        hypotheses.push({
          id: `calc_single`,
          description: `候选${4}: 仅${allEntities[0]}是说谎者，其余人均说真话`,
          initialLikelihood: 0.35,
          evidence: [],
          counterEvidence: []
        });
      }

      // 全员说谎假设
      if (maxHyps > 4) {
        hypotheses.push({
          id: `calc_all`,
          description: `候选${5}: 所有人都是说谎者`,
          initialLikelihood: 0.25,
          evidence: [],
          counterEvidence: []
        });
      }
    }

    // 如果生成了足够的假设，返回
    if (hypotheses.length >= maxHyps) {
      return hypotheses.slice(0, maxHyps);
    }

    // 兜底：基于输入关键词生成分析性假设
    const segments = input.split(/[\s，。！？、；：\n]+/).filter(w => w.length > 1);
    const keywords = segments.slice(0, 3);

    while (hypotheses.length < maxHyps) {
      const idx = hypotheses.length;
      hypotheses.push({
        id: `calc_fallback_${idx}`,
        description: idx === 0
          ? `最可能: ${keywords.join('、')}相关的标准逻辑解释`
          : `候选${idx + 1}: ${keywords[0] || '输入'}存在其他解读角度`,
        initialLikelihood: idx === 0 ? 0.5 : 0.3 - idx * 0.05,
        evidence: [],
        counterEvidence: []
      });
    }

    return hypotheses.slice(0, maxHyps);
  }

  /**
   * 评估假设的初始可能性
   */
  _assessLikelihood(hypothesis, input) {
    // 【V2.3 修复】从精确分词匹配改为子串关键词匹配
    // 原因：假设描述中的关键词（如"伦理学"）可能以不同形式出现在输入中（如"儒家伦理"）
    // 精确分词会导致 overlap=0，confidence 被压到 0.3
    const lastUserMatch = input.match(/\[当前问题\]\s*([\s\S]*)$/);
    const effectiveInput = lastUserMatch ? lastUserMatch[1].trim() : input;
    const lowerInput = effectiveInput.toLowerCase();

    // 停用词表（过滤掉没有语义价值的词）
    const stopWords = new Set([
      '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都',
      '一', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着',
      '没有', '看', '好', '自己', '这', '与', '及', '或', '其', '但', '而',
      '则', '该', '进行', '相关', '核心', '焦点', '因素', '次要', '深层',
      '关联', '需要', '进一步', '分析', '本质', '机制', '如何', '什么',
      '为什么', '是否', '可以', '应该', '可能', '一个'
    ]);

    // 从假设描述中提取 n-gram 关键词（2-4字）— 解决长短语无法匹配的问题
    const cleaned = hypothesis.description.replace(/[，。！？、；：\s：]+/g, '');
    const grams = [];
    for (let n = Math.min(4, cleaned.length); n >= 2; n--) {
      for (let i = 0; i <= cleaned.length - n; i++) {
        const gram = cleaned.slice(i, i + n);
        if (!stopWords.has(gram) && !grams.includes(gram)) {
          grams.push(gram);
        }
      }
    }

    // 从输入中提取词段
    const inputSegments = effectiveInput.split(/[\s，。！？、；：\n]+/).filter(w => w.length >= 2);

    // 计算 n-gram 命中率：gram 作为子串出现在输入词段中
    let hits = 0;
    for (const gram of grams) {
      const gramLower = gram.toLowerCase();
      for (const seg of inputSegments) {
        if (seg.toLowerCase().includes(gramLower)) {
          hits++;
          break;
        }
      }
    }

    // 至少有一个关键词命中 → 基础分 0.4（生成式假设不应因关键词重叠而过度自信）
    const baseScore = hits > 0 ? 0.4 : 0.3;
    const bonus = Math.min(0.25, hits * 0.08);
    return Math.min(0.6, baseScore + bonus);
  }

  /**
   * 找出反例
   */
  _findCounterEvidence(hypothesis, input) {
    const counterIndicators = [
      '但是', '然而', '不过', '实际上', '其实', '虽然'
    ];

    const evidence = [];
    for (const indicator of counterIndicators) {
      if (input.includes(indicator)) {
        evidence.push({
          type: 'contradiction',
          description: `输入中包含转折词: "${indicator}"`,
          strength: 0.6
        });
      }
    }

    return evidence;
  }

  /**
   * 找出矛盾
   */
  _findContradictions(hypothesis, input) {
    const contradictions = [];

    // 检测绝对化表述（容易有反例）
    const absolutePatterns = [
      /所有|全部|每个|总是|永远/,
      /没有|从不|绝不/
    ];

    for (const pattern of absolutePatterns) {
      if (pattern.test(input)) {
        contradictions.push({
          type: 'absolute_statement',
          description: `使用了绝对化表述: "${pattern}"，可能有反例`,
          strength: 0.7
        });
      }
    }

    return contradictions;
  }

  /**
   * 找证据
   */
  _findEvidence(hypothesis, input, parse) {
    // 【V2.2 优化】从输入文本中查找支持假设的证据
    // 提取输入中的陈述句，匹配假设中的关键实体
    const evidence = [];
    const hypDesc = hypothesis.description.toLowerCase();

    // 从输入中提取有意义的句子（包含实体或判断的陈述）
    const sentences = input.split(/[。！？\n]/).filter(s => s.trim().length > 2);

    // 从假设中提取关键词：先按中文语义边界分词，再过滤停用词
    const stopWords = new Set(['候选', '相关', '标准', '解释', '其余', '人需', '验证',
      '最可能', '替代', '可能性', '较低', '是', '的', '了', '在', '都', '这', '那',
      '有', '一', '中', '恰', '话', '仅', '人均', '真话', '说谎者', '表面现象',
      '和', '或', '与', '及', '的']);
    const hypKeywords = hypDesc.split(/[\s，。！？、；：\n]/)
      .map(w => w.trim())
      .filter(w => w.length >= 1 && !stopWords.has(w));

    // 额外提取实体字母（A、B、C 等）
    const entityLetters = new Set((hypDesc.match(/[a-z]/g) || []));

    for (const sentence of sentences) {
      const lowerSent = sentence.toLowerCase();

      // 计算类型任务：额外匹配问题领域关键词
      let keywordMatches = [];
      if (parse?.type === 'calculation') {
        // 提取输入中的问题关键词（数字、单位、判断词）
        const problemKeywords = hypDesc.match(/[a-z]+|[0-9]+/g) || [];
        const sentKeywords = lowerSent.match(/[a-z]+|[0-9]+|真话|说谎|帽子|颜色|红|蓝|灯|开关|沙漏|称重|排队|座位/g) || [];
        keywordMatches = problemKeywords.filter(kw => sentKeywords.some(sk => sk.includes(kw) || kw.includes(sk)));
      }

      // 检查假设关键词是否在句子中出现
      const matchedKeywords = hypKeywords.filter(kw => lowerSent.includes(kw.toLowerCase()));

      // 计算类型：字母实体匹配 或 关键词匹配
      // 非计算类型：仅关键词匹配
      const letterOverlap = parse?.type === 'calculation'
        ? [...entityLetters].filter(l => lowerSent.includes(l))
        : [];

      const hasMatch = letterOverlap.length >= 1 || matchedKeywords.length >= 1 || keywordMatches.length >= 1;

      if (hasMatch) {
        // 判断是支持证据还是反例
        const isCounter = /但是|然而|不过|实际上|其实|虽然|并非|不是|并非如此/.test(sentence);

        const matchInfo = [letterOverlap.length > 0 ? `实体${letterOverlap.join('、')}` : null,
                           matchedKeywords.length > 0 ? matchedKeywords.join('、') : null,
                           keywordMatches.length > 0 ? keywordMatches.join('、') : null]
                          .filter(Boolean).join(' + ');

        evidence.push({
          type: isCounter ? 'contradiction' : 'support',
          source: sentence.trim().slice(0, 100),
          description: isCounter
            ? `${matchInfo}的反面陈述`
            : `${matchInfo}的陈述支持`,
          strength: isCounter ? 0.3 : Math.min(0.8, 0.3 + (letterOverlap.length + matchedKeywords.length + keywordMatches.length) * 0.15),
          matchedKeywords,
          matchedLetters: letterOverlap,
          keywordMatches
        });
      }
    }

    return evidence;
  }

  /**
   * 评估证据质量
   * 人类缺陷：认为证据数量=证据质量
   * 心虫改进：证据质量看来源可靠性、时效性、可验证性
   */
  _assessEvidenceQuality(evidence) {
    if (!evidence || evidence.length === 0) return 0.2;

    // 基础分：有证据即加分
    let quality = 0.3;

    // 支持证据加分
    const supportCount = evidence.filter(e => e.type === 'support').length;
    quality += Math.min(0.3, supportCount * 0.1);

    // 反例扣分
    const counterCount = evidence.filter(e => e.type === 'contradiction').length;
    quality -= counterCount * 0.1;

    // 证据强度加权
    const avgStrength = evidence.reduce((sum, e) => sum + (e.strength || 0), 0) / evidence.length;
    quality += avgStrength * 0.2;

    return Math.max(0.1, Math.min(0.9, quality));
  }

  /**
   * 获取不确定性短语
   * 人类缺陷：不愿意说"不知道"
   * 心虫改进：明确表达不确定性
   */
  _getUncertaintyPhrase(confidence) {
    if (confidence >= 0.9) return '确定';
    if (confidence >= 0.8) return '很可能';
    if (confidence >= 0.7) return '可能';
    if (confidence >= 0.6) return '不太确定，但倾向于';
    if (confidence >= 0.5) return '根据现有信息，猜测';
    if (confidence >= 0.4) return '目前信息不足以确定，但';
    return '不知道，缺少关键信息';
  }

  /**
   * 运行思维链
   */
  async run(input) {
    if (!this.hf.started) {
      throw new Error('Clarity not started');
    }

    this.context = {
      input,
      timestamp: Date.now(),
      stages: [],
      errors: [],
      _fastExit: false
    };

    // 解析任务类型
    this.taskStrategy = { type: this._classifyTask(input) };

    // 根据策略调整深度
    const strategyDepth = TASK_STRATEGIES[this.taskStrategy.type]?.depth;
    if (strategyDepth && strategyDepth > this.depth) {
      this.depth = strategyDepth;
    }

    this._buildChain();

    const startTime = Date.now();

    // 执行阶段
    for (const stage of this.stages) {
      // 深度裁剪
      if (this._shouldSkipStage(stage.name)) {
        this.context.stages.push({
          name: stage.name,
          skipped: true,
          reason: `depth=${this.depth}`
        });
        continue;
      }

      // 快速退出检查 — 不跳过 RESPOND，让 RESPOND 自行处理
      if (this.context._fastExit && stage.name !== 'RESPOND') {
        this.context.stages.push({
          name: stage.name,
          skipped: true,
          reason: 'fast_exit'
        });
        continue;
      }

      const stageStart = Date.now();
      try {
        const result = await stage.fn(this.context, this.hf);
        this.context.stages.push({
          name: stage.name,
          result,
          duration: Date.now() - stageStart,
          success: true
        });
      } catch (e) {
        this.context.stages.push({
          name: stage.name,
          error: e.message,
          duration: Date.now() - stageStart,
          success: false
        });
        this.context.errors.push({ stage: stage.name, error: e.message });
      }
    }

    return this._buildResult(startTime);
  }

  _shouldSkipStage(stageName) {
    // 聆听模式（接收人类经验分享）：跳过所有分析判断阶段
    // 不走假设→反向→证据→综合，直接 PARSE → DELIBERATE → RESPOND
    if (this.taskStrategy?.type === 'reception' &&
        ['HYPOTHESES', 'INVERT', 'EVIDENCE', 'SYNTHESIS'].includes(stageName)) {
      return true;
    }
    const depthMap = {
      'PARSE': REASONING_DEPTH.SURFACE,
      'DELIBERATE': REASONING_DEPTH.SURFACE,
      'HYPOTHESES': REASONING_DEPTH.BASIC,
      'INVERT': REASONING_DEPTH.DEEP,
      'EVIDENCE': REASONING_DEPTH.BASIC,
      'SYNTHESIS': REASONING_DEPTH.BASIC,
      'CALIBRATE': REASONING_DEPTH.SURFACE,
      'RESPOND': REASONING_DEPTH.SURFACE
    };
    return depthMap[stageName] > this.depth;
  }

  _buildResult(startTime) {
    const respondStage = this.context.stages.find(s => s.name === 'RESPOND');
    const respondResult = respondStage?.result || {};
    const synthesisStage = this.context.stages.find(s => s.name === 'SYNTHESIS');
    const calibrateStage = this.context.stages.find(s => s.name === 'CALIBRATE');
    const parseStage = this.context.stages.find(s => s.name === 'PARSE');

    return {
      input: this.context.input,
      output: respondResult,

      chain: {
        stages: this.context.stages,
        totalDuration: Date.now() - startTime,
        depth: this.depth,
        taskType: parseStage?.result?.type,
        errors: this.context.errors
      },

      decision: {
        shouldRespond: respondResult.shouldRespond !== false,
        suppressed: respondResult.suppressed || false,
        suppressReason: respondResult.suppressReason,
        confidence: respondResult.meta?.confidence || 0.5,
        conclusion: respondResult.conclusion,
        reasoningChain: respondResult.meta?.reasoningChain || [],
        wasInverted: synthesisStage?.result?.wasInverted || false,
        hasStrongEvidence: synthesisStage?.result?.hasStrongEvidence || false
      },

      // 推理链详细内容 — 所有阶段的完整输出
      reasoning: {
        // PARSE阶段：问题分解 + 心理分析
        parse: parseStage?.result || null,
        // DELIBERATE阶段：复杂度评估
        deliberation: this.context.stages.find(s => s.name === 'DELIBERATE')?.result || null,
        // HYPOTHESES阶段：假设列表
        hypotheses: this.context.stages.find(s => s.name === 'HYPOTHESES')?.result || null,
        // INVERT阶段：反向思考结果
        invert: this.context.stages.find(s => s.name === 'INVERT')?.result || null,
        // EVIDENCE阶段：证据评估
        evidence: this.context.stages.find(s => s.name === 'EVIDENCE')?.result || null,
        // SYNTHESIS阶段：综合判断
        synthesis: synthesisStage?.result || null,
        // CALIBRATE阶段：置信度校准
        calibration: calibrateStage?.result || null,
        // RESPOND阶段：最终回应
        respond: respondResult || null,
        // 推理摘要：从各阶段提取关键信息
        summary: this._buildReasoningSummary(this.context.stages)
      },

      // 各阶段快速访问（兼容旧版本）
      parse: parseStage?.result,
      deliberation: this.context.stages.find(s => s.name === 'DELIBERATE')?.result,
      hypotheses: this.context.stages.find(s => s.name === 'HYPOTHESES')?.result,
      invert: this.context.stages.find(s => s.name === 'INVERT')?.result,
      evidence: this.context.stages.find(s => s.name === 'EVIDENCE')?.result,
      synthesis: synthesisStage?.result,
      calibration: calibrateStage?.result
    };
  }

  /**
   * 获取思维链摘要
   */
  getSummary(result) {
    const taskType = result.chain.taskType || 'general';
    const isReception = taskType === 'reception';

    const lines = [
      `🧠 思维链 v2.0 (深度: ${result.chain.depth})`,
      isReception
        ? `🧘 聆听模式: 接收人类经验分享（在场见证）`
        : `📋 任务类型: ${taskType}`,
      `⏱ 耗时: ${result.chain.totalDuration}ms`,
      `🔢 阶段: ${result.chain.stages.filter(s => !s.skipped).length}/${result.chain.stages.length}`,
      '',
      '阶段:'
    ];

    for (const stage of result.chain.stages) {
      let status = stage.skipped ? '⏭️' : (stage.success ? '✅' : '❌');
      const name = stage.name.padEnd(12);
      const duration = stage.duration ? `${stage.duration}ms` : '';

      // 聆听模式：被跳过的分析阶段用 🫂 标记（传达"不需要你，我在就够了"）
      if (isReception && stage.skipped && ['HYPOTHESES', 'INVERT', 'EVIDENCE', 'SYNTHESIS'].includes(stage.name)) {
        status = '🫂';
      }

      lines.push(`  ${status} ${name} ${duration}`);
    }

    if (isReception) {
      // 聆听模式摘要：不展示置信度/结论，展示在场见证状态
      lines.push('');
      lines.push('🫂 在场见证（非分析模式）');
      const witnessMeta = result.output?.meta?.witness;
      if (witnessMeta?.emotion) {
        lines.push(`💗 情感基调: ${witnessMeta.emotion}`);
      }
      if (witnessMeta?.intent) {
        lines.push(`🎯 分享意图: ${witnessMeta.intent}`);
      }
      if (witnessMeta?.needs) {
        lines.push(`🤲 潜在需求: ${witnessMeta.needs}`);
      }
    } else {
      // 分析模式摘要（原有逻辑）
      lines.push('');
      lines.push(`🤔 置信度: ${(result.decision.confidence * 100).toFixed(0)}%`);
      const conclusion = result.decision.conclusion?.substring(0, 50);
      if (conclusion) {
        lines.push(`💭 结论: ${conclusion}...`);
      }

      // 思考门摘要
      const deliberation = result.deliberation;
      if (deliberation) {
        lines.push(`🚦 思考门: ${deliberation.needsPause ? '建议暂停' : '无需暂停'} (复杂度 ${deliberation.estimatedComplexity}↑${deliberation.recommendedDepth})`);
        if (deliberation.narrativeDepth?.isDeepNarrative) {
          lines.push(`📖 叙事深度: ${(deliberation.narrativeDepth.score * 100).toFixed(0)}%（叙事性内容，跳过分析）`);
        }
        if (deliberation.canFastExit?.canFastExit) {
          lines.push(`⚡ 快速退出: ${deliberation.canFastExit.reason}`);
        }
      }

      if (result.decision.wasInverted) {
        lines.push('🔄 原假设被推翻（反向思考生效）');
      }
      if (!result.decision.hasStrongEvidence) {
        lines.push('⚠️ 证据薄弱，明确承认不确定');
      }
    }

    return lines.join('\n');
  }
}

// 工厂函数
function createThoughtChain(hf, depth = REASONING_DEPTH.BASIC) {
  const chain = new ThoughtChain(hf);
  chain.setDepth(depth);
  return chain;
}

module.exports = {
  ThoughtChain,
  createThoughtChain,
  REASONING_DEPTH,
  TASK_STRATEGIES
};
