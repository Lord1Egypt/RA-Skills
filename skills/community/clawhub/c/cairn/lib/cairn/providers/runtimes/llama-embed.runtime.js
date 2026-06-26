import { DIM_BY_MODEL } from '../../constants/embed.constants.js';
import { resolveModel } from '../../resolve.js';
import { getLlamaRuntime } from './llama.js';
// node-llama-cpp embedding runtime. Mirrors the ollama EmbedRuntime contract
// (model, dim, healthCheck, embed, embedBatch). Lazy-loads the model on first
// embed() call so construction stays cheap when the runtime isn't selected.
export class LlamaEmbedRuntime {
    model;
    dim;
    opts;
    handles = null;
    loadPromise = null;
    constructor(opts) {
        this.model = opts.model;
        this.dim = DIM_BY_MODEL[opts.model];
        this.opts = opts;
    }
    async healthCheck() {
        // Cheap probe: verify the native binding is loadable. We deliberately do
        // NOT load the model here — that triggers an 85MB+ download on first use.
        try {
            await getLlamaRuntime();
            return true;
        }
        catch {
            return false;
        }
    }
    async embed(text) {
        const [out] = await this.embedBatch([text]);
        return out;
    }
    async embedBatch(texts) {
        if (texts.length === 0)
            return [];
        const { embeddingContext } = await this.load();
        // node-llama-cpp's embedding context is sequential per sequence; batching
        // here is logical, not parallel. Keeping the loop tight avoids spinning up
        // multiple sequences which fragments the KV cache for sub-second tasks.
        const out = [];
        for (const text of texts) {
            const result = await embeddingContext.getEmbeddingFor(text);
            if (result.vector.length !== this.dim) {
                throw new Error(`llama embed: model returned dim ${result.vector.length}, expected ${this.dim}`);
            }
            out.push(new Float32Array(result.vector));
        }
        return out;
    }
    load() {
        if (this.handles)
            return Promise.resolve(this.handles);
        if (!this.loadPromise) {
            this.loadPromise = (async () => {
                const llama = (await getLlamaRuntime());
                const path = this.opts.modelPath
                    ? this.opts.modelPath
                    : (await resolveModel(this.opts.model, this.opts.cacheDir)).path;
                const model = await llama.loadModel({ modelPath: path });
                const embeddingContext = await model.createEmbeddingContext({
                    contextSize: this.opts.contextSize ?? 2048,
                    threads: this.opts.threads,
                });
                this.handles = { embeddingContext };
                return this.handles;
            })();
        }
        return this.loadPromise;
    }
}
