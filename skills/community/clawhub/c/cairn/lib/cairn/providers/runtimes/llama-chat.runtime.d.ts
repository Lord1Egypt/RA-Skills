import type { ChatJsonRequest, ChatRuntime, LlamaChatRuntimeOptions } from '../../types/chat.types.js';
export declare class LlamaChatRuntime implements ChatRuntime {
    readonly model: string;
    private readonly opts;
    private handles;
    private loadPromise;
    constructor(opts: LlamaChatRuntimeOptions);
    healthCheck(): Promise<boolean>;
    chatJson<T>(req: ChatJsonRequest): Promise<T>;
    private load;
}
