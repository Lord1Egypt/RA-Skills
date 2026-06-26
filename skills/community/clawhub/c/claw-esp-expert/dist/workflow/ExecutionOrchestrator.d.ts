import { AsyncBuildManager, type BuildResult } from '../build/AsyncBuildManager';
import { FlashMonitorManager, type FlashMonitorResult } from '../monitor/FlashMonitorManager';
import { PinmuxAuditor, type AuditResult } from '../build/PinmuxAuditor';
export interface ExecuteProjectResult {
    status: 'REJECTED' | 'BUILD_FAILED' | 'FLASH_FAILED' | 'SUCCESS';
    chip: string;
    resolvedChip: string;
    issues: AuditResult[];
    build?: BuildResult;
    flashMonitor?: FlashMonitorResult;
    summary: string;
}
export declare class ExecutionOrchestrator {
    private readonly auditor;
    private readonly builder;
    private readonly flashMonitorManager;
    constructor(auditor: PinmuxAuditor, builder: AsyncBuildManager, flashMonitorManager: FlashMonitorManager);
    execute(args: {
        projectPath: string;
        chip: string;
        port?: string;
        baud?: number;
        elfPath?: string;
        addr2lineBin?: string;
        onProgress?: (message: string) => void;
    }): Promise<ExecuteProjectResult>;
}
