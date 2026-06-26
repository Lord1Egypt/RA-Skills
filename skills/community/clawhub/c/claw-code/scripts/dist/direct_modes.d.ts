/**
 * Direct Modes Module
 * Supports: direct-connect / deep-link modes
 */
export interface DirectModeReport {
    readonly mode: string;
    readonly target: string;
    readonly active: boolean;
}
export declare function asText(report: DirectModeReport): string;
export declare function runDirectConnect(target: string): DirectModeReport;
export declare function runDeepLink(target: string): DirectModeReport;
