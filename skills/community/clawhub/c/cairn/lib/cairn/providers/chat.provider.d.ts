import type { Chat, ChatJsonRequest, ChatRuntime } from '../types/chat.types.js';
export declare class ChatProvider implements Chat {
    private runtime;
    private _healthy;
    constructor(runtime: ChatRuntime);
    get model(): string;
    get healthy(): boolean;
    healthCheck(): Promise<boolean>;
    chatJson<T>(req: ChatJsonRequest): Promise<T>;
}
