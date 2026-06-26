# ClawHub publish notes

Use these commands after the skill is ready:

```bash
python3 /home/openclaw/.local/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py /home/openclaw/.openclaw/agents/automation-helper/workspace/skills/agent-supervision /home/openclaw/.openclaw/agents/automation-helper/workspace/dist
```

If the `clawhub` CLI is installed and logged in, publish with:

```bash
clawhub publish /home/openclaw/.openclaw/agents/automation-helper/workspace/skills/agent-supervision \
  --slug agent-supervision \
  --name "Agent Supervision" \
  --version 0.1.0 \
  --changelog "Initial release: scheduled and ETA-based cross-session agent supervision"
```

If `clawhub` is not installed:

```bash
npm i -g clawhub
clawhub login
clawhub whoami
```

The publisher account must already exist on ClawHub.
