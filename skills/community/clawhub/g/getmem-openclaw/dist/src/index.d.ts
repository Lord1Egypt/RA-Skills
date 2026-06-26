/**
 * getmem.ai OpenClaw Plugin
 *
 * Adds persistent memory to every OpenClaw agent session.
 * Memory is stored per-user and automatically injected as context
 * before each LLM call via the message:received hook.
 *
 * Install:
 *   openclaw plugins install clawhub:@getmem/openclaw-getmem
 *   openclaw config set plugins.openclaw-getmem.apiKey gm_live_...
 *   openclaw gateway restart
 */
declare const _default: {
    id: string;
    name: string;
    description: string;
    configSchema: import("openclaw/plugin-sdk/plugin-entry").OpenClawPluginConfigSchema;
    register: NonNullable<import("openclaw/plugin-sdk/plugin-entry").OpenClawPluginDefinition["register"]>;
} & Pick<import("openclaw/plugin-sdk/plugin-entry").OpenClawPluginDefinition, "kind" | "reload" | "nodeHostCommands" | "securityAuditCollectors">;
export default _default;
//# sourceMappingURL=index.d.ts.map