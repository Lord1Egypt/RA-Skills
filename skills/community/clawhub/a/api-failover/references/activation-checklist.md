# API Failover activation checklist

This file is the shortest path from "framework is working" to "real multi-route failover is actually active".

## Current status in this workspace

### Already working
- Local failover endpoint: `http://127.0.0.1:4010/v1`
- Service: `systemctl --user status api-failover.service`
- Primary route: `custom-ai-td-ee/gpt-5.4`
- Primary credential inheritance from OpenClaw config: working
- Health check and real curl chat request: working
- Failure responses now return a readable `user_message` and `summary` when all routes fail

### Not yet active
- Anthropic fallback: missing `ANTHROPIC_API_KEY`
- OpenRouter fallback: missing `OPENROUTER_API_KEY`
- Local fallback: no local backend detected on `127.0.0.1:11434`

## Fastest activation paths

### Path A — enable OpenRouter fallback
Provide in either shell env or `~/.config/api-failover.env`:

```bash
OPENROUTER_API_KEY=...
```

Then run:

```bash
python3 /root/.openclaw/workspace/skills/api-failover/scripts/activate_secondary.py
```

### Path B — enable Anthropic fallback
Provide in either shell env or `~/.config/api-failover.env`:

```bash
ANTHROPIC_API_KEY=...
```

Then run:

```bash
python3 /root/.openclaw/workspace/skills/api-failover/scripts/activate_secondary.py
```

### Path C — enable local emergency fallback
Install and run Ollama or another OpenAI-compatible local backend on `127.0.0.1:11434`.

Example target shape:
- base URL: `http://127.0.0.1:11434/v1`
- chat endpoint: `/chat/completions`

Then run:

```bash
python3 /root/.openclaw/workspace/skills/api-failover/scripts/activate_secondary.py
```

## Recommended env file

You can persist secondary credentials here:

```bash
~/.config/api-failover.env
```

Example:

```bash
OPENROUTER_API_KEY=...
ANTHROPIC_API_KEY=...
OLLAMA_DUMMY_KEY=dummy
```

The user service now reads this file automatically if it exists.

## Minimal client template

Any OpenAI-compatible client can usually be pointed here:

- Base URL: `http://127.0.0.1:4010/v1`
- API key: any placeholder if the client insists on one for local URLs
- Model: `gpt-5.4` or any model field your client requires; the proxy will override by route policy when needed

## Known-good manual test

```bash
curl -s http://127.0.0.1:4010/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [{"role": "user", "content": "Reply with exactly: ok"}],
    "max_tokens": 16,
    "temperature": 0
  }' | jq
```

## Activation script behavior

`activate_secondary.py` will:
1. inspect shell env and `~/.config/api-failover.env`
2. detect Anthropic/OpenRouter/local fallback availability
3. reload + restart the user service
4. run the forced failover drill
5. print whether a secondary path actually activated

If no secondary resource is detected, it will fail clearly instead of pretending activation succeeded.

## Suggested next real action

Do one of these next:
- add `OPENROUTER_API_KEY` to `~/.config/api-failover.env`
- add `ANTHROPIC_API_KEY` to `~/.config/api-failover.env`
- bring up Ollama locally
- point one everyday OpenAI-compatible tool at `http://127.0.0.1:4010/v1`
