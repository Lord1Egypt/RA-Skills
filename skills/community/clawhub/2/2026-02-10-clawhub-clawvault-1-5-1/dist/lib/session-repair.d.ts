/**
 * Session transcript repair logic
 *
 * Repairs corrupted OpenClaw session transcripts by:
 * 1. Finding aborted tool_use blocks (stopReason: "aborted", partialJson present)
 * 2. Finding orphaned tool_result messages that reference non-existent tool_use IDs
 * 3. Removing both the aborted entries and orphaned results
 * 4. Relinking parent chain references
 */
interface TranscriptEntry {
    type: 'session' | 'message' | 'compaction' | 'custom' | 'thinking_level_change' | string;
    id: string;
    parentId: string | null;
    timestamp: string;
    message?: {
        role: 'user' | 'assistant' | 'toolResult' | 'system';
        content: Array<{
            type: string;
            id?: string;
            name?: string;
            arguments?: unknown;
            toolCallId?: string;
            toolUseId?: string;
            partialJson?: string;
            text?: string;
        }>;
        stopReason?: string;
        errorMessage?: string;
    };
    summary?: string;
    customType?: string;
    data?: unknown;
    thinkingLevel?: string;
}
interface ToolUseInfo {
    id: string;
    lineNumber: number;
    entryId: string;
    isAborted: boolean;
    isPartial: boolean;
    name?: string;
}
interface CorruptedEntry {
    lineNumber: number;
    entryId: string;
    type: 'aborted_tool_use' | 'orphaned_tool_result';
    toolUseId: string;
    description: string;
}
interface ParentRelink {
    lineNumber: number;
    entryId: string;
    oldParentId: string;
    newParentId: string;
}
interface RepairResult {
    sessionId: string;
    totalLines: number;
    corruptedEntries: CorruptedEntry[];
    parentRelinks: ParentRelink[];
    removedCount: number;
    relinkedCount: number;
    backupPath?: string;
    repaired: boolean;
}
/**
 * Parse a JSONL file into transcript entries with line numbers
 */
declare function parseTranscript(filePath: string): Array<{
    line: number;
    entry: TranscriptEntry;
    raw: string;
}>;
/**
 * Extract all tool_use IDs from assistant messages
 */
declare function extractToolUses(entries: Array<{
    line: number;
    entry: TranscriptEntry;
}>): Map<string, ToolUseInfo>;
/**
 * Find orphaned tool_result messages that reference non-existent or aborted tool_use IDs
 */
declare function findCorruptedEntries(entries: Array<{
    line: number;
    entry: TranscriptEntry;
}>, toolUses: Map<string, ToolUseInfo>): {
    corrupted: CorruptedEntry[];
    entriesToRemove: Set<string>;
};
/**
 * Compute parent chain relinks after removing entries
 */
declare function computeParentRelinks(entries: Array<{
    line: number;
    entry: TranscriptEntry;
}>, entriesToRemove: Set<string>): ParentRelink[];
/**
 * Analyze a session transcript for corruption without modifying it
 */
declare function analyzeSession(filePath: string): RepairResult;
/**
 * Repair a session transcript
 */
declare function repairSession(filePath: string, options?: {
    backup?: boolean;
    dryRun?: boolean;
}): RepairResult;

export { type CorruptedEntry, type ParentRelink, type RepairResult, type ToolUseInfo, type TranscriptEntry, analyzeSession, computeParentRelinks, extractToolUses, findCorruptedEntries, parseTranscript, repairSession };
