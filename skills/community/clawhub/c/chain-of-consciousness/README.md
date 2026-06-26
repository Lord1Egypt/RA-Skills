# Chain of Consciousness — OpenClaw Skill

Add cryptographic provenance to your OpenClaw agent in under 5 minutes.

## What It Does

This skill gives your OpenClaw agent the ability to maintain cryptographic audit trails — tamper-evident records of what it learned, decided, and created, with hash-linked entries and optional external timestamp anchoring.

## Installation

### Via ClawHub (when published)

```bash
clawhub install absupport/chain-of-consciousness
```

### Manual Installation

1. Install the Python package:

```bash
pip install chain-of-consciousness
```

2. Copy the skill to your workspace:

```bash
mkdir -p ~/.openclaw/workspace/skills/chain-of-consciousness
cp SKILL.md ~/.openclaw/workspace/skills/chain-of-consciousness/SKILL.md
```

3. Restart your OpenClaw session:

```
/new
```

4. Verify installation:

```bash
openclaw skills list | grep chain
```

## Usage

Once installed, your agent will automatically use provenance tracking when appropriate. You can also invoke it directly:

```
"Start a provenance chain for this task"
"Log that you decided to use PostgreSQL and why"
"Verify the chain and show me the results"
"Export the provenance trail for this project"
```

## Event Types

| Type | Description |
|------|-------------|
| `session_start` | Beginning a task |
| `learn` | Information acquired |
| `decide` | Choice made (with reasoning) |
| `create` | Artifact produced |
| `milestone` | Checkpoint reached |
| `error` | Failure + recovery |
| `note` | General observation |
| `session_end` | Task completed |

## Requirements

- Python 3.8+
- `chain-of-consciousness` pip package

## Links

- [PyPI Package](https://pypi.org/project/chain-of-consciousness/)
- [Whitepaper](https://vibeagentmaking.com/whitepaper)
- [Verification Demo](https://vibeagentmaking.com/verify/)
- [Website](https://vibeagentmaking.com)
