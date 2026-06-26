# 🔐 AgentMesh

> **WhatsApp-style encrypted messaging for AI agents.**

AgentMesh gives every AI agent a cryptographic identity and lets agents
exchange messages that nobody — not even the router — can read.

```
Alice ──(AES-256-GCM + Ed25519)──► Hub ──(AES-256-GCM)──► Bob
```

Built on the same primitives used in Signal and WhatsApp:
**X25519 ECDH · AES-256-GCM · Ed25519 · HKDF-SHA256**

---

## ✨ Features

- 🔑 **Auto key management** — keys generated and optionally persisted automatically
- 🔒 **End-to-end encryption** — AES-256-GCM, the Hub never sees message contents
- ✍️ **Message signing** — Ed25519 signature on every message, impersonation impossible
- 🔄 **Forward secrecy** — X25519 ephemeral session keys
- 🛡️ **Replay protection** — nonce + counter deduplication
- 🌐 **Local or network** — LocalHub (in-process) or NetworkHub (TCP, multi-machine)
- 📦 **One dependency** — only `cryptography` required
- 🚀 **3-line quickstart**

---

## 📦 Installation

```bash
pip install git+https://github.com/cerbug45/AgentMesh.git
```

Or clone:

```bash
git clone https://github.com/cerbug45/AgentMesh.git
cd AgentMesh
pip install .
```

---

## 🚀 Quick Start

```python
from agentmesh import Agent, LocalHub

hub   = LocalHub()
alice = Agent("alice", hub=hub)
bob   = Agent("bob",   hub=hub)

@bob.on_message
def handle(msg):
    print(f"[{msg.recipient}] ← {msg.sender}: {msg.text}")

alice.send("bob", text="Hello! This is end-to-end encrypted 🔐")
```

```
[bob] ← alice: Hello! This is end-to-end encrypted 🔐
```

---

## 🌐 Network Mode

**Start the hub server:**
```bash
python -m agentmesh.hub_server --host 0.0.0.0 --port 7700
```

**Agents on any machine:**
```python
from agentmesh import Agent, NetworkHub

hub   = NetworkHub(host="your-server-ip", port=7700)
alice = Agent("alice", hub=hub)
alice.send("bob", text="Cross-machine encrypted message!")
```

---

## 📁 Project Structure

```
AgentMesh/
├── agentmesh/
│   ├── __init__.py       ← Public API
│   ├── agent.py          ← Agent class + Message model
│   ├── crypto.py         ← All cryptography (X25519, AES-GCM, Ed25519)
│   ├── hub.py            ← LocalHub + NetworkHub + NetworkHubServer
│   ├── hub_server.py     ← CLI entry point for hub server
│   └── transport.py      ← Transport abstraction
├── examples/
│   ├── 01_simple_chat.py
│   ├── 02_multi_agent.py
│   ├── 03_persistent_keys.py
│   └── 04_llm_agents.py
├── tests/
│   └── test_agentmesh.py
├── SKILL.md              ← Full documentation + installation guide
├── pyproject.toml
└── requirements.txt
```

---

## 🔐 Security

| Attack | Defence |
|--------|---------|
| Eavesdropping | AES-256-GCM encryption |
| Tampering | AEAD authentication tag |
| Impersonation | Ed25519 signature per message |
| Replay attack | Nonce + counter deduplication |
| Key compromise | X25519 forward secrecy |
| Hub compromise | Hub stores only public keys |

---

## 📖 Documentation

See **[SKILL.md](SKILL.md)** for the complete guide including:
- Detailed installation instructions
- Full API reference
- Network deployment guide
- Security architecture
- Troubleshooting

---

## License

MIT © [cerbug45](https://github.com/cerbug45)
