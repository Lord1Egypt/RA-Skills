# SQL Audit Rules and Inspection Rules Description

## SQL Audit Rules Classification

### MySQL Engine Main Rules

**Performance**:
- Poor current index
- Full table scan exists
- SQL row scan limit

**Standard**:
- SELECT * not allowed
- Force SQL to use WHERE condition

**Security**:
- UPDATE primary key field prohibited
- Table deletion prohibited

### Oracle Engine Main Rules

**Performance**:
- Execution plan analysis (index skip scan, full table scan, cartesian product)

**Standard**:
- Table naming format restrictions
- Index naming conventions
- Field naming conventions

**Security**:
- Modify column type prohibited
- Delete field prohibited
- Partition table usage prohibited

## Rule Priority Description

| Priority | Description | Example |
|--------|------|------|
| **ERROR** | Critical issues, must fix | Full table scan, poor indexing, foreign keys prohibited |
| **WARNING** | Warning issues, recommended to fix | Avoid using SELECT *, limit on number of indexed fields |
| **DANGER** | Dangerous operations, use with caution | Prohibit dropping tables, prohibit TRUNCATE |

## Inspection Rules Classification

### Performance Inspection

- CPU/Memory/Disk IO usage
- QPS/TPS/Connections
- Buffer pool hit rate

### Resource Inspection

- Tablespace usage
- Disk free space
- Long transaction detection

### Configuration Inspection

- Database parameter check
- Archive configuration check
- Backup status check

### Status Inspection

- Database running status
- Master-slave synchronization status
- Deadlock detection

## Common Tools

### SQL Audit Rules Query

```bash
# Get all MySQL audit rules
python scripts/get_sql_audit_rules.py --engine mysql

# Get Oracle ERROR level rules
python scripts/get_sql_audit_rules.py --engine oracle --priority ERROR
```

### Inspection Related Tools

```bash
# Execute instance inspection
python scripts/do_inspect_instance.py --instance-id [instance_id] --tenant [tenant] --project [project]

# Get inspection items list
python scripts/get_inspect_item.py

# Get recent inspection report
python scripts/get_recent_inspect_report.py --instance-id [instance_id] --start-time [start] --end-time [end] --tenant [tenant] --project [project]
```
