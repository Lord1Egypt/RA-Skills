export interface ChatJsonRequest {
    system: string;
    user: string;
    schema: object;
}
export interface ChatRuntime {
    readonly model: string;
    healthCheck(): Promise<boolean>;
    chatJson<T>(req: ChatJsonRequest): Promise<T>;
}
export interface Chat {
    readonly model: string;
    readonly healthy: boolean;
    healthCheck(): Promise<boolean>;
    chatJson<T>(req: ChatJsonRequest): Promise<T>;
}
export interface OllamaChatRuntimeOptions {
    url: string;
    model: string;
}
export interface LlamaChatRuntimeOptions {
    model: string;
    modelPath?: string;
    cacheDir?: string;
    contextSize?: number;
    threads?: number;
    temperature?: number;
}
