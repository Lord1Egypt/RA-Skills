/**
 * OpenClaw Tool Adapter
 * Bridges enhanced permission system with existing OpenClaw tools
 */
import { z } from 'zod';
import { Tool, ToolResult } from './index';
/**
 * Adapter for existing OpenClaw tools
 *
 * This adapter wraps the existing tool execution flow
 * and adds permission checking and Zod validation
 */
/**
 * Read tool schema
 */
export declare const readSchema: z.ZodObject<{
    path: z.ZodString;
    offset: z.ZodOptional<z.ZodNumber>;
    limit: z.ZodDefault<z.ZodOptional<z.ZodNumber>>;
}, "strip", z.ZodTypeAny, {
    limit?: number;
    path?: string;
    offset?: number;
}, {
    limit?: number;
    path?: string;
    offset?: number;
}>;
/**
 * Write tool schema
 */
export declare const writeSchema: z.ZodObject<{
    path: z.ZodString;
    content: z.ZodString;
}, "strip", z.ZodTypeAny, {
    path?: string;
    content?: string;
}, {
    path?: string;
    content?: string;
}>;
/**
 * Edit tool schema
 */
export declare const editSchema: z.ZodObject<{
    path: z.ZodString;
    oldText: z.ZodString;
    newText: z.ZodString;
    offset: z.ZodDefault<z.ZodOptional<z.ZodNumber>>;
    limit: z.ZodOptional<z.ZodNumber>;
}, "strip", z.ZodTypeAny, {
    limit?: number;
    path?: string;
    offset?: number;
    oldText?: string;
    newText?: string;
}, {
    limit?: number;
    path?: string;
    offset?: number;
    oldText?: string;
    newText?: string;
}>;
/**
 * Exec tool schema
 */
export declare const execSchema: z.ZodObject<{
    command: z.ZodString;
    timeout: z.ZodDefault<z.ZodOptional<z.ZodNumber>>;
    elevated: z.ZodDefault<z.ZodOptional<z.ZodBoolean>>;
    ask: z.ZodDefault<z.ZodOptional<z.ZodEnum<["off", "on-miss", "always"]>>>;
    security: z.ZodDefault<z.ZodOptional<z.ZodEnum<["deny", "allowlist", "full"]>>>;
    host: z.ZodOptional<z.ZodEnum<["sandbox", "gateway", "node"]>>;
    workdir: z.ZodOptional<z.ZodString>;
    env: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodString>>;
    node: z.ZodOptional<z.ZodString>;
    pty: z.ZodDefault<z.ZodOptional<z.ZodBoolean>>;
    background: z.ZodDefault<z.ZodOptional<z.ZodBoolean>>;
    yieldMs: z.ZodOptional<z.ZodNumber>;
}, "strip", z.ZodTypeAny, {
    node?: string;
    security?: "deny" | "allowlist" | "full";
    command?: string;
    timeout?: number;
    elevated?: boolean;
    ask?: "off" | "on-miss" | "always";
    host?: "node" | "sandbox" | "gateway";
    workdir?: string;
    env?: Record<string, string>;
    pty?: boolean;
    background?: boolean;
    yieldMs?: number;
}, {
    node?: string;
    security?: "deny" | "allowlist" | "full";
    command?: string;
    timeout?: number;
    elevated?: boolean;
    ask?: "off" | "on-miss" | "always";
    host?: "node" | "sandbox" | "gateway";
    workdir?: string;
    env?: Record<string, string>;
    pty?: boolean;
    background?: boolean;
    yieldMs?: number;
}>;
/**
 * Web search schema
 */
export declare const webSearchSchema: z.ZodObject<{
    query: z.ZodString;
    count: z.ZodDefault<z.ZodOptional<z.ZodNumber>>;
}, "strip", z.ZodTypeAny, {
    count?: number;
    query?: string;
}, {
    count?: number;
    query?: string;
}>;
/**
 * Web fetch schema
 */
export declare const webFetchSchema: z.ZodObject<{
    url: z.ZodString;
    maxChars: z.ZodDefault<z.ZodOptional<z.ZodNumber>>;
    extractMode: z.ZodDefault<z.ZodOptional<z.ZodEnum<["markdown", "text"]>>>;
}, "strip", z.ZodTypeAny, {
    url?: string;
    maxChars?: number;
    extractMode?: "markdown" | "text";
}, {
    url?: string;
    maxChars?: number;
    extractMode?: "markdown" | "text";
}>;
/**
 * Enhanced read tool
 */
export declare const enhancedReadTool: Tool;
/**
 * Enhanced write tool
 */
export declare const enhancedWriteTool: Tool;
/**
 * Enhanced edit tool
 */
export declare const enhancedEditTool: Tool;
/**
 * Enhanced exec tool
 */
export declare const enhancedExecTool: Tool;
/**
 * Enhanced web search tool
 */
export declare const enhancedWebSearchTool: Tool;
/**
 * Enhanced web fetch tool
 */
export declare const enhancedWebFetchTool: Tool;
/**
 * Register all enhanced OpenClaw tools
 */
export declare function registerEnhancedOpenClawTools(): void;
/**
 * Execute tool with full permission checking flow
 *
 * This is the main entry point for tool execution with enhanced permissions
 * Includes: permission check, validation, confirmation dialog, and audit logging
 */
export declare function executeToolWithPermission(toolName: string, params: any, sessionId?: string, options?: {
    skipConfirmation?: boolean;
    userId?: string;
}): Promise<ToolResult>;
//# sourceMappingURL=openclaw-adapter.d.ts.map