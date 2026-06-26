# openclaw Session Inspection — execute_code Pattern

Use `execute_code` (subprocess.run) instead of terminal piping to python.
Shell pipes to python3 time out on `openclaw sessions --json`.

## Session Audit — Full Pattern

```python
import json, subprocess

result = subprocess.run(
    ['openclaw', 'sessions', '--agent', 'AGENT_NAME', '--limit', '10', '--json'],
    capture_output=True, text=True, timeout=30
)

data = json.loads(result.stdout)
sessions = data if isinstance(data, list) else data.get('sessions', [])

for s in sessions:
    kind = s.get('kind', '?')
    model = s.get('model', '?')
    total = s.get('totalTokens', 0) or 0
    inp   = s.get('inputTokens', 0) or 0
    out   = s.get('outputTokens', 0) or 0
    cache = total - inp - out
    cache_pct = f'{cache*100//total}%' if total else 'N/A'
    reply = s.get('replyStatus', s.get('status', '?'))
    print(f'{kind:12} {model:15} total={total:6} inp={inp:5} out={out:4} cache={cache:6}({cache_pct}) reply={reply}')
```

Key fields: `kind` (direct/cron/spawn-child/group), `model`, `totalTokens`, `inputTokens`, `outputTokens`, `replyStatus`.

Cache-dominant sessions (cache > 80% of total): high totalTokens is misleading — incremental cost = input + output only.

## Cron Job Inspection

```python
result = subprocess.run(
    ['openclaw', 'cron', 'list', '--agent', 'AGENT_NAME', '--json'],
    capture_output=True, text=True, timeout=20
)
data = json.loads(result.stdout)
jobs = data.get('jobs', [])
for j in jobs:
    print(j['name'], j['schedule']['expr'], j['enabled'])
```

Known working subcommands:
- `openclaw sessions --agent X --limit N --json` ✓
- `openclaw cron list --agent X --json` ✓
- `openclaw jobs --agent X` ✗ (unknown command)

## NO_REPLY Signal

If a task returns many `NO_REPLY` results while still consuming tokens, treat as strong token-waste signal unless there is clear evidence that NO_REPLY itself is a valuable expected output.
