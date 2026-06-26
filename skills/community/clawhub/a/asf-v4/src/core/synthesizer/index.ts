/**
 * Core Synthesizer Index - ANFSF v2.0
 * 
 * 统一导出 Core Synthesizer 模块的所有内容
 * 包含类定义和工具函数
 * 
 * @module asf-v4/core/synthesizer
 */

// 类定义
export { 
  DefaultVetoEnforcer, 
  VetoEnforcer,
  createDefaultVetoEnforcer,
  DEFAULT_VETO_RULES,
} from './default-veto-enforcer';

export {
  SafeOnlineOptimizer,
  createSafeOptimizer,
} from './safe-optimizer';

export {
  resolveOwnershipConflict,
  generateConflictReport,
} from './conflict-resolver';