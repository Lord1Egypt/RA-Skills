# Memory commit checklist — “memorize this” workflow

Trigger phrases: “memorize this”, “store this”, “commit this session”, “we’ll continue later”.

## 1. Append to today’s daily log
```bash
cd ~/.openclaw/workspace
cat <<'EOF' >> memory/$(date -u +%Y-%m-%d).md
- <brief summary of what happened>
- Decisions:
  - <bullet>
- Follow-ups:
  - <bullet>
EOF
```
(Use UTC date; create the file if it doesn’t exist.)

## 2. Update `memory/now.md`
Keep a short, current-state list. Example:
```
## Current focus
- Manual dr-trading-system run pending (awaiting market-data-provider smoke test).
- Repo permissions: need GitHub push access for Hannah.
```

## 3. Update `memory/open-loops.md`
Add actionable follow-ups with owners/status. Example:
```
### Trading system
- [ ] Verify GitHub push permissions (blocked on access request).
- [ ] Schedule daily report once manual run validated.
```

## 4. Create/update the relevant topic file
If a topic exists, edit it; otherwise create one under `memory/topics/`. Example (`memory/topics/stock-modules.md`):
```
## Modules
- market-data-provider → fetch/normalize data only
...
## Contracts
- strategy-engine depends on market-data-provider
...
```

## 5. Record durable rules in `MEMORY.md`
Add a short bullet under the appropriate section, e.g.:
```
## Standing operating rules
- Stock-system modules are maintained independently with stable contracts (see memory/topics/stock-modules.md).
```

## 6. Confirm
- Run `python3 ./skills/dr-context-pipeline/scripts/memory_watchdog.py --freshness-minutes 240 --min-bytes 200` to ensure files exist.
- Mention in chat that the session was committed and list which files changed.
