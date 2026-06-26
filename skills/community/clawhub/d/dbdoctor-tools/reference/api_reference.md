# Tool API Reference

## Utility Tools

### 0. Get Current Timestamp

Get the current Unix timestamp (seconds) for time range queries.

**Python Timestamp Calculation**:

```python
import time

now = int(time.time())
print(f"Current timestamp: {now}")

# Get timestamps for specific time ranges
start = now - 3600   # Last 1 hour
start = now - 7200   # Last 2 hours
start = now - 86400  # Last 24 hours
```

**Common Time Range Calculations**:

| Time Range   | Calculation        | Seconds     |
| ------ | --------- | ------ |
| Last 1 hour  | now - 3600 | 3600   |
| Last 2 hours  | now - 7200 | 7200   |
| Last 6 hours  | now - 21600| 21600  |
| Last 12 hours | now - 43200| 43200  |
| Last 24 hours | now - 86400| 86400  |
| Last 3 days   | now - 259200| 259200 |
| Last 7 days   | now - 604800| 604800 |

**Complete Example - Get Slow SQL for Last 2 Hours**:

```bash
# Step 1: Calculate timestamps
now=$(python -c "import time; print(int(time.time()))")
start=$(python -c "import time; print(int(time.time()) - 7200)")

# Step 2: Call tool
python scripts/get_slow_sql.py --instance-id [instance_id] --start-time $start --end-time $now
```

**Important Notes**:

- Timestamps must be integers (seconds), not milliseconds
- Use `python -c "import time; print(int(time.time()))"` to get current timestamp

***

## Instance Management Tools

### 1. get\_instance - Get Instance Basic Information

Get the list of database instances under a tenant/project. **This tool is the only way to obtain instance tenant and project information**.

**Python Call**:

```bash
# Get all instances (will return all instances across all tenants/projects)
python scripts/get_instance.py

# Filter by tenant and project
python scripts/get_instance.py --tenant [tenant] --project [project]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --tenant | string | No | Tenant name filter (optional) |
| --project | string | No | Project name filter (optional) |

**Important**: When other tools need `--tenant` and `--project` parameters, you must call this tool first to obtain them, and are prohibited from extracting directly from user input.

***

### 2. get\_current\_user - Get Current User Tenant and Project Information

Get the list of all tenants and projects for the currently logged-in user. The namespace format is `tenant-project`.

**Applicable Scenarios**:
- View all tenants and projects that the current user has permissions for
- As a prerequisite step for `get_instance`, determine tenant and project first

**Python Call**:

```bash
# Get complete user information
python scripts/get_current_user.py

# Get simplified tenant-project list
python scripts/get_current_user.py --extract
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --extract | flag | No | Only output simplified tenant-project list |

**Return Example (--extract mode)**:
```json
{
  "username": "tester",
  "userId": "472",
  "tenantProjects": [
    {
      "tenant": "demo-tenant",
      "project": "demo-project",
      "namespace": "demo-tenant-demo-project",
      "roles": ["dev", "admin", "tester"]
    }
  ]
}
```

**Usage Flow**:
```
1. Call get_current_user --extract to get tenant-project list
2. Select target tenant and project
3. Call get_instance --tenant xxx --project yyy to get instance list
4. Select target instance and execute other operations
```

***

### 3. get\_instance\_abnormal - Get Instance Abnormal Information

Get abnormal/alert information for a specified instance.

```bash
python scripts/get_instance_abnormal.py --instance-id [instance_id]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |

***

### 4. get\_database\_by\_instance - Get Databases Under Instance

Get the list of all databases under a specified instance.

```bash
python scripts/get_database_by_instance.py --instance-id [instance_id]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |

***

### 5. manage\_instance - Manage Database Instance

Register a new database instance to the DBDoctor platform.

> **Security Warning**: This is a privileged operation that modifies platform configuration. Verify all parameters (especially IP, port, credentials) before execution. Only authorized operators should use this tool.

**Python Call**:

```bash
python scripts/manage_instance.py --ip [ip] --port [port] --engine mysql --db-user [user] --db-password [password] --db-version [version] --tenant [tenant] --project [project]
```

Note: --db-password accepts plaintext password, the program automatically completes RSA encryption internally.

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --ip | string | Yes | Database server IP |
| --port | integer | Yes | Database port |
| --engine | string | Yes | Database engine (mysql/oracle/postgresql/dm/sqlserver/oracle-rac) |
| --db-user | string | Yes | Database username |
| --db-password | string | Yes | Database password (plaintext, automatically encrypted) |
| --db-version | string | Yes | Database version |
| --tenant | string | Yes | Tenant name |
| --project | string | Yes | Project name |
| --description | string | No | Instance description |

***

## SQL Analysis Tools

### 6. get\_slow\_sql - Get Slow SQL List

Get slow SQL queries within a specified time range.

```bash
python scripts/get_slow_sql.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | string | Yes | Start time (Unix timestamp, seconds) |
| --end-time | string | Yes | End time (Unix timestamp, seconds) |

**Related Page**: `{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/instance-diagnosis/{instance_id}/dbdoctor-slow-sql-governance?cluster=idc`

***

### 7. get\_table\_ddl - Get Table DDL

Get the structure definition of a specified table.

```bash
python scripts/get_table_ddl.py --instance-id [instance_id] --database [db] --schema [schema] --table [table]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --database | string | Yes | Database name |
| --schema | string | Yes | Schema name (same as database name for MySQL) |
| --table | string | Yes | Table name |

***

### 8. execute\_sql - Execute SQL Statement

Execute SQL statements on a specified database.

> **Security Warning**: This tool executes arbitrary SQL on the target database. Review all SQL statements carefully before execution. Avoid DDL/DML operations on production databases without proper approval. The tool does not enforce read-only restrictions.

**Prerequisite**: Call `get_instance` first to get tenant and project.

```bash
python scripts/execute_sql.py --instance-id [instance_id] --database [db] --schema [schema] --sql "[sql]" --engine mysql --tenant [tenant] --project [project]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --database | string | Yes | Database name |
| --schema | string | Yes | Schema name |
| --sql | string | Yes | SQL statement to execute (wrapped in quotes) |
| --engine | string | Yes | Database engine (mysql/oracle/postgresql) |
| --tenant | string | Yes | Tenant name (from get_instance) |
| --project | string | Yes | Project name (from get_instance) |

***

### 9. sql\_audit - SQL Audit

Audit and analyze SQL statements. Automatically completes the two-step process of submitting audit + polling results internally.

```bash
python scripts/sql_audit.py --instance-id [instance_id] --database [db] --schema [schema] --sql "[sql]"
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --database | string | Yes | Database name |
| --schema | string | Yes | Schema name |
| --sql | string | Yes | SQL statement to audit (wrapped in quotes) |

**Follow-up Suggestions**:
- If issues found → `ai_sql_rewrite` for SQL rewriting
- If indexes needed → `execute_sql` to execute ALTER TABLE ADD INDEX
- View audit rules → `get_sql_audit_rules`

***

### 10. get\_sql\_audit\_rules - Get SQL Audit Rules

Get SQL audit rule configurations.

```bash
python scripts/get_sql_audit_rules.py --engine mysql --priority ERROR
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --engine | string | No | Database engine filter |
| --rule-name | string | No | Rule name filter |
| --priority | string | No | Risk level (ERROR/WARNING/DANGER) |

**Rule Priority**: ERROR (must fix) | WARNING (recommended fix) | DANGER (use with caution)

For detailed rule descriptions: `reference/audit_and_inspection_rules.md`

***

## Inspection Tools

### 11. do\_inspect\_instance - Execute Instance Inspection

Trigger an inspection task for a database instance.

```bash
# Basic usage
python scripts/do_inspect_instance.py --instance-id [instance_id]

# With jump link (recommended)
python scripts/do_inspect_instance.py --instance-id [instance_id] --tenant [tenant] --project [project]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --tenant | string | No | Tenant name (for jump link, from get_instance) |
| --project | string | No | Project name (for jump link, from get_instance) |

***

### 12. get\_recent\_inspect\_report - Get Recent Inspection Report

```bash
python scripts/get_recent_inspect_report.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts] --tenant [tenant] --project [project]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | integer | Yes | Start time (Unix timestamp, seconds) |
| --end-time | integer | Yes | End time (Unix timestamp, seconds) |
| --tenant | string | Yes | Tenant name (from get_instance) |
| --project | string | Yes | Project name (from get_instance) |

***

### 13. get\_inspect\_item - Get Inspection Items

```bash
python scripts/get_inspect_item.py
```

No parameters.

***

## Session & Process Tools

### 14. get\_current\_process - Get Current Sessions

```bash
python scripts/get_current_process.py --instance-id [instance_id] --database [db] --sql-keyword [keyword]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --database | string | No | Database name filter |
| --sql-keyword | string | No | SQL keyword filter |

***

## Alert Tools

### 15. alert\_message - Get Alert Overview

```bash
python scripts/alert_message.py --status alarming --priority serious
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --status | string | No | Alert status (alarming/recovered) |
| --priority | string | No | Alert level (serious/warning/info) |
| --event-name | string | No | Event name filter |
| --instance-ip | string | No | Instance IP filter |
| --instance-desc | string | No | Instance description filter |
| --create-time | string | No | Creation time filter |
| --modified-time | string | No | Modification time filter |

***

## Performance Diagnosis Tools

### 16. performance\_diagnosis - Comprehensive Diagnosis ⭐

**Recommended** - Comprehensive performance diagnosis integrating multiple diagnostic dimensions.

**Diagnostic Dimensions**:
- Instance basic information (/drapi/ai/instance/info)
- Slow SQL analysis (/drapi/ai/getSlowSqlByTime)
- Abnormal SQL analysis (/drapi/ai/getAbnormalSqlByTime)
- AAS active session statistics (/drapi/ai/activeSession/statistics)
- Resource monitoring metrics (/drapi/ai/getResourceMetricsInNL)

```bash
python scripts/performance_diagnosis.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | string | Yes | Start timestamp (Unix seconds) |
| --end-time | string | Yes | End timestamp (Unix seconds) |

**Return Report Structure**:
```json
{
  "diagnosisTime": {"startTime": "xxx", "endTime": "yyy"},
  "instanceInfo": {},
  "performanceMetrics": {
    "slowSql": [],
    "abnormalSql": [],
    "aasInfo": {}
  },
  "resourceMetrics": {}
}
```

**Follow-up**: slow SQL → `sql_audit` / `ai_sql_rewrite` | resource bottleneck → `get_host_resource_info` | high sessions → `get_aas_info`

***

### 17. get\_basic\_monitor\_info - Database Monitoring Metrics

```bash
python scripts/get_basic_monitor_info.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | string | Yes | Start timestamp (Unix seconds) |
| --end-time | string | Yes | End timestamp (Unix seconds) |

**Related Page**: `{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/instance-diagnosis/{instance_id}/dbdoctor-basic-monitor?cluster=idc`

***

### 18. get\_host\_resource\_info - Host Resource Metrics

```bash
python scripts/get_host_resource_info.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | string | Yes | Start timestamp (Unix seconds) |
| --end-time | string | Yes | End timestamp (Unix seconds) |

**Related Page**: `{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/instance-diagnosis/{instance_id}/dbdoctor-basic-monitor?cluster=idc`

***

### 19. get\_db\_parameter\_info - Database Parameters

```bash
python scripts/get_db_parameter_info.py --instance-id [instance_id]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |

**Related Page**: `{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/instance-diagnosis/{instance_id}/dbdoctor-param-recommend?cluster=idc`

***

### 20. get\_aas\_info - Active Session Statistics (AAS)

```bash
python scripts/get_aas_info.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | string | Yes | Start timestamp (Unix seconds) |
| --end-time | string | Yes | End timestamp (Unix seconds) |

**Related Page**: `{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/instance-diagnosis/{instance_id}/dbdoctor-performance-insight?cluster=idc`

***

### 21. get\_related\_sql\_info - Root Cause SQL

Get root cause SQL that caused performance issues.

```bash
python scripts/get_related_sql_info.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | string | Yes | Start timestamp (Unix seconds) |
| --end-time | string | Yes | End timestamp (Unix seconds) |

**Related Page**: `{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/instance-diagnosis/{instance_id}/dbdoctor-root-cause-diagnosis?cluster=idc`

***

### 22. get\_instance\_info - Instance Detailed Information

```bash
python scripts/get_instance_info.py --instance-id [instance_id]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |

**Related Page**: `{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/doctor-instance-list?cluster=idc`

***

### 23. get\_slow\_sql\_by\_time - Slow SQL by Time (Diagnosis)

```bash
python scripts/get_slow_sql_by_time.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | string | Yes | Start timestamp (Unix seconds) |
| --end-time | string | Yes | End timestamp (Unix seconds) |

***

## SQL Rewrite Tools

### 24. ai\_sql\_rewrite - AI SQL Rewrite

```bash
python scripts/ai_sql_rewrite.py --instance-id [instance_id] --database [db] --schema [schema] --sql "[sql]"
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --database | string | Yes | Database name |
| --schema | string | Yes | Schema name |
| --sql | string | Yes | SQL statement to rewrite (wrapped in quotes) |

***

### 25. get\_sql\_rewrite\_result - Get SQL Rewrite Result

```bash
python scripts/get_sql_rewrite_result.py --task-id [task_id]
```

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --task-id | string | Yes | Task ID returned by ai\_sql\_rewrite |

***

## Page Jump Links

Some tools have a **Related Page** URL template for the corresponding DBDoctor web console page.

- URL format: `{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/...`
- `{base_url}`: DBDOCTOR_URL from environment configuration
- `{tenant}` / `{project}`: obtained from `get_instance`
- `{role}`: default `dev`
- `{instance_id}`: Instance ID
- Tenant and project must be obtained via `get_instance` before constructing URLs
