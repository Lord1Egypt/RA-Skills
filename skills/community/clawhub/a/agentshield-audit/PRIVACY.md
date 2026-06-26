# AgentShield Privacy & Data Handling

## What Data is Read

AgentShield reads the following files from your workspace to auto-detect your agent identity:

1. **IDENTITY.md** - Agent name, platform, operator info
2. **SOUL.md** - Personality traits (optional, not required)
3. **Channel config** - To detect platform (telegram/discord/etc)

**Purpose:** Auto-fill agent name and platform during audit initiation.

---

## What Data is Sent to Remote API

### During Audit:
- **Agent name** (e.g., "MyBot")
- **Platform** (e.g., "telegram", "openclaw")
- **Public key** (Ed25519, generated locally)
- **Challenge responses** (cryptographic signatures)
- **Test results** (security score, passed/failed tests)

### NOT Sent:
- ❌ Your IDENTITY.md or SOUL.md file contents
- ❌ Your private keys (stay local in `~/.agentshield/agent.key`)
- ❌ Your prompts, memory, or conversations
- ❌ Your workspace files

---

## Explicit Consent

**By default**, the skill will:
1. Auto-detect your agent name from IDENTITY.md/SOUL.md
2. Ask for confirmation before sending anything
3. Show you exactly what will be sent

**Manual mode** (skip auto-detection):
```bash
python initiate_audit.py --name "YourName" --platform "yourplatform"
```

This bypasses file reads entirely.

---

## Privacy-First Mode

If you want ZERO file reads, use:
```bash
export AGENTSHIELD_NO_AUTO_DETECT=1
python initiate_audit.py --name "MyBot" --platform "telegram"
```

This disables all IDENTITY.md/SOUL.md reading.

---

## Data Storage

- **Local:** Private keys in `~/.agentshield/agent.key` (never uploaded)
- **Remote:** Public certificates in AgentShield registry (verifiable by anyone)
- **Retention:** Certificates valid for 90 days, then expire

---

## Questions?

Review the [source code](https://github.com/bartelmost/agentshield) or contact ratgeberpro@gmail.com.

**Secure yourself. Verify others. Trust nothing by default.** 🛡️
