# Data Source Configuration & Connection

## Database Connection

| Parameter | Description |
|-----------|-------------|
| Type | mysql / postgres / snowflake / sqlite / bigquery / redshift |
| Host | Database address |
| Port | Connection port |
| Database | Target database name |
| Username | Connection user |
| Password | Connection password |
| Table whitelist | (Optional) List of queryable tables |

## File Data Reading

Supported local file formats:

| Format | Description |
|--------|-------------|
| `.xlsx` / `.xls` | Excel, multiple sheets, auto-detect headers and types |
| `.json` | Standard JSON, auto-flatten nested structures |
| `.jsonl` | JSON Lines, one record per line |
| `.csv` | Comma-separated |

### Excel Reading

```python
import pandas as pd
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')
df.head()       # Show first 5 rows
df.info()       # Column names and types
df.describe()   # Numerical column statistics
```

### JSON / JSONL Reading

```python
import pandas as pd
df = pd.read_json('data.json')                # Standard JSON
df = pd.read_json('logs.jsonl', lines=True)   # JSON Lines
```

## Behavior Without Configured Data Source

- Uses built-in mock data to demonstrate the full query workflow
- Mock data based on e-commerce scenario (orders table)
- Auto-displays mock table structure on first use

## Security Constraints

- Generated SQL limited to read-only SELECT
- Privacy fields (phone numbers, emails, etc.) auto-masked
- Large datasets prompt for LIMIT or time range
- No INSERT/UPDATE/DELETE execution