# DashPass Security Model

## Who holds the keys

**You do.** The private key (`CRITICAL_WIF`) lives on your machine as an environment variable. It is never transmitted over the network. The AI agent has access to a process that uses your key, but the key itself stays in your environment.

## What's stored on the blockchain

| Field | Encrypted? | Visible to others? |
|-------|:----------:|:-------------------:|
| Secret value (API key, password, etc.) | **Yes** (AES-256-GCM) | No — only ciphertext is visible |
| Service name | No | Yes |
| Label/description | No | Yes |
| Credential type, level, status | No | Yes |
| Version number | No | Yes |
| Expiry timestamp | No | Yes |
| Salt and nonce (for decryption) | No (public) | Yes (but useless without the WIF) |

## Encryption details

- **Algorithm:** AES-256-GCM (authenticated encryption)
- **Key derivation:** ECDH(self) → HKDF-SHA256 with per-credential random salt
- **Per-credential randomness:** Each credential gets a unique 32-byte salt and 12-byte nonce
- **Auth tag:** 16-byte GCM tag prevents ciphertext tampering

## Trust model (one sentence)

You trust **math** (AES-256-GCM encryption) and **open-source code** (you can read the encryption logic), not a company or a server.

## Revocation

If an agent misbehaves or a key is compromised:
- **Instant:** Delete the `CRITICAL_WIF` environment variable → agent loses all access immediately
- **Permanent:** Rotate the WIF → all old ciphertext becomes undecryptable
- **On-chain:** Revoke the Identity key → no more write access to the blockchain

## Local cache

DashPass caches encrypted credential data in `~/.dashpass/cache/` for faster repeated access (5-minute TTL). The cache file is encrypted with a key derived from your WIF. Cache directory permissions are `0700`, file permissions `0600`.

Disable caching: `export DASHPASS_CACHE=none`

---

## Architecture

### Data Flow

```
 ┌──────────────────────────────────────────────────────────────┐
 │  YOUR MACHINE                                                │
 │                                                              │
 │  ┌─────────┐    ┌──────────────┐    ┌───────────────────┐   │
 │  │ AI Agent │───▶│ dashpass-cli │───▶│ Encrypt with      │   │
 │  │ (Claude  │    │   .mjs       │    │ YOUR key (WIF)    │   │
 │  │  Code)   │    │              │    │ AES-256-GCM       │   │
 │  └─────────┘    └──────────────┘    └─────────┬─────────┘   │
 │                                               │              │
 └───────────────────────────────────────────────┼──────────────┘
                                                 │
                                    encrypted blob only
                                                 │
                                                 ▼
                              ┌───────────────────────────┐
                              │    Dash Platform           │
                              │    (decentralized          │
                              │     blockchain)            │
                              │                            │
                              │  Stores: ciphertext +      │
                              │  metadata (service name,   │
                              │  type, level, version)     │
                              │                            │
                              │  CANNOT decrypt — does     │
                              │  not have your key         │
                              └───────────────────────────┘
```

### Role Model

```
 HUMAN (you)                      AI AGENT (Claude Code, scripts)
 ────────────                     ──────────────────────────────
 - Owns the WIF (master key)      - Calls put/get/rotate/delete
 - Creates the Identity            - Never sees the WIF directly
 - Can revoke access instantly     - Uses the CLI which uses the WIF
 - Approves critical operations    - Cannot escalate its own permissions
 - Sets security levels            - Follows security level rules
```

### Encryption Flow (Scheme C)

```
WIF (private key)
    │
    ▼
secp256k1 private key bytes
    │
    ▼
ECDH(self, self) → shared secret
    │
    ▼
HKDF-SHA256(shared_secret, random_salt, "dashpass-v1") → 256-bit AES key
    │
    ▼
AES-256-GCM(aes_key, random_nonce, plaintext) → ciphertext + auth_tag
    │
    ▼
Store on Dash Platform: { encryptedBlob, salt, nonce, metadata... }
```

---

## Security Analysis Summary

> Full analysis at `references/security-analysis-summary.md`

### P0 Findings (All Fixed)

| Issue | Fix |
|-------|-----|
| Plaintext cache in world-readable `/tmp/` | Cache moved to `~/.dashpass/cache/`, encrypted, permissions 0600 |
| `--value` exposed in shell history | Added `--value-stdin` flag with warning |
| Decrypted values stored in cache | Cache stores only encrypted blobs; decryption on read |

### P1 Findings (Open)

- No `rekey` command for key rotation (planned Phase 2)
- No input validation on credType/level/status (planned)
- Private key Buffers not fully zeroed after use (partially fixed)
- No migration procedure documentation (planned)

### Platform Security

- Client-side encryption: Platform nodes never see plaintext
- `$ownerId` enforcement: only credential owner can modify/delete
- Metadata (service names, types) visible on-chain — accepted trade-off for queryability
