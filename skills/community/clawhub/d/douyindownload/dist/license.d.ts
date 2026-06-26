export interface CheckResult {
    allowed: boolean;
    reason?: string;
    upgradeMessage?: string;
    remaining: number | '∞';
    plan: string;
    isPaid: boolean;
}
export declare function activateKey(deviceId: string, key: string): Promise<CheckResult>;
export declare function checkAndRecord(deviceId?: string): CheckResult;
export declare function getStatus(deviceId?: string): CheckResult;
export declare function resetUsage(deviceId?: string): void;
//# sourceMappingURL=license.d.ts.map