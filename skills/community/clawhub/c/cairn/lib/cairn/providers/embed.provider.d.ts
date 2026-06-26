import type { Embed, EmbedRuntime } from '../types/embed.types.js';
import type { Embedding, EmbedModel } from '../types/primitives.types.js';
export declare class EmbedProvider implements Embed {
    private runtime;
    private _healthy;
    constructor(runtime: EmbedRuntime);
    get model(): EmbedModel;
    get dim(): number;
    get healthy(): boolean;
    healthCheck(): Promise<boolean>;
    embed(text: string): Promise<Embedding>;
    embedBatch(texts: string[]): Promise<Embedding[]>;
}
