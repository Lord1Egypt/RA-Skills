# 🧠 CXM (ContextMachine) - Neural Memory for AI Agents

**CXM is a high-performance local framework that gives your AI Agents (like Openclaw, Hermes, or Maestro) a "Neural Memory" of your entire codebase.**

Stop relying on basic keyword searches (grep). CXM uses a localized **Mini-BERT model** and **AST-Parsing** to understand the *meaning* and *structure* of your code, ensuring your agents never lose context in large-scale projects.

---

## 🚀 Why do you need CXM?

Traditional agents often suffer from **Context Collapse**. They see a file, but they don't know what depends on it or where the related logic is hidden. 

**CXM solves this by providing:**
1.  **Semantic Retrieval**: Find code by "vibe" or intent (e.g., *"Where is the auth gate?"*) instead of just matching words.
2.  **Dependency Telepathie**: Automatically map how files, classes, and functions are connected.
3.  **Real-Time Sync**: A background daemon that updates the agent's memory the moment you save a file.
4.  **Agent-First Design**: A dedicated `--agent-mode` that outputs strict JSON for seamless LLM integration.

---

## 🛠️ Installation Guide

### 1. Prerequisites
- Python 3.9+
- Pip

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/Joeavaib/partner.git
cd partner

# Install dependencies (Transformers, FAISS, Watchdog, NetworkX)
pip install -r requirements.txt

# (Optional) Install in editable mode to use 'cxm' command globally
pip install -e .
```

---

## 📖 Quick Start & Demonstration

### 🔍 Scenario: The "Blind" Search
Imagine you are looking for the rate-limiting logic. You don't know if the developer called it `limiter`, `throttle`, or `shield`.

**Traditional Grep:**
```bash
grep -r "rate_limit" .  # Returns 0 results because the file is named 'traffic_control.py'
```

**CXM Semantic Search:**
```bash
python src/cli.py harvest --semantic "How do we prevent API abuse?"
```
*CXM uses Mini-BERT to understand that "prevent API abuse" is semantically related to the code in `traffic_control.py` and fetches it instantly.*

### 🕸️ Scenario: The "Safe" Refactor
Before an agent modifies a core file, it needs to know the "blast radius."
```bash
python src/cli.py map src/core/rag.py
```
*CXM builds an AST-graph and shows exactly which files import or depend on the RAG engine.*

### 👁️ Scenario: The "Always-Ready" Context
Run the background watcher to keep the memory fresh:
```bash
python src/cli.py watch
```
*Every time you or an agent saves a file, the Vector Index is updated in milliseconds.*

---

## 🤖 Using CXM as an Agent Skill (Openclaw/Hermes)

CXM is designed to be consumed by other LLMs. Use the `--agent-mode` flag to get machine-readable JSON:

```bash
python src/cli.py --agent-mode search "Database connection logic"
```

**Output:**
```json
{
  "results": [
    {
      "path": "src/db/connector.py",
      "similarity": 0.92,
      "content": "class DBHandler: ..."
    }
  ]
}
```

**Agent Integration:**
Load the tool definitions from `docs/agent_skill.json` into your agent's framework to allow it to call CXM autonomously.

---

## ⚡ Technical Specs (Resource Footprint)

CXM is highly optimized for local execution on developer machines:

- **RAM**: ~300 MB (Standard Mini-BERT) / ~1.1 GB (High-Precision MPNet)
- **CPU**: Uses all threads for initial indexing; near-zero idle usage during search.
- **Latency**: Sub-20ms retrieval on 10,000+ code snippets.
- **Privacy**: **100% Local.** No code ever leaves your machine for indexing.

---

## 📄 License
MIT
