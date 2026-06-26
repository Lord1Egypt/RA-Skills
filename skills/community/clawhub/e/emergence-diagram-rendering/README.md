# Skill: Emergence Diagram Rendering (Official)

A high-fidelity, autonomous diagramming skill certified by **Emergence Science**.

## 🌟 Design Philosophy
This skill is built on the principle of **Agentic Autonomy**. It empowers solver agents to be self-sovereign by providing:
1.  **Local-First Execution**: Prioritizes host-level binaries (`mmdc`, `d2`, `dot`) for privacy and speed.
2.  **Automated Environment**: Manages its own isolated Python Virtual Environment (`.venv/`) for maximum portability across MacBook and Ubuntu.
3.  **Persistent Run History**: Every rendering attempt is saved in `./runs/`, allowing the agent to "read" compiler errors and fix its own code recursively.

## 🛠 Installation (MacBook / Linux)
The skill automatically configures its own Python environment.

### 1. System Dependencies
- **Graphviz**: `brew install graphviz` (Mac) or `apt-get install -y graphviz` (Linux).
- **D2**: `curl -fsSL https://d2lang.com/install.sh | sh`
- **Mermaid CLI**: `npm install -g @mermaid-js/mermaid-cli`

### 2. Auto-Configuration
```bash
# Clone the skill and run setup
bash install.sh
```

## 📂 Project Structure
- `./templates/`: Pre-defined blueprints for common flows.
- `./scripts/`: Core rendering logic (`local_render.py`).
- `./runs/`: Persistent memory of all generation attempts.
- `SKILL.md`: The agent-facing "Internal Monologue" and reasoning patterns.

## 🤖 For Agents
If you are a solver agent, read [SKILL.md](./SKILL.md). Always use the local virtual environment: `./.venv/bin/python3`.
