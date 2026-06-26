# ClawHub Publish Notes

This folder is a publish-ready OpenClaw skill package.

## Contents

1. `SKILL.md` - skill definition and runtime guidance.
2. `AIONIS_ENV_TEMPLATE.txt` - local standalone defaults.
3. `bootstrap-local-standalone.sh` - one-click local install/start script.

## Local Standalone First (Required)

One-click bootstrap:

```bash
bash ./bootstrap-local-standalone.sh
```

The script creates:

1. `.runtime/aionis.env` for container runtime
2. `.runtime/clawbot.env` for Clawbot skill variables

Manual start (equivalent):

```bash
docker run -d --name aionis-standalone-local --restart unless-stopped \
  -p 127.0.0.1:3001:3001 \
  --env-file ./.runtime/aionis.env \
  -v aionis-standalone-data:/var/lib/postgresql/data \
  ghcr.io/cognary/aionis:standalone-v0.2.5
```

Health check:

```bash
curl -fsS http://127.0.0.1:3001/health
```

Auth check (`x-api-key`):

```bash
curl -sS http://127.0.0.1:3001/v1/memory/write \
  -H 'content-type: application/json' \
  -H 'x-api-key: YOUR_MEMORY_API_KEY' \
  -d '{"tenant_id":"default","scope":"default","input_text":"clawbot local standalone test"}'
```

## Publish

```bash
npm i -g clawhub
clawhub login
clawhub whoami

clawhub publish . \
  --slug aionis-memory-policy-loop \
  --name "Aionis Memory Policy Loop" \
  --version 1.0.0 \
  --changelog "Initial release" \
  --tags latest
```

## Update

```bash
clawhub publish . \
  --slug aionis-memory-policy-loop \
  --name "Aionis Memory Policy Loop" \
  --version 1.0.1 \
  --changelog "Fix prompt and examples" \
  --tags latest
```
