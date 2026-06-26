# Analysis Patterns & Known Issue Cross-Reference

## Known Patterns to Check

Cross-reference telemetry results against `memory/amg-check-pg-flex/report.md` before presenting findings.

### Connection Storm / Thundering Herd

A fleet-wide connection surge where all Grafana instances simultaneously increase their DB connection rate. This is the most common cause of PostgreSQL CPU spikes in the AMG fleet.

**Signals in telemetry:**
- CPU jumps from baseline to >95% within a single 5-minute interval
- Log volume triples (e.g., 23K to 77K per 5 minutes)
- Connection rate per host jumps 3-4x while distinct host count stays the same
- Massive "PID xxx in cancel request did not match any process" messages
- Network egress spikes 2-3x while IOPS stays flat (CPU-bound, not I/O-bound)

**Investigation technique:**
1. Check session duration distribution before and during spike
2. If timeout sessions (30s) dominate before the spike, it's a pre-existing illness amplified by retry storms
3. If fast sessions (<1s) explode during the spike, a new workload triggered the storm
4. Check per-host and per-database connection rates to determine if it's fleet-wide or single-tenant

### 30-Second Session Timeout Pattern

Grafana instances use a 30-second query timeout. When many sessions cluster at exactly 30.0xx seconds, it indicates queries are timing out rather than completing.

**Signals:**
- Disconnection log session times clustered at `0:00:30.0xx`
- High timeout percentage (>50% of all sessions)
- Cancel requests that don't match any process (query already timed out and was cleaned up)

**Impact:** Each 30-second timeout holds a connection slot and a backend process for the full 30 seconds, consuming CPU even though no useful work is done.

### Backend Process Crash

PostgreSQL postmaster detects a crashed backend process and terminates all connections for safety.

**Signals:**
- WARNING: `terminating connection because of crash of another server process`
- Detail: `The postmaster has commanded this server process to roll back the current transaction and exit, because another server process exited abnormally and possibly corrupted shared memory.`
- Immediate forced checkpoint after crash
- Active connections drop to zero then recover
- Often resolves a preceding CPU spike (the crash breaks the feedback loop)

**Investigation:** Check if the crash was caused by OOM (out of memory), a buggy extension, or resource exhaustion. The specific crashed PID may not appear in AzureDiagnostics — check if memory_percent was high before the crash.

### Provisioning Retry Noise

When RP Worker retries Grafana instance provisioning, it attempts to create roles and databases that may already exist.

**Signals:**
- ERROR: `role "owner_role_grafana_<id>" already exists`
- ERROR: `role "user_grafana_<id>" already exists`
- ERROR: `database "db_grafana_<id>" already exists`
- These come in batches of 3-4 errors at regular intervals

**Impact:** Low — these are harmless retries. But if frequent, they indicate the RP Worker is stuck retrying a failed provisioning.

### Dashboard Usage Stats Write Contention

Multiple Grafana instances concurrently inserting into the `dashboard_usage_sums` table.

**Signals:**
- ERROR: `duplicate key value violates unique constraint "dashboard_usage_sums_pkey"`
- Detail: `Key (dashboard_id)=(N) already exists`

**Impact:** Medium — indicates concurrent write conflicts. Each conflict wastes a transaction. High volumes suggest a Grafana bug in usage stats collection.

### Missing Function: pg_last_removed_wal_lsn()

A monitoring query calls `public.pg_last_removed_wal_lsn()` which doesn't exist on the current PostgreSQL version.

**Signals:**
- ERROR: `function public.pg_last_removed_wal_lsn() does not exist at character 80`
- Occurs every ~30 seconds continuously

**Impact:** Low — pure noise. Does not affect server performance. Should be fixed in the monitoring configuration.

### Idle Session Timeout Misconfiguration

Connection attempts with `idle_session_timeout` parameter that isn't supported on the current PostgreSQL version.

**Signals:**
- ERROR: `unrecognized configuration parameter "idle_session_timeout"`

**Impact:** Low — the connection likely falls back to defaults. May indicate a version mismatch between Grafana config and PG server.

## Analysis Techniques

### Identifying the Spike Trigger

When a CPU spike is detected:

1. **Check log volume per minute** around the onset — a sharp jump in log volume precedes or coincides with CPU rise
2. **Compare connection rate per host** before vs during — if all hosts increase uniformly, it's fleet-wide; if one host spikes, it's single-tenant
3. **Check session duration distribution** — shift from fast to timeout or vice versa reveals the workload change
4. **Check for provisioning activity** — role/database creation errors indicate RP Worker operations
5. **Check for checkpoint frequency** — more frequent checkpoints indicate higher write load

### Timeout Amplification Detection

A modest server slowdown can be amplified into a CPU crisis by retry logic:

1. Server gets slightly slow (maybe from a checkpoint or vacuum)
2. More queries hit the 30-second timeout
3. Grafana retries timed-out queries, creating more connections
4. More connections = more CPU overhead (TLS, auth, query processing)
5. Server gets even slower, more timeouts, more retries
6. Feedback loop drives CPU to 100%

**Detection:** Compare the absolute number of timeout sessions before and during the spike. If timeouts increased, it's amplification. If fast sessions increased, it's a new workload.

### Post-Crash Baseline Comparison

After a crash-restart cycle, compare the new baseline CPU/connections to the pre-spike baseline:
- **Lower CPU after crash**: The crash killed a problematic workload that hasn't reconnected
- **Same CPU after crash**: The issue is systemic and will likely recur
- **Fewer connections after crash**: Some clients didn't reconnect — may need manual restart of affected Grafana instances
