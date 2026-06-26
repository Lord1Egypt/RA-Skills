/**
 * Design 模块索引
 * 
 * 版本：V1.0.0
 * 状态：✅ 完成
 */

// 配置加载器
export {
  DesignSystemConfigLoader,
  default as DesignSystemConfigLoaderDefault,
} from './design-system-config';

// UI/UX Harness 集成
export {
  DesignHarness,
  getDesignHarness,
  default as DesignHarnessDefault,
} from './design-harness';

// 类型定义
export type {
  DesignMappingConfig,
  DesignSystemMeta,
  MatchResult,
} from './design-system-config';

export type {
  DesignContext,
  DesignSystemResponse,
} from './design-harness';
