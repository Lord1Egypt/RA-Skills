/**
 * OpenClaw Enhanced Permission System
 * Based on Claw Code analysis - 2026-04-01
 */
/**
 * Permission levels for operations
 *
 * - SAFE: Read-only operations, no confirmation needed
 * - MODERATE: Write operations, auto-approve in trusted sessions
 * - DANGEROUS: Delete/Execute operations, always confirm
 * - DESTRUCTIVE: Irreversible operations, explicit confirm + audit
 */
export declare enum PermissionLevel {
    SAFE = "safe",
    MODERATE = "moderate",
    DANGEROUS = "dangerous",
    DESTRUCTIVE = "destructive"
}
/**
 * Tool result interface
 */
export interface ToolResult {
    success: boolean;
    data?: any;
    error?: string;
    metadata?: {
        tokensUsed?: number;
        executionTimeMs?: number;
        permissionLevel?: PermissionLevel;
        confirmMessage?: string;
        cancelled?: boolean;
        audited?: boolean;
        [key: string]: any;
    };
}
/**
 * Standard tool interface with Zod validation
 */
export interface Tool<Params = any, Result = any> {
    /** Tool name (snake_case) */
    name: string;
    /** Human-readable description */
    description: string;
    /** Zod schema for parameter validation */
    inputSchema: any;
    /** Required permission level */
    permissionLevel: PermissionLevel;
    /** Execute the tool */
    execute: (params: Params) => Promise<ToolResult & {
        data?: Result;
    }>;
    /** Optional: Example parameters */
    examples?: Params[];
    /** Optional: Related tools */
    relatedTools?: string[];
}
/**
 * Operation context for permission checking
 */
export interface OperationContext {
    sessionId: string;
    operation: string;
    params: any;
    timestamp: number;
    userId?: string;
}
/**
 * Permission check result
 */
export interface PermissionResult {
    /** Is the operation allowed? */
    allowed: boolean;
    /** Does it require user confirmation? */
    requiresConfirm: boolean;
    /** Reason (if denied or confirmation required) */
    reason?: string;
    /** Suggested confirmation message */
    confirmMessage?: string;
}
/**
 * Audit log entry
 */
export interface AuditLogEntry {
    timestamp: string;
    operation: string;
    riskLevel: PermissionLevel;
    sessionId: string;
    userId?: string;
    params: any;
    allowed: boolean;
    userConfirmed: boolean;
    result: {
        success: boolean;
        error?: string;
    };
}
/**
 * Memory hotness events
 */
export type MemoryEvent = 'created' | 'accessed' | 'referenced' | 'daily_decay' | 'archived';
/**
 * Memory data structure
 */
export interface Memory {
    /** Unique identifier */
    id: string;
    /** Memory content */
    content: string;
    /** Creation timestamp */
    timestamp: number;
    /** Hotness score (0-100) */
    hotness: number;
    /** Tags for categorization */
    tags: string[];
    /** Vector embedding (for similarity search) */
    vector?: number[];
    /** Number of times accessed */
    accessCount: number;
    /** Last access timestamp */
    lastAccessed: number;
    /** Is this memory archived? */
    archived: boolean;
}
/**
 * Memory recall options
 */
export interface RecallOptions {
    /** Maximum number of memories to return */
    limit?: number;
    /** Minimum hotness threshold */
    minHotness?: number;
    /** Filter by tags */
    tags?: string[];
    /** Include archived memories? */
    includeArchived?: boolean;
}
/**
 * Context optimization config
 */
export interface ContextConfig {
    /** Maximum tokens per request */
    tokenBudget: number;
    /** Budget by section */
    sectionBudgets: {
        systemPrompts: number;
        history: number;
        toolSchemas: number;
        skills: number;
        memory: number;
        reserved: number;
    };
    /** Enable schema caching? */
    enableSchemaCache: boolean;
    /** Enable auto-compression? */
    enableAutoCompression: boolean;
}
export type { z } from 'zod';
//# sourceMappingURL=types.d.ts.map