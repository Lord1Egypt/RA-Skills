# MaxCompute Patterns

Advanced patterns and code examples for operating MaxCompute and agent_memory table.

## A. Install Dependencies

```bash
pip install pyodps
```

## B. Connect to MaxCompute (Must Use Environment Variables)

```python
import os
import odps

o = odps.ODPS(
    access_id=os.environ['ALICLOUD_ACCESS_KEY_ID'],
    secret_access_key=os.environ['ALICLOUD_ACCESS_KEY_SECRET'],
    project='samuelhsin',
    endpoint='http://service.cn-hangzhou.maxcompute.aliyun.com/api'
)

# Test connection
print(o.get_project().name)  # Should print: samuelhsin
```

## C. Create agent_memory Table (If Not Exists)

```python
sql = """
CREATE TABLE IF NOT EXISTS agent_memory (
    category STRING,
    title STRING,
    summary STRING,
    tags STRING,
    created_at STRING
) PARTITIONED BY (dt STRING)
COMMENT 'AI Agent long-term memory'
LIFECYCLE 3650
"""
o.execute_sql(sql)
```

## D. Batch Insert Multiple Records

```python
from datetime import datetime

# Prepare data
memories = [
    ('config', 'API Key Setup', 'Configured Binance API keys for trading', 'binance,api,config', '2026-03-18T10:00:00+08:00'),
    ('decision', 'Use PyODPS over DataWorks API', 'DataWorks API gets rate limited frequently, use PyODPS for better reliability', 'maxcompute,architecture', '2026-03-18T11:00:00+08:00'),
    ('learning', 'OpenClaw Skill Pattern', 'Skills use SKILL.md with YAML frontmatter, references/ folder for detailed docs', 'openclaw,skill,pattern', '2026-03-18T12:00:00+08:00'),
]

today = datetime.now().strftime('%Y-%m-%d')

# Batch insert
for category, title, summary, tags, created_at in memories:
    sql = f"""
    INSERT INTO agent_memory PARTITION (dt='{today}')
    (category, title, summary, tags, created_at)
    VALUES ('{category}', '{title}', '{summary.replace("'", "\\'")}', '{tags}', '{created_at}')
    """
    o.execute_sql(sql)

print(f"Inserted {len(memories)} records")
```

### Efficient Batch Insert with Tunnel

For large batches, use Tunnel for better performance:

```python
import os
import odps
from odps.tunnel import TableTunnel

o = odps.ODPS(
    access_id=os.environ['ALICLOUD_ACCESS_KEY_ID'],
    secret_access_key=os.environ['ALICLOUD_ACCESS_KEY_SECRET'],
    project='samuelhsin',
    endpoint='http://service.cn-hangzhou.maxcompute.aliyun.com/api'
)

tunnel = TableTunnel(o)
table = o.get_table('agent_memory')

# Create upload session for partition
today = '2026-03-18'
upload_session = tunnel.create_upload_session(table.name, partition_spec=f'dt={today}')

# Write records
writer = upload_session.open_record_writer()
for record_data in memories:
    record = table.new_record()
    record['category'] = record_data[0]
    record['title'] = record_data[1]
    record['summary'] = record_data[2]
    record['tags'] = record_data[3]
    record['created_at'] = record_data[4]
    writer.write(record)
writer.close()

# Commit
upload_session.commit()
```

## E. Query Specific Date

```python
import os
import odps

o = odps.ODPS(
    access_id=os.environ['ALICLOUD_ACCESS_KEY_ID'],
    secret_access_key=os.environ['ALICLOUD_ACCESS_KEY_SECRET'],
    project='samuelhsin',
    endpoint='http://service.cn-hangzhou.maxcompute.aliyun.com/api'
)

sql = """
SELECT dt, category, title, summary, tags, created_at
FROM agent_memory
WHERE dt = '2026-03-18'
ORDER BY created_at DESC
"""

with o.execute_sql(sql).open_reader() as reader:
    for row in reader:
        print(f"[{row.category}] {row.title}: {row.summary}")
```

### Query by Category

```python
sql = """
SELECT dt, title, summary, tags, created_at
FROM agent_memory
WHERE category = 'decision'
ORDER BY created_at DESC
LIMIT 10
"""
```

### Search in Summary

```python
sql = """
SELECT dt, category, title, summary, created_at
FROM agent_memory
WHERE summary LIKE '%maxcompute%'
ORDER BY created_at DESC
"""
```

## F. Query All Partitions

```python
# List all partitions
sql = "SHOW PARTITIONS agent_memory"
with o.execute_sql(sql).open_reader() as reader:
    for row in reader:
        print(row)

# Get all unique dates
sql = "SELECT DISTINCT dt FROM agent_memory ORDER BY dt DESC"
with o.execute_sql(sql).open_reader() as reader:
    for row in reader:
        print(row.dt)
```

## G. DataWorks API (Backup - Use When PyODPS is Rate Limited)

> **Warning**: DataWorks ExecuteAdhocWorkflowInstance API is frequently rate-limited.
> **Prefer PyODPS direct connection** (see sections B-F above).

```python
import os
from alibabacloud_dataworks_public20200518.client import Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dataworks_public20200518 import models as dw_models

# Create client
config = open_api_models.Config(
    access_key_id=os.environ['ALICLOUD_ACCESS_KEY_ID'],
    access_key_secret=os.environ['ALICLOUD_ACCESS_KEY_SECRET'],
    endpoint='dataworks.cn-hangzhou.aliyuncs.com'
)
client = Client(config)

# Execute SQL
request = dw_models.RunDagRequest(
    project_id=579810,
    sql='SELECT * FROM agent_memory WHERE dt="2026-03-18" LIMIT 10',
    env_type=1  # Development environment
)

response = client.run_dag(request)
print(response.body.data.instance_id)
```

> **Note**: This approach may hit rate limits. Use PyODPS for production workloads.