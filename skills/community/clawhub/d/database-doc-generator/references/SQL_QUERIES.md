# SQL Queries for Database Documentation

This document contains the SQL queries used by the Database Documentation Generator skill.

## Main Structure Query

The primary query extracts column information from PostgreSQL's information_schema:

```sql
SELECT
 a.column_name AS 代码,
 udt_name AS 数据类型,
 CASE
 WHEN udt_name IN ('varchar', 'character varying') AND COALESCE(character_maximum_length, -999) = -999 THEN '2000'
 WHEN udt_name IN ('timestamp', 'timestamptz', 'time', 'timetz') AND COALESCE(datetime_precision, -999) = -999 THEN '6'
 ELSE
 (CASE
 WHEN COALESCE(character_maximum_length, -999) = -999 THEN 
   CASE 
   WHEN numeric_precision IS NOT NULL THEN numeric_precision::text
   WHEN datetime_precision IS NOT NULL THEN datetime_precision::text
   ELSE NULL
   END
 ELSE character_maximum_length::text
 END)||(CASE
 WHEN udt_name IN ('numeric', 'decimal') THEN ','||COALESCE(numeric_scale::text, '0')
 ELSE '' 
 END)
 END AS 长度,

 CASE
 WHEN is_nullable = 'YES' THEN 'FALSE'
 ELSE 'TRUE'
 END AS 强制,
 col_description(b.oid, a.ordinal_position) AS 注释
FROM
 information_schema.columns AS a
 LEFT JOIN
 pg_class AS b ON a.table_name = b.relname
 LEFT JOIN
 information_schema.key_column_usage AS pk ON a.table_name = pk.table_name AND a.column_name = pk.column_name
 LEFT JOIN
 information_schema.table_constraints AS tc ON pk.constraint_name = tc.constraint_name
WHERE
 a.table_name = %s
ORDER BY
 a.table_schema,
 a.table_name,
 a.ordinal_position;
```

## Default Values

### varchar/character varying
- Default length: 2000
- Applied when: `character_maximum_length` is NULL or -999

### timestamp/timestamptz/time/timetz
- Default precision: 6
- Applied when: `datetime_precision` is NULL or -999

### numeric/decimal
- Format: `precision,scale` (e.g., `10,2`)
- Scale defaults to 0 if NULL

## Table List Query

Get all tables in the public schema:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

## Column Types Mapping

PostgreSQL to Excel type mapping:

| PostgreSQL Type | Excel Display | Notes |
|----------------|---------------|-------|
| int8, int4, int2 | int8, int4, int2 | Integer types |
| varchar, text | varchar | Character types |
| timestamp, timestamptz | timestamp | Date/time types |
| numeric, decimal | numeric | Decimal numbers |
| bool | bool | Boolean |
| json, jsonb | json | JSON data |
| uuid | uuid | UUID |

## Performance Considerations

1. **Large Schemas**: The query is optimized for performance but may be slow on databases with thousands of tables
2. **Caching**: Consider caching results for frequently accessed schemas
3. **Permissions**: Ensure the database user has read access to information_schema

## Security Considerations

### Query Safety
- This skill only executes **SELECT** queries against `information_schema`
- No data modification (INSERT, UPDATE, DELETE, DROP, etc.)
- Read-only access to metadata only

### Permission Requirements
The database user needs:
- `CONNECT` permission to the database
- `SELECT` permission on `information_schema` views
- No other permissions required

### Network Security
```python
# Recommended: Use SSL/TLS for connections
db_config = {
    'host': 'your_host',
    'port': 5432,
    'database': 'your_db',
    'user': 'your_user',
    'EXAMPLE_PASSWORD': 'your_EXAMPLE_PASSWORD',
    'sslmode': 'require'  # Enable SSL
}
```

## Customization

### Modify Default Values
Edit the CASE statements in the main query to change default values:

```sql
-- Change varchar default from 2000 to 1000
WHEN udt_name IN ('varchar', 'character varying') AND COALESCE(character_maximum_length, -999) = -999 THEN '1000'

-- Change timestamp default from 6 to 3
WHEN udt_name IN ('timestamp', 'timestamptz', 'time', 'timetz') AND COALESCE(datetime_precision, -999) = -999 THEN '3'
```

### Add Additional Information
To include primary key information:

```sql
-- Add primary key column
CASE
 WHEN tc.constraint_type = 'PRIMARY KEY' THEN 'TRUE'
 ELSE 'FALSE'
END AS 主键,
```

### Filter by Schema
To filter tables by specific schema:

```sql
-- In WHERE clause
AND a.table_schema = 'your_schema'
```

## Security Audit Queries

### Verify Read-Only Access
```sql
-- Check user permissions (run as superuser)
SELECT 
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.role_table_grants
WHERE grantee = 'your_username'
ORDER BY table_schema, table_name;
```

### Verify No Data Access
```sql
-- Confirm user cannot access actual table data
-- This should fail for a properly restricted user
SELECT * FROM your_table LIMIT 1;
```

### Monitor Query Activity
```sql
-- Monitor queries from this user (PostgreSQL 9.2+)
SELECT 
    usename,
    application_name,
    query_start,
    query
FROM pg_stat_activity
WHERE usename = 'your_username'
ORDER BY query_start DESC;
```