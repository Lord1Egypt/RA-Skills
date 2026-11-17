---
name: claimcheck
description: Sanitize PII/secrets (FEIN, SSN, names, credentials) from text or files with the local ClaimCheck CLI before anything leaves the machine; reversible via the local encrypted vault.
version: 1.1.4
metadata:
  openclaw:
    emoji: "🛡️"
    homepage: https://claimcheck.saasclaw.ai
    envVars:
      - name: SANITIZE_DATES
        required: false
        description: Dates are NOT ticketed by default (v0.9.2) — they're operational context. Set to 1 to re-enable DATE ticketing when dates are sensitive.
      - name: SANITIZE_NER
        required: false
        description: Off by default. Set to 1 to enable the NER tier (free-text names/orgs/locations; ~109MB model cached on first use).
      - name: SANITIZE_NER_TYPES
        required: false
        description: NER whitelist (default all four types) — e.g. ORG,LOC lets person-names pass through. Per-type thresholds via SANITIZE_NER_THRESHOLD_<TYPE>.
      - name: SANITIZE_VAULT_PASSWORD
        required: false
        description: Set to a password to encrypt vault files at rest (AES-GCM). On Windows, vaults are DPAPI-encrypted by default without it.
---

# ClaimCheck — local PII pseudonymization

ClaimCheck replaces sensitive values with stable, reversible placeholders
([FEIN_1], [PASSWORD_2], [PERSON_1]...) and keeps the mapping in a local
encrypted vault. Nothing leaves the machine — no account, no API key, no
network calls.

## Why: the debug-leak problem

Every time an agent debugs a live project it reads .env, appsettings.json,
logs and scripts — and those secrets ride into the LLM provider's stored
context. ClaimCheck tickets them before they leave: the model works over
tickets, your secrets stay local, and files the agent writes come back with
the real values restored.

## Install (one-time)

Windows PowerShell (installs to %USERPROFILE%\claimcheck\ClaimCheck.exe):

    irm https://raw.githubusercontent.com/saasclawai-org/ClaimCheck/main/tools/install.ps1 | iex

Linux (per-user, no sudo; x64 + arm64 prebuilt):

    curl -fsSL https://raw.githubusercontent.com/saasclawai-org/ClaimCheck/main/tools/install.sh | bash

Proxy as a systemd --user service: run `./install.sh --proxy --upstream <base-url> [--port 8766]`.

Repo: https://github.com/saasclawai-org/ClaimCheck — full configuration reference in docs/CONFIGURATION.md.

## When to use (always for client-adjacent data)

- Before quoting any file's contents into chat, tickets, docs, emails, or
commits when it may contain client data (FEIN, SSN, account numbers, names,
credentials)

- Before sharing sample data — share the sanitized sample instead

- To CHECK a file for PII without reading it: sanitize-file <path> (no --content)

## Commands

ClaimCheck sanitize-text              # text from stdin → JSON {summary, findings, sanitized}
ClaimCheck sanitize-text "some text"  # text as argument
ClaimCheck sanitize-file <path>       # file → summary only (no content)
ClaimCheck sanitize-file <path> --content
ClaimCheck restore <file|->           # placeholders → real values (local vault only)
ClaimCheck restore <file|-> --bare    # also restore bracket-less tickets (SSN_1)
ClaimCheck restore - --vault <path>   # pin exactly one vault (no sweep)
ClaimCheck vault-list [--summary]     # inspect the vault (counts or full entries)
ClaimCheck status                     # proxy running? NER? vault? presidio?

## Recognized (regex tier, always on, any input size)

FEIN, SSN, email, phone, cards (Luhn) + CVV/expiry, IBAN, AWS/GitHub/Slack
tokens, API keys, JWTs, connection-string passwords, PEM private-key blocks,
base64/hex blobs (decoded and masked when decoded content matches),
.env/config label anchoring (KEY/SECRET/TOKEN/PASSWORD/COOKIE labels),
provider prefixes (github_pat_, whsec_, sess_, npm_, glpat_), account
numbers, ID labels (customer/invoice/policy/patient/claim/employee
numbers), IMEI, VIN, US street addresses, medical licenses, insurance
member IDs.

## Dates are not ticketed by default (v0.9.2)

Deadlines and notice dates are operational context — ticketing them made the
model unable to answer "which deadline is earlier?" style questions. Set
`SANITIZE_DATES=1` if your documents treat dates as sensitive.

## Optional tiers

- Known-value re-ticketing: once a value is in the vault it can never reach
the model again in any form — re-reads, echoes, and tool outputs all re-ticket.

- Presidio (local container, SANITIZE_PRESIDIO_URL): crypto wallets +
international ID formats. Skipped above 50K chars (regex tiers still full).

- NER (SANITIZE_NER=1): free-text names/orgs/locations. Whitelist types with
SANITIZE_NER_TYPES and tune per-type via SANITIZE_NER_THRESHOLD_<TYPE>.

## Rules

- Share ONLY the sanitized field — findings show placeholders, never values.

- Never paste raw FEIN/SSN/card/credential values into chat, logs, or commits.

- The vault lives in ~/.sanitize-mcp/vaults (encrypted at rest on Windows
via DPAPI; AES-GCM with SANITIZE_VAULT_PASSWORD elsewhere). The machine is
the trust boundary.

- Not 100% — verify sanitized output before high-stakes sharing (DISCLAIMER.md).

## On-wire proxy (scrub any OpenAI-compatible client)

The proxy sits between your client and the LLM provider: every request is
scrubbed, every response restored. Works with Cline, Cursor, Codex CLI — any
client that takes a custom Base URL.

Windows (one-time): install the GitHub release — install.ps1 registers a
logon task that runs the tray, which hosts the proxy on :8766.

Any OS (manual): run the binary as the proxy:

ClaimCheck --proxy --upstream https://api.z.ai/api/coding/paas/v4/ --port 8766

Point your client's Base URL at the proxy — it mirrors the upstream path:

http://127.0.0.1:8766/api/coding/paas/v4 (z.ai)
http://127.0.0.1:8766/v1 (OpenAI/Anthropic/OpenRouter)

Keep your real API key in the client — auth passes through untouched.
Optional tiers on the proxy: SANITIZE_PRESIDIO_URL (local presidio
container) + SANITIZE_NER=1 (local NER model).
Full story: https://claimcheck.saasclaw.ai
