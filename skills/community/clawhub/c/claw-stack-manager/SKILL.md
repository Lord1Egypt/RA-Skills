---
name: claw-stack-manager
description: "Manage Docker stacks via Portainer API. v2.41 compatible: preserves env vars during redeploy. Claw stack uses one-shot redeployer; other stacks via PUT update."
---

# Claw Stack Manager

Manage stacks via Portainer API. Compatible with Portainer 2.41+.

## How it works

- **Claw stack** — one-shot redeployer: stop → PUT (compose + preserved env) → async deploy
- **Other stacks** — same PUT-based flow

The redeployer is an `alpine:latest` container (outside the stack, survives stop).

## Usage

### Update (pull image + redeploy)

```bash
# Claw stack (default)
python3 {{SKILL_DIR}}/scripts/manage.py --mode update

# Other stack by ID
python3 {{SKILL_DIR}}/scripts/manage.py --mode update --stack 92

# Other stack by name
python3 {{SKILL_DIR}}/scripts/manage.py --mode update --stack searxng

# Skip image pull
python3 {{SKILL_DIR}}/scripts/manage.py --mode update --no-pull
```

### Other modes

```bash
# Restart gateway container only
python3 {{SKILL_DIR}}/scripts/manage.py --mode restart

# Just pull image
python3 {{SKILL_DIR}}/scripts/manage.py --mode pull-only
```

## Environment variables

- `PORTAINER_API_KEY` — required
- `PORTAINER_URL` — required (e.g. `http://portainer:9000`)
- `PORTAINER_ENDPOINT` (default: `2`)
- `CLAW_STACK_ID` (default: `89`)
- `CLAW_IMAGE` (default: `liyujiang/openclaw:latest`)

## Portainer compatibility

| Portainer version | Mode | Notes |
|------------------|------|-------|
| 2.19.x | update | Stop → sleep → start (old flow) |
| 2.41+ | update | Stop → PUT with env → async deploy |
