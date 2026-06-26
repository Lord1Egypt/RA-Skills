---
name: feishu-bitable
description: Read and edit Feishu Bitable (多维表格) data like a database. Use when working with Feishu multidimensional tables for: (1) Listing tables and views, (2) Getting table schema, (3) Querying/filtering records, (4) Creating new records, (5) Updating existing records, (6) Deleting records, (7) Aggregating data. Provides SQL-like interface with SELECT, INSERT, UPDATE, DELETE operations. Supports --url parameter to auto-extract app_token, table_id, view_id from Feishu URL.
metadata: {"openclaw":{"emoji":"🧩","requires":{"bins":["python3"],"env":["FEISHU_APP_ID","FEISHU_APP_SECRET"]},"primaryEnv":"FEISHU_APP_SECRET"}}
---

# Feishu Bitable - SQL-like Database Interface

Read and edit Feishu Bitable (多维表格) data with a familiar SQL-like interface.

## Quick Start with URL

Simply pass the Feishu URL and the skill will auto-extract all parameters:

```bash
# Parse URL to see extracted parameters
python3 {baseDir}/feishu_bitable.py parse-url "https://xxx.feishu.cn/base/APP_TOKEN?table=TABLE_ID&view=VIEW_ID"

# Query records using URL
python3 {baseDir}/feishu_bitable.py select --url "https://xxx.feishu.cn/base/APP_TOKEN?table=TABLE_ID" --limit 10

# Get table schema using URL
python3 {baseDir}/feishu_bitable.py describe --url "https://xxx.feishu.cn/base/APP_TOKEN?table=TABLE_ID"
```

## Quick Reference

| Operation     | Command                                                       |
| ------------- | ------------------------------------------------------------- |
| Parse URL     | `parse-url <URL>`                                             |
| List tables   | `list-tables --url <URL>`                                     |
| Get schema    | `describe --url <URL>`                                        |
| Query records | `select --url <URL> --limit 100`                              |
| Count records | `count --url <URL>`                                           |
| Insert record | `insert --url <URL> --data '{"field":"value"}'`               |
| Update record | `update --url <URL> --record-id R --data '{"field":"value"}'` |
| Delete record | `delete --url <URL> --record-id R`                            |
| Aggregate     | `aggregate --url <URL> --group-by Field --agg "SUM(Amount)"`  |

## URL Format

Feishu Bitable URLs follow this pattern:

```
https://<domain>.feishu.cn/base/<app_token>?table=<table_id>&view=<view_id>

Example:
https://ncnv0ov0snlp.feishu.cn/base/IsPPb8tkYaIiwdsjiS1cG8tTnhe?table=tblOetM5ZD9wSTGH&view=vew6BTuyh8

Extracted:
- app_token: IsPPb8tkYaIiwdsjiS1cG8tTnhe
- table_id: tblOetM5ZD9wSTGH
- view_id: vew6BTuyh8
```

## Commands

### 1. Parse URL

Extract parameters from a Feishu URL:

```bash
python3 {baseDir}/feishu_bitable.py parse-url "https://xxx.feishu.cn/base/APP_TOKEN?table=TABLE_ID&view=VIEW_ID"
```

Output:

```json
{
  "ok": true,
  "app_token": "IsPPb8tkYaIiwdsjiS1cG8tTnhe",
  "table_id": "tblOetM5ZD9wSTGH",
  "view_id": "vew6BTuyh8"
}
```

### 2. List Tables

List all tables in a Bitable app:

```bash
python3 {baseDir}/feishu_bitable.py list-tables --url <URL>
# Or with app-token
python3 {baseDir}/feishu_bitable.py list-tables --app-token <APP_TOKEN>
```

Output:

```json
{
  "ok": true,
  "tables": [
    { "table_id": "tblXXX", "name": "Orders", "revision": 1 },
    { "table_id": "tblYYY", "name": "Products", "revision": 1 }
  ]
}
```

### 3. Describe Table (Get Schema)

Get table fields and views:

```bash
python3 {baseDir}/feishu_bitable.py describe --url <URL>
```

Output includes:

- `fields`: Field definitions with names, types, and properties
- `views`: Available views with IDs and names

Field types: 1=Text, 2=Number, 3=SingleSelect, 4=MultiSelect, 5=Date, 7=Checkbox, 11=Person, 15=URL, 17=Attachment, 18=Link

### 4. SELECT - Query Records

Basic query (returns all records up to limit):

```bash
python3 {baseDir}/feishu_bitable.py select --url <URL> --limit 100
```

Filter by view (recommended for filtering):

```bash
python3 {baseDir}/feishu_bitable.py select --url <URL> --view-id <VIEW_ID> --limit 100
```

Select specific fields:

```bash
python3 {baseDir}/feishu_bitable.py select --url <URL> --fields "Name,Status,Amount" --limit 100
```

Sort results:

```bash
python3 {baseDir}/feishu_bitable.py select --url <URL> --order-by "created_time DESC" --limit 100
```

### 5. COUNT - Count Records

```bash
python3 {baseDir}/feishu_bitable.py count --url <URL>
```

Output:

```json
{ "ok": true, "count": 42 }
```

### 6. AGGREGATE - Group By & Sum

Group by field with aggregations:

```bash
python3 {baseDir}/feishu_bitable.py aggregate \
  --url <URL> \
  --group-by "Category" \
  --agg "SUM(Amount), COUNT(), AVG(Score)"
```

Output:

```json
{
  "ok": true,
  "total_groups": 3,
  "groups": [
    { "Category": "Electronics", "sum_Amount": 15000, "count": 42, "avg_Score": 4.5 },
    { "Category": "Clothing", "sum_Amount": 8000, "count": 30, "avg_Score": 4.2 }
  ]
}
```

Aggregation functions: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`

With alias:

```bash
--agg "SUM(Amount) as total, AVG(Score) as avg_score"
```

### 7. INSERT - Create Records

Create single record:

```bash
python3 {baseDir}/feishu_bitable.py insert \
  --url <URL> \
  --data '{"Name": "New Item", "Status": "Pending", "Amount": 100}'
```

Create multiple records:

```bash
python3 {baseDir}/feishu_bitable.py insert-batch \
  --url <URL> \
  --data '[{"Name": "Item 1"}, {"Name": "Item 2"}, {"Name": "Item 3"}]'
```

### 8. UPDATE - Update Records

Update by record_id:

```bash
python3 {baseDir}/feishu_bitable.py update \
  --url <URL> \
  --record-id recXXXXXX \
  --data '{"Status": "Done"}'
```

### 9. DELETE - Delete Records

Delete by record_id:

```bash
python3 {baseDir}/feishu_bitable.py delete \
  --url <URL> \
  --record-id recXXXXXX
```

Delete multiple records:

```bash
python3 {baseDir}/feishu_bitable.py delete \
  --url <URL> \
  --record-ids "recXXX,recYYY,recZZZ"
```

## Field Value Formats

| Field Type   | Value Format                                  |
| ------------ | --------------------------------------------- |
| Text         | `"string"`                                    |
| Number       | `123` or `45.67`                              |
| SingleSelect | `"Option Name"`                               |
| MultiSelect  | `["Tag1", "Tag2"]`                            |
| Checkbox     | `true` or `false`                             |
| Date         | `1709000000000` (timestamp in ms)             |
| Person       | `{"id": "ou_xxx"}`                            |
| Link         | `["recXXX", "recYYY"]`                        |
| Attachment   | `[{"file_token": "...", "name": "file.pdf"}]` |

## Common Workflows

### Explore a new Bitable

```bash
# 1. Parse URL to verify
python3 {baseDir}/feishu_bitable.py parse-url "https://xxx.feishu.cn/base/APP?table=TBL&view=VIEW"

# 2. Get schema
python3 {baseDir}/feishu_bitable.py describe --url <URL>

# 3. Query first few records
python3 {baseDir}/feishu_bitable.py select --url <URL> --limit 5
```

### Query and aggregate data

```bash
# 1. Query records
python3 {baseDir}/feishu_bitable.py select --url <URL> --limit 100

# 2. Aggregate by category
python3 {baseDir}/feishu_bitable.py aggregate \
  --url <URL> \
  --group-by "Category" \
  --agg "SUM(Amount), COUNT()"
```

### Create multiple records

```bash
python3 {baseDir}/feishu_bitable.py insert-batch \
  --url <URL> \
  --data '[
    {"Name": "Task 1", "Status": "Todo"},
    {"Name": "Task 2", "Status": "Todo"},
    {"Name": "Task 3", "Status": "Done"}
  ]'
```

## Troubleshooting

### Authentication Errors

- Verify `FEISHU_APP_ID` and `FEISHU_APP_SECRET` are set
- Check app has required permissions: `bitable:app`, `bitable:app:readonly`

### Permission Errors (403)

- Share the Bitable to the app bot as collaborator
- Check API permissions in Feishu admin console

### Empty Results

- Verify URL is correct
- Try using `--view-id` to filter by a specific view

### Rate Limits

- 100 requests/minute per app per tenant
- 10 requests/second per app per tenant

## Environment Variables

Required:

- `FEISHU_APP_ID` - Feishu application ID
- `FEISHU_APP_SECRET` - Feishu application secret

Optional:

- `FEISHU_API_HOST` - API host (default: `https://open.feishu.cn`)
- `FEISHU_DEBUG` - Set to `1` for debug output
- `FEISHU_PRETTY` - Set to `1` for pretty JSON output
