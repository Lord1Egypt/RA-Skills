/**
 * Permission Checker Implementation
 * Based on Claw Code permission system
 */
import { PermissionLevel, PermissionResult, OperationContext, AuditLogEntry } from './types';
/**
 * Permission Checker Class
 *
 * Usage:
 * ```typescript
 * const checker = new PermissionChecker();
 * const result = await checker.check('exec', { sessionId: 'abc', operation: 'exec', params: {...}, timestamp: Date.now() });
 * if (result.allowed && !result.requiresConfirm) {
 *   // Execute directly
 * } else if (result.requiresConfirm) {
 *   // Ask user for confirmation
 * }
 * ```
 */
export declare class PermissionChecker {
    private userLevel;
    private requireConfirm;
    private trustedSessions;
    private auditLog;
    constructor(options?: {
        userLevel?: PermissionLevel;
        requireConfirm?: PermissionLevel;
        trustedSessions?: string[];
    });
    /**
     * Check if an operation is allowed
     */
    check(operation: string, context: OperationContext): Promise<PermissionResult>;
    /**
     * Get permission level for an operation
     */
    getPermissionLevel(operation: string): PermissionLevel;
    /**
     * Add a session to trusted list
     */
    addTrustedSession(sessionId: string): void;
    /**
     * Remove a session from trusted list
     */
    removeTrustedSession(sessionId: string): void;
    /**
     * Check if a session is trusted
     */
    isTrustedSession(sessionId: string): boolean;
    /**
     * Log an operation to audit log
     */
    logOperation(entry: AuditLogEntry): void;
    /**
     * Get audit log entries
     */
    getAuditLog(): AuditLogEntry[];
    /**
     * Get risk emoji for display
     */
    getRiskEmoji(level: PermissionLevel): string;
    private getLevelScore;
    private buildConfirmMessage;
}
/**
 * Default permission checker instance
 */
export declare const defaultPermissionChecker: PermissionChecker;
//# sourceMappingURL=permission-checker.d.ts.map