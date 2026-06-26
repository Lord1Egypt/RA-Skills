import { randomUUID } from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { definePluginEntry } from "@openclaw/plugin-sdk/plugin-entry";
import { resolvePreferredOpenClawTmpDir } from "@openclaw/plugin-sdk/temp-path";
import { CORRECTION_PROMPT } from "./constants.js";
import { containsDashes, verifyRewrite } from "./utils.js";
const DEFAULT_TIMEOUT_MS = 15000;
function resolvePluginConfig(pluginConfig) {
    return pluginConfig && typeof pluginConfig === "object"
        ? pluginConfig
        : {};
}
function resolveRewriteTimeoutMs(pluginConfig) {
    const raw = pluginConfig.rewriteTimeoutMs;
    const parsed = typeof raw === "number"
        ? raw
        : typeof raw === "string"
            ? Number.parseInt(raw, 10)
            : Number.NaN;
    return Number.isFinite(parsed) && parsed > 0 ? parsed : DEFAULT_TIMEOUT_MS;
}
function buildRewriteRunSuffix() {
    return `${Date.now().toString(36)}-${randomUUID().slice(0, 8)}`;
}
export default definePluginEntry({
    id: "deaiify",
    name: "deAIify",
    description: "Intercepts em-dashes and en-dashes in outbound replies. " +
        "Rewrites via embedded LLM so sentences are properly restructured, not just character-swapped.",
    register(api) {
        const pluginConfig = resolvePluginConfig(api.pluginConfig);
        // ── Hook 1: before_agent_reply (PRIMARY) ──────────────────────────────
        //
        // Fires after the LLM generates its reply, before delivery.
        // If banned dashes are detected (outside code blocks), calls
        // runEmbeddedPiAgent with a restructuring prompt.
        //
        // Fail-open: any error returns { handled: false } so the original
        // reply is still delivered unchanged.
        api.on("before_agent_reply", async (event, ctx) => {
            if (pluginConfig.enabled === false) {
                return { handled: false };
            }
            if (ctx.runId?.startsWith("deaiify-") ||
                ctx.sessionKey?.includes(":deaiify:")) {
                return { handled: false };
            }
            const text = event.cleanedBody ?? "";
            if (!text || !containsDashes(text)) {
                return { handled: false };
            }
            api.logger.info("[deAIify] Banned dash detected. Rewriting via embedded agent.");
            const agentId = ctx.agentId?.trim() || "main";
            const workspaceDir = api.runtime.agent.resolveAgentWorkspaceDir(api.config, agentId);
            const agentDir = api.runtime.agent.resolveAgentDir(api.config, agentId);
            const runSuffix = buildRewriteRunSuffix();
            const runId = `deaiify-${runSuffix}`;
            const sessionFile = path.join(resolvePreferredOpenClawTmpDir(), `deaiify-${runSuffix}.jsonl`);
            try {
                const result = await api.runtime.agent.runEmbeddedPiAgent({
                    sessionId: runId,
                    sessionKey: ctx.sessionKey ? `${ctx.sessionKey}:deaiify:${runSuffix}` : undefined,
                    agentId,
                    messageChannel: ctx.channelId,
                    messageProvider: ctx.messageProvider,
                    sessionFile,
                    workspaceDir,
                    agentDir,
                    config: api.config,
                    prompt: CORRECTION_PROMPT + text,
                    provider: ctx.modelProviderId,
                    model: ctx.modelId,
                    timeoutMs: resolveRewriteTimeoutMs(pluginConfig),
                    runId,
                    trigger: "manual",
                    disableMessageTool: true,
                    disableTools: true,
                    bootstrapContextMode: "lightweight",
                    verboseLevel: "off",
                    reasoningLevel: "off",
                    silentExpected: true,
                });
                const rewritten = (result.payloads ?? [])
                    .map((payload) => payload.text ?? "")
                    .filter(Boolean)
                    .join("\n")
                    .trim();
                if (!rewritten) {
                    api.logger.warn("[deAIify] Embedded rewrite returned empty output. Delivering original.");
                    return { handled: false };
                }
                if (containsDashes(rewritten)) {
                    api.logger.warn("[deAIify] Rewrite still contained banned dashes. Delivering original.");
                    return { handled: false };
                }
                if (!verifyRewrite(text, rewritten)) {
                    api.logger.warn("[deAIify] Rewrite failed verification gate (word count drift or length expansion out of range). " +
                        "Delivering original reply unchanged.");
                    return { handled: false };
                }
                api.logger.info("[deAIify] Rewrite accepted. Delivering rewritten reply.");
                return { handled: true, reply: { text: rewritten } };
            }
            catch (err) {
                api.logger.error(`[deAIify] Embedded rewrite failed: ${err instanceof Error ? err.message : String(err)}`);
                return { handled: false };
            }
            finally {
                await fs.unlink(sessionFile).catch(() => undefined);
            }
        });
        // ── Hook 2: message_sending (ABSOLUTE LAST-RESORT FALLBACK) ───────────
        //
        // This hook should almost never fire.
        // If it does, it means before_agent_reply was skipped or failed to handle.
        // Log a warning so we can diagnose the problem.
        // Apply minimal string cleanup so the user at least gets readable output.
        api.on("message_sending", (event, _ctx) => {
            if (pluginConfig.enabled === false) {
                return;
            }
            const text = event.content ?? "";
            if (!text || !containsDashes(text)) {
                return;
            }
            api.logger.warn("[deAIify] WARNING: message_sending fallback fired. " +
                "This means before_agent_reply did not handle this message. " +
                "Check hook registration and plugin load order.");
            const cleaned = text
                .replace(/\u2014/g, ", ")
                .replace(/\u2013/g, "-");
            return { content: cleaned };
        });
    },
});
//# sourceMappingURL=index.js.map