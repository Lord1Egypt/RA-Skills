// Single runtime-agnostic chat provider. Holds the cached `_healthy` flag and
// delegates real work to the injected ChatRuntime (Ollama or Llama). Adding a
// new backend is just a new ChatRuntime impl — this class doesn't change.
export class ChatProvider {
    runtime;
    _healthy = true;
    constructor(runtime) {
        this.runtime = runtime;
    }
    get model() {
        return this.runtime.model;
    }
    get healthy() {
        return this._healthy;
    }
    async healthCheck() {
        this._healthy = await this.runtime.healthCheck();
        return this._healthy;
    }
    chatJson(req) {
        return this.runtime.chatJson(req);
    }
}
