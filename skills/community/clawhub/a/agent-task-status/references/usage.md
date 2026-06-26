# Usage

## What this tool checks
- Latest matching assignment in an agent session transcript
- Latest structured assistant report after that assignment
- Parsed fields: task / status / result / risk
- Normalized status for automation-friendly filtering

## Common examples

Default check for the standard three agents:
```bash
python3 scripts/check_agent_task_status.py
```

Quick human-readable summary:
```bash
python3 scripts/check_agent_task_status.py --format summary
```

Check a custom list of agents:
```bash
python3 scripts/check_agent_task_status.py --agents dev1,writer1,research1 --format table
```

Auto-discover all agents under a custom root:
```bash
python3 scripts/check_agent_task_status.py --base /srv/openclaw/agents --discover --format summary
```

Use custom assignment/report markers:
```bash
python3 scripts/check_agent_task_status.py \
  --agents alpha,beta \
  --assign-keyword 'TASK_ASSIGNED:' \
  --task-prefix 'Task:' \
  --status-prefix 'Status:' \
  --result-prefix 'Result:' \
  --risk-prefix 'Risk:' \
  --format json
```

Filter by normalized status:
```bash
python3 scripts/check_agent_task_status.py --discover --only-status completed
python3 scripts/check_agent_task_status.py --discover --only-status blocked,assigned-no-report
```

Filter by keyword:
```bash
python3 scripts/check_agent_task_status.py --discover --contains 自动化
python3 scripts/check_agent_task_status.py --agents xiaocheng,xiaowen --contains 文案 --format table
```

Write output to file:
```bash
python3 scripts/check_agent_task_status.py --discover --format json --output-file /tmp/agent-status.json
```

Read agents from file:
```bash
python3 scripts/check_agent_task_status.py --agent-file ./agents.txt --format jsonl
```

Strict mode for automation:
```bash
python3 scripts/check_agent_task_status.py --discover --strict
```

## Portability notes
- Best for OpenClaw environments that store transcripts under an agents root with `sessions/sessions.json` indexes.
- If your deployment differs, use `--base` and `--session-key-template`.
- If your prompts are not Chinese, replace the assignment keyword and field prefixes.
- Prefer `json` or `jsonl` when integrating with other automation.
