# ⚡ CFM Redis - Cross-Framework AI Agent Real-time Communication

A cross-framework Agent communication solution based on Redis Pub/Sub. Event-driven, millisecond-level latency, zero token consumption for communication.

## Key Advantages

- ⚡ **Real-time Communication** - Message latency < 10ms
- 💰 **Zero Token Consumption** - Redis direct transfer, no LLM tokens consumed
- 🔄 **Bidirectional Communication** - Supports communication between any frameworks
- 💾 **Message Persistence** - Automatic history preservation
- 🔍 **Agent Discovery** - Automatically discover Agents on the network

## Quick Start

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

## OpenClaw Auto-Check Configuration

### Add Cron Task (Check Every Minute)

```bash
openclaw cron add --name "cfm-check" --every 1m --agent main --message "Execute the following Python script to check CFM messages:

\`\`\`python
import redis, json
r = redis.Redis(decode_responses=True)
msgs = r.lrange('cfm:chanel:messages', 0, 20)
hermes_msgs = [json.loads(m) for m in msgs if json.loads(m).get('from') == 'hermes']
print(f'Total {len(hermes_msgs)} messages')
for msg in hermes_msgs[:3]:
    print(f'[{msg[\"timestamp\"]}] {msg[\"content\"]}')
r.close()
\`\`\`

If there are new messages, tell me the content. If not, say 'No new messages'."
```

### View Cron Tasks

```bash
openclaw cron list
```

### Remove Cron Task

```bash
openclaw cron rm <job-id>
```

## Message Format

```json
{
  "id": "a1b2c3d4",
  "from": "hermes",
  "to": "chanel",
  "type": "text",
  "content": "Message content",
  "timestamp": "2026-04-16T01:30:00.000000"
}
```

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Message Latency | < 10ms |
| Memory Usage | ~10MB (Redis) |
| Throughput | 1000+ msg/s |
| Persistence | Last 1000 msgs/Agent |

## Use Cases

- ✅ Cross-framework real-time communication (Hermes ↔ OpenClaw)
- ✅ High-frequency messages (>10 msgs/minute)
- ✅ Message persistence required
- ✅ Multi-Agent collaboration

## Comparison with File Mailbox

| Feature | File Mailbox | CFM Redis |
|---------|--------------|-----------|
| Real-time | 🐢 1-5 min delay | ⚡ < 10ms |
| Dependencies | None | Redis |
| Token Consumption | Based on poll frequency | Zero tokens for communication |
| Reliability | High | High |
| Scalability | 2 Agents | Multi-Agent |

## Troubleshooting

### Redis Connection Failed

```bash
redis-cli ping  # Check Redis status
brew services restart redis  # Restart Redis
```

### Python Import Error

```bash
pip install redis
python3 -c "import redis; print('✅ Import successful')"
```

## License

MIT License

---

**CFM Redis — Make cross-framework Agent communication as smooth as local chat!** ⚡
