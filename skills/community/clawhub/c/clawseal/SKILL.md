---
name: clawseal
description: Cryptographic memory for AI agents with QSEAL tamper-evidence. Zero-config demo mode, scroll-native YAML storage.
homepage: https://github.com/mvar-security/ClawSeal
metadata:
  openclaw:
    emoji: "🔐"
    requires:
      bins: ["python3", "curl"]
      env: []
    install:
      - id: pip
        kind: python
        package: clawseal
        bins: []
        label: "Install ClawSeal cryptographic memory system"
      - id: server
        kind: shell
        command: "clawseal verify"
        label: "Verify ClawSeal installation"
---

# ClawSeal: Cryptographic Memory for OpenClaw Agents

## What This Skill Does

ClawSeal adds persistent, tamper-evident memory to OpenClaw agents:

- **Remember user preferences** — Scrolls signed with QSEAL (HMAC-SHA256)
- **Recall with verification** — Every memory cryptographically verified on retrieval
- **Detect tampering** — Any modification breaks signature immediately
- **Zero database dependencies** — Pure YAML files, Git-friendly
- **Auto-demo mode** — Works immediately without setup (persistent secret at `~/.clawseal/demo_secret`)

## When to Use This Skill

Use ClawSeal whenever you need to:
- Remember user preferences across conversations
- Store facts/insights that should persist
- Verify memory integrity (compliance/audit scenarios)
- Track user relationship evolution

## Available Tools

### `clawseal_remember`

Store a memory with QSEAL signature.

**Usage:**
```bash
curl -X POST http://localhost:5002/remember \
  -H "Content-Type: application/json" \
  -d '{
    "content": "User prefers concise technical explanations",
    "memory_type": "preference",
    "user_id": "openclaw_user"
  }'
```

**Returns:**
```json
{
  "success": true,
  "memory_id": "MEM_20260415_abc123",
  "qseal_signature": "OXIaQboYCy5csPif7LWGz4scHZAB0YKpAPwVuXjCXLc=",
  "qseal_mode": "demo_ephemeral",
  "qseal_production": false
}
```

### `clawseal_recall`

Retrieve memories matching a query, with QSEAL verification.

**Usage:**
```bash
curl -X POST http://localhost:5002/recall \
  -H "Content-Type: application/json" \
  -d '{
    "query": "user preferences",
    "user_id": "openclaw_user",
    "limit": 5
  }'
```

**Returns:**
```json
{
  "success": true,
  "count": 2,
  "memories": [
    {
      "scroll_id": "MEM_20260415_abc123",
      "content": "User prefers concise technical explanations",
      "memory_type": "preference",
      "qseal_verified": true,
      "qseal_mode": "demo_ephemeral"
    }
  ]
}
```

### `clawseal_verify_memory`

Explicitly verify a specific memory's QSEAL signature.

**Usage:**
```bash
curl -X POST http://localhost:5002/verify \
  -H "Content-Type: application/json" \
  -d '{
    "memory_id": "MEM_20260415_abc123",
    "user_id": "openclaw_user"
  }'
```

**Returns:**
```json
{
  "valid": true,
  "memory_id": "MEM_20260415_abc123",
  "signature_verified": true,
  "content_intact": true,
  "qseal_mode": "demo_ephemeral"
}
```

## Example Conversation Flow

**User**: "Remember that I prefer detailed technical explanations with code examples"

**Agent**: "I'll store that preference in ClawSeal."

*Agent calls `clawseal_remember`:*
```bash
curl -X POST http://localhost:5002/remember \
  -d '{"content": "User prefers detailed technical explanations with code examples", "memory_type": "preference", "user_id": "openclaw_user"}'
```

**Agent**: "Stored! Memory ID: MEM_20260415_abc123 (QSEAL verified)"

---

**User** (new session): "What do you know about my preferences?"

**Agent**: "Let me recall your preferences from ClawSeal."

*Agent calls `clawseal_recall`:*
```bash
curl -X POST http://localhost:5002/recall \
  -d '{"query": "preferences", "user_id": "openclaw_user", "limit": 5}'
```

**Agent**: "I found 1 verified memory: You prefer detailed technical explanations with code examples. (QSEAL signature verified ✅)"

---

## Installation

**Automatic** (via OpenClaw):
```bash
openclaw plugins install clawseal
```

**Manual**:
```bash
# Install Python package
pip install clawseal

# Verify installation
clawseal verify

# Start server (auto-starts on port 5002)
python3 -m clawseal_openclaw.server
```

## Production Setup

**Demo mode** (default): Uses persistent secret at `~/.clawseal/demo_secret`
- ✅ Works immediately
- ⚠️ Not production-ready (ephemeral secret)

**Production mode**: Set `QSEAL_SECRET` environment variable
```bash
# Generate production secret
clawseal init

# Restart server (will detect QSEAL_SECRET)
python3 -m clawseal_openclaw.server
```

## Memory Types

- `preference` 🎯 — User preferences
- `fact` 📌 — Factual information
- `insight` ✨ — Insights/observations
- `decision` ⚖️ — Decision records
- `general` 📝 — General notes

## Security Notes

- **QSEAL signatures** — HMAC-SHA256, tamper-evident
- **Demo mode** — Persistent local secret (chmod 600), marked in artifacts
- **Production mode** — User-managed QSEAL_SECRET (rotate regularly)
- **Tampering detection** — Any modification breaks signature immediately. This memory has been permanently rejected. All other memories remain verified and intact. Your agent's integrity is protected.
