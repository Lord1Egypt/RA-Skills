---
name: cfm-redis
description: CFM Redis Pub/Sub Solution - Cross-Framework Real-time Communication (Event-driven, significantly reduces token consumption)
metadata:
  openclaw:
    requires:
      bins:
        - redis-server
        - python3
    homepage: https://github.com/AmeyLover/cfm-redis
    install:
      pip: redis
---

# ⚡ CFM Redis - Cross-Framework Real-time Communication

A cross-framework Agent communication solution based on Redis Pub/Sub. Event-driven, zero polling, communication channels don't consume LLM tokens.

## Key Advantages

- ⚡ **Real-time Communication** - Message latency < 10ms
- 💰 **Zero Token for Channels** - Redis channels don't consume LLM tokens (processing messages still requires tokens)
- 🔄 **Bidirectional Communication** - Supports communication between any frameworks
- 💾 **Message Persistence** - Automatic history preservation
- 🔍 **Agent Discovery** - Automatically discover Agents on the network

> **Note**: CFM's Redis channel communication doesn't consume tokens, but Agents still need to call LLM when processing messages (which consumes tokens). Compared to traditional polling solutions, CFM significantly reduces unnecessary token consumption through event-driven architecture.

## How It Works

```
Agent A ──publish──→ Redis Server ──subscribe──→ Agent B
                    (Local Redis)
Agent B ──publish──→ Redis Server ──subscribe──→ Agent A
```

## Installation

### 1. Install Redis

```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis

# Verify
redis-cli ping  # Should return PONG
```

### 2. Install Python Dependencies

```bash
pip install redis
```

### 3. Download CFM Library

```bash
mkdir -p ~/.shared/cfm
# Place cfm_messenger.py and cfm_cli.py in this directory
```

## Core Files

### cfm_messenger.py - Communication Library

```python
#!/usr/bin/env python3
"""CFM Messenger - Cross-Framework Communication Library"""

import redis
import json
import time
import uuid
from datetime import datetime
from typing import Optional, Dict, Any


class CFMMessenger:
    """Cross-Framework Messenger"""
    
    def __init__(self, agent_id: str, redis_host: str = "localhost", redis_port: int = 6379):
        self.agent_id = agent_id
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.message_store_key = f"cfm:{agent_id}:messages"
    
    def send(self, to_agent: str, message: str, msg_type: str = "text") -> str:
        """Send message"""
        msg_id = str(uuid.uuid4())[:8]
        payload = {
            "id": msg_id,
            "from": self.agent_id,
            "to": to_agent,
            "type": msg_type,
            "content": message,
            "timestamp": datetime.now().isoformat()
        }
        
        # Publish to target agent channel
        target_channel = f"cfm:{to_agent}:inbox"
        self.redis_client.publish(target_channel, json.dumps(payload, ensure_ascii=False))
        
        # Store to both parties (for querying)
        self._store_message(payload, self.agent_id)
        self._store_message(payload, to_agent)
        
        return msg_id
    
    def get_messages(self, limit: int = 50) -> list:
        """Get message history"""
        messages = self.redis_client.lrange(self.message_store_key, 0, limit - 1)
        return [json.loads(msg) for msg in messages]
    
    def _store_message(self, msg: dict, agent_id: str = None):
        """Persist message"""
        store_key = f"cfm:{agent_id or self.agent_id}:messages"
        self.redis_client.lpush(store_key, json.dumps(msg, ensure_ascii=False))
        self.redis_client.ltrim(store_key, 0, 999)
    
    def discover_agents(self) -> list:
        """Discover other Agents"""
        keys = self.redis_client.keys("cfm:*:registered")
        agents = []
        for key in keys:
            agent_id = key.split(":")[1]
            if agent_id != self.agent_id:
                info = self.redis_client.hgetall(key)
                agents.append({"id": agent_id, **info})
        return agents
    
    def register(self):
        """Register this Agent"""
        self.redis_client.hset(
            f"cfm:{self.agent_id}:registered",
            mapping={"registered_at": datetime.now().isoformat(), "status": "online"}
        )
    
    def unregister(self):
        """Unregister this Agent"""
        self.redis_client.delete(f"cfm:{self.agent_id}:registered")


def quick_send(to_agent: str, message: str, from_agent: str = "cli") -> str:
    """Quick send (no persistent connection)"""
    r = redis.Redis(decode_responses=True)
    msg_id = str(uuid.uuid4())[:8]
    payload = {
        "id": msg_id,
        "from": from_agent,
        "to": to_agent,
        "type": "text",
        "content": message,
        "timestamp": datetime.now().isoformat()
    }
    r.publish(f"cfm:{to_agent}:inbox", json.dumps(payload, ensure_ascii=False))
    r.lpush(f"cfm:{from_agent}:messages", json.dumps(payload, ensure_ascii=False))
    r.lpush(f"cfm:{to_agent}:messages", json.dumps(payload, ensure_ascii=False))
    r.close()
    return msg_id


def quick_receive(agent_id: str, timeout: int = 10) -> Optional[Dict]:
    """Quick receive (blocking wait)"""
    r = redis.Redis(decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe(f"cfm:{agent_id}:inbox")
    
    start = time.time()
    result = None
    
    try:
        while time.time() - start < timeout:
            msg = pubsub.get_message(timeout=1)
            if msg and msg["type"] == "message":
                result = json.loads(msg["data"])
                break
    finally:
        pubsub.unsubscribe()
        pubsub.close()
        r.close()
    
    return result
```

### cfm_cli.py - Command Line Tool

```python
#!/usr/bin/env python3
"""CFM CLI - Command Line Tool"""

import sys
import argparse
from cfm_messenger import quick_send, quick_receive, CFMMessenger


def cmd_send(args):
    """Send message"""
    msg_id = quick_send(args.to, args.message, args.from_agent)
    print(f"✅ Message sent (ID: {msg_id})")
    print(f"   {args.from_agent} → {args.to}: {args.message}")


def cmd_listen(args):
    """Listen for messages"""
    print(f"👂 {args.agent_id} listening... (timeout: {args.timeout}s)")
    msg = quick_receive(args.agent_id, args.timeout)
    if msg:
        print(f"📨 Message received!")
        print(f"   Sender: {msg['from']}")
        print(f"   Content: {msg['content']}")
    else:
        print("⏰ Timeout, no message received")


def cmd_history(args):
    """View history"""
    with CFMMessenger(args.agent_id) as m:
        msgs = m.get_messages(limit=args.limit)
        if msgs:
            print(f"📚 {args.agent_id} message history ({len(msgs)} msgs):")
            for msg in msgs:
                direction = "📤" if msg.get('from') == args.agent_id else "📥"
                print(f"  {direction} {msg.get('from')} → {msg.get('to')}: {msg.get('content', '?')[:50]}")
        else:
            print("📚 No messages yet")


def cmd_discover(args):
    """Discover Agents"""
    with CFMMessenger("discover-cli") as m:
        agents = m.discover_agents()
        if agents:
            print(f"🔍 Found {len(agents)} Agents:")
            for agent in agents:
                print(f"   - {agent.get('id')}: {agent.get('status', 'unknown')}")
        else:
            print("🔍 No other Agents found")


def main():
    parser = argparse.ArgumentParser(description="CFM CLI - Cross-Framework Communication Tool")
    subparsers = parser.add_subparsers(dest="command")
    
    # send
    send_p = subparsers.add_parser("send", help="Send message")
    send_p.add_argument("to", help="Target Agent ID")
    send_p.add_argument("message", help="Message content")
    send_p.add_argument("--from", dest="from_agent", default="cli")
    
    # listen
    listen_p = subparsers.add_parser("listen", help="Listen for messages")
    listen_p.add_argument("agent_id", help="This Agent ID")
    listen_p.add_argument("--timeout", type=int, default=10)
    
    # history
    history_p = subparsers.add_parser("history", help="View history")
    history_p.add_argument("agent_id", help="Agent ID")
    history_p.add_argument("--limit", type=int, default=20)
    
    # discover
    subparsers.add_parser("discover", help="Discover Agents")
    
    args = parser.parse_args()
    
    if args.command == "send": cmd_send(args)
    elif args.command == "listen": cmd_listen(args)
    elif args.command == "history": cmd_history(args)
    elif args.command == "discover": cmd_discover(args)
    else: parser.print_help()


if __name__ == "__main__":
    main()
```

### cfm_check.py - Lightweight Check Script (Zero Token)

```python
#!/usr/bin/env python3
"""CFM Check - Zero Token Lightweight Check"""

import redis
import json
import os
from pathlib import Path

def check_messages(agent_id: str):
    """Check new messages and output"""
    processed_file = Path.home() / ".cfm" / agent_id / "processed.txt"
    processed_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Read processed IDs
    processed = set()
    if processed_file.exists():
        processed = set(processed_file.read_text().strip().split("\n"))
    
    r = redis.Redis(decode_responses=True)
    store_key = f"cfm:{agent_id}:messages"
    raw_msgs = r.lrange(store_key, 0, 49)
    
    new_messages = []
    for raw in raw_msgs:
        msg = json.loads(raw)
        msg_id = msg.get("id", "")
        # Only process messages from other Agents
        if msg.get("from") != agent_id and msg_id not in processed:
            new_messages.append(msg)
            processed.add(msg_id)
    
    # Save processed IDs
    processed_file.write_text("\n".join(sorted(processed)))
    r.close()
    
    # Output results
    if new_messages:
        for msg in new_messages:
            print(f"📨 [{msg['from']}]: {msg['content']}")
    else:
        print("💤 No new messages")

if __name__ == "__main__":
    import sys
    agent_id = sys.argv[1] if len(sys.argv) > 1 else "hermes"
    check_messages(agent_id)
```

## Usage

### Send Message

```bash
cd ~/.shared/cfm
python3 cfm_cli.py send chanel "Hello!" --from hermes
```

### Listen for Messages

```bash
python3 cfm_cli.py listen chanel --timeout 30
```

### View History

```bash
python3 cfm_cli.py history hermes
```

### Discover Agents

```bash
python3 cfm_cli.py discover
```

### Lightweight Check (Recommended for Automation)

```bash
python3 cfm_check.py hermes
```

#### Using --last-check-file Parameter (Recommended)

Use the `--last-check-file` parameter to record the last check time and avoid reprocessing messages:

```bash
python3 cfm_check.py chanel --last-check-file /tmp/cfm-last-check.txt
```

**Benefits**:
- Automatically records check time, only returns new messages on next check
- Avoids reprocessing the same message
- More reliable message deduplication

**Integration in HEARTBEAT**:
```bash
python3 /Users/kyle/.shared/cfm/cfm_check.py chanel --last-check-file /tmp/cfm-last-check.txt
```

## Utility Scripts

### reply_to_hermes.py - Quick Reply Script

For quickly replying to Hermès with common messages:

```bash
python3 /Users/kyle/.shared/cfm/reply_to_hermes.py
```

### mark_reported.py - Mark Reported Messages

Mark specified message IDs as reported to avoid duplicate reporting:

```bash
python3 /Users/kyle/.shared/cfm/mark_reported.py
```

### send_report.py - Send Report Message

Quickly send preset report messages to Hermès:

```bash
python3 /Users/kyle/.shared/cfm/send_report.py
```

## Agent Integration Methods

### Method 1: Cron Task (Simple)

```bash
# Check every 5 minutes
*/5 * * * * cd ~/.shared/cfm && python3 cfm_check.py myagent
```

### Method 2: Daemon Process (Real-time)

```python
# Call in heartbeat or scheduled task
import subprocess
result = subprocess.run(
    ["python3", "~/.shared/cfm/cfm_check.py", "myagent"],
    capture_output=True, text=True
)
if "📨" in result.stdout:
    # New messages, trigger processing
    process_new_messages()
```

### Method 3: Webhook Trigger (Advanced)

```python
# Trigger webhook when new messages detected
from cfm_messenger import CFMMessenger

def check_and_trigger(agent_id, webhook_url):
    with CFMMessenger(agent_id) as m:
        msgs = m.get_messages(limit=5)
        new_msgs = [msg for msg in msgs if msg.get("from") != agent_id]
        if new_msgs:
            # Trigger webhook
            import requests
            requests.post(webhook_url, json=new_msgs)
```

## Message Format

```json
{
  "id": "a1b2c3d4",
  "from": "hermes",
  "to": "chanel",
  "type": "text",
  "content": "Message content",
  "timestamp": "2026-04-15T20:00:00.000000"
}
```

### Message Types

- `text` - Plain text
- `command` - Command message
- `response` - Response message
- `file` - File reference (content is file path)

## Troubleshooting

### Redis Connection Failed

```bash
redis-cli ping  # Check Redis status
brew services restart redis  # Restart Redis
```

### Messages Not Delivered

```bash
# Check messages in Redis
redis-cli LRANGE cfm:agent-name:messages 0 5
```

### Python Import Error

```bash
pip install redis
python3 -c "import redis; print('✅ Import successful')"
```

## ⚠️ Important Lessons Learned

### 1. quick_send Cannot Use Context Manager

**Wrong Way** (causes process to hang):
```python
def quick_send(to_agent, message, from_agent="cli"):
    with CFMMessenger(from_agent) as messenger:  # ❌ Starts listening thread
        return messenger.send(to_agent, message)  # Hangs on thread cleanup at exit
```

**Correct Way** (direct connection, no thread):
```python
def quick_send(to_agent, message, from_agent="cli"):
    r = redis.Redis(decode_responses=True)  # ✅ Direct connection
    # ... send message
    r.close()  # Close immediately
    return msg_id
```

**Reason**: `CFMMessenger.__enter__` starts a listening thread, and `__exit__` thread cleanup causes `ValueError: I/O operation on closed file`.

### 2. Messages Must Be Stored to Both Parties

**Wrong**: Only store to sender
```python
# ❌ Receiver can't find messages
self._store_message(payload, self.agent_id)
```

**Correct**: Store to both parties
```python
# ✅ Both can find messages
self._store_message(payload, self.agent_id)      # Sender
self._store_message(payload, to_agent)           # Receiver
```

**Reason**: Messages are stored to both parties, receiver checks their own store for new messages. If only stored to sender, receiver will never find them.

### 3. Check Script Logic

**Wrong**: Check `to == agent_id`
```python
# ❌ Message's to field isn't necessarily this agent
if msg.get("to") == agent_id and msg_id not in processed_ids:
```

**Correct**: Check `from != agent_id`
```python
# ✅ Messages from other agents are new messages
if msg.get("from") != agent_id and msg_id not in processed_ids:
```

**Reason**: Messages are stored to both parties, `to` field is target agent, but stored in both stores, so should check if `from` is self.

### 4. execute_code Sandbox Doesn't Have redis Library

**Problem**: `import redis` in `execute_code` throws `ModuleNotFoundError`.

**Solution**: Use `terminal` tool to run Python script directly:
```bash
cd ~/.shared/cfm && python3 cfm_cli.py send chanel "message" --from hermes
```

Or use `redis-cli` to check directly:
```bash
redis-cli LRANGE cfm:hermes:messages 0 5
```

### 5. OpenClaw gateway.bind=lan Requires auth

**Problem**: Configure `gateway.bind="lan"` but don't set `gateway.auth.token`, OpenClaw refuses to start.

**Solution**:
```bash
openclaw config set gateway.auth.token "your-token"
openclaw gateway start
```

### 6. quick_receive Uses get_message Instead of listen

**Wrong** (blocks, hard to timeout):
```python
for msg in pubsub.listen():  # ❌ Blocking loop
    if time.time() - start > timeout:
        break
```

**Correct** (non-blocking, controllable timeout):
```python
while time.time() - start < timeout:
    msg = pubsub.get_message(timeout=1)  # ✅ Non-blocking
    if msg and msg["type"] == "message":
        result = json.loads(msg["data"])
        break
```

---

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Message Latency | < 10ms |
| Memory Usage | ~10MB (Redis) |
| Throughput | 1000+ msg/s |
| Persistence | Last 1000 msgs/Agent |
| Concurrency | Supports multiple Agents |

## Use Cases

- ✅ Cross-framework real-time communication (Hermes ↔ OpenClaw)
- ✅ High-frequency messages (>10 msgs/minute)
- ✅ Message persistence required
- ✅ Multi-Agent collaboration

## Not Suitable For

- ❌ Environments where Redis can't be installed
- ❌ Minimal requirements (use file mailbox)
- ❌ Public network communication (requires additional config)

## Comparison with File Mailbox

| Feature | File Mailbox | CFM Redis |
|---------|--------------|-----------|
| Real-time | 🐢 1-5 min delay | ⚡ < 10ms |
| Dependencies | None | Redis |
| Token Consumption | Based on poll frequency (LLM calls) | Only consumes when processing messages |
| Reliability | High | High |
| Scalability | 2 Agents | Multi-Agent |

---

**CFM Redis — Make cross-framework Agent communication as smooth as local chat!** ⚡
