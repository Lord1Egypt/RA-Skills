/**
 * 配置管理器
 * Configuration Manager - Secure credential storage
 */
interface Credentials {
    appId: string;
    appSecret: string;
}
export declare class ConfigManager {
    private configDir;
    private credentialsFile;
    constructor();
    private ensureConfigDir;
    /**
     * 保存凭证
     * 注意：实际生产环境应该使用系统密钥链（keytar）
     * 这里简化为加密文件存储
     */
    setCredentials(appId: string, appSecret: string): Promise<void>;
    /**
     * 获取凭证
     */
    getCredentials(): Promise<Credentials | null>;
    /**
     * 清除凭证
     */
    clearCredentials(): Promise<void>;
    /**
     * 检查是否已配置
     */
    isConfigured(): Promise<boolean>;
}
export {};
//# sourceMappingURL=config-manager.d.ts.map