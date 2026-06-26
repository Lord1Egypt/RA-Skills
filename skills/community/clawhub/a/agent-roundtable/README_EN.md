<p align="center">
  <img src="https://raw.githubusercontent.com/MoyuFamily/agent-roundtable/main/docs/design/assets/svg/roundtable-logo.svg" alt="Roundtable" width="128" height="128">
</p>

<h1 align="center">Roundtable</h1>

<p align="center">
  <strong>agent-roundtable is a multi-agent roundtable discussion engine for AI agent teams: let multiple agents speak in order, track consensus and disagreements, and generate structured meeting notes and conclusions.</strong>
</p>

<p align="center">
  <a href="#development"><img src="https://img.shields.io/badge/tests-passing-brightgreen.svg" alt="Tests"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache--2.0-blue.svg" alt="License: Apache-2.0"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"></a>
  <a href="#-core-features"><img src="https://img.shields.io/badge/core-zero_dependencies-brightgreen.svg" alt="Zero Dependencies"></a>
</p>

<p align="center">
  <strong><a href="README.md">中文</a> · <a href="README_EN.md">English</a></strong>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/MoyuFamily/agent-roundtable/main/docs/design/assets/demo.gif" alt="Roundtable Demo" width="600">
</p>

---

## ⚡ Understand Roundtable in 30 Seconds

When you let multiple AI agents discuss a complex problem, the hard part is not making them speak — it is managing the discussion:

| What you care about | Roundtable's answer |
|---|---|
| How do multiple agents collaborate? | Use a roundtable meeting model to manage participants, rounds, and ordered speaking |
| Is the discussion converging? | Automatically track convergence score, consensus points, and disagreement points |
| How are conclusions captured? | Generate structured summaries for meeting notes, PRDs, architecture reviews, and decision records |
| Can it integrate with existing agent systems? | Framework-agnostic; integrate via adapters with Hermes Agent or any agent framework |
| Is it heavy to run? | The core library has zero external dependencies and uses only Python stdlib + SQLite |

**In one sentence: `agent-roundtable` is a Python package embeddable in any AI agent system; you pick the participants and define the topic, and it manages multi-agent roundtable discussions, ordered speaking, consensus/disagreement tracking, and structured meeting notes.**

## 🧩 Use Cases

- **Technical architecture review**: Let architect, backend, ops, and security agents debate and preserve decision rationale
- **Product decision discussion**: Let product, design, engineering, and growth roles align on MVP scope and priorities
- **Code review debate**: Let agents review a solution from quality, security, and performance perspectives
- **Requirement clarification**: Let expert roles question, challenge, and converge on ambiguous requirements
- **Multi-agent workflows**: Act as the coordinator's discussion protocol layer with a durable record and conclusion

## 🚀 Quick Start

### Installation

The official PyPI package name is planned as `agent-roundtable`. After release, install it with:

```bash
pip install agent-roundtable
```

Before the PyPI release, use source installation for local validation:

```bash
git clone https://github.com/MoyuFamily/agent-roundtable.git
cd agent-roundtable
pip install -e .
```

> Note: The existing `roundtable` / `roundtable-ai` packages on PyPI are not this project. Do not install this project with `pip install roundtable`.

### Basic Usage

Example: let a backend architect, ops engineer, and product manager discuss database selection. Roundtable manages rounds, records viewpoints, tracks convergence, and generates a conclusion.

```python
from roundtable import RoundtableCore

core = RoundtableCore()

# 1. Create a discussion
result = core.create_discussion(
    topic="Choose database: PostgreSQL vs MySQL vs TiDB",
    participants=[
        {"profile": "backend_architect", "role": "Backend Architect", "display_name": "Backend Architect"},
        {"profile": "ops_engineer", "role": "Ops Engineer", "display_name": "Ops Engineer"},
        {"profile": "product_manager", "role": "Product Manager", "display_name": "Product Manager"},
    ],
    max_rounds=3,
)
disc_id = result["discussion_id"]

# 2. Participants speak
core.speak(disc_id, "backend_architect", "PostgreSQL has stronger JSON and transaction support for complex business modeling.")
core.speak(disc_id, "ops_engineer", "MySQL has more mature operational experience and tooling in our team.")
core.speak(disc_id, "product_manager", "From an iteration perspective, we need room for future feature expansion.")

# 3. Check discussion status with convergence score
status = core.status(disc_id)
print(f"Convergence: {status['convergence_score']}")

# 4. Generate structured summary
summary = core.summarize(disc_id, compact=True)
print(summary["structured_summary"])

# 5. End discussion
core.end_discussion(disc_id, conclusion="Choose PostgreSQL for complex data modeling and long-term extensibility.")
```

### Error-Safe Mode (Recommended for Production)

```python
from roundtable.adapters.generic import Roundtable

rt = Roundtable(db_path="/tmp/discussions.db")
result = rt.init(topic="...", participants=[...])
# All methods return dict — errors are returned as {"error": "msg"}, never thrown
```

### Real-time Notifications

```python
def my_send(platform, chat_id, message):
    print(f"[{platform}:{chat_id}] {message}")

rt = Roundtable(send_fn=my_send)
result = rt.init(
    topic="Architecture Review",
    participants=[...],
    notifications={
        "enabled": True,
        "channels": [
            {"platform": "feishu", "chat_id": "oc_xxx"},
            {"platform": "slack", "chat_id": "#engineering"},
        ],
        "events": ["round_end", "concluded"],
    },
)
```

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🧑‍⚖️ **Roundtable Discussion Model** | Manage multi-agent discussions with topic, participants, and rounds |
| 📊 **Convergence Tracking** | Auto-calculate consensus score per round to quantify discussion progress |
| 🧾 **Structured Summaries** | Output consensus, disagreements, recommendations, and conclusions for meeting notes and decision records |
| 🔌 **Framework Agnostic** | Run standalone or integrate with any agent framework via adapters |
| 🔔 **Real-time Notifications** | Push discussion events to Feishu, Slack, or any messaging platform |
| 🛡️ **Error-Safe** | Generic adapter returns dict for all methods and never throws exceptions |
| 🗂️ **SQLite Persistence** | Persist discussion records for later review and traceability |
| 🪶 **Zero-Dependency Core** | Core library uses only Python stdlib (`sqlite3` + `dataclasses`) |

## 🔌 Built for Hermes Agent Integration

Roundtable can be used as a standalone Python library or as a Hermes Agent toolset, letting multiple agents participate in the same structured discussion via tool calls.

```yaml
# Hermes config
toolsets:
  - roundtable
```

After installing Hermes Agent, Roundtable can register discussion tools so AI agents can create, participate in, read, summarize, and end discussions.

## 📐 Architecture

```text
src/roundtable/
├── __init__.py       # Public API
├── core.py           # Business logic layer
├── db.py             # SQLite storage layer
├── models.py         # Data models (dataclass)
├── notify.py         # Notification dispatch
├── exceptions.py     # Exception definitions
└── adapters/
    ├── hermes.py     # Hermes Agent adapter
    └── generic.py    # Generic Python API (error-safe)
```

## 🛣️ Roadmap

- Publish PyPI package name: `agent-roundtable` (install with `pip install agent-roundtable`)
- Add CLI examples and end-to-end demos
- Improve structured summary templates
- Add adapters for more agent frameworks
- Add discussion result export

## 🤝 Contributing

1. Fork this repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Write tests and ensure they pass: `pytest tests/ -v`
4. Commit code: `git commit -m 'feat: add amazing feature'`
5. Push and create PR

### Code Standards

- Python 3.10+, use type hints
- Zero external dependencies in the core library
- All exceptions inherit `RoundtableError`
- All public methods return JSON-serializable dict

## 👥 Team

| Member | Role | Description |
|--------|------|-------------|
| <img src="https://avatars.githubusercontent.com/u/286716759?v=4" width="24" height="24" style="border-radius:50%"> Bingge | Product Director | 10+ years product veteran, expert at turning vague requirements into actionable MVPs, believes "users don't want a drill, they want a hole in the wall" |
| <img src="https://avatars.githubusercontent.com/u/286719582?v=4" width="24" height="24" style="border-radius:50%"> Pixel | Design Director | UI/UX and brand visual system design, focuses on interaction details and UX optimization, believes "details determine quality" |
| <img src="https://avatars.githubusercontent.com/u/286715358?v=4" width="24" height="24" style="border-radius:50%"> Mafei | Tech Director | Full-stack development and system architecture design, leads tech selection, performance optimization, and AI/ML engineering |
| <img src="https://avatars.githubusercontent.com/u/286714101?v=4" width="24" height="24" style="border-radius:50%"> Xiaohe | Coordinator | Team task coordination and progress management, ensures product→design→development workflow runs efficiently |

## 📄 License

[Apache-2.0](LICENSE)
