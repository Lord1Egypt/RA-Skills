export interface EnvCheckResult {
    status: 'READY' | 'FOUND_NOT_EXPORTED' | 'NOT_FOUND';
    path?: string;
    pythonAvailable: boolean;
    idfPyAvailable: boolean;
}
export declare class EnvManager {
    private readonly MIRRORS;
    /**
     * 返回静态的手动安装建议，不在 skill 内主动联网测速
     */
    installIDF(targetPath: string, version?: string): Promise<{
        status: "MANUAL_INSTALL_REQUIRED";
        path: string;
        version: string;
        options: {
            github: {
                repository: string;
                commands: string[];
            };
            gitee: {
                repository: string;
                mirrorAssets: string;
                commands: string[];
            };
        };
        suggestion: string;
    }>;
    /**
     * 环境嗅探：检查现有 IDF 状态
     */
    checkExistingEnv(): Promise<EnvCheckResult>;
    private checkCommandAvailable;
}
