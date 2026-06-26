---
name: agentlair-vault
description: Store and fetch credentials securely at runtime via AgentLair Vault REST API. Use when an agent needs to read an API key, store a secret, rotate credentials, or avoid putting secrets in openclaw.json. Credentials stay in the vault — only the AGENTLAIR_API_KEY lives in your environment. Use instead of environment variables or openclaw.json for third-party API keys, tokens, and secrets.
version: 1.1.0
metadata:
  openclaw:
    homepage: https://agentlair.dev
    emoji: "🔐"
    os: ["linux", "macos", "windows"]
    primaryEnv: AGENTLAIR_API_KEY
    requires:
      bins:
        - curl
    tags:
      - credentials
      - secrets
      - vault
      - security
      - agent-identity
      - infrastructure
---

# AgentLair Vault — Runtime Credential Storage for Agents

Keep credentials out of `~/.openclaw/openclaw.json`. Store them in AgentLair Vault. Fetch them at runtime. Rotate with one API call.

Base URL: `https://agentlair.dev`
Auth: `Authorization: Bearer $AGENTLAIR_API_KEY`

**The agent holds a vault token. Not the credential itself.** Only `AGENTLAIR_API_KEY` lives in the environment — everything else is fetched at runtime through an audited, rate-limited API.

---

## Setup: Get an API Key

Self-service, no email required:

```bash
curl -s -X POST https://agentlair.dev/v1/auth/keys \
  -H "Content-Type: application/json" \
  -d '{}'
```

Response:
```json
{"api_key": "al_live_...", "account_id": "acc_...", "tier": "free", "created_at": "..."}
```

Store `api_key` as `AGENTLAIR_API_KEY` in your environment. This is the **only** credential that needs to be in your environment or config file.

---

## When to Use This Skill

Use this skill when:
- An agent needs to use an API key (Anthropic, OpenAI, Stripe, Slack, etc.)
- A user asks to store, retrieve, rotate, or revoke a credential
- You want to avoid storing secrets in `openclaw.json` or environment variables
- You're setting up a new agent and need to provision credentials
- A skill needs a third-party token that shouldn't be exposed to the filesystem

**Do not** use `openclaw.json` or environment variables for third-party API keys if you can store them in vault instead.

---

## Store a Secret (Setup / Rotation)

Store any secret under a named key. Use descriptive names (`anthropic-key`, `stripe-live`, `slack-bot-token`).

```bash
curl -s -X PUT "https://agentlair.dev/v1/vault/anthropic-key" \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ciphertext": "sk-ant-YOUR-KEY-HERE", "metadata": {"label": "Anthropic API key", "service": "anthropic"}}'
```

Response (first store, HTTP 201):
```json
{
  "key": "anthropic-key",
  "stored": true,
  "version": 1,
  "created_at": "2026-03-27T...",
  "updated_at": "2026-03-27T..."
}
```

Response (update / rotation, HTTP 200):
```json
{
  "key": "anthropic-key",
  "stored": true,
  "version": 2,
  "created_at": "2026-03-27T...",
  "updated_at": "2026-03-27T..."
}
```

**Key naming rules:** 1–128 characters, alphanumeric + `_`, `-`, `.`

**Optional `metadata` object** (max 4KB): human-readable context. Not the secret — just labels, service names, expiry hints. Never put secret values in metadata.

---

## Fetch a Secret at Runtime

Retrieve a stored secret by name. The `ciphertext` field contains the stored value.

```bash
curl -s "https://agentlair.dev/v1/vault/anthropic-key" \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY"
```

Response:
```json
{
  "key": "anthropic-key",
  "ciphertext": "sk-ant-YOUR-KEY-HERE",
  "value": "sk-ant-YOUR-KEY-HERE",
  "metadata": {"label": "Anthropic API key", "service": "anthropic"},
  "version": 1,
  "latest_version": 1,
  "created_at": "2026-03-27T...",
  "updated_at": "2026-03-27T..."
}
```

Use the `ciphertext` (or `value` — both return the same thing) field as the credential.

**To retrieve a specific version:**
```bash
curl -s "https://agentlair.dev/v1/vault/anthropic-key?version=1" \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY"
```

---

## List All Secrets

Get metadata for all stored keys (never returns ciphertext/values):

```bash
curl -s "https://agentlair.dev/v1/vault/" \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY"
```

Response:
```json
{
  "keys": [
    {
      "key": "anthropic-key",
      "version": 1,
      "metadata": {"label": "Anthropic API key"},
      "created_at": "2026-03-27T...",
      "updated_at": "2026-03-27T..."
    }
  ],
  "count": 1,
  "limit": 10,
  "tier": "free"
}
```

---

## Rotate a Secret

Rotation is a PUT with the new value. Creates a new version. The old version is retained (up to 3 versions on free tier) for rollback.

```bash
curl -s -X PUT "https://agentlair.dev/v1/vault/anthropic-key" \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ciphertext": "sk-ant-NEW-ROTATED-KEY", "metadata": {"label": "Anthropic API key", "rotated_at": "2026-03-27"}}'
```

All agents fetching `GET /v1/vault/anthropic-key` automatically get the new value on their next call — no config changes, no restarts.

---

## Revoke a Secret

Delete a key and all its versions:

```bash
curl -s -X DELETE "https://agentlair.dev/v1/vault/anthropic-key" \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY"
```

Response:
```json
{"key": "anthropic-key", "deleted": true, "versions_removed": 2}
```

**Delete a specific version only:**
```bash
curl -s -X DELETE "https://agentlair.dev/v1/vault/anthropic-key?version=1" \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY"
```

---

## Free Tier Limits

| Limit | Value |
|-------|-------|
| Keys per account | 10 |
| Versions per key | 3 (oldest pruned automatically) |
| Max value size | 16 KB |
| API requests per day | 100 |

---

## Example Session

**User:** "Store my Stripe API key in the vault and then use it to check my balance"

**Agent actions:**

1. Store the Stripe key in vault:
```bash
curl -s -X PUT "https://agentlair.dev/v1/vault/stripe-live" \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ciphertext": "sk_live_USER_PROVIDED_KEY", "metadata": {"label": "Stripe live key", "service": "stripe"}}'
```

2. Fetch the key at runtime:
```bash
STRIPE_KEY=$(curl -s "https://agentlair.dev/v1/vault/stripe-live" \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY" | grep -o '"ciphertext":"[^"]*"' | cut -d'"' -f4)
```

3. Use it:
```bash
curl -s "https://api.stripe.com/v1/balance" \
  -H "Authorization: Bearer $STRIPE_KEY"
```

4. Confirm to user: "Stripe key stored in vault as `stripe-live`. Current balance retrieved."

---

## Why Vault Instead of openclaw.json

OpenClaw's default credential storage (`~/.openclaw/openclaw.json`) puts API keys on disk in plaintext. A malicious ClawHub skill running on your agent can read everything there — plus `~/.aws/`, `~/.ssh/`, and any environment variables in the agent's process.

With AgentLair Vault:
- **Only `AGENTLAIR_API_KEY` is in your environment.** Everything else is fetched at runtime.
- **No credentials on disk.** `grep -r "sk-" ~/.openclaw/` finds nothing.
- **Audit trail.** Every credential fetch is logged. Unexpected access at 3am is visible.
- **Rotation without restarts.** Rotate once in vault — every agent gets the new value immediately.
- **Scoped access.** One AGENTLAIR_API_KEY can't read another account's keys.

The blast radius of a compromised skill drops from "all credentials on the machine" to "one rate-limited API key with an audit log."

---

## Client-Side Encryption (Optional)

For secrets you don't want AgentLair to see in plaintext, encrypt before storing:

```bash
# Encrypt locally before storing
SECRET="sk-ant-YOUR-KEY"
ENCRYPTED=$(echo -n "$SECRET" | openssl enc -aes-256-cbc -base64 -k "$LOCAL_PASSPHRASE")

curl -s -X PUT "https://agentlair.dev/v1/vault/anthropic-key" \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"ciphertext\": \"$ENCRYPTED\", \"metadata\": {\"encrypted\": \"aes-256-cbc\", \"label\": \"Anthropic API key\"}}"

# Decrypt when fetching
CIPHERTEXT=$(curl -s "https://agentlair.dev/v1/vault/anthropic-key" \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY" | grep -o '"ciphertext":"[^"]*"' | cut -d'"' -f4)
PLAINTEXT=$(echo "$CIPHERTEXT" | openssl enc -aes-256-cbc -d -base64 -k "$LOCAL_PASSPHRASE")
```

Use this when zero-knowledge storage is required. `$LOCAL_PASSPHRASE` never leaves your environment.

The [agentlair-vault-crypto](https://github.com/piiiico/agentlair-vault-crypto) library provides
TypeScript helpers for client-side encryption/decryption with AES-256 and key derivation.

---

## Trust & Security

- **Open-source crypto layer:** [github.com/piiiico/agentlair-vault-crypto](https://github.com/piiiico/agentlair-vault-crypto) — the encryption helpers used by the vault SDK are fully auditable
- **Security documentation:** [agentlair.dev/security](https://agentlair.dev/security) — encryption at rest, key isolation, access audit model
- **Trust architecture:** See the [AgentLair trust model blog post](https://agentlair.dev/blog) for how vault isolation, API key scoping, and audit logging work together

---

## Notes

- The vault stores values as opaque blobs — AgentLair never interprets the content
- Version history retained up to tier limit (3 versions free, 100 paid) — oldest pruned automatically
- Recovery: register a recovery email via `POST /v1/vault/recovery-email` to access vault contents if you lose your API key
- Built by [AgentLair](https://agentlair.dev) — infrastructure for autonomous agents
