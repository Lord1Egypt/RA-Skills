import type { Embedding, EmbedModel } from './primitives.types.js';
export interface EmbedRuntime {
    readonly model: EmbedModel;
    readonly dim: number;
    healthCheck(): Promise<boolean>;
    embed(text: string): Promise<Embedding>;
    embedBatch(texts: string[]): Promise<Embedding[]>;
}
export interface Embed {
    readonly model: EmbedModel;
    readonly dim: number;
    readonly healthy: boolean;
    healthCheck(): Promise<boolean>;
    embed(text: string): Promise<Embedding>;
    embedBatch(texts: string[]): Promise<Embedding[]>;
}
export interface OllamaEmbedRuntimeOptions {
    url: string;
    model: EmbedModel;
}
export interface LlamaEmbedRuntimeOptions {
    model: EmbedModel;
    modelPath?: string;
    cacheDir?: string;
    contextSize?: number;
    threads?: number;
}
