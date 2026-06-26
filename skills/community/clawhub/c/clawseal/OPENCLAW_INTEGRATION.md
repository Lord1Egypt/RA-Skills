# ClawSeal + OpenClaw: Integration Guide

**One-page guide for OpenClaw users: Why you need ClawSeal, how it works with your existing memory setup, and how to add it in under 5 minutes.**

---

## The Problem OpenClaw Has (And Doesn't Know It)

**OpenClaw agents are stateless between conversations.**

Every time you start a new session:
- Agent forgets your preferences
- No memory of past decisions
- Zero continuity across conversations
- Complete amnesia = 100% identity drift

**You've probably experienced this:**
- "User prefers concise explanations" → Forgotten next session
- "Working on AI security project" → Lost forever
- "Don't use marketing jargon" → Agent uses it anyway next time

**This is not a bug. This is the default state of LLM-based agents.**

---

## What ClawSeal Fixes

ClawSeal adds **persistent, cryptographically-verified memory** to OpenClaw:

1. **Remember user preferences** — Agent stores memories across sessions
2. **QSEAL cryptographic signatures** — Every memory signed with HMAC-SHA256
3. **Tamper detection** — Any modification breaks signature immediately
4. **Zero database dependencies** — Pure YAML files, Git-friendly
5. **Auto-demo mode** — Works immediately without setup

**Result**: Your OpenClaw agent remembers you. Forever. With cryptographic proof.

---

## How It Works with OpenClaw's Existing Memory

**OpenClaw's memory** (if it has any): Ephemeral, session-scoped, no verification.

**ClawSeal's memory**: Persistent, cryptographically signed, tamper-evident.

**They work together:**
- **Short-term memory** → OpenClaw (conversation context, current session)
- **Long-term memory** → ClawSeal (user preferences, facts, decisions across sessions)

**ClawSeal does NOT replace OpenClaw's memory.** It extends it.

Think of it as:
- **OpenClaw** = RAM (fast, temporary)
- **ClawSeal** = Hard drive (persistent, verified)

---

## Installation (Under 5 Minutes)

### Step 1: Install ClawSeal

```bash
# From the clawseal-openclaw-plugin directory
bash install.sh
```

**What this does:**
1. Installs `clawseal` Python package from PyPI
2. Installs Flask server dependencies
3. Registers auto-start daemon (launchd on macOS, systemd on Linux)
4. Starts server on port 5002

**Total time**: ~2 minutes

### Step 2: Verify Server is Running

```bash
curl http://localhost:5002/health
# {"status": "ok", "service": "clawseal-openclaw-server"}
```

**If this works, you're done.** ClawSeal is now available to all OpenClaw agents.

### Step 3: Test with OpenClaw Agent

In your next OpenClaw conversation, try:

**User**: "Remember that I prefer concise technical explanations without marketing jargon"

**Agent** (if ClawSeal-aware): Stores this in ClawSeal with QSEAL signature.

**Next session, new conversation:**

**User**: "What do you know about my preferences?"

**Agent**: Recalls from ClawSeal, shows verified memory.

---

## How OpenClaw Agents Use ClawSeal

**Three simple curl commands:**

### 1. Store a memory

```bash
curl -X POST http://localhost:5002/remember \
  -H "Content-Type: application/json" \
  -d '{
    "content": "User prefers concise explanations",
    "memory_type": "preference",
    "user_id": "openclaw_user"
  }'
```

**Returns**:
```json
{
  "success": true,
  "memory_id": "MEM_20260415_abc123",
  "qseal_signature": "OXIaQboYCy5csPif7LWGz4scHZAB0YKpAPwVuXjCXLc=",
  "qseal_mode": "demo_ephemeral"
}
```

### 2. Recall memories

```bash
curl -X POST http://localhost:5002/recall \
  -H "Content-Type: application/json" \
  -d '{
    "query": "preferences",
    "user_id": "openclaw_user",
    "limit": 5
  }'
```

**Returns**:
```json
{
  "success": true,
  "count": 1,
  "memories": [
    {
      "scroll_id": "MEM_20260415_abc123",
      "content": "User prefers concise explanations",
      "memory_type": "preference",
      "qseal_verified": true
    }
  ]
}
```

### 3. Verify integrity

```bash
curl -X POST http://localhost:5002/verify \
  -H "Content-Type: application/json" \
  -d '{
    "memory_id": "MEM_20260415_abc123",
    "user_id": "openclaw_user"
  }'
```

**Returns**:
```json
{
  "valid": true,
  "signature_verified": true,
  "content_intact": true
}
```

---

## Memory Types

ClawSeal supports 5 memory types:

- `preference` 🎯 — User preferences (how they like info presented)
- `fact` 📌 — Factual information (user is working on X project)
- `insight` ✨ — Observations/insights (user responds well to Y approach)
- `decision` ⚖️ — Decision records (user chose Z option)
- `general` 📝 — General notes (anything else)

**Use the right type for the right memory.** This helps with retrieval relevance.

---

## Demo Mode vs Production Mode

### Demo Mode (Default)

**How it works:**
- Auto-generates persistent secret at `~/.clawseal/demo_secret` (chmod 600)
- All memories marked with `"qseal_mode": "demo_ephemeral"`
- Works immediately, zero config

**Use for:**
- Testing ClawSeal
- Development
- Demos/videos

**NOT for:**
- Production deployments
- Compliance scenarios (HIPAA, SOC2, etc.)

### Production Mode

**How to enable:**
```bash
# Generate production QSEAL_SECRET
clawseal init

# Restart server (will detect env var)
# macOS:
launchctl unload ~/Library/LaunchAgents/com.mvar.clawseal.plist
launchctl load ~/Library/LaunchAgents/com.mvar.clawseal.plist

# Linux:
systemctl --user restart clawseal-server
```

**What changes:**
- Memories marked with `"qseal_mode": "production"`
- Secret managed by you (rotate regularly)
- Suitable for production deployments

---

## Why OpenClaw Users Need This

### Without ClawSeal

- ❌ Agent forgets preferences every session
- ❌ No memory of past decisions
- ❌ Zero continuity across conversations
- ❌ No way to verify memory integrity
- ❌ Complete amnesia between sessions

### With ClawSeal

- ✅ Agent remembers preferences forever
- ✅ Persistent memory of facts/decisions
- ✅ Full continuity across all conversations
- ✅ Cryptographic proof of memory integrity (HMAC-SHA256)
- ✅ Tamper detection (any modification breaks signature)

**Bottom line**: ClawSeal transforms OpenClaw from **stateless chat bot** to **persistent AI assistant**.

---

## Security & Compliance

### What ClawSeal Provides

- **Tamper-evidence**: HMAC-SHA256 signatures on every memory
- **Auditable**: Memories stored as human-readable YAML with signatures
- **Verifiable**: Anyone with QSEAL_SECRET can verify integrity
- **Fail-closed**: Missing secret = hard error (no silent fallbacks)

### What It's Good For

- ✅ Detecting unauthorized memory modifications
- ✅ Compliance audit trails (HIPAA, SOC2 if in production mode)
- ✅ Preventing memory drift/corruption
- ✅ Cryptographic proof of agent behavior

### What It's NOT

- ❌ Protection against secret theft (if attacker has QSEAL_SECRET, they can forge)
- ❌ Network-level security (use HTTPS for remote deployments)
- ❌ Multi-party verification (single shared secret model)

**For most OpenClaw users**: Demo mode is sufficient for personal/development use. Production mode required for compliance scenarios.

---

## Common Questions

### Does ClawSeal replace OpenClaw's memory?

**No.** ClawSeal extends it. Think of OpenClaw's memory as RAM (fast, temporary) and ClawSeal as a hard drive (persistent, verified).

### Do I need to change my OpenClaw setup?

**No.** ClawSeal runs as a separate HTTP service. OpenClaw agents call it via standard `curl` commands.

### What if the server crashes?

**It auto-restarts.** The installation script registers ClawSeal as a system service (launchd on macOS, systemd on Linux) that restarts on failure.

### Can I use this with multiple agents?

**Yes.** Use different `user_id` values to isolate memories per agent.

### What happens if I manually edit a YAML file?

**Signature breaks immediately.** Next recall/verify will detect tampering and reject the memory. This is by design.

### Can I migrate from demo mode to production mode?

**Yes.** Generate a production secret (`clawseal init`), restart the server. Existing demo-mode memories remain but are marked as `demo_ephemeral`.

---

## Next Steps

1. **Install ClawSeal** — `bash install.sh` (2 minutes)
2. **Test health** — `curl http://localhost:5002/health`
3. **Run demo** — Follow [demo_conversation.md](demo_conversation.md) (2 minutes)
4. **Integrate with OpenClaw** — Add curl calls to your agent workflows
5. **Record video** — Show off ClawSeal's tampering detection

---

## Links

- **ClawSeal on PyPI**: https://pypi.org/project/clawseal/
- **GitHub**: https://github.com/mvar-security/ClawSeal
- **Issues/Support**: https://github.com/mvar-security/ClawSeal/issues

---

**This guide is designed to be linked in:**
- OpenClaw GitHub issues/discussions
- OpenClaw ecosystem documentation
- HN/Reddit comments about OpenClaw
- Your demo videos

**One page. Five minutes. Cryptographically-verified memory for OpenClaw agents.**

Install it. Use it. Share it.
