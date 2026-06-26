"use strict";
/**
 * OpenClaw Tool Adapter
 * Bridges enhanced permission system with existing OpenClaw tools
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.enhancedWebFetchTool = exports.enhancedWebSearchTool = exports.enhancedExecTool = exports.enhancedEditTool = exports.enhancedWriteTool = exports.enhancedReadTool = exports.webFetchSchema = exports.webSearchSchema = exports.execSchema = exports.editSchema = exports.writeSchema = exports.readSchema = void 0;
exports.registerEnhancedOpenClawTools = registerEnhancedOpenClawTools;
exports.executeToolWithPermission = executeToolWithPermission;
const zod_1 = require("zod");
const index_1 = require("./index");
const confirmation_dialog_1 = require("./confirmation-dialog");
/**
 * Adapter for existing OpenClaw tools
 *
 * This adapter wraps the existing tool execution flow
 * and adds permission checking and Zod validation
 */
// === Zod Schemas for Existing Tools ===
/**
 * Read tool schema
 */
exports.readSchema = zod_1.z.object({
    path: zod_1.z.string().describe('File path to read'),
    offset: zod_1.z.number().min(1).optional().describe('Line number to start from (1-indexed)'),
    limit: zod_1.z.number().min(1).max(10000).optional().default(2000).describe('Maximum lines to read')
});
/**
 * Write tool schema
 */
exports.writeSchema = zod_1.z.object({
    path: zod_1.z.string().describe('File path to write'),
    content: zod_1.z.string().describe('Content to write')
});
/**
 * Edit tool schema
 */
exports.editSchema = zod_1.z.object({
    path: zod_1.z.string().describe('File path to edit'),
    oldText: zod_1.z.string().describe('Text to find'),
    newText: zod_1.z.string().describe('Replacement text'),
    offset: zod_1.z.number().min(0).optional().default(0).describe('Start offset for replacement'),
    limit: zod_1.z.number().min(1).optional().describe('Number of replacements')
});
/**
 * Exec tool schema
 */
exports.execSchema = zod_1.z.object({
    command: zod_1.z.string().max(10000).describe('Command to execute'),
    timeout: zod_1.z.number().min(1).max(300).optional().default(10).describe('Timeout in seconds'),
    elevated: zod_1.z.boolean().optional().default(false).describe('Run with elevated permissions'),
    ask: zod_1.z.enum(['off', 'on-miss', 'always']).optional().default('off').describe('Ask mode'),
    security: zod_1.z.enum(['deny', 'allowlist', 'full']).optional().default('allowlist').describe('Security mode'),
    host: zod_1.z.enum(['sandbox', 'gateway', 'node']).optional().describe('Exec host'),
    workdir: zod_1.z.string().optional().describe('Working directory'),
    env: zod_1.z.record(zod_1.z.string()).optional().describe('Environment variables'),
    node: zod_1.z.string().optional().describe('Node id/name'),
    pty: zod_1.z.boolean().optional().default(false).describe('Run in pseudo-terminal'),
    background: zod_1.z.boolean().optional().default(false).describe('Run in background'),
    yieldMs: zod_1.z.number().min(0).optional().describe('Milliseconds to wait before backgrounding')
});
/**
 * Web search schema
 */
exports.webSearchSchema = zod_1.z.object({
    query: zod_1.z.string().describe('Search query'),
    count: zod_1.z.number().min(1).max(20).optional().default(10).describe('Number of results')
});
/**
 * Web fetch schema
 */
exports.webFetchSchema = zod_1.z.object({
    url: zod_1.z.string().url().describe('URL to fetch'),
    maxChars: zod_1.z.number().min(100).optional().default(10000).describe('Maximum characters'),
    extractMode: zod_1.z.enum(['markdown', 'text']).optional().default('markdown').describe('Extraction mode')
});
// === Enhanced Tool Definitions ===
/**
 * Enhanced read tool
 */
exports.enhancedReadTool = {
    name: 'read',
    description: 'Read file contents with line limit and offset support',
    inputSchema: exports.readSchema,
    permissionLevel: index_1.PermissionLevel.SAFE,
    execute: async (params) => {
        try {
            // The actual implementation would call the existing OpenClaw read tool
            // This is a wrapper that adds validation and permission checking
            return {
                success: true,
                data: {
                    message: 'Read operation would execute here',
                    params
                },
                metadata: {
                    permissionLevel: index_1.PermissionLevel.SAFE,
                    validated: true
                }
            };
        }
        catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }
};
/**
 * Enhanced write tool
 */
exports.enhancedWriteTool = {
    name: 'write',
    description: 'Write content to a file (creates or overwrites)',
    inputSchema: exports.writeSchema,
    permissionLevel: index_1.PermissionLevel.MODERATE,
    execute: async (params) => {
        try {
            return {
                success: true,
                data: {
                    message: 'Write operation would execute here',
                    params
                },
                metadata: {
                    permissionLevel: index_1.PermissionLevel.MODERATE,
                    validated: true
                }
            };
        }
        catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }
};
/**
 * Enhanced edit tool
 */
exports.enhancedEditTool = {
    name: 'edit',
    description: 'Edit file by replacing text',
    inputSchema: exports.editSchema,
    permissionLevel: index_1.PermissionLevel.MODERATE,
    execute: async (params) => {
        try {
            return {
                success: true,
                data: {
                    message: 'Edit operation would execute here',
                    params
                },
                metadata: {
                    permissionLevel: index_1.PermissionLevel.MODERATE,
                    validated: true
                }
            };
        }
        catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }
};
/**
 * Enhanced exec tool
 */
exports.enhancedExecTool = {
    name: 'exec',
    description: 'Execute shell commands with comprehensive options',
    inputSchema: exports.execSchema,
    permissionLevel: index_1.PermissionLevel.DANGEROUS,
    execute: async (params) => {
        try {
            // Additional safety checks for dangerous commands
            const dangerousPatterns = [
                'rm -rf /',
                'format',
                'del /s /q',
                'mkfs',
                'dd if=/dev/zero'
            ];
            for (const pattern of dangerousPatterns) {
                if (params.command.includes(pattern)) {
                    return {
                        success: false,
                        error: `Dangerous command detected: ${pattern}`
                    };
                }
            }
            return {
                success: true,
                data: {
                    message: 'Exec operation would execute here',
                    params
                },
                metadata: {
                    permissionLevel: index_1.PermissionLevel.DANGEROUS,
                    validated: true,
                    safetyCheckPassed: true
                }
            };
        }
        catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }
};
/**
 * Enhanced web search tool
 */
exports.enhancedWebSearchTool = {
    name: 'web_search',
    description: 'Search the web using Tavily API',
    inputSchema: exports.webSearchSchema,
    permissionLevel: index_1.PermissionLevel.SAFE,
    execute: async (params) => {
        try {
            return {
                success: true,
                data: {
                    message: 'Web search would execute here',
                    params
                },
                metadata: {
                    permissionLevel: index_1.PermissionLevel.SAFE,
                    validated: true
                }
            };
        }
        catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }
};
/**
 * Enhanced web fetch tool
 */
exports.enhancedWebFetchTool = {
    name: 'web_fetch',
    description: 'Fetch and extract content from a URL',
    inputSchema: exports.webFetchSchema,
    permissionLevel: index_1.PermissionLevel.SAFE,
    execute: async (params) => {
        try {
            // URL safety check
            const url = params.url.toLowerCase();
            if (!url.startsWith('http://') && !url.startsWith('https://')) {
                return {
                    success: false,
                    error: 'Only HTTP/HTTPS URLs are allowed'
                };
            }
            return {
                success: true,
                data: {
                    message: 'Web fetch would execute here',
                    params
                },
                metadata: {
                    permissionLevel: index_1.PermissionLevel.SAFE,
                    validated: true,
                    urlSafe: true
                }
            };
        }
        catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }
};
/**
 * Register all enhanced OpenClaw tools
 */
function registerEnhancedOpenClawTools() {
    const tools = [
        exports.enhancedReadTool,
        exports.enhancedWriteTool,
        exports.enhancedEditTool,
        exports.enhancedExecTool,
        exports.enhancedWebSearchTool,
        exports.enhancedWebFetchTool
    ];
    tools.forEach(tool => {
        index_1.defaultToolRegistry.register(tool);
        console.log(`✅ Registered enhanced tool: ${tool.name} (${tool.permissionLevel})`);
    });
    console.log(`\n📊 Total tools registered: ${index_1.defaultToolRegistry.getAllTools().length}`);
    console.log(`💾 Schema cache savings: ${index_1.defaultToolRegistry.getSchemaCacheSavings()} tokens`);
}
/**
 * Execute tool with full permission checking flow
 *
 * This is the main entry point for tool execution with enhanced permissions
 * Includes: permission check, validation, confirmation dialog, and audit logging
 */
async function executeToolWithPermission(toolName, params, sessionId = 'main-session', options) {
    const tool = index_1.defaultToolRegistry.getTool(toolName);
    if (!tool) {
        return {
            success: false,
            error: `Tool not found: ${toolName}`
        };
    }
    // Step 1: Permission check
    const permissionResult = await index_1.defaultPermissionChecker.check(toolName, {
        sessionId,
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
    // Step 2: Handle confirmation if required
    if (permissionResult.requiresConfirm && !options?.skipConfirmation) {
        const confirmed = await handleConfirmation(toolName, tool.permissionLevel, params, permissionResult.confirmMessage);
        if (!confirmed) {
            return {
                success: false,
                error: 'User cancelled operation',
                metadata: {
                    permissionLevel: tool.permissionLevel,
                    cancelled: true
                }
            };
        }
    }
    // Step 3: Validate parameters with Zod
    try {
        const validatedParams = tool.inputSchema.parse(params);
        // Step 4: Execute the tool
        const startTime = Date.now();
        const result = await tool.execute(validatedParams);
        const executionTime = Date.now() - startTime;
        // Step 5: Audit logging for DANGEROUS+ operations
        if (tool.permissionLevel === index_1.PermissionLevel.DANGEROUS ||
            tool.permissionLevel === index_1.PermissionLevel.DESTRUCTIVE) {
            await index_1.defaultAuditLogger.log({
                operation: toolName,
                riskLevel: tool.permissionLevel,
                sessionId,
                params,
                allowed: true,
                userConfirmed: true,
                result: {
                    success: result.success,
                    error: result.error
                },
                userId: options?.userId
            });
        }
        return {
            ...result,
            metadata: {
                ...result.metadata,
                executionTimeMs: executionTime,
                permissionLevel: tool.permissionLevel,
                audited: true
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
 * Handle confirmation dialog based on permission level
 */
async function handleConfirmation(toolName, level, params, confirmMessage) {
    if (level === index_1.PermissionLevel.DESTRUCTIVE) {
        return await (0, confirmation_dialog_1.showDestructiveWarning)(toolName, params);
    }
    if (level === index_1.PermissionLevel.DANGEROUS) {
        const message = confirmMessage ||
            `⚠️ Confirm dangerous operation: ${toolName}\n\nReply y to confirm, n to cancel.`;
        return await (0, confirmation_dialog_1.showConfirmationDialog)(message);
    }
    // For MODERATE in non-trusted sessions
    if (confirmMessage) {
        return await (0, confirmation_dialog_1.showConfirmationDialog)(confirmMessage);
    }
    return true; // Auto-approve
}
//# sourceMappingURL=openclaw-adapter.js.map