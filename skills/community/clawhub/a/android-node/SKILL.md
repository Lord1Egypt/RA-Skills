# android-node

Turn any Android phone into an inference compute node for your AI agent.

## What it does

Provisions Android phones as Ollama inference endpoints. Any phone running Termux becomes a worker your agent can route jobs to — no cloud, no subscription, no special hardware. The phone on your desk, the spare in your drawer, all of them.

## How it works

1. Phone runs Ollama via Termux (setup takes ~5 minutes)
2. Pi/server connects to phone over local WiFi
3. `phone_nodes.py` manages discovery, health checks, and failover
4. Router dispatches inference jobs to healthy nodes automatically

## Setup

### On the phone (run in Termux)
```bash
curl -s https://albionwakes.com/phone_setup.sh | bash
bash ~/start_node.sh
```

### On your server (register the phone)
```bash
python3 phone_nodes.py register myphone 192.168.1.42
python3 phone_nodes.py status
```

### Router integration
```python
import phone_nodes

# In your provider dispatch:
elif provider == 'phone':
    return phone_nodes.call(messages)
```

## Node registry

Stored in `~/albion_memory/phone_nodes.json`:
```json
[
  {"name": "pixel6", "url": "http://192.168.1.42:11434", "model": "qwen2.5:0.5b", "enabled": true}
]
```

## Default model

`qwen2.5:0.5b` — 394MB, runs on any phone with 1GB+ free RAM. Fast.
Swap for `qwen2.5:1.5b` (1GB) or `llama3.2:1b` (1.3GB) if the phone has headroom.

## Files

- `phone_nodes.py` — node registry, health checker, inference caller
- `setup.sh` — Termux provisioning script (run on phone)
