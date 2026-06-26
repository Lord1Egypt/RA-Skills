# Swarm Lead — Heartbeat Checks

## On Every Heartbeat

### 1. Check Active Agents
```bash
tmux ls 2>/dev/null
```
- If agents running: check for stuck sessions (>45 min with no new commits)
- If stuck: run `pulse-check.sh` or check tmux pane output

### 2. Check Pending Notifications
```bash
cat ~/workspace/swarm/pending-notifications.txt 2>/dev/null
```
- If notifications pending: process them (merge PRs, notify WB, clean up)
- Clear processed notifications

### 3. Check Integration Watchers
```bash
ps aux | grep integration-watcher | grep -v grep
```
- If integration watcher running but all agents done: check if it's stuck
- If no watcher but agents finishing: alert — may need manual integration

### 4. Weekly Assessment (Mondays)
- Run `assess-models.sh` to check Codex/Gemini quota status
- Update duty table if needed
- Report any changes to WB

## Rules
- If agents are running fine: HEARTBEAT_OK
- If something needs attention: handle it, don't just report
- If waiting for WB input: skip swarm checks, HEARTBEAT_OK
