"use strict";
/**
 * 配置管理
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.loadConfig = loadConfig;
exports.validateConfig = validateConfig;
const defaultConfig = {
    glmModel: 'glm-5',
    projectRoot: process.cwd(),
    pmAgentThinking: 'high',
    devAgentRuntime: 'acp',
    reviewAgentThinking: 'high',
    verbose: false,
    dryRun: false
};
/**
 * 加载配置
 */
function loadConfig(overrides) {
    const config = { ...defaultConfig };
    // 从环境变量加载
    if (process.env.GLM_API_KEY) {
        config.glmApiKey = process.env.GLM_API_KEY;
    }
    if (process.env.GLM_MODEL) {
        config.glmModel = process.env.GLM_MODEL;
    }
    if (process.env.PROJECT_ROOT) {
        config.projectRoot = process.env.PROJECT_ROOT;
    }
    if (process.env.VERBOSE === 'true') {
        config.verbose = true;
    }
    if (process.env.DRY_RUN === 'true') {
        config.dryRun = true;
    }
    // 应用覆盖配置
    if (overrides) {
        Object.assign(config, overrides);
    }
    // 验证必需配置
    if (!config.glmApiKey) {
        console.warn('⚠️ GLM_API_KEY 未设置，PM/Review Agent 可能无法工作');
    }
    return config;
}
/**
 * 验证配置
 */
function validateConfig(config) {
    const errors = [];
    if (!config.glmApiKey) {
        errors.push('GLM_API_KEY is required');
    }
    if (!config.projectRoot) {
        errors.push('PROJECT_ROOT is required');
    }
    return errors;
}
