/**
 * 配置管理
 */
export interface ClawCompanyConfig {
    glmApiKey?: string;
    glmModel: string;
    projectRoot: string;
    pmAgentThinking: 'low' | 'medium' | 'high';
    devAgentRuntime: 'acp' | 'subagent';
    reviewAgentThinking: 'low' | 'medium' | 'high';
    verbose: boolean;
    dryRun: boolean;
}
/**
 * 加载配置
 */
export declare function loadConfig(overrides?: Partial<ClawCompanyConfig>): ClawCompanyConfig;
/**
 * 验证配置
 */
export declare function validateConfig(config: ClawCompanyConfig): string[];
