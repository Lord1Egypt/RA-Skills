# Snapshot Mode

To make hourly and multi-hour CLS queries reliable, V1.1 adds local snapshot storage.

## Default cadence

Recommended default: every 30 minutes.

## Snapshot command

```bash
python3 skills/cailianpress-unified/scripts/cls_snapshot.py
```

This stores the current CLS telegraph window into:

```text
skills/cailianpress-unified/data/telegraph_snapshots.jsonl
```

## Query local history

```bash
python3 skills/cailianpress-unified/scripts/cls_history_query.py telegraph --hours 1
python3 skills/cailianpress-unified/scripts/cls_history_query.py red --hours 24
python3 skills/cailianpress-unified/scripts/cls_history_query.py hot --hours 2 --min-reading 50000
```

## Suggested cron

```cron
*/30 * * * * cd /home/tim/.openclaw/workspace && python3 skills/cailianpress-unified/scripts/cls_snapshot.py >> /tmp/cls_snapshot.log 2>&1
```

## Notes

- This mode complements the live NodeAPI window.
- It is the recommended way to support stable 1-hour / 24-hour historical queries.
- Dedupe is done by `id`, keeping the latest `ctime` version.
