---
name: database-replication-advisor
description: Analyze database replication topology, detect lag, and recommend replication strategy based on CAP tradeoffs
---

# Database Replication Advisor

Analyze the health and design of database replication setups. This skill teaches an AI agent to inspect replication lag, evaluate topology choices (single-leader, multi-leader, leaderless), assess failover readiness, and recommend replication strategies grounded in CAP theorem tradeoffs and real operational constraints.

Use when: "check replication lag", "replication health", "failover readiness", "replication topology", "CAP tradeoffs", "design replication", "replica drift", "split-brain risk", "failover drill"

## Commands

### 1. `assess` -- Check current replication health

Inspect the running replication state, measure lag, detect divergence, and flag risks.

#### Step 1: Identify the database engine and topology

```bash
# PostgreSQL: check if this is a primary or standby
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "SELECT pg_is_in_recovery();"

# PostgreSQL: list replication slots and connected standbys
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "
SELECT slot_name, slot_type, active, restart_lsn
FROM pg_replication_slots;
"

# MySQL: check replication status on a replica
mysql -h "$REPLICA_HOST" -u "$DB_USER" -p"$DB_PASS" -e "SHOW REPLICA STATUS\G"

# Redis: check replication info
redis-cli -h "$REDIS_HOST" INFO replication
```

#### Step 2: Measure replication lag

Lag is the most critical replication health metric. Measure it from both the database internals and from application-level probes.

```bash
# PostgreSQL: lag in bytes and seconds for each standby
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "
SELECT client_addr,
       state,
       sent_lsn,
       write_lsn,
       flush_lsn,
       replay_lsn,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag,
       replay_lag
FROM pg_stat_replication;
"

# MySQL: seconds behind primary
mysql -h "$REPLICA_HOST" -u "$DB_USER" -p"$DB_PASS" -e "
SELECT
  CHANNEL_NAME,
  SOURCE_UUID,
  LAST_APPLIED_TRANSACTION_END_APPLY_TIMESTAMP,
  APPLYING_TRANSACTION,
  LAST_APPLIED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP
FROM performance_schema.replication_applier_status_by_worker;
"

# Application-level heartbeat probe (write timestamp to primary, read from replica)
python3 -c "
import time, psycopg2

primary = psycopg2.connect(host='$PRIMARY_HOST', dbname='$DB_NAME', user='$DB_USER')
replica = psycopg2.connect(host='$REPLICA_HOST', dbname='$DB_NAME', user='$DB_USER')

# Write heartbeat to primary
with primary.cursor() as cur:
    cur.execute('CREATE TABLE IF NOT EXISTS _repl_heartbeat (id int PRIMARY KEY, ts timestamptz)')
    cur.execute('INSERT INTO _repl_heartbeat VALUES (1, now()) ON CONFLICT (id) DO UPDATE SET ts = now()')
    primary.commit()
    cur.execute('SELECT ts FROM _repl_heartbeat WHERE id = 1')
    write_ts = cur.fetchone()[0]

time.sleep(0.5)

# Read heartbeat from replica
with replica.cursor() as cur:
    cur.execute('SELECT ts FROM _repl_heartbeat WHERE id = 1')
    read_ts = cur.fetchone()[0]

lag = (write_ts - read_ts).total_seconds() if write_ts > read_ts else 0
print(f'Application-level replication lag: {lag:.3f}s')
print(f'Assessment: {\"HEALTHY\" if lag < 1 else \"WARNING\" if lag < 10 else \"CRITICAL\"}')
"
```

#### Step 3: Check for replication conflicts and errors

```bash
# PostgreSQL: check for replication conflicts (queries cancelled on standby)
psql -h "$REPLICA_HOST" -U "$DB_USER" -d "$DB_NAME" -c "
SELECT datname, confl_tablespace, confl_lock, confl_snapshot, confl_bufferpin, confl_deadlock
FROM pg_stat_database_conflicts
WHERE datname = '$DB_NAME';
"

# PostgreSQL: check WAL archiving health on primary
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "
SELECT archived_count, failed_count, last_archived_wal, last_archived_time, last_failed_time
FROM pg_stat_archiver;
"

# MySQL: check for replication errors
mysql -h "$REPLICA_HOST" -u "$DB_USER" -p"$DB_PASS" -e "
SELECT LAST_ERROR_NUMBER, LAST_ERROR_MESSAGE, LAST_ERROR_TIMESTAMP
FROM performance_schema.replication_applier_status_by_worker
WHERE LAST_ERROR_NUMBER != 0;
"
```

#### Step 4: Evaluate network and disk bottlenecks

```bash
# Check WAL generation rate on primary (PostgreSQL)
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "
SELECT pg_wal_lsn_diff(pg_current_wal_lsn(), '0/0') / (1024*1024*1024) AS total_wal_gb,
       pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) / (1024*1024) AS pending_mb
FROM pg_stat_replication;
"

# Check disk I/O on replica
iostat -x 1 3 | tail -20

# Check network latency between primary and replica
ping -c 5 "$REPLICA_HOST" | tail -1
```

#### Report template

```
## Replication Health Assessment

**Date:** YYYY-MM-DD
**Engine:** PostgreSQL 16 / MySQL 8 / Redis 7
**Topology:** Single-leader with 2 async standbys

### Replication Status
| Replica | State | Byte Lag | Time Lag | Conflicts | Verdict |
|---------|-------|----------|----------|-----------|---------|
| replica-1 | streaming | 1.2 MB | 0.3s | 0 | HEALTHY |
| replica-2 | streaming | 45 MB | 8.2s | 12 | WARNING |

### Risk Assessment
- **Data loss window (RPO):** ~8s (worst replica lag)
- **Failover time estimate (RTO):** ~30s (manual), ~5s (Patroni/orchestrator)
- **Split-brain risk:** LOW (single leader, no multi-master)
- **WAL accumulation:** Normal (archiving healthy)

### Recommendations
1. Investigate replica-2 lag -- likely disk I/O bottleneck (iostat shows 95% util)
2. Consider synchronous replication for replica-1 if zero-data-loss RPO required
3. Add replication lag alerting at 5s threshold
```

---

### 2. `design` -- Recommend replication topology

Given application requirements, recommend the right replication strategy with explicit CAP tradeoff analysis.

#### Step 1: Gather requirements

The agent must determine these constraints before recommending a topology:

```
1. Read/write ratio (read-heavy? write-heavy? balanced?)
2. Geographic distribution (single region? multi-region?)
3. Consistency requirement (strong? eventual? causal?)
4. Durability requirement (zero data loss? seconds acceptable?)
5. Availability target (99.9%? 99.99%? 99.999%?)
6. Write throughput (transactions per second)
7. Budget constraints (how many replicas can you afford?)
```

#### Step 2: Apply the decision framework

```python
import json

def recommend_topology(requirements):
    """Recommend replication topology based on requirements."""
    read_heavy = requirements.get("read_write_ratio", 10) > 5
    multi_region = requirements.get("multi_region", False)
    strong_consistency = requirements.get("consistency") == "strong"
    zero_data_loss = requirements.get("max_data_loss_seconds", 5) == 0
    high_write_throughput = requirements.get("writes_per_second", 100) > 5000

    recommendation = {}

    # Topology selection
    if multi_region and not strong_consistency:
        recommendation["topology"] = "multi-leader"
        recommendation["rationale"] = (
            "Multi-region with eventual consistency favors multi-leader. "
            "Each region has a local leader for low-latency writes. "
            "Conflict resolution required (last-writer-wins or custom)."
        )
        recommendation["cap_choice"] = "AP (availability + partition tolerance)"
    elif high_write_throughput and not strong_consistency:
        recommendation["topology"] = "leaderless (Dynamo-style)"
        recommendation["rationale"] = (
            "High write throughput with eventual consistency suits leaderless replication. "
            "Use quorum reads/writes (W + R > N) for tunable consistency."
        )
        recommendation["cap_choice"] = "AP with tunable consistency via quorums"
    else:
        recommendation["topology"] = "single-leader"
        recommendation["rationale"] = (
            "Single leader is the safest default. Strong consistency via synchronous replication, "
            "read scaling via async replicas."
        )
        recommendation["cap_choice"] = "CP (consistency + partition tolerance)"

    # Sync mode selection
    if zero_data_loss:
        recommendation["sync_mode"] = "synchronous (at least one sync standby)"
        recommendation["tradeoff"] = "Higher write latency, but guaranteed zero RPO"
    else:
        recommendation["sync_mode"] = "asynchronous"
        recommendation["tradeoff"] = f"Possible data loss up to {requirements.get('max_data_loss_seconds', 5)}s, but lower write latency"

    # Replica count
    if read_heavy:
        recommendation["min_replicas"] = max(2, requirements.get("read_write_ratio", 10) // 5)
        recommendation["replica_note"] = "Read replicas sized to absorb read traffic"
    else:
        recommendation["min_replicas"] = 1
        recommendation["replica_note"] = "Single replica for failover, not load distribution"

    return recommendation

reqs = {
    "read_write_ratio": 20,
    "multi_region": False,
    "consistency": "strong",
    "max_data_loss_seconds": 0,
    "writes_per_second": 500
}
result = recommend_topology(reqs)
print(json.dumps(result, indent=2))
```

#### Step 3: Validate against infrastructure

```bash
# Check current DB instance specs to verify replicas can handle load
# AWS RDS example
aws rds describe-db-instances --query 'DBInstances[*].{ID:DBInstanceIdentifier,Class:DBInstanceClass,Engine:Engine,MultiAZ:MultiAZ,ReadReplicas:ReadReplicaDBInstanceIdentifiers}' --output table

# Check available storage and IOPS
aws rds describe-db-instances --db-instance-identifier "$DB_INSTANCE" --query 'DBInstances[0].{Storage:AllocatedStorage,IOPS:Iops,StorageType:StorageType}'

# Check cross-region latency (for multi-region decisions)
for region in us-east-1 eu-west-1 ap-southeast-1; do
  echo -n "$region: "
  ping -c 3 "ec2.$region.amazonaws.com" 2>/dev/null | tail -1 | awk -F'/' '{print $5 "ms"}'
done
```

#### Report template

```
## Replication Design Recommendation

**Application:** [service-name]
**Current state:** Single PostgreSQL instance, no replication

### Requirements Analysis
- Read/write ratio: 20:1 (read-heavy)
- Regions: Single (us-east-1)
- Consistency: Strong required for financial transactions
- Max acceptable data loss: 0 seconds
- Availability target: 99.99%

### Recommended Topology
**Single-leader with 1 synchronous + 2 asynchronous standbys**

### CAP Tradeoff
Choosing CP: consistency and partition tolerance. During a network partition, writes block rather than risk inconsistency. This is correct for financial data.

### Architecture
```
Primary (us-east-1a) --sync--> Standby-1 (us-east-1b) [failover target]
                     --async-> Standby-2 (us-east-1c) [read replica]
                     --async-> Standby-3 (us-east-1c) [read replica]
```

### Configuration
- `synchronous_standby_names = 'FIRST 1 (standby1)'`
- `max_wal_senders = 10`
- `wal_level = replica`
- `hot_standby = on`
- Connection pooler (PgBouncer) routing reads to standbys
```

---

### 3. `failover-test` -- Plan and validate a failover drill

Design a safe failover test, define success criteria, and provide runbooks for both automated and manual failover.

#### Step 1: Pre-flight checks

```bash
# Ensure replication is healthy before testing failover
psql -h "$PRIMARY_HOST" -U "$DB_USER" -d "$DB_NAME" -c "
SELECT client_addr, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication;
"

# Verify the failover target is caught up (lag < 1MB)
lag=$(psql -h "$PRIMARY_HOST" -U "$DB_USER" -d "$DB_NAME" -t -c "
SELECT pg_wal_lsn_diff(sent_lsn, replay_lsn)
FROM pg_stat_replication WHERE client_addr = '$FAILOVER_TARGET_IP';
")
if [ "$lag" -gt 1048576 ]; then
  echo "ABORT: Failover target has ${lag} bytes lag. Wait for it to catch up."
  exit 1
fi
echo "Pre-flight OK: lag is ${lag} bytes"

# Check Patroni cluster state (if using Patroni)
patronictl -c /etc/patroni.yml list

# Check connection pool state
pgbouncer -d "$PGBOUNCER_DB" -c "SHOW POOLS;"
```

#### Step 2: Define the failover procedure

```bash
# Option A: Patroni-managed failover (preferred)
patronictl -c /etc/patroni.yml switchover --master "$PRIMARY_NAME" --candidate "$STANDBY_NAME" --force

# Option B: Manual PostgreSQL failover
# 1. Stop writes on primary (set to read-only)
psql -h "$PRIMARY_HOST" -U "$DB_USER" -c "ALTER SYSTEM SET default_transaction_read_only = on; SELECT pg_reload_conf();"
# 2. Wait for standby to fully catch up
# 3. Promote the standby
psql -h "$STANDBY_HOST" -U "$DB_USER" -c "SELECT pg_promote();"
# 4. Repoint application connection strings or update DNS/proxy

# Option C: AWS RDS failover
aws rds failover-db-cluster --db-cluster-identifier "$CLUSTER_ID" --target-db-instance-identifier "$FAILOVER_TARGET"
```

#### Step 3: Validate failover success

```bash
# Check new primary is accepting writes
psql -h "$NEW_PRIMARY" -U "$DB_USER" -d "$DB_NAME" -c "
CREATE TABLE _failover_test_$(date +%s) (id int);
DROP TABLE _failover_test_$(date +%s);
SELECT 'WRITES OK' AS status;
"

# Check old primary is no longer primary
psql -h "$OLD_PRIMARY" -U "$DB_USER" -d "$DB_NAME" -c "SELECT pg_is_in_recovery();"
# Should return: t (true = standby)

# Check application connectivity
curl -s "$APP_HEALTH_ENDPOINT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
db_status = data.get('database', {}).get('status', 'unknown')
print(f'Application DB status: {db_status}')
assert db_status == 'healthy', 'Application not connected to new primary!'
"

# Measure total downtime
echo "Failover started at: $FAILOVER_START"
echo "First successful write at: $(date -Iseconds)"
echo "Total downtime: calculate difference"
```

#### Step 4: Post-failover recovery

```bash
# Rebuild old primary as a new standby
# PostgreSQL: use pg_rewind if timeline hasn't diverged too far
pg_rewind --target-pgdata=/var/lib/postgresql/data --source-server="host=$NEW_PRIMARY dbname=$DB_NAME user=$DB_USER"

# Verify the new standby is streaming
psql -h "$NEW_PRIMARY" -U "$DB_USER" -d "$DB_NAME" -c "SELECT * FROM pg_stat_replication;"
```

#### Report template

```
## Failover Drill Report

**Date:** YYYY-MM-DD
**Trigger:** Planned drill / Unplanned incident
**Engine:** PostgreSQL 16 with Patroni

### Timeline
| Event | Timestamp | Duration |
|-------|-----------|----------|
| Failover initiated | 14:00:00 | - |
| Old primary stopped accepting writes | 14:00:02 | 2s |
| New primary promoted | 14:00:05 | 3s |
| Application reconnected | 14:00:08 | 3s |
| **Total write downtime** | - | **8 seconds** |

### Success Criteria
- [x] Total downtime < 30 seconds (actual: 8s)
- [x] Zero data loss (sync replication confirmed)
- [x] Application auto-reconnected without manual intervention
- [x] Old primary successfully rebuilt as standby
- [ ] Alerting fired within 60 seconds (actual: 90s -- needs tuning)

### Findings
1. Application connection pool took 3s to detect primary change -- consider reducing health check interval
2. Alerting delay of 90s -- adjust PagerDuty integration threshold
3. Old primary rewind completed in 45s -- acceptable

### Action Items
- [ ] Reduce PgBouncer server_check_delay from 30s to 5s
- [ ] Tune monitoring alert threshold to < 60s detection
- [ ] Schedule next drill in 90 days
```
