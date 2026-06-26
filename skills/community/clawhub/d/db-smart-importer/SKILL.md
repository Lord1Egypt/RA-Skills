---
name: db-smart-importer
description: "Intelligent database import from .csv and .sql dumps into MySQL, MariaDB, and SQLite. Analyzes schemas, parses SQL dumps, suggests column mappings based on content patterns and executes data transfers. Use when: (1) Importing CSV/SQL data into MySQL/MariaDB, (2) Migrating data between databases, (3) Parsing .sql dump files, (4) Automating data ingestion with smart column correlation."
---

# DB Smart Importer

This skill provides a workflow for importing CSV and SQL dump files into MySQL, MariaDB, and SQLite databases with intelligent column mapping.

## When to Use This Skill

- User needs to import CSV files into MySQL/MariaDB/SQLite
- User has a .sql dump file they want to execute
- Column names in source don't match destination (e.g., "email address" → "email")
- User wants automated mapping suggestions based on patterns
- Data migration between database tables

## NEVER Do

- NEVER import directly without reviewing the suggested mappings first
- NEVER assume column types match — verify before import
- NEVER skip backing up the database before bulk imports

## Workflow

### Step 1: Analyze Source and Destination

Use analyze_schema.py to extract schema information from your source (CSV/SQL dump) and destination database.

**Examples:**

```bash
# Analyze CSV file
python scripts/analyze_schema.py csv /path/to/data.csv

# Analyze SQL dump file
python scripts/analyze_schema.py sql /path/to/dump.sql

# Analyze SQLite database
python scripts/analyze_schema.py sqlite /path/to/database.db

# Analyze MySQL/MariaDB database (requires mysql-connector-python)
python scripts/analyze_schema.py mysql localhost --user root --password secret --database mydb
```

### Step 2: Get Column Mapping Suggestions

Once you have analyzed both source and destination, use map_columns.py to get mapping suggestions:

```powershell
python scripts/map_columns.py '["account name", "email address"]' '["client", "email"]'
```

### Step 3: Execute Import

After confirming mappings, use execute_import.py:

**CSV Import to SQLite:**
```bash
python scripts/execute_import.py csv /path/to/data.csv --db-type sqlite --db-path /path/db.db --table clients --mapping '{"email": "email", "name": "client"}'
```

**CSV Import to MySQL/MariaDB:**
```bash
python scripts/execute_import.py csv /path/to/data.csv --db-type mysql --host localhost --user root --password secret --database mydb --table clients --mapping '{"email": "email", "name": "client"}'
```

**Execute SQL Dump:**
```bash
# To SQLite
python scripts/execute_import.py sql /path/to/dump.sql --db-type sqlite --db-path /path/db.db

# To MySQL/MariaDB
python scripts/execute_import.py sql /path/to/dump.sql --db-type mysql --host localhost --user root --password secret --database mydb
```

## Script Reference

| Script | Purpose |
|--------|---------|
| analyze_schema.py | Extract schema from MySQL/MariaDB/SQLite, parse SQL dumps, or sample CSV data |
| map_columns.py | Suggest column mappings using fuzzy pattern matching |
| execute_import.py | Import CSV into databases or execute SQL dump files |

## Tips

- The mapper uses fuzzy matching: "phone" ≈ "contact_number" ≈ "phone_number"
- Providing sample data improves mapping accuracy
- Always review mappings before executing — automated suggestions aren't perfect