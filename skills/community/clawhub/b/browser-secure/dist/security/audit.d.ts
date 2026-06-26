export interface AuditAction {
    action: string;
    timestamp: string;
    details?: Record<string, unknown>;
    screenshot?: string;
    userApproved?: boolean;
    approvalToken?: string;
}
export interface AuditSession {
    event: 'BROWSER_SECURE_SESSION';
    timestamp: string;
    sessionId: string;
    site?: string;
    vaultTokenHash?: string;
    actions: AuditAction[];
    session: {
        duration: number;
        autoClosed: boolean;
        cleanupSuccess: boolean;
    };
    chainHash: string;
}
export declare function startAuditSession(site?: string): string;
export declare function logAction(action: string, details?: Record<string, unknown>, options?: {
    screenshot?: string;
    userApproved?: boolean;
    approvalToken?: string;
}): void;
export declare function finalizeAuditSession(duration: number, cleanupSuccess: boolean): void;
export declare function readAuditLog(sessionId?: string): AuditSession[];
export declare function getCurrentSessionId(): string | null;
export declare function rotateAuditLog(retentionDays: number): void;
