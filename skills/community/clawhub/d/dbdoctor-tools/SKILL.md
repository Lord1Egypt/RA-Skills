---
name: dbdoctor-tools
description: >
  DBdoctor database performance diagnosis platform tools.
  Invoke when user needs to query database instances, slow SQL,
  inspection reports, performance metrics, or perform SQL audit/rewrite operations.
license: Apache-2.0
compatibility: Requires Python 3.9+ with requests, pycryptodome, python-dotenv packages. Network access to DBdoctor API server required.
allowed-tools: Bash Read
requires:
  env:
    - DBDOCTOR_URL
  commands:
    - python
    - pip
metadata:
  author: DBdoctor-DAS
  version: 1.1.0
  tags: [database, performance, diagnosis, slow-sql, sql-audit, monitoring, dbdoctor]
---

## Quick Start Examples

### Scenario 1: Diagnose Instance Performance Issues (Recommended)

```bash
# 1. Get tenant and project
python scripts/get_current_user.py --extract

# 2. Get instance list
python scripts/get_instance.py --tenant [tenant] --project [project]

# 3. Execute comprehensive performance diagnosis (last 1 hour)
python scripts/performance_diagnosis.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

### Scenario 2: Execute Instance Inspection

```bash
# 1. Get tenant and project of the instance
python scripts/get_instance.py

# 2. Execute inspection
python scripts/do_inspect_instance.py --instance-id [instance_id] --tenant [tenant] --project [project]

# 3. Get inspection report
python scripts/get_recent_inspect_report.py --instance-id [instance_id] --start-time [start] --end-time [end] --tenant [tenant] --project [project]
```

### Scenario 3: SQL Optimization

```bash
# 1. Get slow SQL list
python scripts/get_slow_sql.py --instance-id [instance_id] --start-time [start] --end-time [end]

# 2. Audit slow SQL
python scripts/sql_audit.py --instance-id [instance_id] --database [db] --schema [schema] --sql "[sql]"

# 3. Use AI to rewrite SQL (optional)
python scripts/ai_sql_rewrite.py --instance-id [instance_id] --database [db] --schema [schema] --sql "[sql]"
```

***

## Security

### Credential Management

This skill supports two authentication modes:

- **Mode 1 - Password login** (企业版（免费试用）): Requires `DBDOCTOR_URL`, `DBDOCTOR_USER`, `DBDOCTOR_PASSWORD`.
- **Mode 2 - Email verification code login** (免费版（永久免费）, Windows/Mac): Requires `DBDOCTOR_URL`, `DBDOCTOR_EMAIL`. When a verification code is needed, the user will be prompted interactively.

If `DBDOCTOR_EMAIL` is configured, email mode takes precedence.

Credentials are managed by the platform and injected as environment variables at runtime. **This skill does not write credentials to disk.** The `.token_cache` file (API session token only) is the only file persisted locally and is listed in `.gitignore`.

### Privileged Operations

Two tools perform write operations that require operator care:

- **execute\_sql**: Executes arbitrary SQL on the target database. Review all SQL statements before execution. The tool does not enforce read-only restrictions.
- **manage\_instance**: Registers new database instances to the platform. Verify all connection parameters (IP, port, credentials) before execution.

All other tools are read-only queries against the DBdoctor API.

### Authentication Mechanism

The program supports two login methods:

1. **Password mode**: Reads username/password from environment variables, AES-encrypts the password, and calls `/nephele/login` to obtain a Token.
2. **Email mode**: Sends a verification code to the configured email via `/drapi/user/verificationCode`, prompts the user to enter the code, AES-encrypts it, and calls `/nephele/login` with `authType=authCode`.

Token is cached in `.token_cache`. When the token expires, the system automatically re-authenticates (password mode is silent; email mode prompts for a new verification code). No manual auth management is required.

***

## Configuration

Set the following environment variables based on your login mode:

| Variable | Description | Required |
| --- | --- | --- |
| DBDOCTOR\_URL | DBdoctor API base URL (e.g. `http://host:port`) | Always |
| DBDOCTOR\_USER | Login username (also used as UserId) | Password mode only |
| DBDOCTOR\_PASSWORD | Login password (sensitive) | Password mode only |
| DBDOCTOR\_EMAIL | Login email for verification code | Email mode only |

> **Note**: If `DBDOCTOR_EMAIL` is set, email verification code mode is used. Otherwise, username/password mode is used.

### Mode 1: Password login (企业版（免费试用）)

```bash
# CLI configuration (recommended)
clawdbot skills config dbdoctor-tools DBDOCTOR_URL "http://[host]:[port]"
clawdbot skills config dbdoctor-tools DBDOCTOR_USER "[username]"
clawdbot skills config dbdoctor-tools DBDOCTOR_PASSWORD "[password]"
```

### Mode 2: Email verification code login (免费版（永久免费）)

```bash
# CLI configuration (recommended)
clawdbot skills config dbdoctor-tools DBDOCTOR_URL "http://[host]:[port]"
clawdbot skills config dbdoctor-tools DBDOCTOR_EMAIL "[email]"
```

### Manual configuration

Edit `~/.clawdbot/clawdbot.json`:

```json5
{
  skills: {
    entries: {
      "dbdoctor-tools": {
        env: {
          // Mode 1: Password login
          DBDOCTOR_URL: "http://[host]:[port]",
          DBDOCTOR_USER: "[username]",
          DBDOCTOR_PASSWORD: "[password]"

          // Mode 2: Email login (use this instead of USER/PASSWORD)
          // DBDOCTOR_URL: "http://[host]:[port]",
          // DBDOCTOR_EMAIL: "[email]"
        }
      }
    }
  }
}
```

### System environment variables

```bash
# Linux / Mac - Password mode
export DBDOCTOR_URL="http://[host]:[port]"
export DBDOCTOR_USER="[username]"
export DBDOCTOR_PASSWORD="[password]"

# Linux / Mac - Email mode
export DBDOCTOR_URL="http://[host]:[port]"
export DBDOCTOR_EMAIL="[email]"

# Windows PowerShell - Password mode
$env:DBDOCTOR_URL="http://[host]:[port]"
$env:DBDOCTOR_USER="[username]"
$env:DBDOCTOR_PASSWORD="[password]"

# Windows PowerShell - Email mode
$env:DBDOCTOR_URL="http://[host]:[port]"
$env:DBDOCTOR_EMAIL="[email]"
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies: requests, pycryptodome, python-dotenv

***

## Instance Information Retrieval Guidelines

**Important**: When tenant and project information is needed, **it must be dynamically retrieved through tools**, and is prohibited from being extracted directly from user input.

**Strictly prohibited from fabricating tenant and project information**

**Method 1: Retrieve via get_current_user (Recommended)**
```
1. Call get_current_user --extract to get all tenants and projects
2. Select target tenant and project
3. Call get_instance --tenant xxx --project yyy
4. Select target instance and execute other operations
```

**Method 2: Retrieve via get_instance (Recommended)**
```
1. Call get_instance to query all instances (no parameters needed)
2. Find target instance from returned data
3. Extract tenant and project from instance data
```

### API Usage Constraints

**Strictly prohibited from calling interfaces not defined in this document**

- Only use tools and interfaces listed in the API Reference
- Prohibited from fabricating or inferring interface paths
- Prohibited from calling interfaces of other systems or services

***

## Tool Combination Patterns

### Pattern 1: Performance Diagnosis Workflow (Most Common)

```
get_current_user --extract
        |
get_instance --tenant xxx --project yyy
        |
performance_diagnosis --instance-id xxx --start-time t1 --end-time t2
        |
[Based on diagnosis results]
    - Many slow SQLs -> sql_audit / ai_sql_rewrite
    - Resource bottleneck -> get_host_resource_info / get_basic_monitor_info
    - High active sessions -> get_aas_info / get_current_process
```

### Pattern 2: Instance Inspection Workflow

```
get_instance -> do_inspect_instance -> get_recent_inspect_report
```

### Pattern 3: SQL Optimization Workflow

```
get_slow_sql / get_related_sql_info -> sql_audit -> ai_sql_rewrite (if needed)
```

### Pattern 4: New Instance Registration Workflow

```
get_current_user --extract -> manage_instance -> get_instance (confirm)
```

***

## Information Collection Matrix

| Task Type | Required Information | Collection Strategy | Notes |
| --- | --- | --- | --- |
| Query Instance | None | Call tool directly | Get instance list and tenant/project |
| **Instance Inspection** | **Instance ID** | **Check -> Ask -> Call** | tenant/project via get_instance |
| **Performance Diagnosis** | **Instance ID + Time Range** | **Check -> Ask -> Call** | tenant/project via get_instance |
| **View Data** | **Instance ID** | **Check -> Ask -> Call** | tenant/project via get_instance |

For detailed processing strategies, decision trees and rules: `reference/agent_guidelines.md`

***

## Tool API Reference

For complete API documentation with parameters, examples, and related pages, see: [reference/api_reference.md](reference/api_reference.md)

### Quick Reference: Parameter Requirements Summary

| Tool | Required Parameters |
| --- | --- |
| get\_instance | None (returns all instances) |
| get\_current\_user | None (get current user tenant-project info) |
| get\_instance\_abnormal | --instance-id |
| get\_database\_by\_instance | --instance-id |
| manage\_instance | --ip, --port, --engine, --db-user, --db-password, --db-version, --tenant, --project |
| get\_slow\_sql | --instance-id, --start-time, --end-time |
| get\_table\_ddl | --instance-id, --database, --schema, --table |
| execute\_sql | --instance-id, --database, --schema, --sql, --engine, --tenant, --project |
| sql\_audit | --instance-id, --database, --schema, --sql |
| get\_sql\_audit\_rules | --engine (optional), --priority (optional) |
| do\_inspect\_instance | --instance-id, --tenant (optional), --project (optional) |
| get\_recent\_inspect\_report | --instance-id, --start-time, --end-time, --tenant, --project |
| get\_inspect\_item | None |
| get\_current\_process | --instance-id |
| alert\_message | --status (optional), --priority (optional), --instance-ip (optional) |
| performance\_diagnosis | --instance-id, --start-time, --end-time (comprehensive, recommended) |
| get\_basic\_monitor\_info | --instance-id, --start-time, --end-time |
| get\_host\_resource\_info | --instance-id, --start-time, --end-time |
| get\_db\_parameter\_info | --instance-id |
| get\_aas\_info | --instance-id, --start-time, --end-time |
| get\_related\_sql\_info | --instance-id, --start-time, --end-time |
| get\_instance\_info | --instance-id |
| get\_slow\_sql\_by\_time | --instance-id, --start-time, --end-time |
| ai\_sql\_rewrite | --instance-id, --database, --schema, --sql |
| get\_sql\_rewrite\_result | --task-id |

***

## Notes

1. **Timestamps**: Time range parameters use Unix timestamps (seconds), not milliseconds
2. **Schema**: For MySQL, schema name equals database name
3. **Engine Types**: mysql, oracle, postgresql, dm (Dameng), sqlserver, oracle-rac
4. **SQL Parameter**: When --sql contains spaces or special characters, wrap in quotes
5. **tenant/project**: Must be obtained via `get_instance` — never fabricate or extract from user input
6. **Time Range Default**: Alert queries default to last 2 hours if not specified
7. **Performance Diagnosis**: Recommended time ranges: last 1h, 6h, or 24h

### Reference Document Index

- `reference/api_reference.md` - Complete Tool API Reference (parameters, examples, related pages)
- `reference/performance_diagnosis_guide.md` - Performance Diagnosis Knowledge Base
- `reference/best_practices.md` - Best Practices Guide
- `reference/audit_and_inspection_rules.md` - SQL Audit Rules and Inspection Rules
- `reference/troubleshooting.md` - Common Issues and Solutions
- `reference/agent_guidelines.md` - Agent Processing Strategies and Decision Guidelines
