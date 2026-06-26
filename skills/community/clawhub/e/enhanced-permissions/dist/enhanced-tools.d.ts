/**
 * Enhanced Tool Implementations
 * Based on Claw Code patterns with Zod validation
 */
import { Tool } from './types';
/**
 * Read file tool with validation
 */
export declare const readFileTool: Tool<{
    path: string;
    limit?: number;
    offset?: number;
}>;
/**
 * List directory tool
 */
export declare const listDirectoryTool: Tool<{
    path: string;
    recursive?: boolean;
}>;
/**
 * Write file tool with validation
 */
export declare const writeFileTool: Tool<{
    path: string;
    content: string;
    append?: boolean;
}>;
/**
 * Edit file tool (text replacement)
 */
export declare const editFileTool: Tool<{
    path: string;
    oldText: string;
    newText: string;
    replaceAll?: boolean;
}>;
/**
 * Execute command tool with strict validation
 */
export declare const execCommandTool: Tool<{
    command: string;
    timeout?: number;
}>;
/**
 * Delete file tool
 */
export declare const deleteFileTool: Tool<{
    path: string;
    recursive?: boolean;
}>;
/**
 * Register all enhanced tools
 */
export declare function registerAllEnhancedTools(registry: any): void;
//# sourceMappingURL=enhanced-tools.d.ts.map