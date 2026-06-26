import type { ChatJsonRequest, ChatRuntime, OllamaChatRuntimeOptions } from '../../types/chat.types.js';
export declare class OllamaChatRuntime implements ChatRuntime {
    readonly model: string;
    private url;
    constructor(opts: OllamaChatRuntimeOptions);
    healthCheck(): Promise<boolean>;
    chatJson<T>(req: ChatJsonRequest): Promise<T>;
}
