/**
 * ComfyUI 工作流集成模块
 * 
 * 版本：V1.0.0
 * 状态：🟡 Phase 2 开发中
 * 
 * 导出所有 ComfyUI 相关组件
 */

// ============== Phase 1: 基础组件 ==============

export {
  ComfyUIWorkflowOrchestrator,
  default as ComfyUIWorkflowOrchestratorDefault,
} from './comfyui-workflow-orchestrator';

export type {
  VideoGenerationRequest,
  VideoGenerationResponse,
  GovernanceConfig,
  SandboxConfig,
} from './comfyui-workflow-orchestrator';

export {
  VideoGenerationSkill,
  default as VideoGenerationSkillDefault,
} from './video-generation-skill';

export type {
  VideoGenerationTask,
  TaskStatus,
  TaskExecutionResult,
  AgentMessage,
} from './video-generation-skill';

export {
  VideoQualityGuard,
  default as VideoQualityGuardDefault,
} from './video-quality-guard';

export type {
  QualityCheckItem,
  QualityReport,
  QualityGuardConfig,
  RollbackConfig,
} from './video-quality-guard';

// ============== Phase 2: 治理增强 ==============

export {
  MCPVideoBus,
  default as MCPVideoBusDefault,
} from './mcp-video-bus';

export type {
  MCPMessageType,
  MCPMessageHeaders,
  MCPMessageBody,
  MCPMessage,
  MCPMessageResult,
  MCPBusConfig,
} from './mcp-video-bus';

export {
  InMemoryConfigStore,
  ConfigManager,
  default as ConfigManagerDefault,
} from './governance-config-store';

export type {
  ConfigVersion,
  ConfigSnapshot,
  ConfigStore,
  ConfigValidationResult,
} from './governance-config-store';

export {
  CanaryDeployer,
  default as CanaryDeployerDefault,
} from './canary-deployer';

export type {
  CanaryStage,
  DeployStatus,
  CanaryDeployConfig,
  DeployMetrics,
  DeploySession,
  DeployResult,
} from './canary-deployer';

// ============== Phase 3: 场景扩展 ==============

export {
  ProductDemoGenerator,
  default as ProductDemoGeneratorDefault,
} from './product-demo-generator';

export type {
  ProductInfo,
  DemoVideoConfig,
  DemoScene,
  DemoGenerationTask,
  DemoGenerationResult,
} from './product-demo-generator';

export {
  UserFlowVisualizer,
  default as UserFlowVisualizerDefault,
} from './user-flow-visualizer';

export type {
  UserFlowStep,
  UserFlow,
  FlowVisualizationConfig,
  FlowVisualizationResult,
} from './user-flow-visualizer';

export {
  BrandStyleTransferEngine,
  default as BrandStyleTransferEngineDefault,
} from './brand-style-transfer';

export type {
  BrandStyle,
  StyleTransferConfig,
  StyleTransferResult,
} from './brand-style-transfer';

// ============== Phase 4: 优化迭代 ==============

export {
  PerformanceOptimizer,
  default as PerformanceOptimizerDefault,
} from './performance-optimizer';

export type {
  PerformanceMetrics,
  CacheEntry,
  OptimizerConfig,
  BatchRequest,
} from './performance-optimizer';

export {
  CostOptimizer,
  default as CostOptimizerDefault,
} from './cost-optimizer';

export type {
  CostBreakdown,
  BudgetConfig,
  CostOptimizationStrategy,
  OptimizationSuggestion,
  UsageStats,
} from './cost-optimizer';
