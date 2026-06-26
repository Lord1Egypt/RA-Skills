// Wraps ollama `/api/chat` with structured-output. The `format` param accepts
// a JSON Schema and constrains decoding token-by-token, so even sub-1B models
// emit shape-valid output. Doesn't retry — caller handles failure.
export class OllamaChatRuntime {
    model;
    url;
    constructor(opts) {
        this.model = opts.model;
        this.url = opts.url.replace(/\/$/, '');
    }
    async healthCheck() {
        try {
            const res = await fetch(`${this.url}/api/tags`, {
                method: 'GET',
                signal: AbortSignal.timeout(3000),
            });
            if (!res.ok)
                return false;
            const json = (await res.json());
            return (json.models ?? []).some((m) => m.name === this.model || m.model === this.model);
        }
        catch {
            return false;
        }
    }
    async chatJson(req) {
        const res = await fetch(`${this.url}/api/chat`, {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({
                model: this.model,
                messages: [
                    { role: 'system', content: req.system },
                    { role: 'user', content: req.user },
                ],
                format: req.schema,
                stream: false,
                options: {
                    // Doc-extraction is grounded in source text; we want low-temperature,
                    // near-deterministic output. Higher temps make small models invent.
                    temperature: 0.2,
                },
            }),
        });
        if (!res.ok) {
            const body = await res.text().catch(() => '');
            throw new Error(`ollama chat ${res.status}: ${body.slice(0, 200)}`);
        }
        const json = (await res.json());
        const content = json.message?.content;
        if (!content)
            throw new Error('ollama chat: empty content');
        try {
            return JSON.parse(content);
        }
        catch {
            throw new Error(`ollama chat: non-JSON despite constraint: ${content.slice(0, 200)}`);
        }
    }
}
