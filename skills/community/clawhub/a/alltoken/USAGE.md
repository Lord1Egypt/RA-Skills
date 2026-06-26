# Usage — `alltoken` skill

This is the **user-facing manual** for the bootstrap skill at `skills/alltoken/SKILL.md`. If you're an AllToken customer and a teammate just told you to "use the alltoken skill," start here.

## What this skill does

When loaded by an agent runtime (Hermes, OpenClaw, Claude Code, Codex CLI, OpenCode, Vercel AI SDK chat, …), this skill teaches the host agent how to **bootstrap a new TypeScript or Python project** that talks to AllToken — chat, async image generation, async video generation, model discovery, routing, and cost tracking.

**It is a bootstrap recipe, not a slash-command surface.** Invoking it produces *project files*, not a one-shot API call. If you want direct one-shot commands like `/alltoken-image "a cat"` from the agent prompt, load the sibling skill [`skills/alltoken-call/SKILL.md`](../alltoken-call/SKILL.md) instead.

## Who this is for

- Developers building a product that talks to AllToken
- Anyone wiring AllToken in as an OpenAI-compatible provider for an existing agent stack
- Teams who want a known-good agent core with hooks, streaming, tool-calling, image, and video already wired

## Prerequisites

| Need | Where |
|---|---|
| AllToken account | https://alltoken.ai |
| API key | Settings → API Keys (key value shown once — copy immediately) |
| Credits | Settings → Billing; ~$3 covers a full smoke test and a couple of image/video generations |
| Runtime | Node ≥ 20 (for the TypeScript path) or Python ≥ 3.10 (for the Python path) |
| Host agent | Any runtime that loads `SKILL.md`-format skills |

Export your key in the shell that will run the agent:

```bash
export ALLTOKEN_API_KEY="sk-at-..."
```

> Security: never commit the key. Never hard-code it in source. The skill assumes it reads from `process.env.ALLTOKEN_API_KEY` (TypeScript) or `os.environ['ALLTOKEN_API_KEY']` (Python).

## Quick start (60 seconds)

1. **Make the skill available to your agent.** Two common options:
   - Drop `skills/alltoken/SKILL.md` into the project the agent has access to (any path will work — agents that load skills walk the tree).
   - Or reference it by URL when prompting (e.g. paste the raw file into a Claude Code session).
2. **Ask the agent to bootstrap.** Examples:
   - In Claude Code: `> Use the alltoken skill to bootstrap an AllToken agent in ./my-agent`
   - In OpenClaw/Hermes: `> Load alltoken skill and scaffold a TypeScript chat+image agent here`
3. The agent will: install dependencies, create `src/{client,agent,tools,media,headless}.ts` plus optional `src/cli.tsx`, run one chat call as a smoke test, and report the model it used + the token usage.
4. From there you can `npm run start:headless` (Ink-free) or `npm start` (Ink TUI).

## What the agent will produce

```
my-agent/
├── package.json
├── tsconfig.json
└── src/
    ├── client.ts        # OpenAI SDK with baseURL=https://api.alltoken.ai/v1
    ├── agent.ts         # Streaming agent core, hooks, tool-loop (Agent class)
    ├── tools.ts         # timeTool, calculatorTool, defaultTools
    ├── media.ts         # generateImage, generateVideo, cancelVideo
    ├── headless.ts      # Programmatic example
    └── cli.tsx          # Optional Ink TUI
```

Python users get a single-file equivalent under `python/`.

## Picking a model

Don't hardcode model IDs in production. Discover at runtime:

```bash
curl -H "Authorization: Bearer $ALLTOKEN_API_KEY" https://api.alltoken.ai/v1/models | jq '.data[].id'
```

The SKILL.md (in the `## Discovering models` section) ships a **verified-working table as of 2026-05-12** with recommended IDs grouped by use case — cheap/fast vs. flagship vs. code-specialized for chat, plus the current image and video models. Use that table as a starting point; re-run the curl when going to production.

## Two integration patterns for host agents

### Pattern A — AllToken *as* your model provider

If you're using an existing agent runtime that already speaks OpenAI's REST contract (most do), the bootstrap is a config change, not new code. In OpenClaw, Hermes, Continue, OpenCode, Vercel AI SDK, etc., set:

```yaml
provider:
  base_url: https://api.alltoken.ai/v1
  api_key: ${ALLTOKEN_API_KEY}
model: gpt-5.4-mini      # or any ID from /v1/models
```

### Pattern B — AllToken *as a tool* inside your agent

Embed `agent.ts` + `media.ts` and expose three tools (`alltoken_chat`, `alltoken_image`, `alltoken_video`) to your host agent. Use this when your host agent runs on a *different* base model but you want to delegate multimodal work to AllToken on demand. Implementation is in SKILL.md under `## Using AllToken from inside Hermes / OpenClaw`.

## Common pitfalls (verified live during the SKILL evaluation)

| Symptom | Cause | Fix |
|---|---|---|
| `401 invalid_api_key` | wrong/revoked Bearer token | regenerate in Settings → API Keys |
| `401 invalid_token` on `/api-account/user/*` | those endpoints do NOT accept API keys — only the browser session token | go to Settings → API Keys / Billing in the web UI |
| `410 image_already_retrieved` on second poll | image results are one-shot; the temp file is deleted after first read | persist `b64_json` to disk on the first successful `completed` response, never re-poll |
| `usage` is `null` on every streamed chunk | OpenAI SDK doesn't send `include_usage` by default | pass `stream_options: {"include_usage": True}` |
| `503 all_providers_failed` when using `enable_search: true` | only DeepSeek and Qwen model families honor the flag; OpenAI returns 503, Claude/GLM/Kimi/Minimax silently drop | use `deepseek-v4-pro` or `qwen3.6-flash` for search queries |
| Chat response `model` doesn't match the request | AllToken version-pins (`gpt-5.4-nano` ⇒ `gpt-5.4-nano-2026-03-17`) — this is informational, not an error | none |
| Per-request cost not visible | SSE comment line with cost telemetry comes **after** `data: [DONE]` and the OpenAI SDK drops it | parse raw SSE if you need realtime cost tracking |

## Cost expectations (measured)

| Action | Typical cost | Typical latency |
|---|---|---|
| One `gpt-5.4-nano` chat call (~20 tokens out) | < $0.001 | 0.5–2 s |
| One `gpt-image-2` 1024×1024 `quality=low` | ~$0.02 | 15–25 s |
| One `gpt-image-2` 1024×1024 `quality=high` | ~$0.05 | 30–60 s |
| One `seedance-1.5-pro` 5 s @ 480p | ~$0.50 | 30–120 s |
| Read `/v1/models` / `/api-account/health/*` / `/api-account/models` | free | < 200 ms |

## Where to read more

- **The skill itself** — `skills/alltoken/SKILL.md` (1005 lines, exhaustive)
- **Repo authoring rules** — `CLAUDE.md` at the repo root
- **AllToken docs** — https://alltoken.ai/docs/apis/overview
- **OpenAI SDK** — https://github.com/openai/openai-node, https://github.com/openai/openai-python
- **Sibling skill (direct commands)** — `skills/alltoken-call/SKILL.md`

## Asking for help

If the bootstrap fails, the agent should print the request_id from the AllToken error envelope. Include that and the model ID in any support ticket — it lets the AllToken team trace the exact call across the gateway.
