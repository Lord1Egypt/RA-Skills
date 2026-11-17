---
name: "claimcheck"
description: "Local-first secret shield for AI coding agents: tickets passwords, API keys, tokens and client PII before they reach the LLM — reversible via a local encrypted vault. MCP tools + CLI, zero network calls."
---

# ClaimCheck — local PII pseudonymization

ClaimCheck replaces sensitive values with stable, reversible placeholders
(`[FEIN_1]`, `[PASSWORD_2]`, `[PERSON_1]`...) and keeps the mapping in a local
encrypted vault. Nothing leaves the machine — no account, no API key, no
network calls.

## Why: the debug-leak problem

Every time an agent debugs a live project it reads `.env`, `appsettings.json`,
logs and scripts — and those secrets ride into the LLM provider's stored
context. ClaimCheck tickets them before they leave: the model works over
tickets, your secrets stay local, and files the agent writes come back with
the real values restored.

## When to use (always for client-adjacent data)

- Before quoting any file's contents into chat, tickets, docs, emails, or
  commits when it may contain client data (FEIN, SSN, account numbers, names,
  credentials)
- Before sharing sample data — share the sanitized sample instead
- To CHECK a file for PII without reading it: `sanitize-file <path>` (no --content)

## Commands

```bash
# text from stdin → JSON {label, summary, findings, sanitized}
echo "..." | dotnet bin/Release/net9.0/ClaimCheck.dll sanitize-text

# text as argument
dotnet bin/Release/net9.0/ClaimCheck.dll sanitize-text "some text"

# file → summary only (types/counts/lines, no content) or with sanitized content
dotnet bin/Release/net9.0/ClaimCheck.dll sanitize-file /path/to/file --content

# restore placeholders → real values (local vault only)
dotnet bin/Release/net9.0/ClaimCheck.dll restore <file|->
```

Recognized (regex tier, always on): FEIN, SSN, email, phone, cards (Luhn),
IBAN, AWS/GitHub/Slack tokens, API keys, JWTs, connection-string passwords,
PEM private-key blocks, base64/hex blobs, .env/config label anchoring
(KEY/SECRET/TOKEN/PASSWORD/COOKIE labels), provider prefixes (github_pat_,
whsec_, sess_, npm_, glpat_).

Optional tiers:
- Presidio (local container, `SANITIZE_PRESIDIO_URL`): free-text NER + crypto
  wallets, country formats. Skipped above 50K chars (regex tiers still full).
- Known-value re-ticketing: once a value is in the vault it can never reach
  the model again in any form — re-reads, echoes, and tool outputs all re-ticket.

## Rules

1. Share ONLY the `sanitized` field — findings show placeholders, never values.
2. Never paste raw FEIN/SSN/card/credential values into chat, logs, or commits.
3. The vault lives in `~/.sanitize-mcp/vaults` (encrypted at rest on Windows
   via DPAPI; AES-GCM with `SANITIZE_VAULT_PASSWORD` elsewhere). The machine is
   the trust boundary.
4. Not 100% — verify sanitized output before high-stakes sharing (DISCLAIMER.md).

## On-wire proxy (scrub any OpenAI-compatible client)

The proxy sits between your client and the LLM provider: every request is
scrubbed, every response restored. Works with Cline, Cursor, Codex CLI — any
client that takes a custom Base URL.

Windows (one-time): install the GitHub release — `install.ps1` registers a
logon task that runs the tray, which hosts the proxy on `:8766`.

Any OS (manual): run the binary as the proxy:
```
ClaimCheck --proxy --upstream https://api.z.ai/api/coding/paas/v4/ --port 8766
```

Point your client's Base URL at the proxy — it mirrors the upstream path:
```
http://127.0.0.1:8766/api/coding/paas/v4      (z.ai)
http://127.0.0.1:8766/v1                      (OpenAI/Anthropic/OpenRouter)
```

Keep your real API key in the client — auth passes through untouched.
Optional tiers on the proxy: SANITIZE_PRESIDIO_URL (local presidio
container) + SANITIZE_NER=1 (local NER model).
Full story: https://claimcheck.saasclaw.ai
