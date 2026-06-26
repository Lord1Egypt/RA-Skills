# DashPass Security Analysis — Summary

> Condensed from the full analysis at `docs/dashpass-security-analysis.md`
> Date: 2026-04-05

## Encryption: Strong

- AES-256-GCM with per-credential HKDF-SHA256 key derivation
- 32-byte random salt per credential, 12-byte random nonce
- GCM authenticated encryption prevents tampering
- No nonce reuse risk (unique key per credential)

## P0 Findings (Fixed)

| ID | Issue | Fix |
|----|-------|-----|
| P0-1 | Plaintext cache in world-readable `/tmp/` | Cache moved to `~/.dashpass/cache/`, encrypted with AES-256-GCM, file permissions 0600 |
| P0-2 | `--value` exposed in shell history | Added `--value-stdin` flag; warning printed when `--value` used via CLI args |
| P0-3 | Decrypted values stored in cache | Cache stores only encrypted blobs; decryption happens on read |

## P1 Findings (Open)

| ID | Issue | Status |
|----|-------|--------|
| P1-1 | No `rekey` command for key rotation | Planned for Phase 2 |
| P1-2 | No input validation on credType/level/status | Planned |
| P1-3 | Private key Buffers not zeroed after use | Partially fixed (deriveAesKey now zeros) |
| P1-4 | No migration procedure documentation | Planned |
| P1-5 | Cache not integrity-checked (HMAC) | Cache is now AES-GCM encrypted (auth tag provides integrity) |
| P1-6 | Non-unique service index allows injection | Accepted risk (requires Identity key compromise) |

## P2 Findings (Deferred)

- Verbose/quiet error modes
- ECDH self-sign documentation
- Structured exit codes
- Rate limiting
- Metadata encryption

## Platform Security

- Client-side encryption: Platform nodes never see plaintext
- $ownerId enforcement: only credential owner can modify/delete
- Metadata (service names, types) visible on-chain — accepted trade-off for queryability

## Trust Model

See `trust-architecture.md` for the full trust minimization framework.
