import type { Embedding, EmbedModel } from '../../types/primitives.types.js';
import type { EmbedRuntime, OllamaEmbedRuntimeOptions } from '../../types/embed.types.js';
export declare class OllamaEmbedRuntime implements EmbedRuntime {
    readonly model: EmbedModel;
    readonly dim: number;
    private url;
    constructor(opts: OllamaEmbedRuntimeOptions);
    healthCheck(): Promise<boolean>;
    embed(text: string): Promise<Embedding>;
    embedBatch(texts: string[]): Promise<Embedding[]>;
}
