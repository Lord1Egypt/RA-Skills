/**
 * OpenClaw Skill 接口定义
 */
export interface LLMResponse {
    content: string;
    usage?: {
        promptTokens: number;
        completionTokens: number;
        totalTokens: number;
    };
}
export interface LLMChatMessage {
    role: 'user' | 'assistant' | 'system';
    content: string;
}
export interface LLM {
    chat(params: {
        system?: string;
        messages: LLMChatMessage[];
        temperature?: number;
        maxTokens?: number;
    }): Promise<LLMResponse>;
}
export interface SkillContext {
    llm: LLM;
    userId: string;
    channelId: string;
    sessionId?: string;
    metadata?: Record<string, unknown>;
}
export interface SkillResponse {
    type: 'text' | 'file' | 'image' | 'error';
    content: string;
    file?: {
        path: string;
        mimeType: string;
        filename: string;
    };
    metadata?: Record<string, unknown>;
}
export interface Skill {
    id: string;
    name: string;
    version: string;
    description: string;
    initialize(context: SkillContext): Promise<void>;
    handle(message: string, context: SkillContext): Promise<SkillResponse>;
    shutdown(): Promise<void>;
}
//# sourceMappingURL=skill.d.ts.map