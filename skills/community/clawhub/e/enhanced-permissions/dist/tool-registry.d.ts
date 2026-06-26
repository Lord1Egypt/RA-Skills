/**
 * Tool Registry with Schema Caching
 * Based on Claw Code tool system
 */
import { Tool, ToolResult } from './types';
import { PermissionChecker } from './permission-checker';
/**
 * Tool Registry Class
 *
 * Features:
 * - Centralized tool management
 * - Schema caching (saves ~500 tokens per tool)
 * - Permission checking integration
 * - Execution tracking
 *
 * Usage:
 * ```typescript
 * const registry = new ToolRegistry();
 * registry.register(myTool);
 *
 * const result = await registry.execute('read_file', { path: 'test.txt' });
 * ```
 */
export declare class ToolRegistry {
    private tools;
    private schemaCache;
    private permissionChecker;
    private executionLog;
    constructor(permissionChecker?: PermissionChecker);
    /**
     * Register a tool
     */
    register(tool: Tool): void;
    /**
     * Unregister a tool
     */
    unregister(toolName: string): void;
    /**
     * Execute a tool by name
     */
    execute<T = any>(toolName: string, params: any, context?: {
        sessionId?: string;
    }): Promise<ToolResult & {
        data?: T;
    }>;
    /**
     * Get cached schema (saves ~500 tokens)
     */
    getCachedSchema(toolName: string): string | undefined;
    /**
     * Get all registered tools
     */
    getAllTools(): Tool[];
    /**
     * Get tool by name
     */
    getTool(toolName: string): Tool | undefined;
    /**
     * Get execution statistics
     */
    getExecutionStats(): {
        totalExecutions: number;
        successRate: number;
        averageTokensUsed: number;
    };
    /**
     * Get token savings from schema caching
     */
    getSchemaCacheSavings(): number;
    /**
     * Clear execution log
     */
    clearExecutionLog(): void;
}
/**
 * Default tool registry instance
 */
export declare const defaultToolRegistry: ToolRegistry;
//# sourceMappingURL=tool-registry.d.ts.map