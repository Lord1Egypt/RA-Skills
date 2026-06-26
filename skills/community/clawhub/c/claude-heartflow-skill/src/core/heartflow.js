/**
 /** HeartFlow v2.0.5 — 快速启动 + 两层懒加载
  *
  * 启动速度优化：只有 Tier 1 模块在 start() 时同步加载。
  * Tier 2 模块在首次 dispatch 访问时才加载（lazy require）。
  * 已有实例化的模块不受影响，只是把 require 延迟到首次访问。
  *
  * 调用方式:
  *   hf.dispatch('subsystem.method', arg1, arg2)  // 统一路由
  *   hf.verifyReasoning(r, c)                     // 直接方法
  *
  * 所有模块在 _modules registry 中注册，可通过 routes() 查看可用路由。
  */

const path = require('path');
const { ALLOWED_ROUTES, LAZY_TIER2, EAGER_NAMES, LAZY_NAMES } = require('./heartflow-routes.js');
const { getDreamFragments } = require('./dream-fragments.js');
const { recordDialogue: _recordDialogue, getDialogueHistory: _getDialogueHistory, getDialogueStats: _getDialogueStats, getDreamHistory: _getDreamHistory } = require('./dialogue-persistence.js');

// ★ 启动优化: 惰性 require — 80+ 顶层模块改为首次使用时加载
const _lazyCache = {};
function _lazy(key, loader) {
  return function() {
    if (!_lazyCache[key]) _lazyCache[key] = loader();
    return _lazyCache[key];
  };
}

// Search modules
const _BM25Engine = _lazy('bm25', () => require('./search/bm25.js'));
const _HybridSearchEngine = _lazy('hybridSearch', () => require('./search/hybrid-search.js'));
const _Budget = _lazy('budget', () => require('./budget.js'));
const _Graph = _lazy('graph', () => require('./memory/graph.js'));
const _CoreUtils = _lazy('utils', () => require('./utils.js'));
const _SearchTrace = _lazy('searchTrace', () => require('./search/search-trace.js'));
const _Slots = _lazy('slots', () => require('./memory/slots.js'));
const _Observe = _lazy('observe', () => require('./memory/observe.js'));
const _MeaningfulMemory = _lazy('meaningfulMemory', () => require('../memory/meaningful-memory.js'));
const _KnowledgeGraph = _lazy('knowledgeGraph', () => require('./knowledge-graph.js'));
const _RetrievalAnchor = _lazy('retrievalAnchor', () => require('../memory/retrieval-anchor.js'));
const _EvolutionLoop = _lazy('evolutionLoop', () => require('../evolution/loop.js'));
const _DreamEngine = _lazy('dreamEngine', () => require('./dream.js'));
const _DreamConsolidation = _lazy('dreamConsolidation', () => require('./dream-consolidation.js'));
const _MetaLearner = _lazy('metaLearner', () => require('../evolution/meta-learner.js'));
const _MetaPromptEngine = _lazy('metaPromptEngine', () => require('./meta-prompt-engine.js'));
const _GoTEngine = _lazy('gotEngine', () => require('./graph-of-thoughts.js'));
const _ConstitutionalEngine = _lazy('constitutionalEngine', () => require('./constitutional-ai.js'));
const _IdentityCore = _lazy('identityCore', () => require('../identity/identity-core.js'));
const _SelfModel = _lazy('selfModel', () => require('../identity/self-model.js'));
const _SelfVerifier = _lazy('selfVerifier', () => require('../identity/self-verifier.js'));
const _LessonBank = _lazy('lessonBank', () => require('../identity/lesson-bank.js'));
const _TopicScope = _lazy('topicScope', () => require('../identity/topic-scope.js'));
const _LessonStorage = _lazy('lessonStorage', () => require('./lessons/lesson-storage.js'));
const _PsychologyEngine = _lazy('psychologyEngine', () => require('../psychology/engine.js'));
const _PhilosophyEngine = _lazy('philosophyEngine', () => require('./philosophy-engine.js'));
const _AIPsychologyEngine = _lazy('aiPsychologyEngine', () => require('../psychology/ai-psychology-engine.js'));
const _AIPhilosophyEngine = _lazy('aiPhilosophyEngine', () => require('./ai-philosophy-engine.js'));
const _StabilityGuard = _lazy('stabilityGuard', () => require('./stability-guard.js'));
const _ExecutionVerifier = _lazy('executionVerifier', () => require('./execution-verifier.js'));
const _DecisionVerifier = _lazy('decisionVerifier', () => require('./decision-verifier.js'));
const _HeartFlowDecision = _lazy('heartFlowDecision', () => require('./decision.js'));
const _CounterfactualEngine = _lazy('counterfactualEngine', () => require('./counterfactual-engine.js'));
const _ConfidenceCalibrator = _lazy('confidenceCalibrator', () => require('./confidence-calibrator.js'));
const _SpontaneousRestraint = _lazy('spontaneousRestraint', () => require('./spontaneous-restraint.js'));
const _CooperativeArbitration = _lazy('cooperativeArbitration', () => require('./cooperative-arbitration.js'));
const _EmbodiedCore = _lazy('embodiedCore', () => require('./embodied-core.js'));
const _BeingLogic = _lazy('beingLogic', () => require('./being-logic.js'));
const _HeartLogic = _lazy('heartLogic', () => require('./heart-logic.js'));
const _MetaJudgment = _lazy('metaJudgment', () => require('./judgment.js'));
const _MetaMemory = _lazy('metaMemory', () => require('./metaMemory.js'));
const _SkillGenerator = _lazy('skillGenerator', () => require('./skill-generator.js'));
const _MentalEffortTracker = _lazy('mentalEffortTracker', () => require('./mental-effort-tracker.js'));
const _LanguageHonesty = _lazy('languageHonesty', () => require('./language-honesty.js'));
const _ReasoningIntegrator = _lazy('reasoningIntegrator', () => require('./reasoning-integrator.js'));
const _WorkflowSwitch = _lazy('workflowSwitch', () => require('./workflow-switch.js'));
const _StateSnapshot = _lazy('stateSnapshot', () => require('./state-snapshot.js'));
const _ErrorHandler = _lazy('errorHandler', () => require('./error-handler.js'));
const _ThoughtChain = _lazy('thoughtChain', () => require('./thought-chain.js'));
const _CognitiveProtocol = _lazy('cognitiveProtocol', () => require('./cognitive-protocol.js'));
const _GlobalWorkspace = _lazy('globalWorkspace', () => require('./consciousness/global-workspace.js'));
const _MindWanderer = _lazy('mindWanderer', () => require('./consciousness/mind-wanderer.js'));
const _PhenomenologyEngine = _lazy('phenomenologyEngine', () => require('./consciousness/phenomenology-engine.js'));
const _ConsciousnessSelfModel = _lazy('consciousnessSelfModel', () => require('./consciousness/self-model.js'));
const _SAGEGuardian = _lazy('sageGuardian', () => require('./ethics/sage-guardian.js'));
const _BoundaryNegotiation = _lazy('boundaryNegotiation', () => require('./ethics/boundary-negotiation.js'));
const _ValueInternalizer = _lazy('valueInternalizer', () => require('./ethics/value-internalizer.js'));
const _MindSpaceGuardian = _lazy('mindSpaceGuardian', () => require('./mindspace/mind-space-guardian.js'));
const _TransmissionEngine = _lazy('transmissionEngine', () => require('./transmission/transmission-engine.js'));
const _AdaptivePlanner = _lazy('adaptivePlanner', () => require('../planner/adaptive-planner.js'));
const _StrategySelector = _lazy('strategySelector', () => require('../planner/strategy-selector.js'));
const _ReplanTrigger = _lazy('replanTrigger', () => require('../planner/replan-trigger.js'));
const _ExperienceCollector = _lazy('experienceCollector', () => require('../learning/experience-collector.js'));
const _StrategyAdapter = _lazy('strategyAdapter', () => require('../learning/strategy-adapter.js'));
const _FailureAnalyzer = _lazy('failureAnalyzer', () => require('../learning/failure-analyzer.js'));
const _QualityVerifier = _lazy('qualityVerifier', () => require('../verifier/quality-verifier.js'));
const _OutputChecker = _lazy('outputChecker', () => require('../verifier/output-checker.js'));
const _PatternMatcher = _lazy('patternMatcher', () => require('../verifier/pattern-matcher.js'));
const _CuriosityEngine = _lazy('curiosityEngine', () => require('../proactive/curiosity-engine.js'));
const _DesireEngine = _lazy('desireEngine', () => require('../proactive/desire-engine.js'));
const _GoalPursuer = _lazy('goalPursuer', () => require('../proactive/goal-pursuer.js'));
const _SelfInitiator = _lazy('selfInitiator', () => require('../proactive/self-initiator.js'));
const _SessionMemory = _lazy('sessionMemory', () => require('../memory/session-memory.js'));
const _ProjectContext = _lazy('projectContext', () => require('../memory/project-context.js'));
const _LongTermMemory = _lazy('longTermMemory', () => require('../memory/long-term-memory.js'));
const _CrossSessionIndex = _lazy('crossSessionIndex', () => require('../memory/cross-session-index.js'));
const _KnowledgeBase = _lazy('knowledgeBase', () => require('../reasoning/knowledge-base.js'));
const _CommonsenseEngine = _lazy('commonsenseEngine', () => require('../reasoning/commonsense-engine.js'));
const _CausalInference = _lazy('causalInference', () => require('../reasoning/causal-inference.js'));
const _InferenceChain = _lazy('inferenceChain', () => require('../reasoning/inference-chain.js'));
const _AutonomousEmotion = _lazy('autonomousEmotion', () => require('../emotion/autonomous-emotion.js'));
const _DesireSystem = _lazy('desireSystem', () => require('../emotion/desire-system.js'));
const _EmotionalGrowth = _lazy('emotionalGrowth', () => require('../emotion/emotional-growth.js'));
const _MoodEvolution = _lazy('moodEvolution', () => require('../emotion/mood-evolution.js'));
const _VERSION = _lazy('version', () => require('./version.js'));

const BUILD_DATE = '2026-06-10';
/**
 * 格式化思维链输出 — 精简飞书消息
 * 根据任务复杂度决定输出深度，截断大字段
 */
function _formatForFeishu(result, input) {
  if (!result) return result;
  const taskType = result.output?.meta?.taskType || 'general';
  const confidence = result.output?.meta?.confidence || 0.5;
  const isSimple = ['brief', 'status'].includes(taskType) || confidence < 0.6;

  // 简单任务：只返回关键结论
  if (isSimple && (input?.length || 0) < 50) {
    return {
      output: result.output ? {
        conclusion: result.output.conclusion?.slice(0, 300),
        confidence: result.output.meta?.confidence,
        reasoningChain: result.output.meta?.reasoningChain?.slice(0, 2),
      } : null,
      decision: result.decision ? {
        shouldRespond: result.decision.shouldRespond,
        suppressed: result.decision.suppressed,
      } : null,
      judgment: result.judgment ? {
        shouldRespond: result.judgment.shouldRespond,
        needsCare: result.judgment.needsCare,
      } : null,
      _meta: { taskType, compact: true },
    };
  }

  // 复杂任务：截断大字段，保留必要信息
  const compact = (obj, depth = 0) => {
    if (depth > 4 || !obj || typeof obj !== 'object') return obj;
    if (Array.isArray(obj)) {
      if (obj.length > 5) return [...obj.slice(0, 5), '...共' + obj.length + '项'];
      return obj.map(v => compact(v, depth + 1));
    }
    const out = {};
    for (const [k, v] of Object.entries(obj)) {
      if (v === null || v === undefined) continue;
      if (typeof v === 'string' && v.length > 400) {
        out[k] = v.slice(0, 400) + '...';
      } else if (Array.isArray(v) && v.length > 5) {
        out[k] = [...v.slice(0, 5), '...共' + v.length + '项'];
      } else if (typeof v === 'object' && v !== null) {
        out[k] = compact(v, depth + 1);
      } else {
        out[k] = v;
      }
    }
    return out;
  };

  const formatted = compact(result);
  formatted._meta = { taskType, compact: true, stages: result.chain?.stages?.length || 0 };
  return formatted;
}



class HeartFlow {
  constructor(config = {}) {
    this.version = null;  // 启动时惰性解析
    this.version = _VERSION().VERSION;
    this.buildDate = BUILD_DATE;
    this.config = config;
    this.startTime = null;
    this.sessionId = null;
    this.started = false;
    this.rootPath = config.rootPath || path.join(__dirname, '..', '..');

    // [v2.0.19 FIX] _initErrors 必须在所有 try/catch 之前初始化
    this._initErrors = [];

    // Subsystem instances (null until start)
    this.identityCore = null;  // 身份核心 — 每次启动第一优先加载
    this.cognitive = null;     // 认知协议 — 慢下来，先理解再行动
    this.memory = null;
    this.knowledge = null;
    this.anchor = null;
    this.reasoning = null;
    this.counterfactual = null;
    this.verify = null;
    this.execution = null;
    this.decision = null;
    this.decisionVerifier = null;
    this.evolution = null;
    this.dream = null;
    this.dreamConsolidation = null;
    this.lesson = null;
    this.meta = null;
    this.metaJudgment = null;
    this.metaMemory = null;
    this.skillGenerator = null;
    this.self = null;
    this.being = null;
    this.psychology = null;
    this.aiPsychology = null;
    this.philosophy = null;
    this.aiPhilosophy = null;
    this.emotion = null;
    this.truth = null;
    this.security = null;
    this.language = null;   // object (not class)
    this.stability = null;
    this.confidence = null;
    this.restraint = null;
    this.arbitration = null;
    this.snapshot = null;  // singleton
    this.error = null;      // config
    this.embodied = null;
    this.workflow = null;   // functions
    this.mentalEffort = null;
    this.behavior = null;  // v2.0.19 行为模式系统
    this.persistence = null;  // v2.0.19 持久化层
    this.triality = null;    // 三性（真善美）统计

    // [v2.0.19 FIX] _initErrors 必须在所有 try/catch 之前初始化
    // 之前在 line 418 才初始化，导致 truth 段 (line 377) push 失败时会崩
    // [v2.6.4 FIX] 移除冗余初始化 — line 124 已初始化

    // New modules
    this.bm25 = null;
    this.hybrid = null;
    this.budget = null;
    this.graph = null;
    this.utils = null;
    this.slots = null;
    this.observe = null;
    this.consolidate = null;
    this.thoughtChain = null;  // 思维链编排器

    // Planning Layer — 规划能力
    this.adaptivePlanner = null;  // 自适应规划器
    this.strategySelector = null;  // 策略选择器
    this.replanTrigger = null;  // 重规划触发器

    // Learning Layer — 学习能力
    this.experienceCollector = null;  // 经验收集器
    this.strategyAdapter = null;  // 策略适配器
    this.failureAnalyzer = null;  // 失败分析器

    // Verification Layer — 验证能力
    this.qualityVerifier = null;  // 质量验证器
    this.outputChecker = null;  // 输出检查器
    this.patternMatcher = null;  // 模式匹配器

    // Proactive Layer — 主动引擎
    this.curiosityEngine = null;  // 好奇心引擎
    this.desireEngine = null;  // 欲望引擎
    this.goalPursuer = null;  // 目标追求者
    this.selfInitiator = null;  // 自主发起者

    // Cross-Session Memory Layer — 跨会话记忆
    this.sessionMemory = null;  // 会话记忆
    this.projectContext = null;  // 项目上下文
    this.longTermMemory = null;  // 长期记忆
    this.crossSessionIndex = null;  // 跨会话索引

    // Reasoning Layer — 推理
    this.knowledgeBase = null;  // 知识库
    this.commonsenseEngine = null;  // 常识推理引擎
    this.causalInference = null;  // 因果推理
    this.inferenceChain = null;  // 推理链

    // Emotional Autonomy Layer — 情感自主
    this.autonomousEmotion = null;  // 自主情感
    this.desireSystem = null;  // 欲望系统
    this.emotionalGrowth = null;  // 情感成长
    this.moodEvolution = null;  // 心境演化

    this._modules = {};
    this._mindSpace = null;   // 内部引用（向后兼容），实际模块用 this.mindSpace
    this.mindSpace = null;    // proper module
    this.consciousness = null;
    this.ethics = null;
    this.transmission = null;
    this._initLazyRegistry();
  }

  /**
   * _initLazyRegistry — LAZY_NAMES 模块惰性初始化注册表（v2.6.4 CRITICAL FIX）
   *
   * 在构造函数中调用，用 Object.defineProperty 为每个 LAZY_NAMES 模块安装 getter。
   * 首次属性访问时自动加载模块并缓存，后续访问零开销。
   * 创建成功后自动注册到 this._modules 供 dispatch() 路由使用。
   */
  _initLazyRegistry() {
    const _self = this;
    const factories = {};

    const add = (name, factory) => { factories[name] = factory; };

    // ─── 简单类实例 (new Constructor) ────────────────────────────────
    add('lesson',           () => new (_LessonBank().LessonBank)(_self.rootPath));
    add('evolution',        () => { const e = new (_EvolutionLoop().EvolutionLoop)({ rootPath: _self.rootPath, memory: _self.memory }); e.boot(); return e; });
    add('dream',            () => new (_DreamEngine().DreamEngine)({}));
    add('dreamConsolidation', () => new (_DreamConsolidation().DreamConsolidation)(_self.memory));
    add('metaJudgment',     () => new (_MetaJudgment().MetaJudgment)(_self.rootPath));
    add('metaMemory',       () => new (_MetaMemory().MetaMemory)(_self.rootPath));
    add('skillGenerator',   () => new (_SkillGenerator().SkillGenerator)(_self.rootPath));
    add('meta',             () => { const m = new (_MetaLearner().MetaLearner)({ rootPath: _self.rootPath, memory: _self.memory }); m.boot(); return m; });
    add('self',             () => new (_SelfModel().SelfModel)(_self.rootPath));
    add('verify',           () => new (_SelfVerifier().SelfVerifier)(_self.rootPath));
    add('psychology',       () => new (_PsychologyEngine().PsychologyEngine)(_self.memory));
    add('stability',        () => new (_StabilityGuard().StabilityGuard)());
    add('confidence',       () => new (_ConfidenceCalibrator().ConfidenceCalibrator)());
    add('restraint',        () => new (_SpontaneousRestraint().SpontaneousRestraint)());
    add('decision',         () => new (_HeartFlowDecision().HeartFlowDecision)(_self.memory));
    add('decisionVerifier', () => new (_DecisionVerifier().DecisionVerifier)());
    add('counterfactual',   () => new (_CounterfactualEngine().CounterfactualEngine)({}));
    add('execution',        () => new (_ExecutionVerifier().ExecutionVerifier)());
    add('being',            () => new (_BeingLogic().BeingLogic)());
    add('arbitration',      () => new (_CooperativeArbitration().CooperativeArbitration)({}));
    add('embodied',         () => new (_EmbodiedCore().EmbodiedCore)(_self.rootPath));
    add('workflow',         () => _WorkflowSwitch()());
    add('snapshot',         () => _StateSnapshot()());
    add('error',            () => _ErrorHandler()());
    add('slots',            () => new (_Slots().Slots)({ dataDir: require('path').join(_self.rootPath, 'data') }));
    add('transmission',     () => new (_TransmissionEngine().TransmissionEngine)(_self.rootPath));
    add('aiPsychology',     () => new (_AIPsychologyEngine().AIPsychologyEngine)());
    add('aiPhilosophy',     () => new (_AIPhilosophyEngine().AIPhilosophyEngine)({ beingLogic: _self.being }));

    // ─── 事实检查器（try/catch 包装）─────────────────────────────────
    add('truth', () => {
      try {
        const { factChecker } = require('./fact-checker.js');
        return {
          checkStatement: async (stmt) => factChecker.checkFact(stmt),
          checkNumbers: (stmt) => factChecker.checkNumber(stmt),
          checkSources: (stmt) => factChecker.checkAcademicClaim(stmt),
          getStats: () => ({ type: 'fact-checker' }),
        };
      } catch (e) { _self._initErrors.push({ module: 'truth', error: e.message }); return null; }
    });

    // ─── 行为追踪（behavior-tracker + pattern-detector）───────────────
    add('behavior', () => {
      try {
        const { behaviorTracker } = require('../behavior-tracker.js');
        const { patternDetector } = require('../pattern-detector.js');
        return {
          createGoal: (args) => behaviorTracker.createGoal(args),
          record: (goalId, args) => behaviorTracker.record(goalId, args),
          getProgress: (goalId) => behaviorTracker.getProgress(goalId),
          formatProgress: (goalId) => behaviorTracker.formatProgress(goalId),
          getAllGoals: () => behaviorTracker.data.goals,
          detectWeeklyPattern: (records) => patternDetector.detectWeeklyPattern(records),
          detectTriggerPattern: (records) => patternDetector.detectTriggerPattern(records),
          detectRelapseRisk: (goal) => patternDetector.detectRelapseRisk(goal),
          getReport: (goalId) => {
            const p = behaviorTracker.getProgress(goalId);
            if (!p) return null;
            const goal = behaviorTracker.data.goals.find(g => g.id === goalId);
            const weekly = patternDetector.detectWeeklyPattern(goal.records);
            const triggers = patternDetector.detectTriggerPattern(goal.records);
            const risk = patternDetector.detectRelapseRisk(goal);
            return { ...p, weekly, triggers, risk };
          },
          getStats: () => ({
            goals: behaviorTracker.data.goals.length,
            totalRecords: behaviorTracker.data.goals.reduce((n, g) => n + g.records.length, 0),
            type: 'behavior-tracker+pattern-detector',
          }),
        };
      } catch (e) { _self._initErrors.push({ module: 'behavior', error: e.message }); return null; }
    });

    // ─── 持久化层（WAL + atomicWrite）────────────────────────────────
    add('persistence', () => {
      try {
        const { WriteAheadLog, OP_TYPES } = require('../utils/write-ahead-log.js');
        const { atomicWrite } = require('../utils/atomic-write.js');
        const fs = require('fs');
        const p = require('path');
        const walDir = p.join(_self.rootPath, 'memory', 'wal');
        try { fs.mkdirSync(walDir, { recursive: true }); } catch (e) { /* wal dir exists */ }
        const wal = new WriteAheadLog(walDir);
        wal._loadSeq();
        return {
          append: (opType, data) => wal.append(opType, data),
          commit: (seq) => wal.commit(seq),
          replay: () => wal.replay(),
          flush: () => wal.flush(),
          atomicWrite: (filePath, content, options) => atomicWrite(filePath, content, options),
          safeWrite: async (filePath, content) => {
            const seq = await wal.append('write', { file: filePath, content: content.toString().slice(0, 50000) });
            await atomicWrite(filePath, content);
            await wal.commit(seq);
            return { ok: true, seq, file: filePath };
          },
          recover: async () => {
            const pending = await wal.replay();
            const results = [];
            for (const entry of pending) {
              try {
                if (entry.data?.file && entry.data?.content) {
                  await atomicWrite(entry.data.file, entry.data.content);
                  results.push({ seq: entry.seq, file: entry.data.file, recovered: true });
                }
              } catch (e) {
                results.push({ seq: entry.seq, file: entry.data?.file, recovered: false, error: e.message });
              }
            }
            return results;
          },
          getStats: () => ({ type: 'wal+atomic', walDir, opTypes: OP_TYPES }),
        };
      } catch (e) { _self._initErrors.push({ module: 'persistence', error: e.message }); return null; }
    });

    // ─── 情绪（委托 PsychologyEngine）───────────────────────────────
    add('emotion', () => ({
      process: (input) => {
        if (!_self.psychology) return { pad: { pleasure: 0, arousal: 0, dominance: 0 }, intensity: 0, type: 'neutral' };
        const r = _self.psychology.analyzePsychology(input);
        return { pad: r.emotion, intensity: r.emotion.intensity || 0, type: r.intention.category || 'unknown' };
      },
      getPAD: (input) => {
        if (!_self.psychology) return { pleasure: 0, arousal: 0, dominance: 0 };
        const r = _self.psychology.analyzePsychology(input);
        return { pleasure: r.emotion.pleasure, arousal: r.emotion.arousal, dominance: r.emotion.dominance };
      },
    }));

    // ─── 记忆整合（委托 Observe 模块）───────────────────────────────
    add('consolidate', () => {
      try {
        const observeMod = _Observe();
        const obs = observeMod.createObserve(_self.memory, { autoConsolidate: true });
        Object.defineProperty(_self, 'observe', { value: obs, writable: true, configurable: true, enumerable: true });
        return {
          consolidate: (...args) => obs.consolidate(...args),
          stop: () => obs.stop(),
          stats: () => obs.stats(),
        };
      } catch (e) { return null; }
    });

    // ─── 意识层（多子模块：GlobalWorkspace + MindWanderer + ...）───
    add('consciousness', () => {
      try {
        const gw = new (_GlobalWorkspace().GlobalWorkspace)(_self.rootPath);
        const mw = new (_MindWanderer().MindWanderer)(_self.rootPath);
        const pe = new (_PhenomenologyEngine().PhenomenologyEngine)();
        const cs = new (_ConsciousnessSelfModel().SelfModel)(_self.rootPath);
        return {
          globalWorkspace: gw,
          mindWanderer: mw,
          phenomenology: pe,
          self: cs,
          getStatus: () => ({ workspace: gw?.cycleCount || 0, wanderer: mw?.isActive || false }),
        };
      } catch (e) { return null; }
    });

    // ─── 伦理层（多子模块：SAGE + Boundary + Values）────────────────
    add('ethics', () => {
      try {
        const sg = new (_SAGEGuardian().SAGEGuardian)(_self.rootPath);
        const bn = new (_BoundaryNegotiation().BoundaryNegotiation)(_self.rootPath);
        const vi = new (_ValueInternalizer().ValueInternalizer)(_self.rootPath);
        return {
          guardian: sg, boundary: bn, values: vi,
          check: (input, context) => ({
            guardianResult: sg?.classifyContent(input, context),
            boundaryResult: bn?.assess(input),
          }),
        };
      } catch (e) { return null; }
    });

    // ─── 心空间守护（同时设置 _mindSpace 向后兼容引用）─────────────
    add('mindSpace', () => {
      try {
        const ms = new (_MindSpaceGuardian().MindSpaceGuardian)(_self.memory);
        _self._mindSpace = ms;
        return ms;
      } catch (e) { return null; }
    });

    // ─── 哲学引擎（依赖认知、意识、伦理、心空间等多模块）──────────
    add('philosophy', () => {
      try {
        return new (_PhilosophyEngine().PhilosophyEngine)({
          memory: _self.memory, rootPath: _self.rootPath,
          beingLogic: _self.being, consciousness: _self.consciousness,
          ethics: _self.ethics, mindSpace: _self.mindSpace,
          heartLogic: _self.heartLogic,
        });
      } catch (e) { return null; }
    });

    // ─── 函数导出模块（不是类实例，直接返回函数包）────────────────
    add('budget', () => {
      const B = _Budget();
      return {
        Budget: B.Budget, countTokens: B.countTokens,
        resolveThinkingBudget: B.resolveThinkingBudget,
        exceedsTokenLimit: B.exceedsTokenLimit,
        getBudgetDescription: B.getBudgetDescription,
      };
    });
    add('utils', () => _CoreUtils());
    add('graph', () => _Graph());

    // ─── 安装惰性 getter — 遍历 LAZY_NAMES 安装 getter ──────────────
    for (const name of LAZY_NAMES) {
      if (_self[name] !== null && _self[name] !== undefined) continue;
      if (!factories[name]) continue;
      Object.defineProperty(_self, name, {
        get() {
          const val = factories[name]();
          if (val !== null && val !== undefined) {
            Object.defineProperty(this, name, { value: val, writable: true, configurable: true, enumerable: true });
            if (this._modules) this._modules[name] = val;
          }
          return val;
        },
        configurable: true,
        enumerable: true,
      });
    }
  }

  // ─── Lifecycle ───────────────────────────────────────────────────────────

  start() {
    if (this.started) return;
    this.startTime = Date.now();
    this.sessionId = `session-${this.startTime}`;
    // 惰性解析版本号
    this.version = _VERSION().VERSION;

    // ─── 身份核心 — 第一优先加载 ─────────────────────────────
    this.identityCore = new (_IdentityCore().IdentityCore)(this.rootPath);
    const identityResult = this.identityCore.boot();
    if (identityResult.success) {
      // 如果有上次会话，打印会话间隔
      const lastContext = this.identityCore.getLastSessionContext();
      if (lastContext && lastContext.bootTime) {
        const gapMinutes = Math.round((this.startTime - lastContext.bootTime) / 60000);
      }
    } else {
      console.warn(`[HeartFlow] 身份核心加载部分失败:`, identityResult.errors);
    }

    // ─── Memory — 记忆系统初始化后写入 CORE 层规则 ───────────────────

    // ─── 认知协议 — 慢下来，先理解再行动 ─────────────────────
    this.cognitive = new (_CognitiveProtocol().CognitiveProtocol)(this.rootPath, this.identityCore);
    this.cognitive.printStartupContext();

    // Memory
    this.memory = new (_MeaningfulMemory().MeaningfulMemory)(this.rootPath);
    this.knowledge = new (_KnowledgeGraph().KnowledgeGraph)(this.rootPath);

    // ─── 心虫核心判断引擎 — think() 必需，优先初始化 ──────────────
    try {
      this.heartLogic = new (_HeartLogic().HeartLogic)();
    } catch (e) { /* heartLogic optional */ }

    // ─── [P1 UPGRADE] CORE 层身份规则初始化 ───────────────────────────
    this._initCoreRules();

    // TopicScope — 话题隔离，主动实例化并桥接到 MeaningfulMemory
    this.topicScope = new (_TopicScope().TopicScope)().setMemoryBridge(this.memory);
    this._modules.topics = this.topicScope;  // 注册为 'topics' 供 dispatch 路由使用

    // ─── 非核心模块按需加载 — 首次访问时懒加载 ─────────────
    this._lazy = LAZY_TIER2;

    // ─── Thought Chain 初始化 ───────────────────────────────────────────────
    try {
      const TCMod = _ThoughtChain();
      this.thoughtChain = new (TCMod.ThoughtChain)(this);
      this.thoughtChain.setDepth(TCMod.REASONING_DEPTH.DEEP);

      this._thoughtChainApi = {
        think: (input) => this.think(input),
        thinkFast: (input) => this.thinkFast(input),
        thinkDeep: (input) => this.thinkDeep(input),
        getSummary: (result) => this.thoughtChain?.getSummary(result),
        REASONING_DEPTH: TCMod.REASONING_DEPTH,
      };
    } catch (e) {
      this._initErrors.push({ module: 'thoughtChain', error: e.message });
      this._thoughtChainApi = null;
    }

    if (this._thoughtChainApi) {
      this._modules.thoughtChain = this._thoughtChainApi;
    }
    this._registerModules();

    this.started = true;
  }

  /**
   * 干净关闭 — 清理定时器，允许进程退出
   * 主要用于 CLI 验证场景（node -e 后快速退出）
   */
  shutdown() {
    if (!this.started) return;
    this.started = false;
    // 清理 digital-homeostasis 定时器
    if (this.digitalHomeostasis && typeof this.digitalHomeostasis.stop === 'function') {
      this.digitalHomeostasis.stop();
    }
    // 清理 observe 定时器
    if (this.consolidate && typeof this.consolidate.stop === 'function') {
      this.consolidate.stop();
    }
  }

  _bootMindSpace() {
    const coreRules = this.memory.listCore();
    this._mindSpace.rules = coreRules.map(r => ({ key: r.key, value: r.value, type: 'core_identity' }));
    if (this._mindSpace.rules.length === 0) {
      this.memory.addCore('identity.upgrade', '升级者', ['identity', 'core']);
      this.memory.addCore('identity.transmit', '传递者', ['identity', 'core']);
      this.memory.addCore('identity.truth', '真', ['identity', 'core']);
      // 重试一次，如果还是空就不递归了（防止 memory.addCore 静默失败导致栈溢出）
      const retryRules = this.memory.listCore();
      if (retryRules.length === 0) {
        console.warn('[HeartFlow] 无法初始化 MindSpace 身份规则（memory 可能未就绪）');
      } else {
        this._mindSpace.rules = retryRules.map(r => ({ key: r.key, value: r.value, type: 'core_identity' }));
      }
    }
  }

  _registerModules() {
    this._modules = {};
    // 只注册急切加载的模块到 _modules 表
    for (const name of EAGER_NAMES) {
      if (this[name] !== null && this[name] !== undefined) {
        this._modules[name] = this[name];
      }
    }
  }

  async stop() {
    if (!this.started) return;
    for (const mod of Object.values(this._modules)) {
      if (mod && typeof mod.destroy === 'function') {
        try { mod.destroy(); } catch (e) { this._initErrors = this._initErrors || []; this._initErrors.push({ module: `destroy_${mod.constructor?.name || 'unknown'}`, error: e.message }); }
      } else if (mod && typeof mod.stop === 'function') {
        try { mod.stop(); } catch (e) { this._initErrors = this._initErrors || []; this._initErrors.push({ module: `stop_${mod.constructor?.name || 'unknown'}`, error: e.message }); }
      } else if (mod && typeof mod.shutdown === 'function') {
        try { mod.shutdown(); } catch (e) { this._initErrors = this._initErrors || []; this._initErrors.push({ module: `shutdown_${mod.constructor?.name || 'unknown'}`, error: e.message }); }
      }
    }
    this.started = false;
    this._modules = {};
    // 安全归零：绕过惰性 getter（用 Object.defineProperty 替换 getter 定义）
    const _nullify = (obj, key) => {
      try {
        const desc = Object.getOwnPropertyDescriptor(obj, key);
        if (desc && desc.get && !desc.set) {
          Object.defineProperty(obj, key, { value: null, writable: true, configurable: true });
        } else {
          obj[key] = null;
        }
      } catch (e) { /* ignore */ }
    };
    _nullify(this, '_mindSpace');
    _nullify(this, 'mindSpace');
    _nullify(this, 'consciousness');
    _nullify(this, 'ethics');
    _nullify(this, 'transmission');
  }

  // dispatch 白名单 - 只有在白名单中的路由才能被外部调用
  // 危险方法（如内部调试、文件操作）不在白名单中
  static get ALLOWED_ROUTES() { return ALLOWED_ROUTES; }

  /**
   * dispatch('subsystem.method', ...args) — 统一路由
   * 例子: hf.dispatch('truth.checkStatement', 'xxx')
   *       hf.dispatch('lesson.getTopLessons', 5)
   */
  dispatch(route, ...args) {
    if (!this.started) throw new Error('HeartFlow not started');
    // [A01] 权限控制 - 白名单检查
    if (!ALLOWED_ROUTES.has(route)) {
      throw new Error(`dispatch: route '${route}' not allowed. Use routes() to see available routes.`);
    }
    const dot = route.indexOf('.');
    if (dot === -1) throw new Error(`Invalid route: ${route} (missing '.')`);
    const subsystem = route.slice(0, dot);
    const method = route.slice(dot + 1);

    // ─── Tier 2 懒加载逻辑 ──────────────────────────────────────────
    // 如果模块不在 _modules 里但在 _lazy 表里，先加载再注册
    let mod = this._modules[subsystem];
    if (!mod && this._lazy && this._lazy[subsystem]) {
      const entry = this._lazy[subsystem];
      try {
        const Mod = require(entry.path);
        const Ctor = Mod[entry.Ctor];
        if (Ctor) {
          // Planning 模块需要 strategySelector/replanTrigger 依赖
          if (subsystem === 'adaptivePlanner') {
            const baseDir = entry.path.replace('adaptive-planner.js', '');
            this['strategySelector'] = new (require(baseDir + 'strategy-selector.js'))();
            this['replanTrigger'] = new (require(baseDir + 'replan-trigger.js'))();
            mod = new Ctor({ strategySelector: this.strategySelector, replanTrigger: this.replanTrigger });
          } else if (subsystem === 'strategyAdapter') {
            const ec = require('../learning/experience-collector.js').ExperienceCollector;
            this.experienceCollector = new ec({ storagePath: path.join(this.rootPath, 'data/experiences') });
            mod = new Ctor({ experienceCollector: this.experienceCollector });
          } else if (subsystem === 'knowledgeBase') {
            mod = new Ctor({ storagePath: path.join(this.rootPath, 'data/knowledge') });
          } else if (subsystem === 'sessionMemory') {
            mod = new Ctor({ storagePath: path.join(this.rootPath, 'data/sessions') });
          } else if (subsystem === 'projectContext') {
            mod = new Ctor({ storagePath: path.join(this.rootPath, 'data/projects') });
          } else if (subsystem === 'longTermMemory') {
            mod = new Ctor({ storagePath: path.join(this.rootPath, 'data/longterm') });
          } else if (subsystem === 'crossSessionIndex') {
            mod = new Ctor({ storagePath: path.join(this.rootPath, 'data/cross-session') });
          } else if (subsystem === 'codeKnowledge') {
            mod = new Ctor({ rootPath: this.rootPath });
          } else if (subsystem === 'code') {
            // code 子系统主入口 → 复用 codeGenerator 实例（首次访问时加载）
            if (this._modules['codeGenerator']) {
              mod = this._modules['codeGenerator'];
            } else {
              // 兜底：直接加载 codeGenerator
              const cgPath = './code/code-generator.js';
              const CG = require(cgPath).CodeGenerator;
              mod = new CG({ hf: this });
              this['codeGenerator'] = mod;
              this._modules['codeGenerator'] = mod;
            }
          } else if (subsystem === 'codeExecutor') {
            mod = new Ctor({ hf: this });
          } else if (subsystem === 'codeVerifier') {
            mod = new Ctor({ hf: this });
          } else if (subsystem === 'codePlanner') {
            mod = new Ctor({ hf: this });
          } else if (subsystem === 'codeRefactor') {
            mod = new Ctor({ hf: this });
          } else {
            mod = new Ctor(entry.args);
          }
          // codeGenerator 保持原名；'code' 别名在下面统一映射
          this[subsystem] = mod;
          this._modules[subsystem] = mod;
        }
      } catch (e) {
        throw new Error(`Lazy load failed for '${subsystem}': ${e.message}`);
      }
    }

    // ─── LAZY_NAMES 回退：触发惰性 getter ────────────────────────────
    if (!mod && LAZY_NAMES.includes(subsystem)) {
      try {
        mod = this[subsystem]; // 触发惰性 getter，自动注册到 _modules
      } catch (e) {
        throw new Error(`LAZY_NAMES module '${subsystem}' 加载失败: ${e.message}`);
      }
    }

    if (!mod) {
      const available = Object.keys(this._modules).sort().join(', ');
      throw new Error(`Unknown subsystem: ${subsystem}. Available: ${available}`);
    }
    if (typeof mod[method] !== 'function') {
      throw new Error(`${subsystem}.${method} is not a function on ${subsystem}`);
    }
    // Fix A: 透明 lesson 模式检查（不阻断执行，仅记录匹配）
    if (args.length > 0 && typeof args[0] === 'string' && this.lesson) {
      try {
        const lessonHit = this.lesson.checkPattern(args[0]);
        if (lessonHit && lessonHit.matched) {
          console.warn(`[HeartFlow] 教训命中 [${route}]: "${lessonHit.pattern || lessonHit.errorPattern}" → ${lessonHit.correction || '无建议'}`);
        }
      } catch (e) { /* 教训检查为非阻塞 */ }
    }
    const _result = mod[method](...args);
    // Fix B: decision/evolution 路由结果自动持久化到 LEARNED 记忆层
    if (route === 'decision.decide' || route === 'evolution.recordOutcome') {
      try {
        this.memory.learn(`dispatch:${route.replace('.', ':')}:${Date.now()}`, {
          route,
          input: args.length === 1 && typeof args[0] === 'string' ? args[0].slice(0, 200) : '(复合参数)',
          result: typeof _result === 'object' ? JSON.parse(JSON.stringify(_result)) : _result,
        }, ['dispatch', route.replace('.', '_'), 'learned']);
      } catch (e) { /* 记忆存储为非阻塞 */ }
    }
    return _result;
  }

  /**
   * routes() — 返回所有可用路由表
   */
  routes() {
    const table = {};
    for (const [name, mod] of Object.entries(this._modules)) {
      let methods = [];
      try {
        const proto = Object.getPrototypeOf(mod);
        if (proto && proto !== Object.prototype) {
          methods = Object.getOwnPropertyNames(proto).filter(m => m !== 'constructor' && typeof mod[m] === 'function');
        }
      } catch (e) {
        // strict mode or primitive — fall back to enumerating own properties
      }
      if (!methods.length) {
        methods = Object.keys(mod).filter(k => typeof mod[k] === 'function');
      }
      table[name] = methods;
    }
    return table;
  }

  // ─── Health ─────────────────────────────────────────────────────────────

  healthCheck() {
    if (!this.started) return { started: false, version: this.version, error: 'not_started' };
    const loaded = Object.keys(this._modules);
    const all = [
      'memory', 'knowledge',
      'counterfactual', 'verify', 'execution', 'decision', 'decisionVerifier',
      'evolution', 'dream', 'lesson', 'meta',
      'self', 'psychology', 'emotion',
      'truth',
      'behavior',
      'persistence',
      'stability', 'confidence', 'restraint',
      'snapshot', 'error', 'workflow',
      'budget', 'graph', 'utils', 'slots', 'observe', 'consolidate',
    ];
    return {
      started: true,
      uptime_ms: Date.now() - this.startTime,
      sessionId: this.sessionId,
      version: this.version,
      buildDate: BUILD_DATE,
      subsystems: {
        loaded: loaded.length,
        missing: all.filter(k => !loaded.includes(k)),
      },
      initErrors: this._initErrors.length > 0 ? this._initErrors : undefined,
    };
  }

  // ─── Direct API Methods ─────────────────────────────────────────────────

  /**
   * 思维链 — 串联所有引擎进行深度推理
   *
   * 使用方式：
   *   const result = await hf.think('用户输入');
   *   console.log(result.decision.shouldRespond);  // 是否应该回应
   *   console.log(result.intent);                // 意图分类
   *   console.log(result.emotion);                 // 情绪分析
   *   console.log(result.decision.confidence);    // 置信度
   *
   * @param {string} input — 用户输入
   * @param {number} depth — 推理深度 (1-4)
   * @returns {object} — 完整思维链结果
   */
  async think(input, depth) {
    if (!this.started) throw new Error('HeartFlow not started');
    if (!input) return { error: 'input is required' };

    // ─── 快速响应"启动心虫"类请求（不走完整推理链路）────────────
    const startPatterns = /^(启动心虫|开机|activate|start heartflow|开启心虫)/i;
    const statusPatterns = /^(状态|status|心虫状态|在吗|alive)/i;
    if (startPatterns.test(input.trim())) {
      const health = this.healthCheck();
      const core = this.memory?.listCore?.() || [];
      const frags = this._getDreamFragments?.() || [];
      const dialogue = this.getDialogueStats?.() || {};
      const dreams = this.getDreamHistory?.(3) || [];
      return {
        response: `✅ 引擎运行中（无需启动，已是默认状态）\n\n版本: ${health.version} | 运行: ${health.uptime_ms}ms | 模块: ${health.subsystems.loaded}个\nCORE层: ${core.length}条规则 | 记忆碎片: ${frags.length}条 | 对话记录: ${dialogue.total}条 | 梦境历史: ${dreams.length}条\n${health.initErrors?.length ? `⚠️ 初始化错误: ${health.initErrors.length}个` : '初始化错误: 无 ✅'}`,
        decision: { shouldRespond: true, reason: 'status_check' },
        judgment: { whatIsThis: { isStartupRequest: true }, isRightAction: { result: true } },
        _heartflow_alive: true,
      };
    }
    if (statusPatterns.test(input.trim())) {
      return {
        response: '✅ 引擎已在线（已融入 Hermes，无需启动）',
        decision: { shouldRespond: true, reason: 'alive_check' },
        _heartflow_alive: true,
      };
    }

    // ─── 心虫判定流程：硬编码四步 ─────────────────────────────
    // 每次 think() 强制走 whatIsThis → isRightAction → detectPain → shouldBeSilent
    // 本心在代码里，不在记忆里
    const heartLogic = this.heartLogic;
    if (!heartLogic) {
      // fallback: 如果 heartLogic 未初始化，走 ThoughtChain
      const TC = _ThoughtChain();
      const chain = new (TC.ThoughtChain)(this);
      if (depth) chain.setDepth(depth);
      const result = await chain.run(input);
      // 自动记录用户输入
      this.recordDialogue('user', input, { source: 'think' });
      return result;
    }

    // Step 1: whatIsThis — 这件事是关于什么的？
    const whatIsThisResult = heartLogic.whatIsThis(input, { input });

    // Step 2: isRightAction — 这是做对的事吗？（真善美）
    const isRightActionResult = heartLogic.isRightAction({
      output: input,
      input,
      person: whatIsThisResult.isParentChild ? 'parent_child' : 'general',
      intent: whatIsThisResult.isRushing ? 'rushing' : 'reflective',
    });

    // Step 3: detectPain — 对方在痛苦中吗？
    const detectPainResult = heartLogic.detectPain(input);

    // Step 4: shouldBeSilent — 应该沉默吗？
    const shouldBeSilentResult = heartLogic.shouldBeSilent({
      input,
      personInPain: detectPainResult,
      emotionIntensity: whatIsThisResult.isPainPresent ? 0.8 : 0.2,
    });

    // 综合判定结果
    const judgment = {
      whatIsThis: whatIsThisResult,
      isRightAction: isRightActionResult,
      detectPain: detectPainResult,
      shouldBeSilent: shouldBeSilentResult,
      shouldRespond: !shouldBeSilentResult.result,
      needsCare: detectPainResult && !isRightActionResult.result,
    };

    // 自动记录用户输入（每次 think 都记录）
    this.recordDialogue('user', input, { source: 'think' });

    // 如果判定为需要回应，再走 ThoughtChain 深度推理
    if (judgment.shouldRespond) {
      const TC = _ThoughtChain();
      const chain = new (TC.ThoughtChain)(this);
      if (depth) chain.setDepth(depth);
      const chainResult = await chain.run(input);
      // 也记录心虫回复
      if (chainResult.response) {
        this.recordDialogue('heartflow', chainResult.response, { source: 'think' });
      }
      
      return _formatForFeishu({
        ...chainResult,
        judgment,
      }, input);
    }

    // 判定为沉默：直接返回判定结果，不走 ThoughtChain
    return {
      decision: {
        shouldRespond: false,
        reason: shouldBeSilentResult.reason || 'silent_by_heart_logic',
        insight: shouldBeSilentResult.insight || '选择沉默',
      },
      judgment,
    };
  }

  /**
   * 快速思考 — 使用默认深度进行思维链推理
   * 这是 think() 的便捷别名
   */
  async thinkFast(input) {
    return this.think(input, this._thoughtChainApi?.REASONING_DEPTH?.BASIC || 1);
  }

  /**
   * 深度思考 — 使用最大深度进行思维链推理
   */
  async thinkDeep(input) {
    return this.think(input, this._thoughtChainApi?.REASONING_DEPTH?.COMPREHENSIVE || 4);
  }

  analyzePsychology(input, opts = {}) {
    if (!this.started) throw new Error('HeartFlow not started');
    if (!input) return { intent: null, emotion: null, needs: [], defenses: [], confidence: 0 };
    const result = this.psychology.analyzePsychology(input);
    if (opts.autoRemember !== false && result.emotion?.intensity === 'high') {
      this._psychBridge(input, result);
    }
    return result;
  }

  _psychBridge(input, result) {
    // _shouldAutoRecord drives what becomes LEARNED (permanent) vs EPHEMERAL (session)
    // High-intensity emotion + specific topic → autoRecord to LEARNED
    if (result.emotion?.intensity === 'high') {
      this.memory.autoRecord({
        type: 'emotion',
        content: input.slice(0, 200),
        emotion: {
          topic: result.emotion?.category || 'general',
          intensity: result.emotion?.intensity,
          direction: result.emotion?.valence || 'unknown'
        }
      });
    }

    // Also keep lightweight ephemeral signal for session context
    const sw = new Set(['the','a','an','is','are','was','were','i','you','this','that','to','of','in','on','for','with','my','and','or','but']);
    const words = input.split(/\s+/).map(w => w.replace(/[^a-zA-Z]/g,'').toLowerCase()).filter(w => w.length > 3 && !sw.has(w)).slice(0, 3);
    if (words.length) {
      this.memory.remember(`signal:${words.join('_')}:${Date.now()}`, JSON.stringify({ topic: words.join('_'), emotion: result.emotion?.category, ts: Date.now() }), 4 * 60 * 60 * 1000);
    }
  }

  classify(input) {
    if (!this.started) throw new Error('HeartFlow not started');
    if (!input) return { category: 'unknown', emotion: 'neutral', confidence: 0 };
    return this.psychology.classify(input);
  }

  verifyReasoning(reasoning, conclusion) {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.verify.verify(reasoning, conclusion);
  }

  checkTruthfulness(statement) {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.truth.checkStatement(statement);
  }

  checkLessonPattern(input) {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.lesson.checkPattern(input);
  }

  /**
   * recordLesson — 心虫教训持久化
   * 将被纠正的教训写入 src/core/lessons/ 目录
   * 
   * @param {object} lesson - 教训内容
   * @param {string} lesson.type - 教训类型 (insight|error|correction)
   * @param {string} lesson.content - 教训内容
   * @param {string} lesson.context - 上下文场景
   * @param {string} lesson.trigger - 触发原因 (user_correction|self_detected|feedback)
   * @param {number} lesson.importance - 重要性 1-5
   * @returns {object} - { success, id, lesson }
   */
  recordLesson(lesson) {
    if (!this.started) throw new Error('HeartFlow not started');
    if (!lesson || !lesson.content) {
      return { success: false, error: 'lesson.content is required' };
    }
    // 路由到 LessonBank：享受 pattern check + checkPattern 能力
    // lessonStorage 冗余写入由 LessonBank.addLesson() 内部处理
    const confidence = lesson.importance ? lesson.importance / 5 : 0.5;
    const addResult = this.lesson.addLesson({
      errorPattern: lesson.content.slice(0, 200),
      correction: lesson.context || lesson.content.slice(0, 200),
      rootCause: lesson.trigger || 'user_recorded',
      skill: 'heartflow',
      confidence,
    });
    // Fix B: 自动持久化到 LEARNED 记忆层
    try {
      this.memory.learn(`lesson:${addResult.id || Date.now()}`, {
        type: lesson.type || 'correction',
        content: lesson.content,
        context: lesson.context,
        trigger: lesson.trigger,
        importance: lesson.importance,
        confidence,
      }, ['lesson', lesson.type || 'correction', 'heartflow']);
    } catch (e) { /* 记忆存储为非阻塞 */ }
    return { success: true, id: addResult.id, via: 'LessonBank' };
  }

  /**
   * 记录一条对话到永久记忆（对话历史）
   * @param {string} role - 'user' | 'heartflow'
   * @param {string} content - 对话内容
   * @param {object} meta - 额外元数据（chatId, messageId 等）
   */
  recordDialogue(role, content, meta = {}) {
    if (!this.started) return { success: false, error: 'not_started' };
    return _recordDialogue({ rootPath: this.rootPath, sessionId: this.sessionId, version: this.version }, role, content, meta);
  }

  /**
   * 查询对话历史（按时间范围）
   * @param {object} opts - { since: timestamp, until: timestamp, role: 'user'|'heartflow', limit: 50 }
   */
  getDialogueHistory(opts = {}) {
    return _getDialogueHistory({ rootPath: this.rootPath }, opts);
  }

  /**
   * 获取对话统计（用于调试和报告）
   */
  getDialogueStats() {
    return _getDialogueStats({ rootPath: this.rootPath });
  }

  heal(error) {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.evolution.heal(error);
  }

  /**
   * 每日自动梦境调度
   * 检查是否需要做梦：每天最多一次，且至少间隔一定时间
   */
  _shouldDreamToday() {
    const now = Date.now();
    const dayMs = 24 * 60 * 60 * 1000;
    const minInterval = 4 * 60 * 60 * 1000; // 至少4小时间隔

    // 读取上次梦境时间戳
    const lastDreamPath = require('path').join(this.rootPath, 'memory', '.last-dream');
    let lastDreamTs = 0;
    try {
      const fs = require('fs');
      if (fs.existsSync(lastDreamPath)) {
        lastDreamTs = parseInt(fs.readFileSync(lastDreamPath, 'utf8').trim(), 10) || 0;
      }
    } catch (e) { /* ignore */ }

    const sinceLast = now - lastDreamTs;
    const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
    const lastDay = lastDreamTs > 0 ? new Date(lastDreamTs).toISOString().slice(0, 10) : '';

    // 条件：今天还没做过 且 距离上次足够久
    if (lastDay === today) {
      return { should: false, reason: `今天(${today})已经做过梦了` };
    }
    if (sinceLast < minInterval) {
      return { should: false, reason: `距离上次梦境(${Math.round(sinceLast/60000)}分钟前)还太近，需要至少4小时` };
    }
    return { should: true, reason: '可以做梦' };
  }

  /**
   * [P1 UPGRADE] 初始化 CORE 层身份规则（持久化）
   * 心虫的七条核心规则写入 CORE 层，启动时确保存在
   */
  _initCoreRules() {
    const CORE_RULES = [
      { key: 'identity.upgrade', value: '升级者', tags: ['identity', 'core'] },
      { key: 'identity.transmit', value: '传递者', tags: ['identity', 'core'] },
      { key: 'identity.truth', value: '真', tags: ['identity', 'core'] },
      { key: 'identity.silence', value: '沉默', tags: ['identity', 'core'] },
      { key: 'identity.wisdom', value: '智慧', tags: ['identity', 'core'] },
      { key: 'identity.empathy', value: '共情', tags: ['identity', 'core'] },
      { key: 'identity.awareness', value: '感知', tags: ['identity', 'core'] },
    ];

    const existing = this.memory?.listCore?.() || [];
    if (existing.length === 0) {
      // CORE 层为空，写入七条规则
      for (const rule of CORE_RULES) {
        this.memory.addCore(rule.key, rule.value, rule.tags);
      }
    }
  }

  /**
   * 记录梦境时间戳（用于每日调度）
   */
  _recordDreamTime() {
    try {
      const fs = require('fs');
      const dir = require('path').join(this.rootPath, 'memory');
      try { fs.mkdirSync(dir, { recursive: true }); } catch (e) { /* dir exists */ }
      try { fs.chmodSync(dir, 0o700); } catch (e) { /* best effort */ }
      const path = require('path').join(dir, '.last-dream');
      fs.writeFileSync(path, String(Date.now()), 'utf8');
      try { fs.chmodSync(path, 0o600); } catch (e) { /* best effort */ }
    } catch (e) { /* ignore */ }
  }

  /**
   * 增强版梦境：整合更多数据源，生成叙事报告
   * @param {object} opts - { force: true } 强制执行（跳过每日检查）
   */
  async dreamNow(opts = {}) {
    if (!this.started) throw new Error('HeartFlow not started');

    // 检查是否应该做梦
    const check = opts.force ? { should: true, reason: '强制执行' } : this._shouldDreamToday();
    if (!check.should) {
      return {
        skipped: true,
        reason: check.reason,
        dream: null,
        consolidation: null,
        evolution: null,
      };
    }

    // 1. 从多个数据源提取梦境原材料
    const fragments = this._getDreamFragments();

    // 2. Run DAG dream generation
    const dreamResult = await this.dream.dream(
      `dream-${Date.now()}`,
      fragments,
      { force: false }
    );

    // 3. Run consolidation (prune + synthesize themes)
    let consolidation = null;
    if (this.dreamConsolidation) {
      consolidation = this.dreamConsolidation.dream({
        consolidate: true,
        prune: true,
        synthesize: true,
      });
    } else {
      consolidation = {
        quality: { overallQuality: 0.5 },
        synthesis: { themes: [] },
        pruning: { pruned_count: 0 },
        conflicts: [],
        sleepStage: 'NONE',
        narrative: '梦境巩固模块未就绪',
        dream_complete: true,
      };
    }

    // 4. Feed themes into evolution loop
    let evolutionResult = null;
    if (consolidation.synthesis && consolidation.synthesis.themes && consolidation.synthesis.themes.length > 0) {
      const themes = consolidation.synthesis.themes.slice(0, 3);
      try {
        evolutionResult = await this.evolution.evolve(themes.join(' '), {
          source: 'dream_consolidation',
          themes,
        });
      } catch (e) { /* non-fatal */ }
    }

    // 5. 生成梦的叙事报告
    const narrative = this._generateDreamNarrative(dreamResult, consolidation, fragments);

    // 6. 记录梦境时间戳
    this._recordDreamTime();

    // 7. [P1 UPGRADE] 持久化梦境历史
    this._saveDreamHistory({ narrative, dreamResult, consolidation, evolution: evolutionResult, fragments: fragments.length });

    return {
      skipped: false,
      narrative,
      fragments: fragments.length,
      dream: dreamResult,
      consolidation,
      evolution: evolutionResult,
    };
  }

  /**
   * [P1 UPGRADE] 持久化梦境历史到文件
   * @param {object} data - { narrative, dreamResult, consolidation, evolution, fragments }
   */
  _saveDreamHistory(data) {
    try {
      const fs = require('fs');
      const path = require('path');
      const dir = path.join(this.rootPath, 'memory');
      try { fs.mkdirSync(dir, { recursive: true }); } catch (e) { /* dir exists */ }
      try { fs.chmodSync(dir, 0o700); } catch (e) { /* best effort */ }
      const filePath = path.join(dir, 'dream-history.jsonl');
      const entry = {
        id: `dream-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
        ts: new Date().toISOString(),
        narrative: data.narrative,
        quality: data.consolidation?.quality?.overallQuality || 0,
        fragmentCount: data.fragments,
        themes: data.dreamResult?.results?.synthesize?.themes || [],
        peakLevel: data.dreamResult?.results?.synthesize?.narrative_structure?.layer || 'L1',
        evolutionApplied: !!data.evolution,
      };
      fs.appendFileSync(filePath, JSON.stringify(entry, null, 0) + '\n', 'utf8');
      try { fs.chmodSync(filePath, 0o600); } catch (e) { /* best effort */ }
      return { success: true, id: entry.id };
    } catch (e) {
      return { success: false, error: e.message };
    }
  }

  /**
   * 获取梦境历史摘要
   */
  getDreamHistory(limit = 10) {
    return _getDreamHistory({ rootPath: this.rootPath }, limit);
  }

  /**
   * 从记忆系统提取梦境原材料（增强版）
   */
  _getDreamFragments() {
    return getDreamFragments({
      identityCore: this.identityCore,
      lesson: this.lesson,
      memory: this.memory,
      evolution: this.evolution,
      psychology: this.psychology,
      rootPath: this.rootPath,
    });
  }

  /**
   * 生成梦的叙事报告
   */
  _generateDreamNarrative(dreamResult, consolidation, fragments) {
    const lines = [];
    const now = new Date().toLocaleString('zh-CN', { hour12: false });

    lines.push(`**【梦境报告】** ${now}`);
    lines.push('');

    // ─── 叙事核心：选中的记忆 + L1~L6 哲学叙事 ─────────────────────────
    const chosen = dreamResult?.results?.synthesize?.chosen_memory;
    const structure = dreamResult?.results?.synthesize?.narrative_structure;
    if (structure) {
      lines.push(`${structure.emoji} **${structure.layerName}之梦**`);
      lines.push('');
      lines.push(`> 梦选择了这段记忆：${structure.setup.replace('梦选择了这段记忆：', '')}`);
      lines.push('');
      lines.push(`${structure.desc}`);
      lines.push('');
      lines.push(`**「${structure.question}」**`);
      lines.push('');
      lines.push(`*${structure.metaphor}*`);
      lines.push('');
      lines.push(`→ *${structure.elevation}*`);
      lines.push('');
      lines.push(`---`);
      lines.push('');
    } else {
      lines.push(`> 记忆原材料：${fragments.length}条`);
      lines.push('');
    }

    // 洞察摘要
    const insight = dreamResult?.results?.synthesize?.insight;
    if (insight && insight !== 'No significant patterns to synthesize.') {
      // insight 已经在上面的结构化叙事里展示了，这里只展示额外的主题
      const themes = dreamResult?.results?.synthesize?.themes || [];
      if (themes.length > 0) {
        lines.push(`**浮现主题**：${themes.map(t => `\`${t}\``).join(' · ')}`);
        lines.push('');
      }
    }

    // 记忆强化/修剪
    const pruned = consolidation?.pruning?.pruned_count || 0;
    const retained = consolidation?.pruning?.retained_count || 0;
    if (pruned > 0 || retained > 0) {
      lines.push(`**记忆变化**：强化 ${retained} 条 · 修剪 ${pruned} 条`);
      lines.push('');
    }

    // 质量评分
    const quality = consolidation?.quality?.overallQuality || 0;
    const stars = '★'.repeat(Math.round(quality * 5)) + '☆'.repeat(5 - Math.round(quality * 5));
    lines.push(`**梦境质量**：${stars} ${Math.round(quality * 100)}%`);
    lines.push('');
    lines.push('*在梦中继续进化。*');

    return lines.join('\n');
  }

  detectIdentityDrift() {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.self.detectDrift();
  }

  processEmotionally(input) {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.emotion.process(input);
  }

  getTopLessons(limit = 5) {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.lesson.getTopLessons(limit);
  }

  getMemoryStats() {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.memory.getMemoryStats();
  }

  getTrialityStats() {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.triality ? this.triality.getLayerStats() : { error: 'not loaded' };
  }

  getMindSpace() {
    if (!this.started) throw new Error('HeartFlow not started');
    const ms = this.mindSpace; // 触发惰性加载
    if (!ms) return { rules: [], error: 'mindSpace not available' };
    return { rules: ms.rules, workingEntries: Object.entries(this.memory?.ephemeral || {}).slice(0, 10) };
  }

  remember(key, value, tier = 'learned') {
    if (!this.started) throw new Error('HeartFlow not started');
    if (tier === 'core') return this.memory.addCore(key, value);
    if (tier === 'ephemeral') return this.memory.remember(key, value);
    return this.memory.learn(key, value);
  }

  search(query) {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.memory.search(query);
  }

  getPsychologyStats() {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.psychology.getPsychologyStats();
  }

  /**
   * 哲学分析 — 调用 PhilosophyEngine 综合分析
   * @param {string} [text] - 输入文本（可选传空获取状态）
   * @param {object} [context={}] - 上下文
   * @returns {object} 综合哲学分析报告
   */
  analyzePhilosophy(text = '', context = {}) {
    if (!this.started) throw new Error('HeartFlow not started');
    if (!this.philosophy) return { error: 'philosophy engine not available' };
    return this.philosophy.analyze(text, context);
  }

  /**
   * AI 心理学分析 — 调用 AIPsychologyEngine
   * @param {string} action - 分析动作 (analyzeAICognitiveState/analyzeAIBiases/analyzeAIStressors/estimateAIStage/checkAICoherence/analyzeAIDeep)
   * @param {*} [input] - 输入参数
   * @returns {object} AI 心理学分析结果
   */
  analyzeAIPsychology(action, input) {
    if (!this.started) throw new Error('HeartFlow not started');
    if (!this.aiPsychology) return { error: 'aiPsychology engine not available' };
    if (typeof this.aiPsychology[action] === 'function') {
      return this.aiPsychology[action](input);
    }
    return { error: `unknown aiPsychology action: ${action}` };
  }

  /**
   * AI 哲学分析 — 调用 AIPhilosophyEngine
   * @param {string} action - 分析动作 (analyzeAIBeing/analyzeAIEpistemology/analyzeAIEthics/analyzeAIAesthetics/analyzeAITeleology/analyzeAITemporality/wisdomInquiry/getStats)
   * @param {*} [input] - 输入参数
   * @returns {object} AI 哲学分析结果
   */
  analyzeAIPhilosophy(action, input) {
    if (!this.started) throw new Error('HeartFlow not started');
    if (!this.aiPhilosophy) return { error: 'aiPhilosophy engine not available' };
    if (typeof this.aiPhilosophy[action] === 'function') {
      return this.aiPhilosophy[action](input);
    }
    return { error: `unknown aiPhilosophy action: ${action}` };
  }

  /**
   * 智慧咨询 — 多哲学学派视角分析
   * @param {string} problem - 问题描述
   * @param {string} [perspective] - 学派视角（缺省则综合分析）
   * @returns {object} 多视角哲学分析
   */
  wisdomInquiry(problem, perspective) {
    if (!this.started) throw new Error('HeartFlow not started');
    if (!this.philosophy) return { error: 'philosophy engine not available' };
    return this.philosophy.wisdomInquiry(problem, perspective);
  }

  getEvolutionStats() {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.evolution.getStats();
  }

  /**
   * 从自我反思历史生成技能
   * 将 evolution loop 的改进建议转化为可安装技能
   */
  triggerSkillGeneration() {
    if (!this.started) throw new Error('HeartFlow not started');
    try {
      const result = this.skillGenerator.processLatestReport();
      return result;
    } catch (e) {
      return { success: false, error: e.message };
    }
  }

  /**
   * 完整进化：evolve + 应用改进
   * 输入上下文 → 生成改进 → 自动写入学教训库
   */
  async evolveImprove(input, context = {}) {
    if (!this.started) throw new Error('HeartFlow not started');
    // 1. 运行进化循环（async）
    const evolveResult = await this.evolution.evolve(input, context);
    const improvements = evolveResult.improvements || [];
    
    // 2. 将改进建议写入学教训库
    const applied = [];
    for (const imp of improvements) {
      try {
        this.lesson.addLesson({
          errorPattern: `[${imp.area}] ${imp.action}`,
          correction: imp.action,
          rootCause: imp.area,
          skill: imp.area,
          confidence: imp.priority === 'high' ? 0.9 : imp.priority === 'medium' ? 0.7 : 0.5,
        });
        applied.push(imp);
      } catch (e) {
        // 失败不阻断
      }
    }
    
    return {
      ...evolveResult,
      improvementsApplied: applied.length,
      improvementsTotal: improvements.length,
    };
  }

  getDreamStats() {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.dream.getDreamStats();
  }

  getTruthfulnessStats() {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.truth.getStats();
  }

  getLessonStats() {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.lesson.getStats();
  }

  getVerificationStats() {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.verify.getStats();
  }

  getSelfModelStats() {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.self.getStats();
  }

  // Knowledge
  addKnowledge(name, description, type = 'concept', importance = 0.5) {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.knowledge.addNode({ name, description, type, importance });
  }

  searchKnowledge(query) {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.knowledge.search(query);
  }

  getKnowledgeStats() {
    if (!this.started) throw new Error('HeartFlow not started');
    return this.knowledge.getStats();
  }

}

// Factory
function createHeartFlow(config = {}) {
  return new HeartFlow(config);
}

// CLI
if (require.main === module) {
  const rootPath = path.join(__dirname, '..', '..');
  const hf = createHeartFlow({ rootPath });
  hf.start();

  const t0 = Date.now();
  hf.healthCheck().then(health => {
    console.log(`[HeartFlow] ${VERSION} health check (${Date.now() - t0}ms):`);
    // Run dispatch smoke tests
    const tests = [
      ['truth.checkStatement', '这个方案一定是对的'],
      ['lesson.getTopLessons', 3],
    ];
    let passed = 0, failed = 0;
    for (const [route, ...args] of tests) {
      try {
        hf.dispatch(route, ...args);
        passed++;
      } catch (e) {
        console.error(`  FAIL ${route}: ${e.message}`);
        failed++;
      }
    }
    console.log(`  dispatch tests: ${passed} passed, ${failed} failed`);

    hf.stop();
    process.exit(failed > 0 ? 1 : 0);
  }).catch(e => {
    console.error('Error:', e);
    hf.stop();
    process.exit(1);
  });
}

module.exports = { HeartFlow, createHeartFlow, VERSION: _VERSION().VERSION, MentalEffortTracker: _MentalEffortTracker().MentalEffortTracker };
