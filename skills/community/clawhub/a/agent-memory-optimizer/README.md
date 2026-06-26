# Agent Memory Optimizer

Archive old daily memory files into month folders so active memory remains small, fast to search, and cheaper in prompt tokens.

## Install

Copy this folder into your OpenClaw workspace skills:

```text
<workspace>/skills/agent-memory-optimizer/
```

OpenClaw loads workspace skills on the next session.

## Usage

From the skill folder:

```bash
python3 scripts/agent_memory_optimizer.py --dry-run
python3 scripts/agent_memory_optimizer.py
```

## Behavior

- Source: `~/.openclaw/workspace/memory/*.md` (default)
- Target: `~/.openclaw/workspace/memory/archive/YYYY-MM/`
- Default cutoff: archive months older than current month
- Idempotent: reruns do not duplicate files

## Options

```text
--memory-dir PATH   Memory directory (default: ~/.openclaw/workspace/memory)
--before YYYY-MM    Archive months older than this month
--dry-run           Preview file moves without changes
```

## Data and privacy

- No API keys required
- No network calls
- No personal data hardcoded
- Operates only on local files you point it at

## License

MIT-0
