---
name: axiom-hash-multi
description: Multi-algorithm hash generator (MD5/SHA-1/SHA-256/SHA-512/BLAKE2b) — deterministic, byte-to-byte, zero dependencies. Use when you need to hash a file or string with multiple algorithms at once, with no LLM, no cloud, no hallucination.
---

# 🛠️ axiom-hash-multi

**Version:** 1.1.3
**Axioma Tools — Skill #1 (Phase 1)**
**Cluster:** Axioma

## What this skill does

Calculates **5 hash algorithms at once** (or just one) on a file or bytes input:

- MD5
- SHA-1
- SHA-256
- SHA-512
- BLAKE2b (64-byte digest)

**Differentiators:**
- **Zero dependencies** (pure Python stdlib)
- **Byte-to-byte deterministic** (same input → same hash, always)
- **Streaming** for large files (no RAM bloat)
- **No LLM, no cloud, no hallucination**
- **Multiple algorithms in one call** (`--all` flag)

## When to use this skill

- ✅ Hash a file to verify integrity
- ✅ Get multiple algorithms at once for cross-verification
- ✅ Fingerprint files for deduplication
- ✅ Hash a string without writing a script
- ✅ Bulk hash a directory (loop with this CLI)
- ✅ Verify a file matches an expected hash (`--compare`)
- ✅ Verify all hashes in a MANIFEST file (`--verify-manifest`)
- ✅ Get structured JSON output for scripts (`--json`)
- ❌ When you need HMAC or password hashing (use bcrypt/argon2)
- ❌ When you need cryptographic signatures (use GPG/age)

## Usage

### CLI

```bash
# Single algorithm (default: SHA-256)
python3 axiom_hash_multi.py <file>
python3 axiom_hash_multi.py "my string" --string
echo "data" | python3 axiom_hash_multi.py --stdin

# Specific algorithm
python3 axiom_hash_multi.py <file> --algo md5
python3 axiom_hash_multi.py <file> --algo sha512

# All algorithms at once
python3 axiom_hash_multi.py <file> --all

# Verify against expected hash (exit 0 if match, 1 if not)
python3 axiom_hash_multi.py <file> --algo sha256 --compare=<expected_hex>

# Verify a MANIFEST.txt file (all hashes)
python3 axiom_hash_multi.py --verify-manifest MANIFEST.txt

# JSON output (structured for scripts)
python3 axiom_hash_multi.py <file> --all --json
```

### Python API

```python
from axiom_hash_multi import hash_bytes, hash_file, hash_all, hash_file_all, verify_manifest

# Bytes
digest = hash_bytes(b"hello", "sha256")

# File (streaming)
digest = hash_file("path/to/file", "sha256")

# All algorithms
results = hash_all(b"test")  # dict of 5 algorithms
results = hash_file_all("path/to/file")  # dict of 5 algorithms

# Verify MANIFEST
result = verify_manifest("MANIFEST.txt")  # {"verified": True, "checked": 12, "failed": 0}
```

## Validation status

| Check | Status |
|-------|--------|
| Unit tests (≥10 cases) | ✅ 24 tests + 16 stress tests = 40 cases |
| Performance <100ms | ✅ Validated for <100MB |
| Security (no injection) | ✅ Pure stdlib, no eval/subprocess |
| Determinism byte-to-byte | ✅ hashlib spec + 1000-runs test |
| 0 LLM/KAN dependency | ✅ stdlib only (hashlib, pathlib, json) |
| Doc (README + SKILL.md) | ✅ Complete for v1.1.0 |
| License | Apache-2.0 |

**Stress test results (9 groups, 40+ cases):** all green

_Last updated: 2026-06-14 — v1.1.0 release with /dev/null fix + 4 new features._
