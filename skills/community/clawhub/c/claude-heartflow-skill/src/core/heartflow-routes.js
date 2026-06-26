/**
 * HeartFlow Routes v2.6.4 — 路由表 & 注册表
 *
 * 从 heartflow.js 拆出，减少 God Object 体积约 220 行。
 * 包含三个导出：
 *   ALLOWED_ROUTES   — dispatch 白名单（277 条路由）
 *   LAZY_TIER2       — Tier 2 模块懒加载注册表（32 个条目）
 *   SUBSYSTEM_NAMES  — _registerModules 用到的子系统名列表（47 个）
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
  // memory — 主记忆系统（含 triality 合并后的多通道检索）
  'memory.store', 'memory.retrieve', 'memory.search', 'memory.remove',
  'memory.getLayers', 'memory.getStats',
  'memory.semanticSearch', 'memory.narrativeQuery', 'memory.getRecentNarrative',
  'memory.queryByTimeRange', 'memory.queryByRelationType',
  'memory.searchBySemantic', 'memory.searchByKeywords', 'memory.searchByTimeRange',
  'memory.searchByEmotion', 'memory.searchByAssociation', 'memory.multiChannelSearch',
  'memory.addRelationship', 'memory.consolidateMemories',
  'memory.applyForgettingCurve', 'memory.getMemoryHealth',
  'memory.cleanup', 'memory.exportToFile', 'memory.importFromFile',
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
  // evolution — 原则2: 永远不断升级
  'evolution.evolve', 'evolution.recordOutcome', 'evolution.heal', 'evolution.getStats',
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
  // Proactive Layer — 主动引擎
  'curiosityEngine.registerGap', 'curiosityEngine.getTopCuriosityGaps', 'curiosityEngine.getStats',
  'desireEngine.registerDesire', 'desireEngine.satisfy', 'desireEngine.getDominantDesires', 'desireEngine.getSummary',
  'goalPursuer.shouldPursue', 'goalPursuer.getActiveGoals', 'goalPursuer.getStatus',
  'selfInitiator.shouldAct', 'selfInitiator.initiate', 'selfInitiator.getPendingConfirmations', 'selfInitiator.getStatus',
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
  // heartflow — 心虫教训持久化
  'heartflow.recordLesson',
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
  // Code Subsystem — 代码能力路由
  'code.generate', 'code.generateFile', 'code.detectIntent', 'code.getAvailableTemplates', 'code.getStats',
  'codeExecutor.execute', 'codeExecutor.runTests', 'codeExecutor.sandbox', 'codeExecutor.healthCheck',
  'codeVerifier.verify', 'codeVerifier.verifySyntax', 'codeVerifier.verifyLogic', 'codeVerifier.runTDD', 'codeVerifier.getQualityScore', 'codeVerifier.instrumentCode', 'codeVerifier.runWithCoverage', 'codeVerifier.getCoverageReport',
  'codePlanner.plan', 'codePlanner.decompose', 'codePlanner.getPath', 'codePlanner.adapt', 'codePlanner.buildDependencyGraph', 'codePlanner.planMultiFile',
  'codeKnowledge.search', 'codeKnowledge.addSnippet', 'codeKnowledge.getPatterns', 'codeKnowledge.learnFromSuccess', 'codeKnowledge.evolve', 'codeKnowledge.stats', 'codeKnowledge.extractPattern', 'codeKnowledge.learnFromExecution',
  'codeEngine.analyzeCode', 'codeEngine.reviewCode', 'codeEngine.auditCodebase',
  'codeEngine.suggestFix', 'codeEngine.compareVersions',
  'codeRefactor.detect', 'codeRefactor.suggest', 'codeRefactor.transform',
  'codeRefactor.qualityScore', 'codeRefactor.getHistory', 'codeRefactor.getTransformers', 'codeRefactor.getStats',
]);

// ═════════════════════════════════════════════════════════════════════════
// Tier 2 延迟加载注册表
// 格式: lazy: true → 需要 require + new
// ═════════════════════════════════════════════════════════════════════════
const LAZY_TIER2 = {
  adaptivePlanner: { lazy: true, path: '../planner/adaptive-planner.js', Ctor: 'AdaptivePlanner', args: {} },
  strategySelector: { lazy: true, path: '../planner/strategy-selector.js', Ctor: 'StrategySelector', args: {} },
  replanTrigger: { lazy: true, path: '../planner/replan-trigger.js', Ctor: 'ReplanTrigger', args: {} },
  experienceCollector: { lazy: true, path: '../learning/experience-collector.js', Ctor: 'ExperienceCollector', args: {} },
  strategyAdapter: { lazy: true, path: '../learning/strategy-adapter.js', Ctor: 'StrategyAdapter', args: {} },
  failureAnalyzer: { lazy: true, path: '../learning/failure-analyzer.js', Ctor: 'FailureAnalyzer', args: {} },
  qualityVerifier: { lazy: true, path: '../verifier/quality-verifier.js', Ctor: 'QualityVerifier', args: {} },
  outputChecker: { lazy: true, path: '../verifier/output-checker.js', Ctor: 'OutputChecker', args: {} },
  patternMatcher: { lazy: true, path: '../verifier/pattern-matcher.js', Ctor: 'PatternMatcher', args: {} },
  curiosityEngine: { lazy: true, path: '../proactive/curiosity-engine.js', Ctor: 'CuriosityEngine', args: {} },
  desireEngine: { lazy: true, path: '../proactive/desire-engine.js', Ctor: 'DesireEngine', args: {} },
  goalPursuer: { lazy: true, path: '../proactive/goal-pursuer.js', Ctor: 'GoalPursuer', args: {} },
  selfInitiator: { lazy: true, path: '../proactive/self-initiator.js', Ctor: 'SelfInitiator', args: {} },
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
  'evolution', 'dreamConsolidation',
  'lesson', 'meta',
  'self', 'psychology', 'emotion',
  'stability', 'confidence', 'restraint',
  'decision',
  'budget', 'utils', 'graph',
];

module.exports = { ALLOWED_ROUTES, LAZY_TIER2, SUBSYSTEM_NAMES: EAGER_NAMES, EAGER_NAMES, LAZY_NAMES };
