---
name: agent-task-status
description: Verify whether named OpenClaw agents actually received formal task assignments and replied with execution status, using transcript-backed audit checks. Use when auditing real delegation, confirming assignment delivery to specific agents, reviewing recent task completion, checking whether an agent replied after being assigned work, or troubleshooting multi-agent routing from session transcripts. Especially useful for requests like “检查小程/小文/小编有没有收到任务”, “确认任务有没有真正派到 agent 本人”, “看看这些 agent 执行到哪一步”, “汇总最近派单情况”, or “排查多 agent 调度是否真的落到本人并形成回报闭环”.
---

# Agent Task Status

Use the bundled script to inspect OpenClaw session indexes and transcript files, then extract the latest assignment and structured report for each target agent.

## Quick start

Run the script directly:

```bash
python3 /home/lyqadmin/.openclaw/workspace/skills/agent-task-status/scripts/check_agent_task_status.py --format summary
```

For more examples, read `references/usage.md`.

## Workflow

1. Decide which agents to inspect.
   - Use `--agents a,b,c` for explicit targets.
   - Use `--agent-file` when the list comes from a file.
   - Use `--discover` when the deployment has many agents under the same root.
2. Set the agent storage root.
   - Default is `~/.openclaw/agents`.
   - Override with `--base` or `OPENCLAW_AGENTS_BASE` in non-default environments.
3. Match the session shape.
   - Default session key template is `agent:{agent}:main`.
   - Override with `--session-key-template` if your target sessions use another pattern.
4. Match the assignment/report language.
   - Default assignment keyword is `正式任务分配：`.
   - Default report prefixes are `任务：` / `状态：` / `结果：` / `风险：`.
   - Override these when the team uses different markers or another language.
5. Filter the output when needed.
   - `--only-status` filters by normalized status such as `completed`, `blocked`, `accepted`, `no-assignment`, `assigned-no-report`, `error`.
   - `--contains` filters by keyword across assignment text, parsed task, result, and risk.
6. Pick an output format.
   - `table`: best for human inspection
   - `summary`: compact overview
   - `json`: structured automation output
   - `jsonl`: line-oriented pipelines
7. Use `--strict` for CI/automation.
   - Exit `0`: normal
   - Exit `1`: partial problem such as missing assignment/report or agent error
   - Exit `2`: script/runtime error
8. Use `--output-file` to persist results for later review or downstream automation.

## Recommended commands

Human-readable table:
```bash
python3 /home/lyqadmin/.openclaw/workspace/skills/agent-task-status/scripts/check_agent_task_status.py --agents xiaocheng,xiaowen,xiaobian --format table
```

Only completed tasks:
```bash
python3 /home/lyqadmin/.openclaw/workspace/skills/agent-task-status/scripts/check_agent_task_status.py --discover --only-status completed --format summary
```

Filter by keyword:
```bash
python3 /home/lyqadmin/.openclaw/workspace/skills/agent-task-status/scripts/check_agent_task_status.py --discover --contains 自动化 --format table
```

Automation JSON:
```bash
python3 /home/lyqadmin/.openclaw/workspace/skills/agent-task-status/scripts/check_agent_task_status.py --agent-file ./agents.txt --format json --strict --output-file ./agent-status.json
```

## What to inspect in the output

- `sessionKey`: which session was used
- `sessionFile`: exact transcript file path
- `assignedAt` / `assignText`: when and what was assigned
- `reportAt`: when the agent reported back
- `task` / `status_raw` / `status_normalized` / `result` / `risk`: parsed structured fields
- `error`: why the check failed for that agent

## Limitations

- This skill assumes an OpenClaw-style agent root with `sessions/sessions.json` and transcript `sessionFile` paths.
- It only checks the target session pattern you specify; it does not automatically infer every possible routing form.
- If the assignment keyword or report field prefixes change, you must override them.
- It reports what is present in transcripts; it does not infer hidden work with no assignment/report markers.
