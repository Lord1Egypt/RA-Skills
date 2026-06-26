"use strict";
/**
 * Enhanced Tool Implementations
 * Based on Claw Code patterns with Zod validation
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteFileTool = exports.execCommandTool = exports.editFileTool = exports.writeFileTool = exports.listDirectoryTool = exports.readFileTool = void 0;
exports.registerAllEnhancedTools = registerAllEnhancedTools;
const zod_1 = require("zod");
const types_1 = require("./types");
// === SAFE Tools (Read operations) ===
/**
 * Read file tool with validation
 */
exports.readFileTool = {
    name: 'read_file',
    description: 'Read contents of a file with optional line limit and offset',
    inputSchema: zod_1.z.object({
        path: zod_1.z.string().describe('File path to read'),
        limit: zod_1.z.number().min(1).max(10000).optional().default(2000).describe('Maximum lines to read'),
        offset: zod_1.z.number().min(1).optional().default(1).describe('Start line number (1-indexed)')
    }),
    permissionLevel: types_1.PermissionLevel.SAFE,
    examples: [
        { path: 'README.md' },
        { path: 'src/main.ts', limit: 100 },
        { path: 'logs/app.log', limit: 50, offset: 100 }
    ],
    execute: async ({ path, limit = 2000, offset = 1 }) => {
        try {
            // Implementation would use the actual read tool
            // This is a template showing the structure
            return {
                success: true,
                data: {
                    content: `File content here (lines ${offset} to ${offset + limit - 1})`,
                    lines: limit,
                    path
                },
                metadata: {
                    tokensUsed: 150,
                    executionTimeMs: 45
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
 * List directory tool
 */
exports.listDirectoryTool = {
    name: 'list_directory',
    description: 'List contents of a directory',
    inputSchema: zod_1.z.object({
        path: zod_1.z.string().describe('Directory path'),
        recursive: zod_1.z.boolean().optional().default(false).describe('List recursively')
    }),
    permissionLevel: types_1.PermissionLevel.SAFE,
    execute: async ({ path, recursive = false }) => {
        try {
            return {
                success: true,
                data: {
                    path,
                    recursive,
                    entries: ['file1.txt', 'file2.md', 'subdir/']
                },
                metadata: {
                    tokensUsed: 100,
                    executionTimeMs: 30
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
// === MODERATE Tools (Write operations) ===
/**
 * Write file tool with validation
 */
exports.writeFileTool = {
    name: 'write_file',
    description: 'Write content to a file (creates or overwrites)',
    inputSchema: zod_1.z.object({
        path: zod_1.z.string().describe('File path to write'),
        content: zod_1.z.string().describe('Content to write'),
        append: zod_1.z.boolean().optional().default(false).describe('Append to existing file')
    }),
    permissionLevel: types_1.PermissionLevel.MODERATE,
    examples: [
        { path: 'test.txt', content: 'Hello World' },
        { path: 'logs/app.log', content: 'New log entry', append: true }
    ],
    execute: async ({ path, content, append = false }) => {
        try {
            return {
                success: true,
                data: {
                    path,
                    bytesWritten: content.length,
                    appended: append
                },
                metadata: {
                    tokensUsed: 50,
                    executionTimeMs: 20
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
 * Edit file tool (text replacement)
 */
exports.editFileTool = {
    name: 'edit_file',
    description: 'Replace text in a file',
    inputSchema: zod_1.z.object({
        path: zod_1.z.string().describe('File path to edit'),
        oldText: zod_1.z.string().describe('Text to find and replace'),
        newText: zod_1.z.string().describe('Replacement text'),
        replaceAll: zod_1.z.boolean().optional().default(false).describe('Replace all occurrences')
    }),
    permissionLevel: types_1.PermissionLevel.MODERATE,
    execute: async ({ path, oldText, newText, replaceAll = false }) => {
        try {
            return {
                success: true,
                data: {
                    path,
                    replacements: replaceAll ? 'all' : 'first'
                },
                metadata: {
                    tokensUsed: 80,
                    executionTimeMs: 35
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
// === DANGEROUS Tools (Delete/Execute) ===
/**
 * Execute command tool with strict validation
 */
exports.execCommandTool = {
    name: 'exec',
    description: 'Execute a shell command',
    inputSchema: zod_1.z.object({
        command: zod_1.z.string()
            .max(10000)
            .describe('Command to execute')
            .refine(cmd => !cmd.includes('rm -rf /') && !cmd.includes('format'), 'Dangerous command detected'),
        timeout: zod_1.z.number().min(1).max(300).optional().default(30).describe('Timeout in seconds')
    }),
    permissionLevel: types_1.PermissionLevel.DANGEROUS,
    execute: async ({ command, timeout = 30 }) => {
        try {
            return {
                success: true,
                data: {
                    command,
                    timeout,
                    output: 'Command output here'
                },
                metadata: {
                    tokensUsed: 200,
                    executionTimeMs: timeout * 1000
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
 * Delete file tool
 */
exports.deleteFileTool = {
    name: 'delete_file',
    description: 'Delete a file or directory',
    inputSchema: zod_1.z.object({
        path: zod_1.z.string().describe('File or directory path to delete'),
        recursive: zod_1.z.boolean().optional().default(false).describe('Delete recursively for directories')
    }),
    permissionLevel: types_1.PermissionLevel.DANGEROUS,
    execute: async ({ path, recursive = false }) => {
        try {
            return {
                success: true,
                data: {
                    path,
                    deleted: true,
                    recursive
                },
                metadata: {
                    tokensUsed: 50,
                    executionTimeMs: 25
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
// === Tool Registry Helper ===
/**
 * Register all enhanced tools
 */
function registerAllEnhancedTools(registry) {
    const tools = [
        exports.readFileTool,
        exports.listDirectoryTool,
        exports.writeFileTool,
        exports.editFileTool,
        exports.execCommandTool,
        exports.deleteFileTool
    ];
    tools.forEach(tool => registry.register(tool));
}
//# sourceMappingURL=enhanced-tools.js.map