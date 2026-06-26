import { type PartitionAdvice } from './PartitionAdvisor';
export interface BuildResult {
    success: boolean;
    errorType?: 'COMPILATION_ERROR' | 'LINK_ERROR' | 'PARTITION_OVERFLOW' | 'ENV_ERROR' | 'MISSING_HEADER' | 'COMPONENT_ERROR' | 'CONFIG_ERROR' | 'MEMORY_OVERFLOW';
    rawError?: string;
    cleanError?: string;
    suggestion?: string;
    partitionAdvice?: PartitionAdvice;
}
export declare class AsyncBuildManager {
    private readonly partitionAdvisor;
    /**
     * 执行异步编译，并实时反馈进度
     */
    build(projectPath: string, onProgress?: (msg: string) => void): Promise<BuildResult>;
    /**
     * 核心诊断算法：语义化提取错误
     */
    private diagnoseError;
}
