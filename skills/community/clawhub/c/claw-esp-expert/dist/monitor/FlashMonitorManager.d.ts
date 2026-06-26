import { type MonitorAnalysisResult } from './MonitorAnalyzer';
export interface FlashMonitorResult {
    status: 'SUCCESS' | 'FAILED' | 'ENV_ERROR';
    command: string[];
    port?: string;
    baud?: number;
    timeoutMs: number;
    durationMs: number;
    stage: 'preflight' | 'flash_monitor' | 'analysis';
    stageSummary: string;
    log: string;
    logTail: string[];
    analysis?: MonitorAnalysisResult;
    reason?: string;
    failureCategory?: 'TIMEOUT' | 'PORT_PERMISSION' | 'PORT_BUSY' | 'PORT_NOT_FOUND' | 'TOOL_NOT_FOUND' | 'UNKNOWN';
}
export declare class FlashMonitorManager {
    private readonly monitorAnalyzer;
    private readonly defaultTimeoutMs;
    private readonly logTailLines;
    run(args: {
        projectPath: string;
        chip: string;
        port?: string;
        baud?: number;
        elfPath?: string;
        addr2lineBin?: string;
        timeoutMs?: number;
    }): Promise<FlashMonitorResult>;
    private extractLogTail;
    private classifyFailure;
    private buildFailureReason;
    private buildStageSummary;
}
