/**
 * Remote Runtime Module
 * Supports: remote / ssh / teleport modes
 */
export interface RuntimeModeReport {
    readonly mode: string;
    readonly connected: boolean;
    readonly detail: string;
}
export declare function asText(report: RuntimeModeReport): string;
export declare function runRemoteMode(target: string): RuntimeModeReport;
export declare function runSshMode(target: string): RuntimeModeReport;
export declare function runTeleportMode(target: string): RuntimeModeReport;
