# QUICKSTART.md

## Quick Start

This package is for users who want a CEO-style coordinator agent, not just a tool script.

## Fastest path

### Coordinator only

```bash
clawhub install ceo-xiaomao-agent
mkdir -p ~/workspace/ceo-xiaomao
cd ~/workspace/ceo-xiaomao
python3 ~/.openclaw/skills/ceo-xiaomao-agent/scripts/init_agent_workspace.py
```

Then edit:
- `USER.md`
- `MEMORY.md`

Suggested first message:

```text
你好，我是外贸团队的协调总控。请检查我的工作区状态，并告诉我当前进展、下一步和风险点。
```

### Coordinator + capability bundle

```bash
clawhub install ceo-xiaomao-agent
clawhub install ceo-xiaomao
mkdir -p ~/workspace/ceo-team
cd ~/workspace/ceo-team
python3 ~/.openclaw/skills/ceo-xiaomao-agent/scripts/init_agent_workspace.py
```

Suggested first message:

```text
请以CEO小茂身份启动，先读取工作区文件，然后告诉我：团队分工、当前待办、优先级最高的下一步。
```

## What you get after install

- a CEO assistant workspace
- persona and rules
- reporting structure
- role routing guidance
- reusable templates
