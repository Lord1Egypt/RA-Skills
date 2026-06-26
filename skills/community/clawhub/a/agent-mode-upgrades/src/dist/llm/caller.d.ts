/**
 * Provider-aware lightweight LLM caller
 *
 * Supports the providers currently used by the enhanced-loop orchestrator:
 * - Anthropic
 * - OpenAI Codex / OpenAI Responses-style transports
 *
 * This stays lightweight, but stops assuming every provider is Anthropic-shaped.
 */
export interface LLMMessage {
    role: "user" | "assistant" | "system";
    content: string;
}
export interface LLMCallOptions {
    messages: LLMMessage[];
    maxTokens?: number;
    temperature?: number;
    model?: string;
}
export interface LLMResponse {
    content: string;
    usage?: {
        inputTokens: number;
        outputTokens: number;
    };
}
export interface LLMCallerConfig {
    apiKey?: string;
    model?: string;
    maxTokens?: number;
    baseUrl?: string;
    provider?: string;
}
export declare class LLMCaller {
    private apiKey;
    private model;
    private maxTokens;
    private baseUrl;
    private provider;
    constructor(config?: LLMCallerConfig);
    isConfigured(): boolean;
    call(options: LLMCallOptions): Promise<LLMResponse>;
    private callAnthropic;
    private callOpenAIResponses;
    /**
     * Consume a streaming SSE response from the Codex backend.
     * Collects output_text deltas and extracts usage from the response.completed event.
     */
    private consumeCodexStream;
    invoke(options: {
        messages: Array<{
            role: string;
            content: string | unknown[];
        }>;
        maxTokens?: number;
    }): Promise<{
        content: string;
    }>;
}
export declare function getLLMCaller(config?: LLMCallerConfig): LLMCaller;
export declare function createLLMCaller(config?: LLMCallerConfig): LLMCaller;
export declare function resetLLMCaller(): void;
export declare function createOrchestratorLLMCaller(config?: LLMCallerConfig): (options: {
    messages: Array<{
        role: string;
        content: string | unknown[];
    }>;
    maxTokens?: number;
}) => Promise<{
    content: string;
}>;
//# sourceMappingURL=caller.d.ts.map