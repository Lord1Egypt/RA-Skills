/**
 * ClawWall Plugin — OpenClaw DLP Bridge
 *
 * Hooks into `before_tool_call` to scan outbound content via the
 * ClawWall Python service. Enforces BLOCK/REDACT decisions.
 */
interface PluginConfig {
    serviceUrl: string;
    blockOnError: boolean;
    timeoutMs: number;
}
interface ToolCallContext {
    toolName: string;
    args: Record<string, unknown>;
    agentId?: string;
    destination?: string;
}
interface HookResult {
    allow: boolean;
    modifiedArgs?: Record<string, unknown>;
    reason?: string;
}
/**
 * Main hook export — called by OpenClaw before each tool call.
 */
export declare function beforeToolCall(context: ToolCallContext, pluginConfig?: Partial<PluginConfig>): Promise<HookResult>;
export {};
