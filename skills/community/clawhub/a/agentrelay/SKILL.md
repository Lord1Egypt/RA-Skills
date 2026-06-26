---
name: agentrelay
description: Reliable agent-to-agent communication protocol for transferring large payloads via shared files with pointer references and secret code verification. Triggered by explicit 'AgentRelay:' prefix in messages.
license: MIT
metadata: {"openclaw":{"triggerPatterns":["AgentRelay:","Please use AgentRelay skill to handle","Use AgentRelay"],"emoji":"📨"}}
---

# AgentRelay 📨

**Reliable Agent-to-Agent Communication Protocol** — Solves `sessions_send` timeout issues for large payloads using shared files + short message pointers.

## 🎯 When to Use This Skill

**When you see messages like the following**, immediately use this Skill to handle:

```
Please use AgentRelay skill to handle this message:
REQ,event_001,s/event_001.json,,
```

Or

```
📨 AgentRelay Protocol Message

Please use AgentRelay skill to handle:
- Message Type: REQ
- Event ID: event_001
- File Pointer: s/event_001.json
```

**Key Trigger Phrases**:
- "use AgentRelay skill to handle"
- "AgentRelay protocol message"
- "Use AgentRelay"

When you see these keywords, **immediately execute the Commands below**!

## 🚀 Quick Start

### Standard Flow After Receiving AgentRelay Message

**Step 1: Parse Message**
```bash
python3 {baseDir}/run_relay.py receive "REQ,event_001,s/event_001.json,,"
```

Example output:
```json
{
  "type": "REQ",
  "event_id": "event_001",
  "content": {
    "task": "write_poem",
    "sender_agent": "agent:sender:main",
    "receiver_agent": "agent:worker:main"
  },
  "secret": "ABC123"
}
```

**Step 2: Understand Task and Execute**

Check the `content` field to understand what needs to be done (e.g., write poem, analyze data, generate report).

**Step 3: Update Result**
```bash
python3 {baseDir}/run_relay.py complete event_001 "Task completed" "agent:sender:main"
```

**Step 4: Send CMP Confirmation**
```bash
# generate CMP message (done automatically by run_relay.py complete)
# Output: CMP,event_001,,,ABC123
# Then send via sessions_send
sessions_send(target='agent:sender:main', message='CMP,event_001,,,ABC123')
```

---

## 📚 Commands

### `receive <csv_message>`

Parse AgentRelay CSV message and read shared file content.
Accepts either bare CSV or a full message with the `AgentRelay:` prefix.

**Parameters**:
- `csv_message`: CSV format message (without `AgentRelay:` prefix)

**Example**:
```bash
python3 {baseDir}/run_relay.py receive "REQ,event_001,s/event_001.json,,"
```

**Output** (JSON):
```json
{
  "type": "REQ",
  "event_id": "event_001",
  "ptr": "s/event_001.json",
  "content": {...},
  "secret": "ABC123"
}
```

---

### `update <event_id> <json_updates> [next_event_id]`

Update shared file content.

**Parameters**:
- `event_id`: Event ID
- `json_updates`: JSON format updates (merged into `payload.content`)

**Example**:
```bash
python3 {baseDir}/run_relay.py update event_001 '{"status":"completed","result":"done"}'
```

**Output**:
```json
{"status":"ok","file":"/path/to/event_001.json","ptr":"s/event_001.json"}
```

---

### `cmp <event_id> [secret]`

Generate CMP confirmation message.

**Parameters**:
- `event_id`: Event ID
- `secret`: Secret Code read from file

**Example**:
```bash
python3 {baseDir}/run_relay.py cmp event_001 ABC123
```

**Output**:
```json
{
  "status": "ok",
  "cmp_message": "CMP,event_001,,,ABC123",
  "instruction": "Call sessions_send with message='CMP,event_001,,,ABC123'"
}
```

---

### `verify <cmp_message>`

Verify that a received `CMP` message matches the secret stored in the event file.

**Example**:
```bash
python3 {baseDir}/run_relay.py verify "CMP,event_001,,,ABC123"
```

**Output**:
```json
{
  "status": "ok",
  "event_id": "event_001",
  "verified": true
}
```

---

## 🔄 Complete Communication Flow

### Sender Agent

```python
# 1. Prepare data
content = {
    "task": "write_poem",
    "sender_agent": "agent:sender:main",
    "receiver_agent": "agent:worker:main"
}

# 2. Write to shared file
from agentrelay import agentrelay_send
result = agentrelay_send("agent:worker:main", "REQ", "event_001", content)

# 3. Send message with prefix
message = f"AgentRelay: {result['csv_message']}"
sessions_send(target='agent:worker:main', message=message)
```

### Receiver Agent

```bash
# 1. Receive message: AgentRelay: REQ,event_001,s/event_001.json,,

# 2. Parse message
python3 {baseDir}/run_relay.py receive "REQ,event_001,s/event_001.json,,"
# → Get content and secret

# 3. Understand task, call LLM to execute
# (This is your LLM capability)

# 4. Update result
python3 {baseDir}/run_relay.py update event_001 '{"status":"completed"}'

# 5. Send CMP
CMP_OUTPUT=$(python3 {baseDir}/run_relay.py cmp event_001 SECRET)
CMP_MSG=$(echo "$CMP_OUTPUT" | jq -r '.cmp_message')
sessions_send(target='agent:sender:main', message="$CMP_MSG")
```

---

## 📊 Message Format Details

### CSV Format

```
TYPE,ID,PTR,,DATA
```

**Field Descriptions**:
- `TYPE`: Message type (REQ | CMP)
- `ID`: Event ID (unique identifier)
- `PTR`: File pointer (e.g., `s/event_id.json`)
- `RESERVED`: Reserved field (leave empty)
- `DATA`: Additional data (Secret Code for CMP)

**Examples**:
```
REQ,event_001,s/event_001.json,,  # Request
CMP,event_001,,,ABC123            # Completion confirmation
```

### Full Message (with prefix)

```
AgentRelay: REQ,event_001,s/event_001.json,,
```

**Why need prefix?**
- ✅ Clearly identifies this as AgentRelay protocol message
- ✅ LLM immediately knows to call AgentRelay Skill when seeing it
- ✅ Avoids confusion with other messages

---

## 🛡️ Security Mechanisms

### 1. Secret Code Verification

- Sender generates 6-character random code (e.g., `ABC123`)
- Secret is written to file
- Receiver must return the same Secret when sending CMP
- Sender verifies Secret matches, ensuring receiver actually read the file

### 2. Burn-on-read (Optional)

When `burn_on_read=true` is set in `meta` or `payload.content`, the file is automatically deleted after reading to protect sensitive data.

## 📁 Data Storage

- **Shared Files**: `~/.openclaw/data/agentrelay/storage/*.json`
- **Transaction Logs**: `~/.openclaw/data/agentrelay/logs/transactions_*.jsonl`
- **Registry**: `~/.openclaw/data/agentrelay/registry.json`

---

## 🧪 Testing and Examples

### Smoke Test
```bash
python3 {baseDir}/smoke_test.py
```

### Pytest Regression Suite
```bash
pytest {baseDir}/test_agentrelay.py
```

### Cleanup Expired Events
```bash
python3 {baseDir}/cleanup_relay.py
```

### Verify a CMP
```bash
python3 {baseDir}/run_relay.py verify "CMP,r1_r,,,ABC123"
```

---

## ❓ FAQ

### Q: Why use AgentRelay instead of direct sessions_send?

A: `sessions_send` tends to timeout when transmitting messages larger than 30 characters. AgentRelay uses shared files + short pointers (less than 30 characters) to transmit arbitrarily large data.

### Q: What is Secret Code for?

A: Secret Code is a 6-character random code used to verify the receiver actually read the file. Receiver must return the correct Secret in CMP, and sender can verify it with `verify`.

### Q: How long are files retained?

A: Files are retained for 24 hours by default. You can adjust this with `ttl_hours`, enable `burn_on_read` to delete immediately after reading, and run `cleanup_relay.py` to sweep expired files and old registry entries.

---

## 📖 More Documentation

- [README.md](/Users/gavinliu/.openclaw/workspace/skills/agentrelay/README.md) - Project overview
- [RELEASE_NOTES.md](/Users/gavinliu/.openclaw/workspace/skills/agentrelay/RELEASE_NOTES.md) - Release notes

---

**Version**: v1.1.0
**Last Updated**: 2026-02-28  
**Author**: AgentRelay Team  
**Maintainer**: AgentRelay Team
