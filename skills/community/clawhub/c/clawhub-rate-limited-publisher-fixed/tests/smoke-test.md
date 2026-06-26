# Smoke Test

## Preconditions
- `python3 --version`
- `clawhub whoami`
- target skill folder exists and contains `SKILL.md`

## Dry run
```bash
python3 scripts/clawhub_rate_limited_uploader.py --queue examples/queue.sample.json --dry-run
```

Expected:
- prints rolling-window counter
- prints next skill path
- prints the exact `clawhub publish` command
- exits 0

## Execute
```bash
python3 scripts/clawhub_rate_limited_uploader.py --queue examples/queue.sample.json --execute
```

Expected:
- at most one publish attempt per run
- state file `.publisher-state.json` is created next to queue file
- success marks item as `published`
- failure marks item as `failed` and still counts toward hourly cap

## Rate limit verification
Run the execute command repeatedly more than 5 times in an hour.

Expected:
- after 5 attempts in rolling 3600 seconds, script exits 0 without publishing
- it reports roughly how many seconds remain until the next slot
