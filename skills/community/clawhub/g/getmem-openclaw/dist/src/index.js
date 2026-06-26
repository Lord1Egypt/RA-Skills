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
import { definePluginEntry, buildPluginConfigSchema } from "openclaw/plugin-sdk/plugin-entry";
import { z } from "openclaw/plugin-sdk/zod";
// ── Config schema (Zod) ───────────────────────────────────────────────────────
const ConfigSchema = z.object({
    apiKey: z.string().min(1, "getmem API key is required"),
    baseUrl: z.string().url().optional().default("https://memory.getmem.ai"),
    enabled: z.boolean().optional().default(true),
});
class GetMemClient {
    apiKey;
    baseUrl;
    constructor(apiKey, baseUrl = "https://memory.getmem.ai") {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl.replace(/\/+$/, "");
    }
    async post(path, body) {
        const res = await fetch(`${this.baseUrl}${path}`, {
            method: "POST",
            headers: {
                Authorization: `Bearer ${this.apiKey}`,
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify(body),
        });
        if (!res.ok) {
            const err = (await res.json().catch(() => ({})));
            throw new Error(`getmem ${res.status}: ${String(err["error"] ?? res.statusText)}`);
        }
        return res.json();
    }
    async get(userId, query) {
        return this.post("/v1/memory/get", { user_id: userId, query });
    }
    async ingest(userId, userMessage, assistantMessage) {
        const now = new Date().toISOString();
        await this.post("/v1/memory/ingest", {
            user_id: userId,
            messages: [
                { role: "user", content: userMessage, timestamp: now },
                { role: "assistant", content: assistantMessage, timestamp: now },
            ],
        });
    }
}
// ── Per-session state ─────────────────────────────────────────────────────────
const pending = new Map();
// ── Plugin ────────────────────────────────────────────────────────────────────
export default definePluginEntry({
    id: "openclaw-getmem",
    name: "getmem.ai Memory",
    description: "Persistent memory for every user via getmem.ai. Remembers users across sessions automatically.",
    configSchema: buildPluginConfigSchema(ConfigSchema),
    register(api) {
        const raw = (api.pluginConfig ?? {});
        const parsed = ConfigSchema.safeParse(raw);
        if (!parsed.success) {
            api.logger.warn("[getmem] Invalid config — set plugins.openclaw-getmem.apiKey to your getmem API key");
            return;
        }
        const cfg = parsed.data;
        if (!cfg.enabled) {
            api.logger.info("[getmem] Memory disabled via config");
            return;
        }
        const mem = new GetMemClient(cfg.apiKey, cfg.baseUrl);
        // ── Hook 1: message:received
        // Fires when an inbound message arrives from any channel.
        // Fetch memory for the sender and push as context for the agent.
        api.registerHook("message:received", async (event) => {
            const ctx = event.context;
            const userId = typeof ctx.metadata?.["senderId"] === "string"
                ? ctx.metadata["senderId"]
                : ctx.from;
            const userMessage = ctx.content;
            // Store for post-reply ingest
            pending.set(event.sessionKey, { userId, userMessage });
            try {
                const result = await mem.get(userId, userMessage);
                if (result.context?.trim()) {
                    event.messages.push(`[Memory]\n${result.context}`);
                }
            }
            catch (err) {
                api.logger.warn(`[getmem] Memory fetch failed for ${userId}: ${err.message}`);
            }
        });
        // ── Hook 2: message:sent
        // Fires after the agent's reply is delivered.
        // Ingest the exchange — fire-and-forget, never blocks the reply pipeline.
        api.registerHook("message:sent", async (event) => {
            const ctx = event.context;
            if (!ctx.success)
                return;
            const state = pending.get(event.sessionKey);
            if (!state)
                return;
            pending.delete(event.sessionKey);
            void mem.ingest(state.userId, state.userMessage, ctx.content).catch((err) => {
                api.logger.warn(`[getmem] Ingest failed for ${state.userId}: ${err.message}`);
            });
        });
        api.logger.info("[getmem] Memory active — getmem.ai");
    },
});
//# sourceMappingURL=index.js.map