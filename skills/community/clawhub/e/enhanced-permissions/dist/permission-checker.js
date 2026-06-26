"use strict";
/**
 * Permission Checker Implementation
 * Based on Claw Code permission system
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultPermissionChecker = exports.PermissionChecker = void 0;
const types_1 = require("./types");
/**
 * Operation to permission level mapping
 */
const OPERATION_PERMISSIONS = {
    // === SAFE (Read operations) ===
    'read': types_1.PermissionLevel.SAFE,
    'read_file': types_1.PermissionLevel.SAFE,
    'list_directory': types_1.PermissionLevel.SAFE,
    'web_search': types_1.PermissionLevel.SAFE,
    'web_fetch': types_1.PermissionLevel.SAFE,
    'memory_search': types_1.PermissionLevel.SAFE,
    'memory_get': types_1.PermissionLevel.SAFE,
    'image': types_1.PermissionLevel.SAFE,
    'sessions_list': types_1.PermissionLevel.SAFE,
    'sessions_history': types_1.PermissionLevel.SAFE,
    'session_status': types_1.PermissionLevel.SAFE,
    'subagents': types_1.PermissionLevel.SAFE,
    'cron': types_1.PermissionLevel.SAFE,
    // === MODERATE (Write operations) ===
    'write': types_1.PermissionLevel.MODERATE,
    'edit': types_1.PermissionLevel.MODERATE,
    'file_write': types_1.PermissionLevel.MODERATE,
    'memory_update': types_1.PermissionLevel.MODERATE,
    'sessions_send': types_1.PermissionLevel.MODERATE,
    'sessions_yield': types_1.PermissionLevel.MODERATE,
    // === DANGEROUS (Delete/Execute) ===
    'exec': types_1.PermissionLevel.DANGEROUS,
    'process': types_1.PermissionLevel.DANGEROUS,
    'delete_file': types_1.PermissionLevel.DANGEROUS,
    'sessions_spawn': types_1.PermissionLevel.DANGEROUS,
    'sessions_kill': types_1.PermissionLevel.DANGEROUS,
    'cron_remove': types_1.PermissionLevel.DANGEROUS,
    // === DESTRUCTIVE (Irreversible) ===
    'rm_rf': types_1.PermissionLevel.DESTRUCTIVE,
    'format_disk': types_1.PermissionLevel.DESTRUCTIVE,
    'drop_table': types_1.PermissionLevel.DESTRUCTIVE,
    'purge_sessions': types_1.PermissionLevel.DESTRUCTIVE,
    'delete_all_memories': types_1.PermissionLevel.DESTRUCTIVE
};
/**
 * Permission level scores for comparison
 */
const PERMISSION_SCORES = {
    [types_1.PermissionLevel.SAFE]: 1,
    [types_1.PermissionLevel.MODERATE]: 2,
    [types_1.PermissionLevel.DANGEROUS]: 3,
    [types_1.PermissionLevel.DESTRUCTIVE]: 4
};
/**
 * Risk level display
 */
const RISK_EMOJIS = {
    [types_1.PermissionLevel.SAFE]: '🟢',
    [types_1.PermissionLevel.MODERATE]: '🟡',
    [types_1.PermissionLevel.DANGEROUS]: '🟠',
    [types_1.PermissionLevel.DESTRUCTIVE]: '🔴'
};
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
class PermissionChecker {
    constructor(options) {
        this.userLevel = types_1.PermissionLevel.MODERATE;
        this.requireConfirm = types_1.PermissionLevel.MODERATE;
        this.trustedSessions = new Set();
        this.auditLog = [];
        if (options?.userLevel) {
            this.userLevel = options.userLevel;
        }
        if (options?.requireConfirm) {
            this.requireConfirm = options.requireConfirm;
        }
        if (options?.trustedSessions) {
            options.trustedSessions.forEach(s => this.trustedSessions.add(s));
        }
    }
    /**
     * Check if an operation is allowed
     */
    async check(operation, context) {
        const requiredLevel = this.getPermissionLevel(operation);
        // Check if user has sufficient permission
        if (this.getLevelScore(requiredLevel) > this.getLevelScore(this.userLevel)) {
            return {
                allowed: false,
                requiresConfirm: false,
                reason: `Insufficient permission level: ${requiredLevel}. Your level: ${this.userLevel}`
            };
        }
        // Check if confirmation is required
        const needsConfirm = this.getLevelScore(requiredLevel) >=
            this.getLevelScore(this.requireConfirm);
        // Auto-approve in trusted sessions for MODERATE operations
        if (needsConfirm &&
            this.trustedSessions.has(context.sessionId) &&
            requiredLevel === types_1.PermissionLevel.MODERATE) {
            return {
                allowed: true,
                requiresConfirm: false,
                reason: 'Auto-approved in trusted session'
            };
        }
        // Build confirmation message if needed
        let confirmMessage;
        if (needsConfirm) {
            confirmMessage = this.buildConfirmMessage(operation, context, requiredLevel);
        }
        return {
            allowed: true,
            requiresConfirm: needsConfirm,
            reason: needsConfirm ? 'User confirmation required' : undefined,
            confirmMessage
        };
    }
    /**
     * Get permission level for an operation
     */
    getPermissionLevel(operation) {
        return OPERATION_PERMISSIONS[operation] || types_1.PermissionLevel.MODERATE;
    }
    /**
     * Add a session to trusted list
     */
    addTrustedSession(sessionId) {
        this.trustedSessions.add(sessionId);
    }
    /**
     * Remove a session from trusted list
     */
    removeTrustedSession(sessionId) {
        this.trustedSessions.delete(sessionId);
    }
    /**
     * Check if a session is trusted
     */
    isTrustedSession(sessionId) {
        return this.trustedSessions.has(sessionId);
    }
    /**
     * Log an operation to audit log
     */
    logOperation(entry) {
        this.auditLog.push(entry);
    }
    /**
     * Get audit log entries
     */
    getAuditLog() {
        return this.auditLog;
    }
    /**
     * Get risk emoji for display
     */
    getRiskEmoji(level) {
        return RISK_EMOJIS[level];
    }
    // === Private Methods ===
    getLevelScore(level) {
        return PERMISSION_SCORES[level];
    }
    buildConfirmMessage(operation, context, level) {
        const emoji = this.getRiskEmoji(level);
        let message = `${emoji} **Permission Required**\n\n`;
        message += `**Operation**: \`${operation}\`\n`;
        message += `**Risk Level**: ${emoji} ${level.toUpperCase()}\n`;
        message += `**Parameters**:\n\`\`\`json\n${JSON.stringify(context.params, null, 2)}\n\`\`\`\n\n`;
        if (level === types_1.PermissionLevel.DESTRUCTIVE) {
            message += `🔴 **This operation is DESTRUCTIVE and irreversible!**\n\n`;
            message += `Type \`${'CONFIRM'}\` to proceed, or \`${'CANCEL'}\` to abort.`;
        }
        else if (level === types_1.PermissionLevel.DANGEROUS) {
            message += `⚠️ **This operation may be dangerous**\n\n`;
            message += `Reply \`y\` to confirm, \`n\` to cancel.`;
        }
        else {
            message += `Reply \`y\` to confirm, \`n\` to cancel.`;
        }
        return message;
    }
}
exports.PermissionChecker = PermissionChecker;
/**
 * Default permission checker instance
 */
exports.defaultPermissionChecker = new PermissionChecker({
    userLevel: types_1.PermissionLevel.MODERATE,
    requireConfirm: types_1.PermissionLevel.MODERATE,
    trustedSessions: ['main-session'] // Auto-approve MODERATE in main session
});
//# sourceMappingURL=permission-checker.js.map