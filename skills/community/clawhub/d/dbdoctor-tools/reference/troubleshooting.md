# Common Issues and Solutions

## 1. Instance Management Failed: Host is blocked

**Error Information**:
```
Host '10.18.210.10' is blocked because of many connection errors; unblock with 'mysqladmin flush-hosts'
```

**Cause**:
MySQL's `max_connect_errors` security mechanism is triggered. When a client host fails to connect more than the threshold times, MySQL automatically blocks that host.

**Solution**:

Execute either of the following commands on the target MySQL server:

```sql
-- Method 1: Execute inside MySQL
FLUSH HOSTS;
```

```bash
# Method 2: Execute via command line
mysqladmin -u root -p flush-hosts
```

**Permanent Solution**: Adjust MySQL configuration to increase threshold
```sql
-- View current threshold
SHOW VARIABLES LIKE 'max_connect_errors';

-- Increase threshold (e.g., to 10000)
SET GLOBAL max_connect_errors = 10000;
```

Add to `my.cnf`:
```ini
[mysqld]
max_connect_errors = 10000
```

---

## 2. SQL Rewrite Result is Empty

**Phenomenon**: After calling `ai_sql_rewrite`, `get_sql_rewrite_result` returns `content: null`

**Cause**: AI rewrite service responds slowly or is temporarily unavailable

**Solution**:
- Wait longer and retry
- Manually provide optimization suggestions based on SQL audit results (recommended)

**Manual Optimization Suggestions Example**:
```sql
-- Original SQL
SELECT * FROM test_ref_a WHERE a = 1

-- Optimization Plan 1: Specify fields
SELECT id, a, b, c FROM test_ref_a WHERE a = 1

-- Optimization Plan 2: Add index (recommended)
ALTER TABLE test_ref_a ADD INDEX idx_a(a), ALGORITHM=INPLACE, LOCK=NONE;
```

---

## 3. Instance Status Abnormal but No Alerts

**Phenomenon**: Instance is marked as "abnormal", but alert query list is empty

**Cause**: Abnormalities may be issues found during inspection, not real-time alerts

**Solution**:
- Execute instance inspection to get detailed report
- View problem items in inspection report

```bash
# Execute inspection
python scripts/do_inspect_instance.py --instance-id [instance_id] --tenant [tenant] --project [project]

# Get inspection report
python scripts/get_recent_inspect_report.py --instance-id [instance_id] --start-time [start] --end-time [now] --tenant [tenant] --project [project]
```

---

## 4. Timestamp Format Issue

**Error Phenomenon**: Query time range returns no results or error

**Common Issues**:
- Using millisecond timestamp (should be second level)
- Unreasonable time range setting

**Correct Format**:
```bash
# Get current timestamp (second level)
now=$(python3 -c "import time; print(int(time.time()))")

# Get timestamp for one week ago
start=$(python3 -c "import time; print(int(time.time() - 604800))")

# Query using timestamps
python scripts/get_slow_sql.py --instance-id xxx --start-time $start --end-time $now
```

**Common Time Ranges**:

| Time Range | Seconds |
|---------|------|
| Last 1 hour | 3600 |
| Last 2 hours | 7200 |
| Last 24 hours | 86400 |
| Last 7 days | 604800 |
| Last 30 days | 2592000 |
