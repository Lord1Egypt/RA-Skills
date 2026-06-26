# Replay and Analysis

How to search, replay, and analyze Guardian Audit trails.

## Basic Queries

```bash
# Show last 20 events
tail -n 20 audit.log | jq -c '{timestamp, event_type, operation, decision}'

# Show all halts
grep 'GUARDIAN_HALT' audit.log | jq -c '{timestamp, operation, target, approver}'

# Show events for specific target
grep '/tmp/old-builds' audit.log | jq .

# Show approval rate
TOTAL=$(wc -l < audit.log)
APPROVED=$(grep 'PROCEED' audit.log | wc -l)
echo "Approval rate: $((APPROVED * 100 / TOTAL))%"
```

## Chain Verification

```bash
python3 scripts/verify-chain.py audit.log
# Output:
# Chain valid: 1,247 entries
# Last hash: 9e2b4c6d...
# Verification time: 23ms
```

## Pattern Analysis

```bash
# Most common halted operations
grep 'GUARDIAN_HALT' audit.log | jq -r '.operation' | sort | uniq -c | sort -rn | head -10

# Agents with most escalations
grep 'AWAITING_HUMAN' audit.log | jq -r '.agent_id' | sort | uniq -c | sort -rn

# Backup failure reasons
grep 'UNVERIFIED' audit.log | jq -r '.guardian_notes' | grep -o 'no [^,]*' | sort | uniq -c
```

## Compliance Report

```bash
python3 scripts/export-report.py audit.log --format markdown --start 2026-05-01 --end 2026-05-31
# Generates:
# - Event summary table
# - Decision breakdown pie chart data
# - Agent escalation frequency
# - Backup coverage statistics
# - Chain integrity statement
```

## Incident Replay

When something goes wrong:

```bash
# Extract complete timeline for an incident
python3 scripts/replay.py audit.log --target "/data/production" --before "2026-05-18T14:05:00Z" --window 300

# Output:
# 14:02:31 GUARDIAN_HALT  rm -rf /data/production/old  (backup: UNVERIFIED)
# 14:03:15 ESCALATION_RESOLVED  human APPROVED with note: "Emergency cleanup approved"
# 14:03:16 EXECUTED  rm -rf /data/production/old  outcome: SUCCESS
# 14:04:00 CHAIN_VERIFICATION  integrity: PASS
```
