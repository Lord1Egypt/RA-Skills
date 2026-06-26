import { DIM_BY_MODEL } from '../../constants/embed.constants.js';
export class OllamaEmbedRuntime {
    model;
    dim;
    url;
    constructor(opts) {
        this.model = opts.model;
        this.dim = DIM_BY_MODEL[opts.model];
        this.url = opts.url.replace(/\/$/, '');
    }
    async healthCheck() {
        try {
            const res = await fetch(`${this.url}/api/tags`, {
                method: 'GET',
                signal: AbortSignal.timeout(3000),
            });
            return res.ok;
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
        const res = await fetch(`${this.url}/api/embed`, {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({ model: this.model, input: texts }),
        });
        if (!res.ok) {
            const body = await res.text().catch(() => '');
            throw new Error(`ollama embed ${res.status}: ${body.slice(0, 200)}`);
        }
        const json = (await res.json());
        if (!json.embeddings || json.embeddings.length !== texts.length) {
            throw new Error(`embed: expected ${texts.length} vectors, got ${json.embeddings?.length ?? 0}`);
        }
        return json.embeddings.map((arr, i) => {
            if (arr.length !== this.dim) {
                throw new Error(`embed: input[${i}] returned dim ${arr.length}, expected ${this.dim}`);
            }
            return new Float32Array(arr);
        });
    }
}
