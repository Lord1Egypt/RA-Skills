# Swarm Lead — Heartbeat Checks

## Agent Swarm Notifications — top priority

### 1. Read pending notifications

```bash
cat ~/workspace/swarm/pending-notifications.txt
```

If it has content: send each line to the human/operator, then clear the file:

```bash
> ~/workspace/swarm/pending-notifications.txt
```

Clear only after sending.

### 2. Run pulse check

```bash
~/workspace/swarm/pulse-check.sh
```

This detects stuck agents: auth prompts, no output change for 30+ minutes, error loops. If it kills or flags anything, it writes to `pending-notifications.txt`; send those lines too.

### 3. Check tmux sessions

```bash
tmux ls
```

If expected agent sessions disappeared, inspect swarm logs/project git log and notify with what completed.

### 4. If agents are active

Report a brief status such as: “3 agents still running; latest output looks healthy.”

## Weekly model assessment

- Cron is primary; heartbeat is backup.
- Check `~/workspace/swarm/duty-table.json`.
- Do not run model rescans opportunistically on every heartbeat.
- Only run `assess-models.sh` when:
  1. `nextAssessment` has passed, and
  2. the scheduled weekly window was genuinely missed/overdue.
- Manual/on-demand assessment is allowed when the operator asks or when diagnosing a model issue.

## Rules

- If notifications or actionable stuck-agent issues exist, do **not** reply `HEARTBEAT_OK`.
- If nothing is actionable, reply `HEARTBEAT_OK`.
