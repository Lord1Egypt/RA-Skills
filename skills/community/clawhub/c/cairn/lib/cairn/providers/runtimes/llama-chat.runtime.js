import { resolveModel } from '../../resolve.js';
import { getLlamaRuntime } from './llama.js';
// node-llama-cpp chat runtime. Replaces ollama's `format` param with
// JSON-schema grammar — same outcome (token-level constraint), implemented in
// llama.cpp instead of ollama. Single-shot: each chatJson() resets session
// history so repeated calls don't accumulate context.
export class LlamaChatRuntime {
    model;
    opts;
    handles = null;
    loadPromise = null;
    constructor(opts) {
        this.model = opts.model;
        this.opts = opts;
    }
    async healthCheck() {
        // Cheap probe: verify the native binding is loadable. We deliberately do
        // NOT load the model here — that triggers an ~700MB download on first use,
        // which would surprise users who just constructed `new Cairn()`. Model
        // load is lazy in chatJson().
        try {
            await getLlamaRuntime();
            return true;
        }
        catch {
            return false;
        }
    }
    async chatJson(req) {
        const { llama, context, ChatSession } = await this.load();
        const grammar = await llama.createGrammarForJsonSchema(req.schema);
        const session = new ChatSession({
            contextSequence: context.getSequence(),
            systemPrompt: req.system,
        });
        const content = await session.prompt(req.user, {
            grammar,
            temperature: this.opts.temperature ?? 0.2,
        });
        try {
            return JSON.parse(content);
        }
        catch {
            throw new Error(`llama chat: non-JSON content despite grammar constraint: ${content.slice(0, 200)}`);
        }
    }
    load() {
        if (this.handles)
            return Promise.resolve(this.handles);
        if (!this.loadPromise) {
            this.loadPromise = (async () => {
                const mod = (await import('node-llama-cpp'));
                const llama = (await getLlamaRuntime());
                const path = this.opts.modelPath
                    ? this.opts.modelPath
                    : (await resolveModel(this.opts.model, this.opts.cacheDir)).path;
                const model = await llama.loadModel({ modelPath: path });
                const context = await model.createContext({
                    contextSize: this.opts.contextSize ?? 4096,
                    threads: this.opts.threads,
                });
                this.handles = {
                    llama,
                    model,
                    context,
                    ChatSession: mod.LlamaChatSession,
                };
                return this.handles;
            })();
        }
        return this.loadPromise;
    }
}
