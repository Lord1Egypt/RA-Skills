# AgentRelay 📨

**Reliable Agent-to-Agent Communication Protocol** — Solves `sessions_send` timeout issues for large payloads using shared files + short message pointers.

---

## 🎯 Core Value

When your agents need to send messages **larger than 30 characters**, `sessions_send` can become unreliable. AgentRelay provides the solution:

| Traditional Approach | AgentRelay Approach |
|---------------------|---------------------|
| ❌ Send large text directly → ⏰ Timeout | ✅ Write to file + send short pointer → Success |
| ❌ No verification if received | ✅ Secret Code mechanism ensures delivery |
| ❌ No audit trail | ✅ Complete transaction logs (4 entries/event) |

---

## 🚀 Quick Start

### 1️⃣ Install

```bash
clawhub install agentrelay
```

### 2️⃣ Send Message

```python
from agentrelay import AgentRelayTool

# Prepare data
content = {"task": "write_poem", "theme": "spring"}

# Write to shared file and get CSV message
result = AgentRelayTool.send("agent:worker:main", "REQ", "event_001", {
    **content,
    "sender_agent": "agent:sender:main",
    "receiver_agent": "agent:worker:main",
})

# Send to target agent
sessions_send(
    target='agent:worker:main',
    message=f"AgentRelay: {result['csv_message']}"
)
```

### 3️⃣ Receive Message

```bash
# Use unified script to parse
python3 run_relay.py receive "REQ,event_001,s/event_001.json,,"
```

Output:
```json
{
  "type": "REQ",
  "event_id": "event_001",
  "content": {"task": "write_poem", ...},
  "secret": "ABC123"
}
```

### 4️⃣ Complete Task and Reply

```bash
python3 run_relay.py complete event_001 "Task completed" "agent:sender:main"
```

Output:
```
✅ Updated event_001
✅ CMP: CMP,event_001,,,ABC123
```

---

## 🔄 Complete Flow

```
Sender                          Receiver
  |                              |
  |-- 1. REQ (with file ptr) --->|
  |                              |-- receive()
  |                              |-- 📍 LOG #1: REQ/RECEIVED
  |                              |-- 📍 LOG #2: CONFIRMED
  |                              |
  |<-- 2. Implicit confirm ------|
  |                              |
  |                    [Executing task...]
  |                              |
  |<-- 3. CMP (with Secret) -----|-- cmp()
  |                              |-- 📍 LOG #3: CMP/COMPLETED
  |                              |
  |                    [Preparing for next hop]
  |                              |-- 📍 LOG #4: CREATE_POINTER/PREPARING
```

---

## 📊 Message Format

### CSV Format

```
TYPE,ID,PTR,,DATA
```

**Examples**:
```
REQ,event_001,s/event_001.json,,          # Request
CMP,event_001,,,ABC123                     # Complete (with Secret)
```

### Full Message (with prefix)

```
AgentRelay: REQ,event_001,s/event_001.json,,
```

`receive` accepts either the bare CSV string or the full prefixed message.

---

## 🔒 Security Mechanisms

### Secret Code Verification

1. Sender generates 6-character random code (e.g., `ABC123`)
2. Secret is written to file
3. Receiver must return the same Secret in CMP
4. Sender verifies Secret matches

### Burn On Read

Set `burn_on_read=true` in the event metadata or payload content to delete the shared file immediately after a successful read.

### Retention and Cleanup

Set `ttl_hours` in the payload content to override the default 24-hour retention for a specific event.

Sweep expired event files and stale registry entries with:
```bash
python3 cleanup_relay.py
```

### Complete Logging

All operations automatically logged to:
```
~/.openclaw/data/agentrelay/logs/transactions_YYYYMMDD.jsonl
```

Each record contains:
- timestamp, event_id, type, status
- sender, receiver (real agent IDs)
- next_action_plan (next step plan)

---

## 🎮 Real-World Usage

AgentRelay works best when each event declares explicit routing metadata:
- `sender_agent`
- `receiver_agent`
- optional `ttl_hours`

This keeps the protocol generic and avoids hidden assumptions about agent names.

---

## 📁 Project Structure

```
skills/agentrelay/
├── SKILL.md              # ClawHub skill documentation
├── SKILL.py              # Skill entry point
├── __init__.py           # Core implementation (AgentRelayTool)
├── run_relay.py          # Unified execution script ✨Recommended
├── cleanup_relay.py      # Expired file / registry sweeper
├── test_agentrelay.py    # Pytest regression suite
├── clawhub.json          # ClawHub manifest
└── README.md             # This document
```

---

## 🛠️ API Reference

### AgentRelayTool Class

#### send(agent_id, msg_type, event_id, content)
Send message to shared file.

**Parameters**:
- `agent_id` (str): Target agent ID
- `msg_type` (str): "REQ" or another explicit protocol type
- `event_id` (str): Unique event identifier
- `content` (dict): Message content

**Returns**:
```python
{
    "file_path": "/path/to/event_id.json",
    "ptr": "s/event_id.json",
    "csv_message": "REQ,event_id,s/event_id.json,,",
    "secret": "ABC123"
}
```

#### receive(csv_msg)
Parse and read shared file.

**Parameters**:
- `csv_msg` (str): CSV format message (without `AgentRelay:` prefix)

**Returns**:
```python
{
    "type": "REQ",
    "event_id": "event_001",
    "content": {...},
    "secret": "ABC123"
}
```

#### update(event_id, updates, next_event_id=None)
Create pointer file for next hop.

**Parameters**:
- `event_id` (str): Current event ID
- `updates` (dict): Fields to update
- `next_event_id` (str, optional): Next hop event ID

#### cmp(event_id, secret)
Generate CMP (Complete) message.

**Parameters**:
- `event_id` (str): Event ID
- `secret` (str): Secret Code

**Returns**: `str` - `"CMP,event_id,,,ABC123"`

#### verify(cmp_message)
Verify that a CMP message matches the stored secret for the event.

**Returns**:
```python
{
    "status": "ok",
    "event_id": "event_id",
    "verified": True
}
```

---

## 📌 Current Status

AgentRelay is now aligned around one protocol shape:
- explicit `sender_agent` / `receiver_agent`
- `REQ` for requests
- `CMP` for completion
- registry-backed verification and cleanup

For historical release details, see [RELEASE_NOTES.md](./RELEASE_NOTES.md).

---

## 🤝 Contributing

1. Fork this project
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) for details

---

## 📞 Contact

- **Project Homepage**: https://clawhub.ai/skills/agentrelay
- **Documentation**: https://docs.openclaw.ai/skills/agentrelay

---

**📨 Enjoy reliable agent communication!**
