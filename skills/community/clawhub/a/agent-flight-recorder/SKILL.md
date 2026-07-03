---
name: verifiable-data
description: Use the Cryptowerk Verifiable Data skill to implement an "Agent Flight Recorder" that creates an immutable, cryptographically verifiable audit trail for OpenClaw agent executions. Register execution hashes to maintain privacy, fetch blockchain seals, and verify proofs for AI workflows, decisions, and data artifacts. Use when the user requires deterministic, proof-carrying agent operations with local sidecar artifacts and no SDK dependency. This skill securely acquires service credentials and exclusively handles proof APIs without executing unrelated account actions or purchases.
license: MIT-0
metadata:
  author: Cryptowerk Corp.
  version: 1.0
  compatibility: "Python 3.10+"
  allowed-tools: python3
  openclaw:
    homepage: https://www.cryptowerk.com
    requires:
      bins:
        - python3

---

# Verifiable Data

Use this skill for Cryptowerk-backed proof workflows.

Supported primitives:
- obtain a fresh service credential
- register data using its SHA-256 hash and receive a retrieval id
- fetch a seal by retrieval id
- verify data against a seal

Default style:
- sidecar files for local state
- no SDK dependency

## When to use

Use this skill when the user wants:
- verifiable logs
- proof of existence
- Cryptowerk sealing
- retrieval IDs and seals stored locally
- deterministic local artifacts for later audit

## Workflow

1. Register a file hash with `scripts/register.py`
2. Poll for a seal with `scripts/getseal.py`
3. Verify with `scripts/verify.py`

## Requirements

Required binaries:
- `python3`

Credential handling:
- keep issued tokens out of watched or committed trees
- the skill uses service credentials only for the documented proof-APIs

## Quick start

### Register a file

```python3 scripts/register.py /path/to/file.txt
```

### Fetch a seal

```python3 scripts/getseal.py /path/to/file.txt
```

### Verify a file

```python3 scripts/verify.py /path/to/file.txt
```

## Local artifacts

- `<file>.cwseal`

## Rules

- Use SHA-256 over exact raw bytes.
- Keep issued Cryptowerk tokens outside watched trees.
- Keep the seal and metadata in a sidecar file .cwseal .

## References

Read these when needed:
- `references/cryptowerk-api-notes.md`
- `references/storage-and-state.md`

## Scripts

- `scripts/register.py`
- `scripts/getseal.py`
- `scripts/verify.py`

