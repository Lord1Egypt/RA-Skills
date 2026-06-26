/**
 * Provider-aware lightweight LLM caller
 *
 * Supports the providers currently used by the enhanced-loop orchestrator:
 * - Anthropic
 * - OpenAI Codex / OpenAI Responses-style transports
 *
 * This stays lightweight, but stops assuming every provider is Anthropic-shaped.
 */
import fs from "node:fs";
import path from "node:path";
// ============================================================================
// API Key Resolution
// ============================================================================
function resolveApiKey(config) {
    // 1. Explicit config (from enhanced-loop-hook, which resolves via auth profile chain)
    if (config?.apiKey)
        return config.apiKey;
    // 2. Environment variable fallbacks
    if (process.env.ANTHROPIC_API_KEY)
        return process.env.ANTHROPIC_API_KEY;
    if (process.env.OPENAI_API_KEY)
        return process.env.OPENAI_API_KEY;
    // 3. Try to read from OpenClaw auth storage
    const home = process.env.HOME || process.env.USERPROFILE || "";
    const authPaths = [
        path.join(home, ".openclaw", "agents", "main", "agent", "auth-profiles.json"),
        path.join(home, ".openclaw", "auth-profiles.json"),
        path.join(home, ".config", "openclaw", "auth-profiles.json"),
    ];
    for (const authPath of authPaths) {
        try {
            if (!fs.existsSync(authPath))
                continue;
            const content = fs.readFileSync(authPath, "utf-8");
            const auth = JSON.parse(content);
            const profiles = auth.profiles || {};
            const providersInPriorityOrder = [config?.provider, "anthropic", "openai-codex", "openai"]
                .filter((p) => Boolean(p));
            for (const provider of providersInPriorityOrder) {
                const order = auth.order?.[provider];
                if (order?.length) {
                    for (const profileId of order) {
                        const p = profiles[profileId];
                        if (!p || p.provider !== provider)
                            continue;
                        const key = p.access || p.token || p.key || p.apiKey;
                        if (key)
                            return key;
                    }
                }
                const sorted = Object.entries(profiles)
                    .filter(([, p]) => p.provider === provider)
                    .sort(([, a], [, b]) => {
                    const rank = (t) => (t === "token" || t === "oauth" ? 0 : 1);
                    return rank(a.type ?? "api_key") - rank(b.type ?? "api_key");
                });
                for (const [, profile] of sorted) {
                    const p = profile;
                    const key = p.access || p.token || p.key || p.apiKey;
                    if (key)
                        return key;
                }
            }
        }
        catch {
            // Continue to next path
        }
    }
    return null;
}
function normalizeProvider(config) {
    const explicit = config?.provider?.trim().toLowerCase();
    if (explicit === "openai-codex")
        return "openai-codex";
    if (explicit === "openai")
        return "openai";
    if (explicit === "anthropic")
        return "anthropic";
    const model = config?.model?.trim().toLowerCase() || "";
    const baseUrl = config?.baseUrl?.trim().toLowerCase() || "";
    if (explicit?.includes("codex") || model.includes("codex") || baseUrl.includes("chatgpt.com/backend-api")) {
        return "openai-codex";
    }
    if (explicit?.includes("openai") || baseUrl.includes("api.openai.com") || model.startsWith("gpt-")) {
        return "openai";
    }
    return "anthropic";
}
function isAnthropicOAuthToken(key) {
    return key.startsWith("sk-ant-oat") || key.startsWith("Bearer ");
}
function asBearerToken(key) {
    return key.replace(/^Bearer\s*/i, "").trim();
}
function resolveAnthropicBaseUrl(config) {
    return config?.baseUrl?.trim() || "https://api.anthropic.com/v1/messages";
}
function resolveOpenAIBaseUrl(config) {
    const configured = config?.baseUrl?.trim();
    if (!configured)
        return "https://api.openai.com/v1/responses";
    if (/\/responses\/?$/i.test(configured))
        return configured;
    if (/chatgpt\.com\/backend-api\/?$/i.test(configured)) {
        return configured.replace(/\/?$/, "/codex/responses");
    }
    if (/\/v1\/?$/i.test(configured))
        return configured.replace(/\/?$/, "/responses");
    return configured;
}
function toOpenAIInput(messages) {
    return messages
        .filter((m) => m.role !== "system")
        .map((m) => ({
        role: m.role,
        content: [{ type: "input_text", text: m.content }],
    }));
}
// ============================================================================
// LLM Caller
// ============================================================================
const DEFAULT_MODEL = "claude-haiku-4-5";
const DEFAULT_MAX_TOKENS = 1024;
export class LLMCaller {
    apiKey;
    model;
    maxTokens;
    baseUrl;
    provider;
    constructor(config) {
        this.provider = normalizeProvider(config);
        this.apiKey = resolveApiKey(config);
        this.model = config?.model || DEFAULT_MODEL;
        this.maxTokens = config?.maxTokens || DEFAULT_MAX_TOKENS;
        this.baseUrl =
            this.provider === "anthropic"
                ? resolveAnthropicBaseUrl(config)
                : resolveOpenAIBaseUrl(config);
    }
    isConfigured() {
        return !!this.apiKey;
    }
    async call(options) {
        if (!this.apiKey) {
            throw new Error("No API key configured for LLM caller");
        }
        if (this.provider === "anthropic") {
            return this.callAnthropic(options);
        }
        if (this.provider === "openai-codex" || this.provider === "openai") {
            return this.callOpenAIResponses(options);
        }
        throw new Error(`Unsupported provider: ${this.provider}`);
    }
    async callAnthropic(options) {
        if (!this.apiKey)
            throw new Error("No API key configured for Anthropic caller");
        const systemMessage = options.messages.find((m) => m.role === "system");
        const otherMessages = options.messages.filter((m) => m.role !== "system");
        const body = {
            model: options.model || this.model,
            max_tokens: options.maxTokens || this.maxTokens,
            temperature: options.temperature ?? 0.7,
            system: systemMessage?.content,
            messages: otherMessages.map((m) => ({
                role: m.role,
                content: m.content,
            })),
        };
        const authHeaders = isAnthropicOAuthToken(this.apiKey)
            ? {
                Authorization: `Bearer ${asBearerToken(this.apiKey)}`,
                "anthropic-beta": "oauth-2025-04-20",
            }
            : { "x-api-key": this.apiKey };
        const response = await fetch(this.baseUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...authHeaders,
                "anthropic-version": "2023-06-01",
            },
            body: JSON.stringify(body),
        });
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`LLM API error (${response.status}): ${errorText}`);
        }
        const data = (await response.json());
        const textContent = data.content
            .filter((c) => c.type === "text")
            .map((c) => c.text || "")
            .join("");
        return {
            content: textContent,
            usage: data.usage
                ? {
                    inputTokens: data.usage.input_tokens,
                    outputTokens: data.usage.output_tokens,
                }
                : undefined,
        };
    }
    async callOpenAIResponses(options) {
        if (!this.apiKey)
            throw new Error("No API key configured for OpenAI caller");
        const systemMessage = options.messages.find((m) => m.role === "system");
        const body = {
            model: options.model || this.model,
            instructions: systemMessage?.content,
            input: toOpenAIInput(options.messages),
            // Codex backend does not support max_output_tokens
            ...(this.provider !== "openai-codex"
                ? { max_output_tokens: options.maxTokens ?? this.maxTokens }
                : {}),
            ...(options.temperature !== undefined ? { temperature: options.temperature } : {}),
            // Codex backend expects store=false and stream=true
            ...(this.provider === "openai-codex" ? { store: false, stream: true } : {}),
        };
        const response = await fetch(this.baseUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${asBearerToken(this.apiKey)}`,
            },
            body: JSON.stringify(body),
        });
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`LLM API error (${response.status}): ${errorText}`);
        }
        // Codex backend requires stream=true, so we need to consume SSE chunks
        if (this.provider === "openai-codex") {
            return this.consumeCodexStream(response);
        }
        const data = (await response.json());
        const textFromOutput = (data.output ?? [])
            .flatMap((item) => {
            if (item.type === "output_text" && item.text)
                return [item.text];
            return (item.content ?? [])
                .filter((part) => part.type === "output_text" && typeof part.text === "string")
                .map((part) => part.text);
        })
            .join("");
        const textContent = textFromOutput || data.output_text || "";
        return {
            content: textContent,
            usage: data.usage
                ? {
                    inputTokens: data.usage.input_tokens ?? data.usage.inputTokens ?? 0,
                    outputTokens: data.usage.output_tokens ?? data.usage.outputTokens ?? 0,
                }
                : undefined,
        };
    }
    /**
     * Consume a streaming SSE response from the Codex backend.
     * Collects output_text deltas and extracts usage from the response.completed event.
     */
    async consumeCodexStream(response) {
        const reader = response.body?.getReader();
        if (!reader) {
            throw new Error("No response body for streaming Codex response");
        }
        const decoder = new TextDecoder();
        let buffer = "";
        let textContent = "";
        let usage = undefined;
        while (true) {
            const { done, value } = await reader.read();
            if (done)
                break;
            buffer += decoder.decode(value, { stream: true });
            // Process complete SSE lines
            const lines = buffer.split("\n");
            buffer = lines.pop() ?? "";
            for (const line of lines) {
                if (!line.startsWith("data: "))
                    continue;
                const payload = line.slice(6).trim();
                if (payload === "[DONE]")
                    continue;
                try {
                    const evt = JSON.parse(payload);
                    // Collect text deltas
                    if (evt.type === "response.output_text.delta" && evt.delta) {
                        textContent += evt.delta;
                    }
                    // Some events carry the full output text on completion
                    if (evt.type === "response.output_text.done" && evt.text) {
                        textContent = evt.text;
                    }
                    // Extract usage from response.completed
                    if (evt.type === "response.completed" || evt.type === "response.done") {
                        const u = evt.usage ?? evt.response?.usage;
                        if (u) {
                            usage = {
                                inputTokens: u.input_tokens ?? 0,
                                outputTokens: u.output_tokens ?? 0,
                            };
                        }
                        // Also grab full text if we missed deltas
                        if (!textContent && evt.response?.output_text) {
                            textContent = evt.response.output_text;
                        }
                    }
                }
                catch {
                    // Skip malformed SSE lines
                }
            }
        }
        return { content: textContent, usage };
    }
    async invoke(options) {
        const messages = options.messages.map((m) => ({
            role: m.role,
            content: typeof m.content === "string" ? m.content : JSON.stringify(m.content),
        }));
        return this.call({ messages, maxTokens: options.maxTokens });
    }
}
// ============================================================================
// Factory
// ============================================================================
let defaultCaller = null;
export function getLLMCaller(config) {
    if (!defaultCaller) {
        defaultCaller = new LLMCaller(config);
    }
    return defaultCaller;
}
export function createLLMCaller(config) {
    return new LLMCaller(config);
}
export function resetLLMCaller() {
    defaultCaller = null;
}
// ============================================================================
// Wrapper for orchestrator compatibility
// ============================================================================
export function createOrchestratorLLMCaller(config) {
    const caller = createLLMCaller(config);
    if (!caller.isConfigured()) {
        return async () => {
            throw new Error("LLM caller not configured. Configure provider auth in OpenClaw for the selected orchestrator provider.");
        };
    }
    return (options) => caller.invoke(options);
}
//# sourceMappingURL=caller.js.map