# DBDoctor Best Practices Guide

## 1. Complete Instance Diagnosis Flow

```
1. Get tenant-project
   python scripts/get_current_user.py --extract

2. Get instance list
   python scripts/get_instance.py --tenant [tenant] --project [project]

3. View abnormal instances
   python scripts/get_instance_abnormal.py --instance-id [instance_id]

4. Execute inspection
   python scripts/do_inspect_instance.py --instance-id [instance_id] --tenant [tenant] --project [project]

5. Get inspection report
   python scripts/get_recent_inspect_report.py --instance-id [instance_id] --start-time $start --end-time $now --tenant [tenant] --project [project]

6. View slow SQL
   python scripts/get_slow_sql.py --instance-id [instance_id] --start-time $start --end-time $now

7. View root cause SQL
   python scripts/get_related_sql_info.py --instance-id [instance_id] --start-time $start --end-time $now

8. SQL audit and optimization
   python scripts/sql_audit.py --instance-id [instance_id] --database [db] --schema [schema] --sql "[sql]"
```

## 2. SQL Optimization Flow

```
1. Get slow SQL list
   python scripts/get_slow_sql.py --instance-id [instance_id] --start-time $start --end-time $now

2. Select target SQL for audit
   python scripts/sql_audit.py --instance-id [instance_id] --database [db] --schema [schema] --sql "[sql]"

3. Based on audit results:
   - View recommended indexes
   - View cost comparison
   - View optimization suggestions

4. Apply optimization recommendations:
   - Add recommended indexes
   - Modify SQL statements
   - Adjust database parameters
```

## 3. Performance Problem Troubleshooting Flow

```
1. Confirm problem time range

2. Get root cause SQL
   python scripts/get_related_sql_info.py --instance-id [instance_id] --start-time $start --end-time $now

3. View resource monitoring
   python scripts/get_host_resource_info.py --instance-id [instance_id] --start-time $start --end-time $now

4. View active sessions
   python scripts/get_aas_info.py --instance-id [instance_id] --start-time $start --end-time $now

5. Comprehensive analysis and provide optimization suggestions
```

## 4. Best Practices for Information Collection

### Priority Order

```
User's current question > Conversation history > Ask user
```

### Collect one by one, don't ask multiple at once

❌ Wrong: "Which instance do you want to diagnose? What's the time range?"
✅ Correct: First ask for instance ID, after user answers, then ask for time range

### Provide examples to help user understand

When asking for time range, give examples: "For example: last 1 hour, yesterday 3pm to 5pm"

### Use context

If instance ID was mentioned in conversation history, use it directly, don't ask again

### Clear questioning language

- Ask instance ID: "Which instance would you like to perform XX on?"
- Ask time range: "Which time period would you like to analyze? (e.g.: last 1 hour, yesterday 3pm to 5pm)"

## 5. Performance Diagnosis Best Practices

- Recommend using `performance_diagnosis` for comprehensive diagnosis, get complete report in one call
- Recommended diagnosis time ranges: last 1 hour, last 6 hours, last 24 hours
- Standard performance diagnosis flow:
  ```
  1. Confirm instance ID and time range
  2. Call performance_diagnosis to get comprehensive report
  3. Analyze slow SQL, root cause SQL, resource metrics in the report
  4. Provide optimization suggestions based on analysis results
  ```
- For detailed performance diagnosis knowledge base please refer to: `reference/performance_diagnosis_guide.md`
