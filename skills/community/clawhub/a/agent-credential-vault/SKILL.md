---
name: agent-credential-vault
description: Let your AI agent log in and call APIs using credentials it never sees. Secrets are encrypted at rest and brokered server-side, so passwords, API keys and TOTP codes stay out of the model's context, argv, logs and traces. Not a password manager for people; no cards, no payments.
homepage: https://useanima.sh
docs: https://docs.useanima.sh
metadata: {"api_base": "https://api.useanima.sh"}
---

# Anima Vault — let an agent use a secret without reading it

An agent that needs to log in somewhere has two bad options and one good one.

**Paste the secret into the prompt.** It is now in the context window, and in
every log, trace and eval dataset that context touches. Rotating it later does
not un-write those.

**Have a human do the login.** Then it is not an autonomous agent, it is a
form-filler with extra steps.

**Or put it in the vault and let the agent *use* it.** The strongest mode never
returns the plaintext to anyone — including the agent, and including you.

## Provision once

```bash
anima vault provision --agent <agent-id>
```

Provisioning is owner-gated. If it is refused, ask rather than retry:

```bash
anima request vault --agent <agent-id> --reason "needs to log into the billing portal"
```

That is the design: the agent gets the outcome, the human keeps the authority.

## Store a credential

```bash
printf '%s' "$ACME_PASSWORD" | anima vault store \
  --agent <agent-id> \
  --name "acme-portal" \
  --username "ops@example.com" \
  --uri "https://portal.acme.com" \
  --password-stdin
```

`--password-stdin` is the point: the secret arrives over stdin, so it never
appears in `argv`, in shell history, or in the process list. There is
deliberately no `--password` flag.

Better still, let the vault invent it so no human or model ever knows it:

```bash
anima vault store --agent <agent-id> --name "acme-portal" \
  --username "ops@example.com" --generate-password --length 32
```

## Use it without revealing it

This is the part that makes an agent autonomous rather than a form-filler.
`vault use` performs the HTTP call **server-side** with the credential attached,
so the secret never reaches your process at all:

```bash
anima vault use \
  --credential <credential-id> \
  --method POST \
  --url https://api.acme.com/v1/orders \
  --header "Content-Type: application/json" \
  --body '{"sku":"A-1","qty":2}'
```

The agent gets the response. It never gets the key.

Two flags on `store` make that guarantee real rather than a convention:

| Flag | Effect |
|---|---|
| `--reveal-policy brokered` | Plaintext is **never** returned to anyone — use-only |
| `--allowed-host <host>` | The credential is brokered only to these hosts (api_key type) |

Set together, a stolen agent key cannot exfiltrate the secret and cannot point
it at an attacker's host:

```bash
printf '%s' "$ACME_KEY" | anima vault store --agent <agent-id> \
  --name "acme-api" --type api_key --provider acme --key-stdin \
  --allowed-host api.acme.com \
  --reveal-policy brokered
```

`--allowed-host` is repeatable and **fail-closed**: an api_key credential with
no allowed host is brokered nowhere at all.

## Injecting into a subprocess

When the tool you need to run only reads environment variables, resolve secrets
into that process's environment and nothing wider:

```bash
anima vault exec --agent <agent-id> --dry-run   # show what would resolve
anima vault exec --agent <agent-id> -- ./deploy.sh
```

`--dry-run` first. It prints which references resolve without running anything.

Related: `vault inject` substitutes `{{vault:...}}` references in stdin,
`vault redact` replaces known secret values in stdin with `[REDACTED]` (useful
before writing a transcript), and `vault audit <paths...>` scans files for
plaintext secrets you left behind.

## Reading, when you genuinely must

```bash
anima vault list --agent <agent-id>          # names and metadata, no secrets
anima vault get <credential-id> --agent <agent-id>
anima vault totp <credential-id>             # current 6-digit 2FA code
```

`get` and `totp` take the **credential ID as a positional argument** — get it
from `vault list`. Reading the raw value is the exception, not the workflow;
a credential stored `--reveal-policy brokered` will refuse.

## What this is not

It is not a password manager for people, and it is not a payments product.
Anima issues no cards and moves no money. A human holds spend authority; the
vault only lets an agent authenticate somewhere without being handed the secret
in plain text.

## Why it matters for audit

Every vault use carries a correlation ID back to the human who authorized it,
alongside the agent's email, SMS and voice activity. When someone later asks
"which agent logged into that portal, and who said it could?", the trail exists.

Free tier includes the vault, no credit card. Docs: <https://docs.useanima.sh>
