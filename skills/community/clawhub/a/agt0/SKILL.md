---
name: agt0
description: Local-first agent storage — SQLite database, virtual filesystem, and memory in one .db file. Use when persisting agent state, querying CSV/JSONL/logs with SQL, or using fs_read/fs_write via the agt0 CLI or Node API.
---

# agt0 — Agent Storage Skill

> **One file. All your agent needs.**
> Local-first database + filesystem + memory in a single SQLite file.

You are using **agt0** to persist data. Follow this reference precisely.

---

## Setup

```bash
npm install -g @seekcontext/agt0
agt0 init <dbname>
agt0 use <dbname>          # set as default (omit db name in later commands)
```

After `agt0 use`, you can omit `<db>` from all commands below.

---

## Essential Patterns

### Store and retrieve data (SQL)

```bash
# Inline SQL
agt0 sql -q "CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT, status TEXT)"
agt0 sql -q "INSERT INTO tasks (title, status) VALUES ('Build API', 'doing')"
agt0 sql -q "SELECT * FROM tasks WHERE status = 'doing'"

# Execute SQL file
agt0 sql -f schema.sql
```

### Store and retrieve files (CLI)

```bash
agt0 fs put ./data.csv myapp:/data/data.csv        # upload file
agt0 fs put -r ./src myapp:/src                     # upload directory
agt0 fs cat myapp:/data/data.csv                    # read file
agt0 fs ls myapp:/data/                             # list directory
agt0 fs get myapp:/data/data.csv ./local.csv        # download file
agt0 fs rm myapp:/data/old.csv                      # delete file
agt0 fs mkdir myapp:/data/exports                   # create directory
```

### Store and retrieve files (SQL)

```sql
SELECT fs_write('/memory/context.md', 'User prefers dark mode');
SELECT fs_read('/memory/context.md');
SELECT fs_append('/logs/session.log', 'Step completed' || char(10));
SELECT fs_exists('/config.json');                  -- 1 or 0
SELECT fs_size('/config.json');                    -- bytes
```

### Query files as tables (zero-import)

```sql
-- CSV → queryable rows (each row is JSON in _data column)
SELECT json_extract(_data, '$.name') AS name,
       json_extract(_data, '$.email') AS email
FROM fs_csv('/data/users.csv')
WHERE json_extract(_data, '$.role') = 'admin';

-- JSONL structured logs
SELECT json_extract(line, '$.level') AS level, COUNT(*)
FROM fs_jsonl('/logs/app.jsonl')
GROUP BY level;

-- Grep across text files
SELECT _path, _line_number, line
FROM fs_text('/src/**/*.ts')
WHERE line LIKE '%TODO%';

-- Directory listing
SELECT path, type, size, mtime FROM fs_list('/data/');
```

### CSV / JSONL with real columns (virtual tables; single file only)

Use **`CREATE VIRTUAL TABLE ... USING csv_expand(...)`** / **`tsv_expand`** / **`jsonl_expand`** when you want **native column names** instead of `json_extract(_data, ...)`. **No globs** — one path per `CREATE`. For `**/*.csv` patterns, keep using `fs_csv` / `fs_jsonl`.

```sql
CREATE VIRTUAL TABLE v_users USING csv_expand('/data/users.csv');
SELECT name, email FROM v_users WHERE role = 'admin';

CREATE VIRTUAL TABLE v_logs USING jsonl_expand('/logs/app.jsonl');
SELECT level, msg FROM v_logs WHERE level = 'error';
```

Schema is fixed at `CREATE` time; `DROP` and recreate if the file layout changes. JSONL columns = sorted union of object keys from the first `AGT0_FS_EXPAND_JSONL_SCAN_LINES` non-empty lines (default `256`). Optional 2nd arg: same JSON as TVFs (`strict`, `delimiter`, `header`, etc.).

**`agt0 sql` (CLI only):** for a **literal single-file path** (no globs), `fs_csv` / `fs_tsv` / `fs_jsonl` are **auto-rewritten** so `SELECT *` returns real columns. Set `AGT0_SQL_FS_EXPAND=0` to disable. In Node, call `expandFsTableSql(sql, db)` from the package if you need the same rewrite.

### Import file data into tables

```sql
INSERT INTO users (name, email)
SELECT DISTINCT
  json_extract(_data, '$.name'),
  json_extract(_data, '$.email')
FROM fs_csv('/data/users.csv')
WHERE json_extract(_data, '$.email') IS NOT NULL;
```

---

## Complete SQL Function Reference

### Scalar Functions

| Function | Returns | Description |
|---|---|---|
| `fs_read(path)` | TEXT | Read file content as text |
| `fs_write(path, content)` | INTEGER | Write/overwrite file, returns bytes |
| `fs_append(path, data)` | INTEGER | Append to file, returns total bytes |
| `fs_exists(path)` | INTEGER | 1 if path exists, 0 otherwise |
| `fs_size(path)` | INTEGER | File size in bytes |
| `fs_mtime(path)` | TEXT | Last modified time (ISO 8601) |
| `fs_remove(path [, recursive])` | INTEGER | Delete file/dir, returns deleted count |
| `fs_mkdir(path [, recursive])` | INTEGER | Create directory (1=recursive) |
| `fs_truncate(path, size)` | INTEGER | Truncate to byte size |
| `fs_read_at(path, offset, length)` | TEXT | Read byte range as UTF-8 |
| `fs_write_at(path, offset, data)` | INTEGER | Write at byte offset (pads with NUL) |

### Table-Valued Functions

| Function | Columns | Description |
|---|---|---|
| `fs_list(dir)` | path, type, size, mode, mtime | List directory entries |
| `fs_text(path [, opts])` | _line_number, line, _path | Read text by line |
| `fs_csv(path [, opts])` | _line_number, _data, _path | Read CSV (row → JSON) |
| `fs_tsv(path [, opts])` | _line_number, _data, _path | Read TSV (row → JSON) |
| `fs_jsonl(path [, opts])` | _line_number, line, _path | Read JSONL by line |

**Virtual table modules** (dynamic columns; **single path**, no globs):

| Module | Example |
|---|---|
| `csv_expand` | `CREATE VIRTUAL TABLE t USING csv_expand('/data/x.csv' [, opts])` |
| `tsv_expand` | `CREATE VIRTUAL TABLE t USING tsv_expand('/data/x.tsv' [, opts])` |
| `jsonl_expand` | `CREATE VIRTUAL TABLE t USING jsonl_expand('/logs/x.jsonl' [, opts])` |

**Path globs:** `*` = one segment, `**` = any depth, `?` = one char. Example: `/logs/**/*.log`.

**Options** (JSON string, 2nd arg): `exclude` (comma-separated globs), `strict` (bool — fail on bad rows), `delimiter` (string), `header` (bool). (`exclude` is ignored by `*_expand` modules.)

**Limits** (env vars): `AGT0_FS_MAX_FILES`, `AGT0_FS_MAX_FILE_BYTES`, `AGT0_FS_MAX_TOTAL_BYTES`, `AGT0_FS_MAX_ROWS` (optional cap per TVF / expand scan), `AGT0_FS_PARSE_CHUNK_BYTES`, `AGT0_FS_PREVIEW_BYTES` (multi-file CSV/TSV column discovery), `AGT0_FS_EXPAND_JSONL_SCAN_LINES` (JSONL key discovery for `jsonl_expand`), `AGT0_SQL_FS_EXPAND` (CLI rewrite of literal-path `fs_*` TVFs; default on).

---

## Database Management

```bash
agt0 list                                # list all databases
agt0 inspect <db>                        # overview (tables, files, size)
agt0 inspect <db> tables                 # table list with row counts
agt0 inspect <db> schema                 # show CREATE statements
agt0 dump <db> -o backup.sql             # full SQL export
agt0 dump <db> --ddl-only                # schema only
agt0 seed <db> schema.sql                # run SQL file
agt0 delete <db> --yes                   # delete database
agt0 branch create <db> --name staging   # branch (copy) database
agt0 branch list <db>                    # list branches
agt0 branch delete <db> --name staging   # delete branch
```

---

## Interactive Shells

### SQL REPL

```bash
agt0 sql <db>
```

Type SQL ending with `;` to execute. Dot commands: `.help`, `.tables`, `.schema`, `.fshelp`, `.quit`.

### Filesystem Shell

```bash
agt0 fs sh <db>
```

Commands: `ls`, `cd`, `cat`, `echo <text> > <path>`, `mkdir`, `rm`, `pwd`, `exit`, `help`.

---

## Storage Layout

```
~/.agt0/
├── config.json              # default database setting
└── databases/
    ├── myapp.db             # single file = tables + files + memory
    └── myapp-staging.db     # branch
```

Override with `AGT0_HOME` env var.

---

## Critical Rules

- All data is **local**. No network calls, no API keys.
- Each database is a **single `.db` file**. Copy it to back up or share.
- The `_fs` table is internal. **Never drop it.**
- CSV rows from **`fs_csv`** are JSON in `_data` (`json_extract(_data, '$.column_name')`), or use **`csv_expand`** / **`tsv_expand`** for real columns after `CREATE VIRTUAL TABLE`.
- `fs_read_at` / `fs_write_at` operate on **byte** offsets.
- The SQL REPL (`.fshelp`) and the filesystem shell (`help`) are **different** interfaces with different commands.
- Glob `*` matches one path segment (no `/`). Use `**` to match across directories.
