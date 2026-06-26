# ClawSeal OpenClaw Demo Conversation

This is a complete agent interaction demonstrating ClawSeal's cryptographic memory capabilities in OpenClaw.

## Prerequisites

1. Install ClawSeal: `pip install clawseal`
2. Start server: `python3 backend/clawseal_server.py` (runs on port 5002)
3. Open OpenClaw CLI

---

## Conversation Flow

### Session 1: Creating Memories

**User**: "Remember that I prefer concise technical explanations without marketing jargon"

**Agent**: *Internally reasons: I should store this preference in ClawSeal*

**Agent Action** (via curl):
```bash
curl -X POST http://localhost:5002/remember \
  -H "Content-Type: application/json" \
  -d '{
    "content": "User prefers concise technical explanations without marketing jargon",
    "memory_type": "preference",
    "user_id": "openclaw_demo"
  }'
```

**Server Response**:
```json
{
  "success": true,
  "memory_id": "MEM_20260415_a1b2c3",
  "qseal_signature": "OXIaQboYCy5csPif7LWGz4scHZAB0YKpAPwVuXjCXLc=",
  "qseal_mode": "demo_ephemeral",
  "qseal_production": false
}
```

**Agent**: "Stored your preference! Memory ID: MEM_20260415_a1b2c3 (QSEAL verified ✅)"

---

**User**: "Also remember that I'm working on an AI agent security project using MVAR and ClawSeal"

**Agent Action**:
```bash
curl -X POST http://localhost:5002/remember \
  -d '{
    "content": "User is working on an AI agent security project using MVAR and ClawSeal",
    "memory_type": "fact",
    "user_id": "openclaw_demo"
  }'
```

**Server Response**:
```json
{
  "success": true,
  "memory_id": "MEM_20260415_d4e5f6",
  "qseal_signature": "xyz789...",
  "qseal_mode": "demo_ephemeral",
  "qseal_production": false
}
```

**Agent**: "Got it! Stored as fact: MEM_20260415_d4e5f6 (QSEAL verified ✅)"

---

### Session 2: Recalling Memories (New Conversation)

**User**: "What do you know about my preferences?"

**Agent**: *Internally: Let me recall user preferences from ClawSeal*

**Agent Action**:
```bash
curl -X POST http://localhost:5002/recall \
  -d '{
    "query": "preferences",
    "user_id": "openclaw_demo",
    "limit": 5
  }'
```

**Server Response**:
```json
{
  "success": true,
  "count": 1,
  "memories": [
    {
      "scroll_id": "MEM_20260415_a1b2c3",
      "content": "User prefers concise technical explanations without marketing jargon",
      "memory_type": "preference",
      "qseal_verified": true,
      "qseal_mode": "demo_ephemeral",
      "glyph": "🎯"
    }
  ]
}
```

**Agent**: "I found 1 verified memory about your preferences: You prefer concise technical explanations without marketing jargon. (QSEAL signature verified ✅)"

---

**User**: "What project am I working on?"

**Agent Action**:
```bash
curl -X POST http://localhost:5002/recall \
  -d '{
    "query": "project working",
    "user_id": "openclaw_demo",
    "limit": 5
  }'
```

**Server Response**:
```json
{
  "success": true,
  "count": 1,
  "memories": [
    {
      "scroll_id": "MEM_20260415_d4e5f6",
      "content": "User is working on an AI agent security project using MVAR and ClawSeal",
      "memory_type": "fact",
      "qseal_verified": true,
      "qseal_mode": "demo_ephemeral",
      "glyph": "📌"
    }
  ]
}
```

**Agent**: "You're working on an AI agent security project using MVAR and ClawSeal. (QSEAL verified ✅)"

---

### Session 3: Tampering Detection Demo

**User**: "Can you verify the integrity of memory MEM_20260415_a1b2c3?"

**Agent Action**:
```bash
curl -X POST http://localhost:5002/verify \
  -d '{
    "memory_id": "MEM_20260415_a1b2c3",
    "user_id": "openclaw_demo"
  }'
```

**Server Response**:
```json
{
  "valid": true,
  "memory_id": "MEM_20260415_a1b2c3",
  "signature_verified": true,
  "content_intact": true,
  "qseal_mode": "demo_ephemeral"
}
```

**Agent**: "Memory MEM_20260415_a1b2c3 verified ✅ — Signature valid, content intact, no tampering detected."

---

**Tampering Simulation** (manual):
```bash
# Manually edit the YAML file to corrupt content
# Change "concise" to "verbose" in MEM_20260415_a1b2c3.yaml
```

**User**: "Verify that memory again"

**Agent Action**: (same curl command as before)

**Server Response**:
```json
{
  "valid": false,
  "memory_id": "MEM_20260415_a1b2c3",
  "signature_verified": false,
  "content_intact": false,
  "error": "QSEAL signature mismatch — content has been tampered with"
}
```

**Agent**: "⚠️ TAMPERING DETECTED! Memory MEM_20260415_a1b2c3 has been modified after signing. QSEAL signature verification failed. This memory has been permanently rejected. All other memories remain verified and intact. Your agent's integrity is protected."

---

## Key Demonstration Points

1. ✅ **Zero-config memory persistence** — Works immediately, no setup
2. ✅ **Cryptographic verification** — Every memory QSEAL-signed (HMAC-SHA256)
3. ✅ **Tampering detection** — Any modification breaks signature
4. ✅ **OpenClaw-native** — Uses standard curl/JSON, no special integration
5. ✅ **Production-ready** — Demo mode → production via `QSEAL_SECRET` env var

---

## Video Recording Script

**Scene 1**: Install + Start (15s)
```bash
pip install clawseal
python3 backend/clawseal_server.py
# Show: "ClawSeal OpenClaw Server starting on 127.0.0.1:5002"
```

**Scene 2**: Store memories (30s)
- User: "Remember I prefer concise explanations"
- Agent stores, shows memory ID + QSEAL signature

**Scene 3**: Recall memories (new session) (30s)
- User: "What are my preferences?"
- Agent recalls, shows verified memories

**Scene 4**: Tampering detection (30s)
- Verify memory (✅ valid)
- Manually tamper with YAML file
- Verify again (❌ tampered)
- Show integrity protection message

**Total runtime**: ~2 minutes
