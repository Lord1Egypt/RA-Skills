# Provider Model Identity Tracing

When a model name is an opaque alias (e.g. `big-pickle` on OpenCode Zen,
`@cf/moonshotai/kimi-k2.6` on Cloudflare), you need to trace through
multiple layers to discover the underlying identity.

## The Tracing Workflow

### 1. Config Layer — What's wired up

```yaml
# config.yaml
model:
  provider: opencode-zen
  base_url: https://opencode.ai/zen/v1
  api_mode: chat_completions
  default: big-pickle
```

This tells you: the provider name, the API endpoint, and the model alias
being sent in the wire payload. The provider name and model alias are
both potentially opaque here.

### 2. Cache Layer — What the catalog knows

Hermes caches model catalogs locally:

- `~/.hermes/webui/models_cache.json` — model list used by the WebUI
- `~/.hermes/models_dev_cache.json` — model catalog for the active profile
- `~/.hermes/profiles/<name>/models_dev_cache.json` — per-profile catalogs

These contain the model IDs and labels that were fetched when Hermes
queried the provider's API. Search for the alias to see all associated
entries and labels:

```bash
grep -A 3 'big-pickle' ~/.hermes/webui/models_cache.json
```

The `label` field may give a more descriptive name (e.g. `"BIG Pickle"`).

### 3. Log Layer — What actually happens at call time

Agent logs show the exact wire-format request:

```
~/.hermes/logs/agent.log:
  OpenAI client created ... provider=opencode-zen
  base_url=https://opencode.ai/zen/v1 model=big-pickle
```

This confirms: the model alias passes through as-is. No intermediate
resolution happens client-side — the alias is what hits the wire.

### 4. API Layer — What the provider advertises

Hit the provider's OpenAI-compatible model list endpoint:

```bash
curl -s https://opencode.ai/zen/v1/models | python3 -m json.tool
```

This returns every model the provider serves. The alias will be in the
list (`"id": "big-pickle"`) but without metadata about the underlying
model — it's just an ID string.

Some providers return additional metadata per model (context length,
pricing, capabilities) — if they do, that's your best signal.

### 5. Source Layer — Open-source providers

If the provider is open-source (OpenCode/XB, vLLM, Ollama), check their
repo:

```bash
# Find the default branch
curl -s https://api.github.com/repos/anomalyco/opencode \
  | python3 -c "import json,sys; print(json.load(sys.stdin).get('default_branch','unknown'))"
# → "dev" (not "main")
```

Then explore:
- **`packages/llm/src/providers/`** — provider adapter implementations
- **`packages/<name>/src/config/`** — model configuration, model-id schemas
- **`specs/`** — specification docs for provider-model relationships
- **`packages/<name>/src/provider/`** — provider model definitions

If the model routing is server-side (closed-source), the alias will not
appear in the repo at all — confirmation that resolution is opaque.

### 6. Website Layer — Docs, pricing, product pages

Check the provider's website for:
- `/docs` — provider documentation
- `/pricing` — model pricing which may list all available models
- `/zen` or similar product pages — curated model lists
- FAQ / blog posts — may mention model identities in prose

Look for patterns: when a provider uses mostly transparent names
(`deepseek-v4-flash`, `qwen3.5-plus`) alongside one opaque name
(`big-pickle`), the opaque name is likely their own branding for a
specific hosted model — but the server-side routing is the only
definitive source.

### 7. When to Stop

Some model aliases are **intentionally opaque** — the provider routes
them server-side and doesn't publish the mapping. This is common with
proxy/bundled-model services. In that case:

> Tell the user: "I found the config chain (provider → API → alias)
> and probed all available sources, but the underlying model isn't
> documented. Here's what I *can* tell you about its capabilities…"

## Capability Inference (when identity is opaque)

Even without the underlying model name, you can often infer capabilities:

| Signal | What it tells you |
|--------|------------------|
| Tool calling works | Supports function-calling schema |
| Reasoning content returned | Has native reasoning/chain-of-thought |
| Context window size configured | From config or cache metadata |
| Temperature support | Check if model config allows `temperature` |
| Position in model list | Often correlates with capability tier |

## Example: Tracing `big-pickle`

```
config.yaml              → provider=opencode-zen, base_url=https://opencode.ai/zen/v1
models_cache.json        → label="BIG Pickle", sits between qwen3.5-plus and deepseek-v4-flash-free
agent.log                → actual call uses big-pickle as-is, no client-side resolution
/v1/models API           → listed as "big-pickle" with no metadata — opaque ID
GitHub (anomalyco/opencode, dev branch) → no model routing table in public repo (server-side)
Website (/zen)           → lists Zen model categories but no per-model identity details
```

**Result:** The underlying model is server-routed and not publicly
documented. Capabilities (tool calling, reasoning) can be verified
through use, but the specific weights are unknowable from the client.
