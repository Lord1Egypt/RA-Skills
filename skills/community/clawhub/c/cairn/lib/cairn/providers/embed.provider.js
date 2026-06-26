// Single runtime-agnostic embed provider. Holds the cached `_healthy` flag
// and delegates real work to the injected EmbedRuntime.
export class EmbedProvider {
    runtime;
    _healthy = true;
    constructor(runtime) {
        this.runtime = runtime;
    }
    get model() {
        return this.runtime.model;
    }
    get dim() {
        return this.runtime.dim;
    }
    get healthy() {
        return this._healthy;
    }
    async healthCheck() {
        this._healthy = await this.runtime.healthCheck();
        return this._healthy;
    }
    embed(text) {
        return this.runtime.embed(text);
    }
    embedBatch(texts) {
        return this.runtime.embedBatch(texts);
    }
}
