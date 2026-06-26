# Agent SCIF

**Sensitive Compartmented Information Facility — for AI agents.**

**A way to obfuscate sensitive data from friendly agents.**

Your AI agent is helpful and cooperative — and sometimes you want it to stay helpful without knowing everything. Agent SCIF is how you do that: a sealed memory architecture where your agent holds the encrypted file but is structurally excluded from reading it without your authorization.

> ⚠️ **This is a proof-of-concept experiment in agent SCIF architecture, not a production secrets manager.** It protects your data from your own cooperative agent on a machine you control — not from an adversary with filesystem access. See [Security Limitations](#security-limitations).

---

## The Problem

AI agents have two memory modes and neither is ideal:

| Mode | Persistent | Agent-blind |
|------|-----------|-------------|
| Normal memory | ✅ | ❌ Agent knows everything |
| No memory ("incognito") | ❌ | ✅ Nothing survives the session |
| **Agent SCIF** | ✅ | ✅ Agent is structurally excluded |

A SCIF (in the real world) is a room where classified work happens — no phones, no recording devices, no external connections. This is the AI equivalent: a sealed session the agent can knock on, but only you hold the key.

---

## How It Works

### At Rest
Your entries are stored in an AES-256-GCM encrypted file on disk. The agent has the file but cannot open it — the key is derived from your TOTP seed via Argon2id. No TOTP seed, no key. No key, no vault.

### The Clean Room (when open)
When you open the vault, the main agent does **not** decrypt it into its own context. Instead:

1. You send `open vault: [6-digit code]`
2. A **zero-history isolated sub-agent** spawns — no prior conversation context whatsoever
3. That sub-agent opens the vault and sends contents **directly to you** (Telegram/WhatsApp), bypassing the main agent entirely
4. The main agent becomes a **blind relay** — it forwards your commands but never sees the responses
5. `close vault` terminates the clean room and wipes the session key

```
You ──────────────────────────────────────────────────> You
     ↓ your commands    ↑ blind relay    ↑ direct response
     main agent ──────> sessions_send ─> [SCIF / clean room]
                                         zero history
                                         vault contents here only
                                         responds directly to you
```

**Main agent sees:** your commands. Nothing else.  
**Clean room sees:** vault contents + your commands. Responds only to you.

---

## Security Limitations

Be honest about what this protects and what it doesn't.

### ✅ What the SCIF protects against

- **Agent reading your vault at rest** — no code, no access
- **Prior context poisoning** — clean room starts with zero history; a poisoned main session can't reach inside
- **Vault contents leaking into agent memory** — responses bypass main agent entirely
- **Cross-user attacks** — ciphertext is bound to your `sender_id` via AAD; can't be decrypted by a different user's vault

### ❌ What it does NOT protect against

- **Filesystem access** — the TOTP seed lives in `vault/<id>.totp` on the same machine as the encrypted data. An attacker with filesystem access has everything they need to derive the vault key. The TOTP code you enter is a *software gate*, not a cryptographic factor. This is by design — the vault is meant to protect against the *agent*, not against root access to the host machine.
- **Typing secrets in main chat** — if you type your secret in the main chat to tell the agent to add it, that text is in the main agent's context. Use stdin piping or v1.1's direct-input clean room when it ships.
- **A compromised sub-agent process** — you're trusting the clean-room agent's behavior. Code review the SKILL.md instructions if paranoid.
- **Shell history / process list** — stdin piping (`echo "secret" | vault.py add <id> -`) mitigates this, but depends on correct usage.

### The honest one-liner
**This protects your secrets from your own AI assistant, on a machine you control.** It is not a replacement for a hardware security key or a proper secrets manager. It's an experiment in agent SCIF architecture — and the first of its kind.

---

## Security Model

- **Argon2id KDF** — Base32-decoded TOTP seed → KPK (time=3, mem=64MB, parallelism=4, GPU/ASIC resistant)
- **AES-256-GCM** — all encryption bound to `sender_id` as AAD (user-bound ciphertext)
- **TOTP auth** — 30s window, 1-code tolerance; ephemeral code never stored
- **Session key** — lives in `/tmp/.vault-<id>/` (mode 0o700), auto-expires 2h, wiped on close
- **Stdin for secrets** — content passed via pipe, not CLI args (no shell history / ps leakage)
- **Agent never sees TOTP seed or vault key** — only ever receives a 30s-valid 6-digit code

**Audited by Gemini 3 Pro Preview before publication.** See [Audit Results](#audit-results).

---

## Install

```bash
clawhub install agent-scif
```

**Dependencies:**

```bash
pip install argon2-cffi pyotp qrcode cryptography
```

---

## Setup

```bash
python3 scripts/vault.py setup <your_sender_id> --name "Your Name"
```

1. Scan the QR with Google Authenticator or Authy
2. **Delete the QR file** (`vault/<id>-setup.png`) immediately after
3. Guard `vault/<id>.totp` — it's your recovery key and your vault's security anchor

---

## Usage

### Open vault (launches clean room)
```
open vault: [6-digit code]
```
Clean room spawns. Vault contents delivered direct to you — not through the agent.

### Add an entry
```
add to vault: [content]
```
Agent forwards blind. Your entry goes in via stdin — not visible in process list or shell history.

### Close vault
```
close vault
```
Clean room terminates. Session key wiped. Vault re-locks.

### Delete an entry
```
delete from vault: [index]
```

---

## Audit Results

Audited by **Gemini 3 Pro Preview**. Findings addressed:

| Severity | Finding | Status |
|----------|---------|--------|
| CRITICAL | TOTP is software gate only (seed on disk) | 📄 Documented — by design; protects against agent, not filesystem access |
| HIGH | Command injection in cleanroom (unvalidated inputs) | ✅ Fixed — regex validation on sender_id + totp_code |
| HIGH | Secrets visible in shell history / ps aux | ✅ Fixed — stdin piping (`vault.py add <id> -`) |
| HIGH | TOTP seed printed to stdout on setup | ✅ Fixed (prior audit) |
| MEDIUM | Incomplete crash cleanup | ✅ Mitigated — 2h TTL auto-expires; atexit not used |
| LOW | Base32 seed not decoded before Argon2id | ✅ Fixed — Base32 decoded to raw bytes |
| LOW | Argon2id memory cost could be higher | 📄 Noted — 64MB meets OWASP minimum; increase for higher-security deployments |

Previous audit by Grok-3 also addressed: PBKDF2 → Argon2id, AAD binding, session dir permissions.

---

## Roadmap

- **v1.0** — Text vault + clean room (current)
- **v1.1** — Clean room prompts user directly for input (eliminates relay exposure entirely)
- **v2.0** — True cryptographic encryption via out-of-band passphrase input:
  - KDF becomes `Argon2id(TOTP_seed + passphrase, salt)` — neither alone is sufficient
  - Passphrase collected via a **local micro HTTP server** (never through chat)
  - Clean room spins up `localhost:PORT/vault-auth` on open → you submit passphrase in browser → server shuts down immediately
  - Passphrase lives in RAM for milliseconds, never logged, never in any message
  - True 2FA: something you have (TOTP device) + something you know (passphrase)
- **v2.1** — File sidecar support (images, documents as encrypted blobs)

---

*Built by Cory Miller. Audited by Gemini 3 Pro Preview. Shipped from zero dev experience. 🚀*  
*An experiment in agent SCIF architecture — proof that sealed memory for AI agents is possible.*
