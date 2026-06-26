import type { Embedding, EmbedModel } from '../../types/primitives.types.js';
import type { EmbedRuntime, LlamaEmbedRuntimeOptions } from '../../types/embed.types.js';
export declare class LlamaEmbedRuntime implements EmbedRuntime {
    readonly model: EmbedModel;
    readonly dim: number;
    private readonly opts;
    private handles;
    private loadPromise;
    constructor(opts: LlamaEmbedRuntimeOptions);
    healthCheck(): Promise<boolean>;
    embed(text: string): Promise<Embedding>;
    embedBatch(texts: string[]): Promise<Embedding[]>;
    private load;
}
