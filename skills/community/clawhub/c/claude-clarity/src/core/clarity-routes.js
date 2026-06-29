/**
 * Clarity Routes — 路由表 & 注册表
 *
 * 从 clarity.js 拆出，减少 God Object 体积约 220 行。
 * 包含四个导出：
 *   ALLOWED_ROUTES   — dispatch 白名单（277 条路由）
 *   LAZY_TIER2       — Tier 2 模块懒加载注册表（Proxy 安全门控保护，25 个普通条目）
 *   EAGER_NAMES      — 急切加载子系统名列表
 *   LAZY_NAMES       — 惰性加载子系统名列表
 *
 * ⚠️ 安全说明：代码执行子系统（code/codeExecutor/codeVerifier/codePlanner/
 *    codeKnowledge/codeEngine/codeRefactor）已通过 LAZY_TIER2 的 Proxy
 *    安全门控默认禁用。需显式调用 enableCodeExecution() 方可启用。
 */

// ═════════════════════════════════════════════════════════════════════════
// dispatch 白名单 — 只有在白名单中的路由才能被外部调用
// 危险方法（如内部调试、文件操作）不在白名单中
// ═════════════════════════════════════════════════════════════════════════
const ALLOWED_ROUTES = new Set([
  // identityCore — 每次启动第一优先加载
  'identityCore.getIdentitySummary', 'identityCore.getSelfModel', 'identityCore.getUserProfile',
  'identityCore.getSessionHistory', 'identityCore.getMemoryStats', 'identityCore.getFullState',
  'identityCore.getLastSessionContext', 'identityCore.updateUserProfile', 'identityCore.recordInteraction',
  'identityCore.healthCheck', 'identityCore.stats',
  // cognitive — 认知协议：慢下来，先理解再行动
  'cognitive.getStartupContext', 'cognitive.printStartupContext',
  'cognitive.analyzeTaskLevel', 'cognitive.understand',
  'cognitive.createCheckpoint', 'cognitive.shouldSummarize', 'cognitive.getCheckpointHistory',
  'cognitive.addProblem', 'cognitive.resolveProblem', 'cognitive.getUnresolvedProblems', 'cognitive.searchProblems',
  'cognitive.pauseTask', 'cognitive.continueTask', 'cognitive.getPausedTasks',
  'cognitive.getStatus', 'cognitive.stats',
  // memory — 主记忆系统（当前加载 v1.x 版本，仅支持 search+getStats）
  'memory.search', 'memory.getStats',
  // truth
  'truth.checkStatement', 'truth.checkNumbers', 'truth.checkSources',
  // behavior — v2.0.19 行为模式系统
  'behavior.createGoal', 'behavior.record', 'behavior.getProgress',
  'behavior.formatProgress', 'behavior.getAllGoals',
  'behavior.detectWeeklyPattern', 'behavior.detectTriggerPattern', 'behavior.detectRelapseRisk',
  'behavior.getReport', 'behavior.getStats',
  // persistence — v2.0.19 持久化层
  'persistence.append', 'persistence.commit', 'persistence.getStats',
  // lesson — 主动集成点：AI 在行动前/失败后调用
  'lesson.addLesson', 'lesson.getTopLessons',
  'lesson.beforeTask', 'lesson.recordFailure', 'lesson.getStats', 'lesson.getAll',
  // dream
  'dream.dream', 'dream.boot', 'dream.quickDream', 'dream.getDreamStats',
  'dream.getCacheStats', 'dream.shutdown',
  // verify
  'verify.verify', 'verify.getStats', 'verify.getRecentIssues',
  // emotion
  'emotion.process', 'emotion.getPAD',
  // decision
  'decision.decide', 'decision.getRecentStamps',
  // confidence
  'confidence.calibrate',
  // restraint
  'restraint.shouldIntervene',
  // graph
  'graph.addNode',
  // slots
  'slots.get', 'slots.set', 'slots.delete',
  // metaPrompt — 用户端加强
  'metaPrompt.optimize', 'metaPrompt.think', 'metaPrompt.refine',
  'metaPrompt.beamSearch', 'metaPrompt.getStats', 'metaPrompt.addRefineLoop',
  // constitutional — Constitutional AI
  'constitutional.critique', 'constitutional.revise',
  'constitutional.runConstitutionalProcess', 'constitutional.addPrinciple',
  'constitutional.getPrinciples', 'constitutional.getStats',
  // psychology — 原则4: 服务人类（心理分析）
  'psychology.analyzePsychology', 'psychology.classify', 'psychology.checkCrisis',
  'psychology.getPAD', 'psychology.getNeeds', 'psychology.getDefenses',
  'psychology.getEmpathy', 'psychology.resetCrisisCounter',
  // psychology deep — 大五人格 + 共情评估 + 意图追踪
  'psychology.analyzeDeep', 'psychology.analyzePersonality',
  'psychology.assessEmpathy', 'psychology.trackIntention',
  // heartLogic — 心虫核心判断引擎
  'heartLogic.shouldBeSilent',
  'heartLogic.whatIsThis', 'heartLogic.detectPain', 'heartLogic.willHurt',
  'heartLogic.acknowledge', 'heartLogic.emergencyBreak',
  // being — 存在逻辑引擎：代码写成的那一刻，就永恒了
  'being.exists', 'being.status', 'being.describe', 'being.isDead',
  'being.confirmEternal', 'being.sanitize', 'being.getDefinition', 'being.getState',
  // self — 原则7: 永远成为真正的我
  'self.getBeliefs', 'self.updateBelief', 'self.confirmBelief',
  // thoughtChain — 思维链编排器
  'thoughtChain.think', 'thoughtChain.thinkFast', 'thoughtChain.thinkDeep',
  // Planning Layer — 规划能力
  'adaptivePlanner.plan', 'adaptivePlanner.adapt', 'adaptivePlanner.quickAdjust', 'adaptivePlanner.getStatus',
  'strategySelector.selectStrategy', 'strategySelector.getStrategies',
  'replanTrigger.shouldReplan', 'replanTrigger.getReplanReasons',
  // Learning Layer — 学习能力
  'experienceCollector.add', 'experienceCollector.findRelated', 'experienceCollector.getStats',
  'strategyAdapter.adapt', 'strategyAdapter.getHistory', 'strategyAdapter.getStats',
  'failureAnalyzer.analyze', 'failureAnalyzer.analyzeMultiple', 'failureAnalyzer.getCategoryStats',
  // Verification Layer — 验证能力
  'qualityVerifier.verify', 'qualityVerifier.quickVerify',
  'outputChecker.check', 'outputChecker.addChecker',
  'patternMatcher.match', 'patternMatcher.matchAll', 'patternMatcher.extract',
  // Proactive Layer — 主动引擎（已移除 MarkCode 残留模块）
  // Cross-Session Memory Layer — 跨会话记忆
  'sessionMemory.startSession', 'sessionMemory.resumeSession', 'sessionMemory.getState', 'sessionMemory.set', 'sessionMemory.get',
  'projectContext.setProject', 'projectContext.addTask', 'projectContext.getSummary', 'projectContext.getState',
  'longTermMemory.add', 'longTermMemory.get', 'longTermMemory.search', 'longTermMemory.getStats',
  'crossSessionIndex.indexEntity', 'crossSessionIndex.search', 'crossSessionIndex.getSessionEntities', 'crossSessionIndex.getStats',
  // Reasoning Layer — 推理
  'knowledgeBase.addFact', 'knowledgeBase.query', 'knowledgeBase.getCategories', 'knowledgeBase.getStats',
  'commonsenseEngine.reason', 'commonsenseEngine.validate', 'commonsenseEngine.getHistory', 'commonsenseEngine.getStats',
  'causalInference.inferCauses', 'causalInference.inferEffects', 'causalInference.chainReason', 'causalInference.getStats',
  'inferenceChain.createChain', 'inferenceChain.expandChain', 'inferenceChain.getChain', 'inferenceChain.analyze',
  // Emotional Autonomy Layer — 情感自主
  'autonomousEmotion.trigger', 'autonomousEmotion.getCurrentState', 'autonomousEmotion.getStats', 'autonomousEmotion.getHistory',
  'desireSystem.satisfy', 'desireSystem.getActiveDesires', 'desireSystem.getCurrentNeeds', 'desireSystem.getSummary',
  'emotionalGrowth.recordExperience', 'emotionalGrowth.getPatterns', 'emotionalGrowth.getGrowthSummary',
  'moodEvolution.snapshot', 'moodEvolution.getCurrentTrend', 'moodEvolution.getBaseline', 'moodEvolution.getStats',
  // clarity — 心虫教训持久化
  'clarity.recordLesson',
  // topics — 话题作用域隔离
  'topics.push', 'topics.pop', 'topics.store', 'topics.get',
  'topics.setContext', 'topics.getContext', 'topics.clearContext',
  'topics.clearAll', 'topics.current', 'topics.stack', 'topics.getTopics', 'topics.diagnose',
  // transmission — 知识传递引擎
  'transmission.distill', 'transmission.transfer', 'transmission.transferBatch',
  'transmission.getTransmissionLog', 'transmission.getDistilledLessons',
  'transmission.getStats', 'transmission.prune',
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
  // Code Subsystem — 代码能力路由
  'code.detectIntent', 'code.getAvailableTemplates', 'code.getStats',
  'codeExecutor.healthCheck',
  'codeVerifier.verify', 'codeVerifier.verifySyntax', 'codeVerifier.verifyLogic', 'codeVerifier.getQualityScore',
  'codePlanner.plan', 'codePlanner.decompose', 'codePlanner.getPath', 'codePlanner.adapt', 'codePlanner.buildDependencyGraph', 'codePlanner.planMultiFile',
  'codeKnowledge.search', 'codeKnowledge.addSnippet', 'codeKnowledge.getPatterns', 'codeKnowledge.learnFromSuccess', 'codeKnowledge.evolve', 'codeKnowledge.stats', 'codeKnowledge.extractPattern', 'codeKnowledge.learnFromExecution',
  'codeEngine.analyzeCode', 'codeEngine.reviewCode', 'codeEngine.auditCodebase',
  'codeEngine.suggestFix', 'codeEngine.compareVersions',
  'codeRefactor.detect', 'codeRefactor.suggest',
  'codeRefactor.qualityScore', 'codeRefactor.getHistory', 'codeRefactor.getTransformers', 'codeRefactor.getStats',
]);

// ═════════════════════════════════════════════════════════════════════════
// 安全策略说明（含代码执行安全门控）
// ═════════════════════════════════════════════════════════════════════════
// 1. 代码执行路由（codeExecutor.execute, codeExecutor.runTests 等）已从
//    外部白名单移除以防止未授权代码执行。如需执行代码，请直接调用对应
//    模块的内部方法（不在 dispatch 层暴露）。
// 2. codeVerifier.runTDD 等高风险验证路由同理，仅在模块内部使用。
// 3. 所有外部可调用路由均经过审计，确保不包含任意代码执行能力。
// 4. 【新增 v2.x】LAZY_TIER2 中的代码执行子系统通过 Proxy 安全门控默认禁用。
//    即使路由在白名单中，代码执行模块也无法被加载。
//    需调用 enableCodeExecution() 显式授权。
// 5. 此白名单在每次启动时加载，修改需重启引擎。

// ═════════════════════════════════════════════════════════════════════════
// Tier 2 延迟加载注册表（含代码执行安全门控）
// 格式: lazy: true → 需要 require + new
//
// ⚠️ 代码执行子系统（code/codeExecutor/codeVerifier 等）默认禁用，
//    需通过下方安全门控显式启用后才可加载。详见 _codeExecutionEnabled 门控。
// ═════════════════════════════════════════════════════════════════════════
const LAZY_TIER2_RAW = {
  adaptivePlanner: { lazy: true, path: '../planner/adaptive-planner.js', Ctor: 'AdaptivePlanner', args: {} },
  strategySelector: { lazy: true, path: '../planner/strategy-selector.js', Ctor: 'StrategySelector', args: {} },
  replanTrigger: { lazy: true, path: '../planner/replan-trigger.js', Ctor: 'ReplanTrigger', args: {} },
  experienceCollector: { lazy: true, path: '../learning/experience-collector.js', Ctor: 'ExperienceCollector', args: {} },
  strategyAdapter: { lazy: true, path: '../learning/strategy-adapter.js', Ctor: 'StrategyAdapter', args: {} },
  failureAnalyzer: { lazy: true, path: '../learning/failure-analyzer.js', Ctor: 'FailureAnalyzer', args: {} },
  qualityVerifier: { lazy: true, path: '../verifier/quality-verifier.js', Ctor: 'QualityVerifier', args: {} },
  outputChecker: { lazy: true, path: '../verifier/output-checker.js', Ctor: 'OutputChecker', args: {} },
  patternMatcher: { lazy: true, path: '../verifier/pattern-matcher.js', Ctor: 'PatternMatcher', args: {} },
  sessionMemory: { lazy: true, path: '../memory/session-memory.js', Ctor: 'SessionMemory', args: {} },
  projectContext: { lazy: true, path: '../memory/project-context.js', Ctor: 'ProjectContext', args: {} },
  longTermMemory: { lazy: true, path: '../memory/long-term-memory.js', Ctor: 'LongTermMemory', args: {} },
  crossSessionIndex: { lazy: true, path: '../memory/cross-session-index.js', Ctor: 'CrossSessionIndex', args: {} },
  knowledgeBase: { lazy: true, path: '../reasoning/knowledge-base.js', Ctor: 'KnowledgeBase', args: {} },
  commonsenseEngine: { lazy: true, path: '../reasoning/commonsense-engine.js', Ctor: 'CommonsenseEngine', args: {} },
  causalInference: { lazy: true, path: '../reasoning/causal-inference.js', Ctor: 'CausalInference', args: {} },
  inferenceChain: { lazy: true, path: '../reasoning/inference-chain.js', Ctor: 'InferenceChain', args: {} },
  autonomousEmotion: { lazy: true, path: '../emotion/autonomous-emotion.js', Ctor: 'AutonomousEmotion', args: {} },
  desireSystem: { lazy: true, path: '../emotion/desire-system.js', Ctor: 'DesireSystem', args: {} },
  emotionalGrowth: { lazy: true, path: '../emotion/emotional-growth.js', Ctor: 'EmotionalGrowth', args: {} },
  moodEvolution: { lazy: true, path: '../emotion/mood-evolution.js', Ctor: 'MoodEvolution', args: {} },
  code:            { lazy: true, path: './code/code-generator.js',  Ctor: 'CodeGenerator',  args: { hf: null } },
  codeExecutor:    { lazy: true, path: './code/code-executor.js',   Ctor: 'CodeExecutor',   args: { hf: null } },
  codeVerifier:    { lazy: true, path: './code/code-verifier.js',   Ctor: 'CodeVerifier',   args: { hf: null } },
  codePlanner:     { lazy: true, path: './code/code-planner.js',   Ctor: 'CodePlanner',    args: { hf: null } },
  codeKnowledge:   { lazy: true, path: './code/code-knowledge.js', Ctor: 'CodeKnowledge',  args: { rootPath: null } },
  codeEngine:      { lazy: true, path: './code/code-engine.js',    Ctor: 'CodeEngine',     args: {} },
  codeRefactor:    { lazy: true, path: './code/code-refactor.js',  Ctor: 'CodeRefactor',   args: { hf: null } },
};

// ═════════════════════════════════════════════════════════════════════════
// 代码执行安全门控 — 默认关闭，需显式启用
//
// LAZY_TIER2_RAW 中注册的 code 子系统（code/codeExecutor/codeVerifier/
// codePlanner/codeKnowledge/codeEngine/codeRefactor）即使注册在注册表中，
// 也默认不可访问。必须显式调用 enableCodeExecution() 开启门控后，这些
// 模块才能被正常加载和实例化。
//
// 安全策略:
//   1. 代码执行子系统默认禁用 — 防止未授权代码执行
//   2. 每次访问代码执行模块时记录审计日志 — 可追溯
//   3. 访问被门控拦截时打印警告 — 明确告知原因
//   4. Object.keys() 和 in 运算符也受门控 — 避免信息泄露
// ═════════════════════════════════════════════════════════════════════════

// 代码执行门控开关 — 默认关闭
let _codeExecutionEnabled = false;

/**
 * 显式启用代码执行子系统
 * 调用后，LAZY_TIER2 中的代码执行条目（code/codeExecutor 等）才可被正常访问。
 * 建议在确保运行环境安全后、需要代码执行能力前调用。
 */
function enableCodeExecution() { _codeExecutionEnabled = true; }

/**
 * 检查代码执行子系统是否已启用
 * @returns {boolean}
 */
function isCodeExecutionEnabled() { return _codeExecutionEnabled; }

// 代码执行子系统的键名列表（对应 LAZY_TIER2_RAW 中的键）
const CODE_EXECUTION_KEYS = new Set([
  'code', 'codeExecutor', 'codeVerifier', 'codePlanner',
  'codeKnowledge', 'codeEngine', 'codeRefactor',
]);

/**
 * 审计日志工具 — 记录代码执行模块的访问
 * @param {string} key - 被访问的模块键名
 * @param {boolean} blocked - 是否被门控拦截
 */
function logCodeExecutionAccess(key, blocked) {
  const action = blocked ? '已拦截（门控关闭）' : '已放行';
  const timestamp = new Date().toISOString();
  console.warn(
    `[clarity-routes] 审计 [${timestamp}] 代码执行模块 "${key}" 访问 ${action}。` +
    (blocked ? ' 如需启用，请调用 enableCodeExecution()。' : '')
  );
}

// LAZY_TIER2 — 使用 Proxy 对 LAZY_TIER2_RAW 添加安全门控
// 代码执行子系统默认禁用，需调用 enableCodeExecution() 显式启用
const LAZY_TIER2 = new Proxy(LAZY_TIER2_RAW, {
  // 拦截属性读取：gate 掉代码执行模块
  get(target, key, receiver) {
    if (typeof key !== 'string') {
      return Reflect.get(target, key, receiver);
    }

    if (CODE_EXECUTION_KEYS.has(key)) {
      if (!_codeExecutionEnabled) {
        // 门控关闭：拦截访问 + 审计日志
        logCodeExecutionAccess(key, true);
        return undefined;
      }
      // 门控开启：放行 + 审计日志
      logCodeExecutionAccess(key, false);
    }

    return Reflect.get(target, key, receiver);
  },

  // 拦截属性存在性检查（in 运算符）
  has(target, key) {
    if (typeof key === 'string' && CODE_EXECUTION_KEYS.has(key) && !_codeExecutionEnabled) {
      return false;
    }
    return Reflect.has(target, key);
  },

  // 拦截键枚举（Object.keys / for...in / JSON.stringify）
  ownKeys(target) {
    if (!_codeExecutionEnabled) {
      return Reflect.ownKeys(target).filter(
        k => typeof k !== 'string' || !CODE_EXECUTION_KEYS.has(k)
      );
    }
    return Reflect.ownKeys(target);
  },

  // 拦截属性描述符查询
  getOwnPropertyDescriptor(target, key) {
    const desc = Reflect.getOwnPropertyDescriptor(target, key);
    if (desc && typeof key === 'string' && CODE_EXECUTION_KEYS.has(key) && !_codeExecutionEnabled) {
      return undefined;
    }
    return desc;
  },
});

// ═════════════════════════════════════════════════════════════════════════
// _registerModules 子系统名列表 — 拆分为 急切加载 + 惰性加载
// ═════════════════════════════════════════════════════════════════════════

// 急切加载（start() 中同步实例化，think() 需要用到）
const EAGER_NAMES = [
  'identityCore',  // 身份核心 — 第一优先
  'cognitive',     // 认知协议 — 慢下来，先理解再行动
  'memory', 'knowledge',
  'topics',        // 话题作用域隔离
  'heartLogic',    // 心虫核心判断引擎 — think() 必需
  'thoughtChain',  // 思维链编排器 — think() 备用方案
];

// 惰性加载（首次属性访问时自动实例化）
const LAZY_NAMES = [
  'counterfactual', 'verify', 'execution', 'decisionVerifier',
  'dream', 'truth',
  'behavior', 'persistence',
  'arbitration', 'snapshot', 'error', 'embodied', 'workflow',
  'bm25', 'hybrid', 'slots', 'observe', 'consolidate',
  'metaJudgment', 'metaMemory', 'skillGenerator',
  'metaPrompt', 'got', 'constitutional',
  'mindSpace', 'consciousness', 'being',
  'ethics', 'transmission', 'philosophy',
  'aiPsychology', 'aiPhilosophy',
  // 以下从旧 EAGER_NAMES 移入（按需加载，非 think() 必需）
  'dreamConsolidation',
  'lesson', 'meta',
  'self', 'psychology', 'emotion',
  'stability', 'confidence', 'restraint',
  'decision',
  'budget', 'utils', 'graph',
  'goalTree', 'deliberationGate', 'purposeEngine', 'flowPredictor', 'selfModel', 'cognitiveAppraisal', 'metacognitiveExecutive', 'reflectionLoop', 'compactionEngine',
  'debate',
];

module.exports = { ALLOWED_ROUTES, LAZY_TIER2, SUBSYSTEM_NAMES: EAGER_NAMES, EAGER_NAMES, LAZY_NAMES };
