import { SessionInfo } from '../lib/session-utils.js';
import { RepairResult } from '../lib/session-repair.js';

/**
 * repair-session command - Repair corrupted OpenClaw session transcripts
 *
 * Fixes issues like:
 * - Aborted tool calls with partial JSON
 * - Orphaned tool_result messages referencing non-existent tool_use IDs
 * - Broken parent chain references
 */

interface RepairSessionOptions {
    sessionId?: string;
    agentId?: string;
    backup?: boolean;
    dryRun?: boolean;
}
/**
 * Resolve the session to repair
 */
declare function resolveSession(options: RepairSessionOptions): SessionInfo | null;
/**
 * Format repair result for CLI output
 */
declare function formatRepairResult(result: RepairResult, options?: {
    dryRun?: boolean;
}): string;
/**
 * Main repair-session command handler
 */
declare function repairSessionCommand(options: RepairSessionOptions): Promise<RepairResult>;
/**
 * List available sessions for an agent (for --list flag)
 */
declare function listAgentSessions(agentId?: string): string;

export { type RepairSessionOptions, formatRepairResult, listAgentSessions, repairSessionCommand, resolveSession };
