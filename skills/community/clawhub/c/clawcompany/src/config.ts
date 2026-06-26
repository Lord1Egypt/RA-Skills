/**
 * 配置管理
 */

export interface ClawCompanyConfig {
  // GLM API 配置
  glmApiKey?: string
  glmModel: string
  
  // 项目配置
  projectRoot: string
  
  // Agent 配置
  pmAgentThinking: 'low' | 'medium' | 'high'
  devAgentRuntime: 'acp' | 'subagent'
  reviewAgentThinking: 'low' | 'medium' | 'high'
  
  // 调试配置
  verbose: boolean
  dryRun: boolean
}

const defaultConfig: ClawCompanyConfig = {
  glmModel: 'glm-5',
  projectRoot: process.cwd(),
  pmAgentThinking: 'high',
  devAgentRuntime: 'acp',
  reviewAgentThinking: 'high',
  verbose: false,
  dryRun: false
}

/**
 * 加载配置
 */
export function loadConfig(overrides?: Partial<ClawCompanyConfig>): ClawCompanyConfig {
  const config = { ...defaultConfig }
  
  // 从环境变量加载
  if (process.env.GLM_API_KEY) {
    config.glmApiKey = process.env.GLM_API_KEY
  }
  
  if (process.env.GLM_MODEL) {
    config.glmModel = process.env.GLM_MODEL
  }
  
  if (process.env.PROJECT_ROOT) {
    config.projectRoot = process.env.PROJECT_ROOT
  }
  
  if (process.env.VERBOSE === 'true') {
    config.verbose = true
  }
  
  if (process.env.DRY_RUN === 'true') {
    config.dryRun = true
  }
  
  // 应用覆盖配置
  if (overrides) {
    Object.assign(config, overrides)
  }
  
  // 验证必需配置
  if (!config.glmApiKey) {
    console.warn('⚠️ GLM_API_KEY 未设置，PM/Review Agent 可能无法工作')
  }
  
  return config
}

/**
 * 验证配置
 */
export function validateConfig(config: ClawCompanyConfig): string[] {
  const errors: string[] = []
  
  if (!config.glmApiKey) {
    errors.push('GLM_API_KEY is required')
  }
  
  if (!config.projectRoot) {
    errors.push('PROJECT_ROOT is required')
  }
  
  return errors
}
