---
name: dashpass
version: "0.9.0"
description: >
  Encrypted credential vault on Dash Platform for AI agents.
  Store and retrieve API keys, tokens, and passwords — encrypted on-chain, decryptable only by you.
  Triggers on: credential management, password vault, API key storage, secret store, Dash Platform credentials.
requires:
  env:
    - CRITICAL_WIF
    - DASHPASS_IDENTITY_ID
  bins:
    - node
  packages:
    - "@dashevo/evo-sdk@3.1.0-dev.1"
    - "@scure/bip39@^2.2.0"
---

<!--
  CHANGELOG
  0.9.0 — Key Backup & Recovery (P0-3). New standalone `dashpass-recover-cli.mjs`
          (backup/recover/verify) that turns the CRITICAL_WIF private key into a
          24-word BIP-39 mnemonic and back. NO evo-sdk dependency by design:
          recovery must run when the WIF is lost (the main CLI exits without it)
          or the Platform is unreachable. Closes "lost WIF = total vault loss".
  0.8.1 — Mutual Confirmation (Shamir 2-of-2).
-->

<!-- Safety: this file is documentation only — no executable code -->

# DashPass — Encrypted Credential Vault on Dash Platform

DashPass lets you store API keys, passwords, and other secrets **encrypted on the Dash blockchain**. Only someone with your private key can decrypt them — not the blockchain nodes, not your AI agent, not anyone else.

Your AI agent calls a CLI tool to store and retrieve credentials. Encryption happens locally *before* anything touches the network. The blockchain only ever sees ciphertext. Think of it as a password manager where the "cloud" is a decentralized blockchain.

## Why DashPass Instead of a `.env` File

| | `.env` file | DashPass |
|---|---|---|
| **Where secrets live** | Plain-text file on one machine | Encrypted on decentralized blockchain |
| **Disk failure** | Secrets gone (unless backed up) | Recoverable with your key |
| **Encryption** | None | AES-256-GCM per credential |
| **Rotation tracking** | Manual | Built-in version history |
| **Expiry alerts** | None | `check --expiring-within 7d` |
| **Multi-machine** | Copy file around (risky) | Any machine with your key |

---

## Quick Reference

```bash
CLI=skills/dashpass/scripts/dashpass-cli.mjs

# Store a credential
echo "sk-xxx" | node $CLI put --service anthropic-api --type api-key --level sensitive --label "Anthropic key" --value-stdin

# Retrieve a credential
node $CLI get --service anthropic-api --pipe

# Retrieve via mutual confirmation (2-of-2 Shamir shares)
node $CLI get --service anthropic-api --mutual

# List all credentials
node $CLI list

# Rotate to new value
echo "sk-NEW" | node $CLI rotate --service anthropic-api --value-stdin

# Check expiring credentials
node $CLI check --expiring-within 7d

# Vault status + credit balance
node $CLI status

# Delete a credential
node $CLI delete --service my-service

# Export as env vars (for eval)
eval $(node $CLI env --services anthropic-api,brave-search-api)

# Initialize Shamir 2-of-2 shares from CRITICAL_WIF
node $CLI init-shares

# Check share health
node $CLI share-status

# --- Key Backup & Recovery (standalone, no evo-sdk needed) ---
REC=skills/dashpass/scripts/dashpass-recover-cli.mjs

# Back up the vault key as a 24-word mnemonic (write it on paper, offline)
node $REC backup > /dev/tty            # prints to stdout; redirect as you see fit

# Confirm a written mnemonic still matches the current key (non-destructive)
cat words.txt | node $REC verify       # exit 0 = matches, 1 = mismatch

# Recover the WIF from the mnemonic after losing CRITICAL_WIF
cat words.txt | node $REC recover      # prints WIF; then: export CRITICAL_WIF=<wif>
```

---

## Mutual Confirmation Protocol

DashPass supports a 2-of-2 mutual confirmation mode using Shamir Secret Sharing over GF(2^8). This upgrades the single-key Scheme C to require both Evo (main agent) and CC (execution agent) to agree before any credential can be decrypted.

### How It Works

1. **`init-shares`**: Splits the 32-byte private key derived from `CRITICAL_WIF` into two Shamir shares using a random degree-1 polynomial evaluated at x=1 (Share A) and x=2 (Share B).
2. **Share storage**: Share A goes to `~/.dashpass/evo.share`, Share B to `~/.dashpass/cc.share` (both 0600 permissions).
3. **`get --mutual`**: Reads both shares, combines via Lagrange interpolation to reconstruct the private key, derives the per-credential AES key (same ECDH+HKDF as Scheme C), decrypts, then zeroes all sensitive buffers.
4. **Audit trail**: Every request/approval/denial/execution is logged to `~/.dashpass/audit.log` in JSONL format. No key or share material is ever logged.

### Security Properties

- **Information-theoretic**: Neither share alone reveals any information about the key (each byte is independently split).
- **Backward-compatible**: Without shares, `get` still works via Scheme C. With shares, `get --mutual` uses the new protocol.
- **Memory-safe**: Private key bytes and AES keys are zeroed immediately after use via `Buffer.fill(0)`.

### Setup

```bash
# One-time: generate shares from CRITICAL_WIF
node $CLI init-shares

# Verify health
node $CLI share-status
```

---

## Key Backup & Recovery (P0-3)

The whole vault is encrypted under one root: the 32-byte private key derived from
`CRITICAL_WIF`. **Lose that key and every credential is gone** — there is no
maintainer-held recovery. v0.9 closes this with a BIP-39 mnemonic backup of the
key, modelled on standard wallet recovery-word practice.

This lives in a **separate, dependency-light tool** (`dashpass-recover-cli.mjs`),
not the main CLI, on purpose:

- `recover` is needed exactly when `CRITICAL_WIF` is **lost** — but the main CLI
  exits immediately when `CRITICAL_WIF` is unset, so recovery cannot live there.
- Recovery must work when the Platform SDK or network is **unavailable**. The tool
  imports only `node:crypto` + `@scure/bip39` — **no `@dashevo/evo-sdk`**.

### Commands

| Command | Input | Output | Notes |
|---------|-------|--------|-------|
| `backup` | `CRITICAL_WIF` (env) | 24-word mnemonic (stdout) | Write it on paper, offline. |
| `verify` | `CRITICAL_WIF` + mnemonic (stdin) | exit 0 / 1 | Non-destructive check that a written backup is correct. |
| `recover` | mnemonic (stdin) | WIF (stdout) | After loss: `export CRITICAL_WIF=<wif>`. |

The mnemonic encodes the raw 32-byte key. Scheme C strips the WIF
version/compression byte, so the derived AES key depends only on those 32 bytes —
a recovered key decrypts **every existing credential**, unchanged.

### Security notes

- The mnemonic is **as sensitive as the WIF itself** — full vault control. Never
  store it on the same disk as the vault; treat it like wallet seed words.
- `backup`/`recover` zero the key buffer (`Buffer.fill(0)`) after use.
- Recovery reconstructs the **same** key — it is not a second key hierarchy and
  does not re-encrypt anything.

---

## Architecture

### Encryption Flow (Scheme C)

```
CRITICAL_WIF
  │
  ▼
wifToPrivateKey()           ← Base58Check decode, extract 32-byte private key
  │
  ▼
ECDH self-sign (secp256k1)  ← computeSecret(getPublicKey()) → sharedSecret
  │
  ▼
HKDF-SHA256                 ← hkdfSync('sha256', sharedSecret, salt, 'dashpass-v1', 32)
  │
  ▼
AES-256-GCM                 ← per-credential encrypt/decrypt
  │
  ▼
Dash Platform               ← encryptedBlob + salt + nonce stored on-chain
```

Each credential gets a unique `salt` (32 bytes) and `nonce` (12 bytes), so even identical plaintext values produce different ciphertext.

### Mutual Confirmation Flow (Shamir 2-of-2)

```
  INIT (one-time):
  ┌─────────────────────────────────────────┐
  │  CRITICAL_WIF → 32-byte private key     │
  │       │                                  │
  │       ▼                                  │
  │  For each byte i:                        │
  │    a0 = key[i], a1 = random              │
  │    f(x) = a0 ⊕ (a1 · x)   [GF(2^8)]   │
  │       │                                  │
  │  ┌────┴────┐                             │
  │  ▼         ▼                             │
  │ f(1)      f(2)                           │
  │ Share A   Share B                        │
  │ evo.share cc.share                       │
  │ (0600)    (0600)                         │
  └─────────────────────────────────────────┘

  DECRYPT (each request):
  ┌─────────────────────────────────────────┐
  │  1. CC: requestDecrypt(service, reason)  │
  │  2. Evo: approveDecrypt(request)         │
  │  3. combineShares(A, B)                  │
  │       │                                  │
  │       ▼                                  │
  │  Lagrange interpolation at x=0:          │
  │    key[i] = sA[i]·L1 ⊕ sB[i]·L2        │
  │    L1 = 2·inv(3), L2 = inv(3)           │
  │       │                                  │
  │       ▼                                  │
  │  Reconstructed private key               │
  │       │                                  │
  │       ▼                                  │
  │  ECDH + HKDF → AES key → decrypt        │
  │       │                                  │
  │       ▼                                  │
  │  Zero all buffers (privKey, aesKey,      │
  │  sharedSecret)                           │
  └─────────────────────────────────────────┘
```

Key design choices:
- **Split the raw private key, not derived AES keys.** One pair of shares covers all credentials — no per-credential splitting needed.
- **GF(2^8) with irreducible polynomial 0x11d.** Standard Rijndael/AES field. Byte-level operations, no bignum library required.
- **Precomputed Lagrange coefficients.** L1 and L2 are constants (2-of-2 at x=1, x=2), computed once at module load.

---

## Security Model

### What This Protects Against

| Threat | Protection |
|--------|-----------|
| **Single share compromise** | Neither share alone reveals any information about the key (information-theoretic security in GF(2^8)) |
| **Unauthorized decryption** | Both shares must be present — a rogue process with access to only one share file cannot decrypt |
| **Key material in memory** | All sensitive buffers (`privKeyBytes`, `aesKey`, `sharedSecret`) are zeroed with `Buffer.fill(0)` after use |
| **Audit evasion** | Every request/approve/deny/execute is logged to `~/.dashpass/audit.log` in JSONL format; no key material is ever logged |
| **File permission escalation** | Share files are stored with `0600` permissions; directory is `0700` |
| **Corrupted shares** | `init-shares` performs a round-trip verification before declaring success |

### What This Does NOT Protect Against

| Limitation | Explanation |
|-----------|-------------|
| **Same-machine attacker with root** | Both shares live on the same filesystem. A root-level attacker can read both. This is a same-machine deployment limitation. |
| **JavaScript string immutability** | Hex-encoded share strings are JS immutable strings — they cannot be zeroed from memory. They persist until garbage collected. |
| **Process memory dump** | If the process is memory-dumped during `executeDecrypt`, the reconstructed key is briefly in a Buffer. The window is minimized but not zero. |
| **Share file backup/sync** | If `~/.dashpass/` is included in backups or cloud sync, shares may be replicated to less-secure locations. |

### Honest Assessment

The current deployment is **same-machine 2-of-2**: both Evo (main agent) and CC (execution agent) run on the same host. This means:

- The security gain is **procedural, not physical** — it enforces a two-step confirmation workflow and audit trail, preventing a single code path from silently accessing credentials.
- It is **not equivalent** to a true multi-party setup where shares are on different machines controlled by different entities.
- The upgrade path to cross-machine deployment is straightforward: move `cc.share` to a separate host and replace `readShareB()` with a network request.

---

## Troubleshooting

### Share files missing or corrupted

```bash
# Check share health
node $CLI share-status

# If shares are missing or unhealthy, re-initialize:
rm -f ~/.dashpass/evo.share ~/.dashpass/cc.share
node $CLI init-shares
```

**Note:** Re-initializing creates new shares from `CRITICAL_WIF`. Existing encrypted credentials are unaffected — they are decrypted using the same private key derived from the same WIF.

### Permission errors on share files

```bash
# Shares must be 0600, directory must be 0700
chmod 700 ~/.dashpass
chmod 600 ~/.dashpass/evo.share ~/.dashpass/cc.share
```

If `init-shares` reports success but `share-status` shows wrong permissions, check if a umask override is active.

### `get --mutual` fails with decryption error

1. **Verify shares are healthy:** `node $CLI share-status` — both must show `Healthy: yes`
2. **Verify WIF hasn't changed:** If `CRITICAL_WIF` was rotated after `init-shares`, the shares are stale. Re-initialize.
3. **Check credential exists:** `node $CLI list` — confirm the service name matches exactly.

### Audit log growing large

The audit log at `~/.dashpass/audit.log` is append-only JSONL. To rotate:

```bash
mv ~/.dashpass/audit.log ~/.dashpass/audit.log.$(date +%Y%m%d)
# New entries will create a fresh audit.log automatically
```

### Scheme C still works without shares

Yes — this is by design. Without shares, `get` (without `--mutual`) decrypts directly using `CRITICAL_WIF`. Shares are optional and additive. You can set up mutual confirmation at any time without re-encrypting existing credentials.

---

## When to Use DashPass

Activate this skill when the user or agent needs to:

- Store an API key, token, password, or other secret
- Retrieve a previously stored credential
- Rotate / update an existing credential
- Check which credentials are expiring
- List all stored credentials
- Delete a credential from the vault
- Export credentials as environment variables
- Check vault status or credit balance
- Discuss credential management strategy
- Compare DashPass with other secret storage approaches

---

## Agent Behavior Rules

1. **Never log or display decrypted values** unless the user explicitly asks. Use `--pipe` for programmatic access.
2. **Always use `--value-stdin`** (pipe) for `put` and `rotate`. Never use `--value` with literal secrets — it leaks to shell history.
3. **Never hardcode WIF or Identity ID** in scripts. They come from environment variables only.
4. **Wait 3-5 seconds** between consecutive write operations (put, rotate, delete) to the same Identity. Platform nonce timing constraint.
5. **Check `status` first** if any operation fails with credit or balance errors.
6. **Testnet only** — do not attempt mainnet operations unless the user explicitly authorizes.
7. **Treat `CRITICAL_WIF` as radioactive** — if it appears in conversation, immediately warn the user about exposure risk.
8. **The recovery mnemonic is as radioactive as the WIF** — it grants full vault control. Never display, log, or store it on the vault's disk; `backup` output goes to paper/offline only.

---

## First-Time Setup

If the user has not used DashPass before, read the setup guide:

```
Read {baseDir}/setup.md
```

---

## Detailed References

For full CLI command documentation (all parameters, examples, output formats):

```
Read {baseDir}/references/cli-commands.md
```

For encryption details, architecture diagrams, trust model, and security analysis:

```
Read {baseDir}/references/security-model.md
```

For troubleshooting common errors and known limitations:

```
Read {baseDir}/references/faq.md
```

For the prior security audit summary:

```
Read {baseDir}/references/security-analysis-summary.md
```

---

## Command → Reference Map

| Intent | CLI Command | Reference |
|--------|-------------|-----------|
| Store a secret | `put` | `{baseDir}/references/cli-commands.md` |
| Retrieve a secret | `get` | `{baseDir}/references/cli-commands.md` |
| List credentials | `list` | `{baseDir}/references/cli-commands.md` |
| Rotate a credential | `rotate` | `{baseDir}/references/cli-commands.md` |
| Check expiring | `check` | `{baseDir}/references/cli-commands.md` |
| Vault status | `status` | `{baseDir}/references/cli-commands.md` |
| Delete credential | `delete` | `{baseDir}/references/cli-commands.md` |
| Export as env vars | `env` | `{baseDir}/references/cli-commands.md` |
| Init Shamir shares | `init-shares` | `{baseDir}/scripts/mutual-confirm.mjs` |
| Check share health | `share-status` | `{baseDir}/scripts/mutual-confirm.mjs` |
| Mutual decrypt | `get --mutual` | `{baseDir}/scripts/mutual-confirm.mjs` |
| Back up the key | `recover-cli backup` | `{baseDir}/scripts/dashpass-recover-cli.mjs` |
| Verify a backup | `recover-cli verify` | `{baseDir}/scripts/dashpass-recover-cli.mjs` |
| Recover a lost key | `recover-cli recover` | `{baseDir}/scripts/dashpass-recover-cli.mjs` |
| How encryption works | — | `{baseDir}/references/security-model.md` |
| Error troubleshooting | — | `{baseDir}/references/faq.md` |
| First-time setup | — | `{baseDir}/setup.md` |
