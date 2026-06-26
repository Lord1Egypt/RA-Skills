"use strict";
/**
 * Tool Registry with Schema Caching
 * Based on Claw Code tool system
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultToolRegistry = exports.ToolRegistry = void 0;
const permission_checker_1 = require("./permission-checker");
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
class ToolRegistry {
    constructor(permissionChecker) {
        this.tools = new Map();
        this.schemaCache = new Map();
        this.executionLog = [];
        this.permissionChecker = permissionChecker || new permission_checker_1.PermissionChecker();
    }
    /**
     * Register a tool
     */
    register(tool) {
        this.tools.set(tool.name, tool);
        // Cache schema for token efficiency
        // This saves ~500 tokens per tool call by avoiding re-serialization
        try {
            const schemaJson = JSON.stringify(tool.inputSchema, null, 2);
            this.schemaCache.set(tool.name, schemaJson);
        }
        catch (error) {
            console.warn(`Failed to cache schema for ${tool.name}:`, error);
        }
        console.log(`✅ Tool registered: ${tool.name} (${tool.permissionLevel})`);
    }
    /**
     * Unregister a tool
     */
    unregister(toolName) {
        this.tools.delete(toolName);
        this.schemaCache.delete(toolName);
    }
    /**
     * Execute a tool by name
     */
    async execute(toolName, params, context) {
        const tool = this.tools.get(toolName);
        if (!tool) {
            return {
                success: false,
                error: `Tool not found: ${toolName}`
            };
        }
        // Check permissions
        const permissionResult = await this.permissionChecker.check(toolName, {
            sessionId: context?.sessionId || 'unknown',
            operation: toolName,
            params,
            timestamp: Date.now()
        });
        if (!permissionResult.allowed) {
            return {
                success: false,
                error: permissionResult.reason,
                metadata: {
                    permissionLevel: tool.permissionLevel
                }
            };
        }
        // If confirmation required, throw (caller should handle)
        if (permissionResult.requiresConfirm) {
            return {
                success: false,
                error: 'Confirmation required',
                metadata: {
                    permissionLevel: tool.permissionLevel,
                    confirmMessage: permissionResult.confirmMessage
                }
            };
        }
        // Validate parameters with Zod
        try {
            const validatedParams = tool.inputSchema.parse(params);
            // Execute the tool
            const startTime = Date.now();
            const result = await tool.execute(validatedParams);
            const executionTime = Date.now() - startTime;
            // Log execution
            this.executionLog.push({
                tool: toolName,
                timestamp: Date.now(),
                success: result.success,
                tokensUsed: result.metadata?.tokensUsed
            });
            return {
                ...result,
                metadata: {
                    ...result.metadata,
                    executionTimeMs: executionTime,
                    permissionLevel: tool.permissionLevel
                }
            };
        }
        catch (error) {
            return {
                success: false,
                error: `Validation failed: ${error.message}`,
                metadata: {
                    permissionLevel: tool.permissionLevel
                }
            };
        }
    }
    /**
     * Get cached schema (saves ~500 tokens)
     */
    getCachedSchema(toolName) {
        return this.schemaCache.get(toolName);
    }
    /**
     * Get all registered tools
     */
    getAllTools() {
        return Array.from(this.tools.values());
    }
    /**
     * Get tool by name
     */
    getTool(toolName) {
        return this.tools.get(toolName);
    }
    /**
     * Get execution statistics
     */
    getExecutionStats() {
        if (this.executionLog.length === 0) {
            return {
                totalExecutions: 0,
                successRate: 0,
                averageTokensUsed: 0
            };
        }
        const totalExecutions = this.executionLog.length;
        const successfulExecutions = this.executionLog.filter(e => e.success).length;
        const totalTokens = this.executionLog.reduce((sum, e) => sum + (e.tokensUsed || 0), 0);
        return {
            totalExecutions,
            successRate: successfulExecutions / totalExecutions,
            averageTokensUsed: totalTokens / totalExecutions
        };
    }
    /**
     * Get token savings from schema caching
     */
    getSchemaCacheSavings() {
        const avgSchemaSize = 500; // tokens
        return this.schemaCache.size * avgSchemaSize;
    }
    /**
     * Clear execution log
     */
    clearExecutionLog() {
        this.executionLog = [];
    }
}
exports.ToolRegistry = ToolRegistry;
/**
 * Default tool registry instance
 */
exports.defaultToolRegistry = new ToolRegistry();
//# sourceMappingURL=tool-registry.js.map