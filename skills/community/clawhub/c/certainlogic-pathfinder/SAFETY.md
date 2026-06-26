# Safety & Security Disclosure

**Agent Pathfinder** — Transparent security practices for users and auditors.

**Last updated:** 2026-04-27
**Version:** 1.2.7
**License:** MIT-0

---

## What This Tool Does

AgentPathfinder tracks AI agent task completion using **cryptographic sharding**: splitting a random 256-bit key into pieces (shards) across task steps. Only when all steps report success can the original key be reconstructed. This provides machine-verifiable proof that every required step finished.

This is **not encryption of user data**. It is a tamper-evident coordination mechanism for task workflow state.

---

## What Data Is Stored

**All data stays in `~/.agentpathfinder/` only.** No external servers, no telemetry, no analytics.

| Data | Location | Content | Purpose |
|------|----------|---------|---------|
| Task metadata | `~/.agentpathfinder/tasks/*.json` | Task name, step names, UUID, timestamps | Track what tasks exist and their state |
| Vault shards | `~/.agentpathfinder/vault/*.shard` | One 32-byte random shard per step + 1 recovery shard | Cryptographic proof—only reconstructable when all steps pass |
| Audit trail | `~/.agentpathfinder/audit/*.jsonl` | Timestamps, step results, HMAC signatures | Tamper-evident log of what happened |
| Agent config | `~/.agentpathfinder/agents/registry.json` | Agent name, shared secret for HMAC (if configured) | Authenticate which agent performed which step |

**No user data, credentials, source code, or external data is ever read, transmitted, or stored.**

### Network Access

| Feature | Network? | Data Sent |
|---------|----------|-----------|
| Local CLI (`pf create`, `pf run`, `pf status`) | ❌ None | Nothing |
| Static dashboard (`pf dashboard --output`) | ❌ None | Nothing |
| Live dashboard (`pf dashboard --live`) | ⚠️ Localhost only | Serves HTML on `127.0.0.1:5000` — no external network |
| Pro tier (coming) | ✅ Yes (future) | Encrypted shard upload to hosted vault (opt-in) |

**The free tier is entirely offline.** No telemetry, no analytics, no phone home.

---

## Cryptographic Details

### Key Generation
```python
# Pseudocode
master_key = secrets.token_bytes(32)  # 256-bit random from OS CSPRNG
shards = xor_split(master_key, n_steps + 1)  # N+1 shards
```
- Uses Python `secrets` module (OS-level `/dev/urandom` or CryptGenRandom)
- No seed, no password, no derivation from user data
- Keys are ephemeral—they exist only for the lifetime of a task

### Sharding (XOR-Based Secret Sharing)
```python
# Pseudocode
shards = [random_bytes(32) for _ in range(n)]
shards[-1] = xor_all(shards[:-1]) ^ master_key
# Reconstruct: master_key = xor_all(shards)
```
- Information-theoretically secure when all shards required
- No single shard leaks information about the master key
- Not threshold scheme—ALL shards required (by design)

### Audit Signing
```python
# Pseudocode
audit_key = hmac_sha256(master_key, b"audit-derivation")
signature = hmac_sha256(audit_key, event_bytes)
```
- HMAC-SHA256 with derived key
- Any tampering with audit log invalidates the signature chain

---

## Why Security Scanners May Flag This Code

Automated security scanners may flag this code because it contains patterns commonly associated with malware:

| Pattern | Why Scanners Flag It | Why It's Safe Here |
|---------|---------------------|-------------------|
| `secrets.token_bytes(32)` | Could be ransomware key generation | Generates ephemeral task coordination keys, not encryption keys |
| `hmac.new(key, ...).hexdigest()` | Could be credential hashing/exfiltration | Signs local audit events only, no data leaves machine |
| `open(..., 'wb').write(data)` | Could be encrypting user files | Writes tiny JSON/shard files to dedicated `~/.agentpathfinder/` directory only |
| `hashlib.sha256()` | Could be password cracking | Used only for HMAC derivation and integrity checks |

**This is a false positive.** The code is open source, auditable, and does nothing hidden.

---

## Tamper Model (What We Protect Against)

### What Is Protected
- ✅ Accidental data corruption (atomic writes + fsync)
- ✅ Audit log tampering (HMAC signatures)
- ⚠️ Malicious agent on same filesystem (detectable, not preventable)

### What Is NOT Protected
- ❌ Root/admin with filesystem access can read vault shards and reconstruct keys
- ❌ No protection against compromised operating system
- ❌ Not a replacement for sandboxing or container security

### Honest Assessment
> **"Tamper-evident, not tamper-proof."**
>
> A malicious agent with filesystem access to `~/.agentpathfinder/vault/` can read shards and reconstruct keys. The audit trail will show this happened (detectable), but cannot prevent it.
>
> **Mitigations:**
> - Pro tier (coming): Hosted remote vault—agents never see raw shards
> - Enterprise: TEE/remote attestation for vault isolation
> - Free tier: Accept filesystem-trust assumption (same as ssh keys, API tokens, etc.)

---

## Permissions Required

| Operation | Permission | Why |
|-----------|-----------|-----|
| Install | Write to `~/.agentpathfinder/` | Create task vault and audit directories |
| Create task | Write to `~/.agentpathfinder/tasks/` and `~/.agentpathfinder/vault/` | Store task metadata and shards |
| Run step | Read/write task file + write audit | Update step state and append to audit log |
| Verify audit | Read audit file | Check HMAC signatures |
| Dashboard | Read all of above | Aggregate and display status |

**No root/admin required.** No access to user files outside `~/.agentpathfinder/`.

---

## How to Verify Safety

### 1. Inspect All Files
```bash
# See exactly what data is stored
ls -la ~/.agentpathfinder/
# View any file—it's all plaintext JSON
```

### 2. Read the Source
```bash
# All code is open source
clawhub inspect agentpathfinder
# or
cat $(python3 -c "import agentpathfinder; print(agentpathfinder.__file__)")
```

### 3. Run Without Install
```bash
# Test in isolated environment
python3 -m venv /tmp/pf_test
source /tmp/pf_test/bin/activate
pip install agentpathfinder
pf create "test" "step1" "step2"
pf status <task_id>
# Inspect ~/.agentpathfinder/ to see exactly what was written
```

### 4. Checksum Verification
All releases are published to GitHub with commit signatures:
- Repo: `https://github.com/CertainLogicAI/agentpathfinder`
- Every commit is signed and auditable

---

## Critical Limitations

### The Audit Trail Cannot Detect a Compromised Agent

AgentPathfinder's audit trail uses HMAC-SHA256 signatures to detect **unauthorized tampering** — edits made by someone who does NOT have the signing key.

However, if an AI agent (or any process) running on the same machine reads the vault shards from `~/.agentpathfinder/vault/`, it can:

1. Reconstruct the master key (all shards are present in the vault)
2. Derive the audit signing key from the master key
3. Create forged audit entries with valid HMAC signatures
4. The `pf audit` command will report these forged entries as valid

**This is a fundamental limitation, not a bug. The audit trail proves "someone with the key signed this" — it does not prove "the agent's claim is true."**

**To protect against this:**
- Run agents in isolated environments where they cannot access `~/.agentpathfinder/`
- Use separate system users: the agent runs as user `agent`, the vault is owned by user `pathfinder` with `chmod 700`
- For production use, wait for the **Pro hosted vault** (separate server, no filesystem access) or **Enterprise TEE** (hardware-isolated execution)
- Always independently verify claimed results using outside checks (CI/CD status, HTTP health endpoints, artifact hashes)

### No Automatic Verification of Truth

AgentPathfinder records and signs claims. It does NOT verify the content of those claims. If an agent claims it completed step 5 but actually skipped it, the system will record a valid "STEP_COMPLETE" event for step 5.

**Verification is always the user's responsibility.**

---

## Responsible Disclosure

Found a security issue? Contact us before going public.

- **Email:** security@certainlogic.ai *(preferred)*
- **GitHub:** Open a private security advisory at `github.com/CertainLogicAI/agentpathfinder/security/advisories`
- **Response time:** Within 48 hours

---

## Compliance Notes

| Standard | Status | Notes |
|----------|--------|-------|
| GDPR | ✅ Compliant | No PII collected, no data leaves machine |
| CCPA | ✅ Compliant | No personal data processing |
| SOC 2 | ⚠️ N/A (free tier) | Type II available for Enterprise |

---

**Trust through transparency.** If something here is unclear, open an issue and we'll fix it.
