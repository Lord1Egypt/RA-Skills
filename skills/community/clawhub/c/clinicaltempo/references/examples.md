# Clinical Tempo — concrete examples

## Cursor / IDE context

```
@public/llm-full.txt
@CLAWHUB.md
@server/index.js
```

## OpenAPI / MPPScan (server must run)

```bash
curl -sS http://127.0.0.1:8787/openapi.json | head -c 400
npm run discovery
```

## Smoke: live MPP routes (server must run)

```bash
curl -sS http://127.0.0.1:8787/api/dance-extras/live | head
```

Expect JSON including `flowKeys` (array). If you get HTML or connection refused → wrong port or server not started.

## Regenerate LLM bundle

```bash
npm run build:llm
```

## Env names (never paste values)

From **`.env.example`**: `MPP_SECRET_KEY`, `MPP_RECIPIENT`, integration base URLs (`OPENAI_MPP_BASE_URL`, `AGENTMAIL_*`, etc.). **Do not** put real secrets in agent prompts.

## CLAWHUB-style success line (illustrative)

```markdown
3. **`GET /api/dance-extras/live` smoke** — returns `flowKeys` after restart of `npm run server` on 8787.
```

## EVVM deep link (attach in chat)

```
https://www.evvm.info/llms-full.txt
```

Use for protocol-level EVVM work; use **`docs/EVVM_TEMPO.md`** for Tempo testnet deploy steps.
