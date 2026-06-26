# Databases

---

## Database Module

### list

List databases in a document.

```bash
affine-cli database list [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --doc | -d | **Yes** | Document ID containing the database |
| --workspace | -w | No | Workspace ID |

### columns

Get column definitions of a database.

```bash
affine-cli database columns [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --doc | -d | **Yes** | Document ID |
| --id | -i | **Yes** | Database block ID |
| --workspace | -w | No | Workspace ID |

### query

Query rows from a database.

```bash
affine-cli database query [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --doc | -d | **Yes** | Document ID |
| --id | -i | **Yes** | Database block ID |
| --rows | -r | No | Comma-separated row IDs to return |
| --columns | -c | No | Comma-separated column names to return |
| --query | -q | No | Filter conditions in JSON format |
| --full | -f | No | Return full row data |
| --workspace | -w | No | Workspace ID |

**Filter format:**
```json
[{"column":"ColumnName","operator":"eq","value":"Value"}]
```

**Operators:**
- `eq` - Equal
- `neq` - Not equal
- `contains` - Contains substring
- `startswith` - Starts with
- `endswith` - Ends with
- `gt` - Greater than
- `gte` - Greater than or equal
- `lt` - Less than
- `lte` - Less than or equal

**Multiple filters (AND logic):**
```json
[{"column":"Status","operator":"eq","value":"Done"},{"column":"Priority","operator":"eq","value":"High"}]
```

**With OR logic:**
```json
{"mode":"or","filters":[{"column":"Status","operator":"eq","value":"Done"},{"column":"Status","operator":"eq","value":"In Progress"}]}
```

**Examples:**
```bash
# Simple filter
affine-cli database query --doc DOC_ID --id DB_ID -q '[{"column":"Status","operator":"eq","value":"Done"}]'

# Multiple columns
affine-cli database query --doc DOC_ID --id DB_ID --columns "Title,Status,Priority"

# Full output
affine-cli database query --doc DOC_ID --id DB_ID --full
```

### create

Create a new database.

```bash
affine-cli database create [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --content | -c | **Yes** | Data in JSON format |
| --doc | -d | No | Document ID (creates new doc if not specified) |
| --title | -t | No | Database title (and new document title) |
| --view-mode | -m | No | View mode: `table` (default) or `kanban` |
| --workspace | -w | No | Workspace ID |

**Content formats:**

Simple array:
```json
[{"Title":"Task 1","Status":"Todo"},{"Title":"Task 2","Status":"Done"}]
```

With column definitions:
```json
{"title":"My Database","columns":[{"name":"Title","type":"text"},{"name":"Status","type":"select","options":["Todo","Done"]},"data":[{"Title":"Task 1","Status":"Todo"}]}
```

**Examples:**
```bash
# Create in new document
affine-cli database create --title "Task Tracker" --content '[{"Task":"Review PR","Status":"Todo"}]'

# Create in existing document
affine-cli database create --doc DOC_ID --content '[{"Task":"New Task","Status":"Todo"}]'

# From file
affine-cli database create --content "@tasks.json"
```

### insert

Insert rows into database.

```bash
affine-cli database insert [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --doc | -d | **Yes** | Document ID |
| --id | -i | **Yes** | Database block ID |
| --content | -c | **Yes** | Row data in JSON format |
| --workspace | -w | No | Workspace ID |

**Content format:**
```json
[{"Title":"Task","Status":"Todo"}]
```

Or single row:
```json
{"Title":"Task","Status":"Todo"}
```

**Examples:**
```bash
# Single row
affine-cli database insert --doc DOC_ID --id DB_ID --content '{"Task":"New","Status":"Todo"}'

# Multiple rows
affine-cli database insert --doc DOC_ID --id DB_ID --content '[{"Task":"A","Status":"Todo"},{"Task":"B","Status":"Done"}]'
```

### update

Update rows in database.

```bash
affine-cli database update [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --doc | -d | **Yes** | Document ID |
| --id | -i | **Yes** | Database block ID |
| --values | -v | **Yes** | Updated cell values in JSON |
| --row | -r | No* | Row block ID |
| --query | -q | No* | Filter conditions |
| --workspace | -w | No | Workspace ID |

*Either `--row` or `--query` is required.

**Examples:**
```bash
# Update specific row
affine-cli database update --doc DOC_ID --id DB_ID --values '{"Status":"Done"}' --row ROW_ID

# Update filtered rows
affine-cli database update --doc DOC_ID --id DB_ID --values '{"Status":"Done"}' -q '[{"column":"Status","operator":"eq","value":"Todo"}]'
```

### delete (database)

Delete entire database.

```bash
affine-cli database delete [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --doc | -d | **Yes** | Document ID |
| --id | -i | **Yes** | Database block ID |
| --workspace | -w | No | Workspace ID |

### remove (row)

Delete rows from database.

```bash
affine-cli database remove [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --doc | -d | **Yes** | Document ID |
| --id | -i | **Yes** | Database block ID |
| --row | -r | No* | Row block ID |
| --query | -q | No* | Filter conditions |
| --workspace | -w | No | Workspace ID |

*Either `--row` or `--query` is required.

**Examples:**
```bash
# Remove specific row
affine-cli database remove --doc DOC_ID --id DB_ID --row ROW_ID

# Remove filtered rows
affine-cli database remove --doc DOC_ID --id DB_ID -q '[{"column":"Status","operator":"eq","value":"Cancelled"}]'