---
name: feishu-setup-troubleshooting
description: Set up and troubleshoot Feishu or Lark messaging integration with Hermes Agent, including connection checks, access control, and common failure modes.
tags: [feishu, lark, messaging, troubleshooting, setup, integration]
version: 1.2.2
primaryEnv: FEISHU_APP_SECRET
requires:
  bins:
    - hermes
  env:
    - FEISHU_APP_ID
    - FEISHU_APP_SECRET
    - FEISHU_DOMAIN
    - FEISHU_CONNECTION_MODE
    - FEISHU_GROUP_POLICY
    - FEISHU_ALLOW_ALL_USERS
    - GATEWAY_ALLOW_ALL_USERS
    - FEISHU_ALLOWED_USERS
    - FEISHU_ENCRYPT_KEY
    - FEISHU_VERIFICATION_TOKEN
---

# Feishu or Lark Setup and Troubleshooting

## When to use

- A user wants to connect Hermes Agent to Feishu or Lark.
- The bot is online but does not reply to messages.
- You need to diagnose permissions, gateway state, or connection issues.

## Prerequisites

- Hermes Agent is installed and the `hermes` CLI is available.
- A Feishu or Lark app exists with bot capability enabled.
- The required App ID and App Secret are available.

## Access-control reminder

Feishu access has two separate layers:

- `FEISHU_ALLOW_ALL_USERS`
- `GATEWAY_ALLOW_ALL_USERS`

If the gateway layer is still closed, Feishu users will be rejected even when the Feishu layer looks open.

## Setup and troubleshooting flow

1. Confirm configuration.
   Check that the required Feishu or Lark variables are present and that the domain and connection mode match the deployment.
2. Confirm the gateway is running.

```bash
hermes gateway status
```

3. Review recent logs.

```bash
hermes logs 2>&1 | grep -i feishu | tail -20
```

4. Test message delivery.
   Send a direct message and look for an inbound message log followed by a model response.
5. Restart after config changes.

```bash
hermes gateway restart
```

## Common issues

- Bot does not reply at all: the gateway is not running.
- `Unauthorized user` in logs: the gateway-level allow rule is still blocking access.
- Wrong region or domain: `FEISHU_DOMAIN` does not match the deployment.
- Messages arrive but there is no answer: the model provider or API key behind Hermes is failing.

## Security notes

- Prefer an allowlist for production.
- Never commit App Secret, encrypt keys, or verification tokens.
- Keep the gateway running under a limited user account.
- Review logs for sensitive output before sharing them externally.
