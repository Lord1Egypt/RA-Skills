/**
 * getmem.ai OpenClaw Plugin v1.0.2
 * Persistent memory for every user via getmem.ai.
 */

import { definePluginEntry, buildPluginConfigSchema } from "openclaw/plugin-sdk/plugin-entry";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";
import type { InternalHookEvent } from "openclaw/plugin-sdk/hook-runtime";
import { z } from "openclaw/plugin-sdk/zod";

const ConfigSchema = z.object({
  apiKey: z.string().min(1, "getmem API key is required"),
  baseUrl: z.string().url().optional().default("https://memory.getmem.ai"),
  enabled: z.boolean().optional().default(true),
});

type GetMemConfig = z.infer<typeof ConfigSchema>;

class GetMemClient {
  constructor(private apiKey: string, private baseUrl = "https://memory.getmem.ai") {
    this.baseUrl = baseUrl.replace(/\/+$/, "");
  }

  private async post<T>(path: string, body: unknown): Promise<T> {
    const res = await fetch(`${this.baseUrl}${path}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${this.apiKey}`, "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`getmem ${res.status}: ${res.statusText}`);
    return res.json() as Promise<T>;
  }

  async get(userId: string, query: string): Promise<{ context: string }> {
    return this.post("/v1/memory/get", { user_id: userId, query });
  }

  async ingest(userId: string, userMsg: string, assistantMsg: string): Promise<void> {
    await this.post("/v1/memory/ingest", {
      user_id: userId,
      messages: [
        { role: "user", content: userMsg },
        { role: "assistant", content: assistantMsg },
      ],
    });
  }
}

/** Strip channel prefix — "telegram:410282253" → "410282253" */
function rawId(id: string): string {
  return id.includes(":") ? id.split(":").pop()! : id;
}

// userId → last user message (keyed by raw ID)
const lastMessage = new Map<string, string>();

export default definePluginEntry({
  id: "getmem-openclaw",
  name: "getmem.ai Memory",
  description: "Persistent memory for every user via getmem.ai.",
  configSchema: buildPluginConfigSchema(ConfigSchema),

  register(api: OpenClawPluginApi) {
    const parsed = ConfigSchema.safeParse(api.pluginConfig ?? {});
    if (!parsed.success) {
      api.logger.warn("[getmem] Invalid config — set plugins.getmem-openclaw.apiKey");
      return;
    }
    const cfg: GetMemConfig = parsed.data;
    if (!cfg.enabled) { api.logger.info("[getmem] Disabled"); return; }

    const mem = new GetMemClient(cfg.apiKey, cfg.baseUrl);

    // Hook 1: fetch memory before agent processes inbound message
    api.registerHook("message:received", async (event: InternalHookEvent) => {
      const ctx = event.context;
      const from = (ctx["from"] as string) ?? "unknown";
      const userId = rawId(from);
      const userMessage = (ctx["content"] as string) ?? "";

      // Store under raw ID for lookup in message:sent
      lastMessage.set(userId, userMessage);

      try {
        const result = await mem.get(userId, userMessage);
        if (result.context?.trim()) {
          event.messages.push(`[Memory]\n${result.context}`);
        }
      } catch (err) {
        api.logger.warn(`[getmem] fetch failed: ${(err as Error).message}`);
      }
    }, { name: "getmem-message-received" });

    // Hook 2: ingest exchange after reply is sent
    api.registerHook("message:sent", async (event: InternalHookEvent) => {
      const ctx = event.context;
      if (!ctx["success"]) return;

      const assistantContent = (ctx["content"] as string) ?? "";
      if (assistantContent.includes("⚠️") || !assistantContent.trim()) return;

      // Extract raw user ID from session key: "agent:main:telegram:direct:USERID"
      const sessionParts = event.sessionKey.split(":");
      const userId = rawId(sessionParts[sessionParts.length - 1] ?? "unknown");

      const userMessage = lastMessage.get(userId) ?? "";
      if (!userMessage) return;

      void mem.ingest(userId, userMessage, assistantContent).catch(
        (err: Error) => api.logger.warn(`[getmem] ingest failed: ${err.message}`)
      );
    }, { name: "getmem-message-sent" });

    api.logger.info("[getmem] Hooks registered: message:received ✓  message:sent ✓");
    api.logger.info("[getmem] Memory active — getmem.ai");
  },
});
