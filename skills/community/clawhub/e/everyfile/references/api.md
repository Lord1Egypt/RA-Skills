# everyfile — Python API Reference

Typed Python library for instant file search via Voidtools Everything.
Zero external dependencies. DB-API 2.0-style `Cursor`/`Row` objects.

## Install

```powershell
pip install everyfile
```

## Import Surface

```python
from everyfile import search, count          # module-level shortcuts
from everyfile import Everything             # reusable client (instance affinity)
from everyfile import Cursor, Row            # types for annotation
from everyfile import EverythingError        # error handling
```

## Complex Examples

```python
from everyfile import Everything, search, count

# --- Reusable client ---
ev = Everything()              # auto-detect instance
ev = Everything("1.5a")       # target specific instance

# --- Search with full options ---
cursor = ev.search(
    "ext:py size:>10kb dm:thisweek",
    fields="name,size,date_modified",   # or "all", "meta", "dates"
    sort="size",                         # name|path|size|ext|created|modified|accessed
    descending=True,
    limit=100,
    offset=0,
    match_case=False,
    match_path=False,                    # True to match against full path
    match_whole_word=False,
    regex=False,
)

# --- Cursor metadata (available before iteration) ---
cursor.total   # int — total matches in Everything DB
cursor.count   # int — results in this page (respects limit/offset)
len(cursor)    # same as cursor.count

# --- Iteration ---
for row in cursor:
    print(row.name, row.size, row.date_modified)

# --- Fetch patterns ---
cursor = ev.search("ext:log", limit=1000, fields="size")
first = cursor.fetchone()              # Row | None
batch = cursor.fetchmany(50)           # list[Row] up to 50
rest  = cursor.fetchall()              # list[Row] all remaining

# Batch processing with chunked reads
cursor = ev.search("ext:csv", limit=10_000, fields="name,size")
while batch := cursor.fetchmany(500):
    process(batch)
```

## Row Access

```python
row = cursor.fetchone()
row.name              # str   — always present
row.path              # str   — parent directory
row.full_path         # str   — complete path
row.size              # int | None
row.date_modified     # str | None (ISO 8601)
row.date_created      # str | None (ISO 8601)
row.is_file           # bool | None
row.ext               # str | None
row.attributes        # str | None (compact: "DA--" etc.)

row["name"]           # dict-style access
row.get("size", 0)    # with default
"size" in row         # membership test
row.to_dict()         # serialize to plain dict
```

## Count (no result transfer)

```python
total = count("ext:py")
total = ev.count("ext:py", match_path=True)
```

## Introspection

```python
ev.version          # {"major": 1, "minor": 5, "revision": 0, "build": 1404, "version": "1.5.0.1404"}
ev.info             # {"version": "1.5.0.1404", "is_admin": False, "is_appdata": False, ...}
ev.instance_name    # "1.5a"
Everything.instances()  # [{"name": "1.5a", "hwnd": ...}, ...]
```

## Error Handling

```python
from everyfile import search, EverythingError

try:
    results = search("ext:py").fetchall()
except EverythingError as e:
    if e.is_not_running:
        print("Everything is not running — start it first")
    else:
        print(f"IPC error: {e}")
```

## Real-World Patterns

```python
from everyfile import Everything
from pathlib import Path
import json

ev = Everything()

# Find largest Python files system-wide
top = ev.search("ext:py", fields="name,full_path,size", sort="size", descending=True, limit=20)
for row in top:
    print(f"{row.size:>12,}  {row.full_path}")

# Collect all .env files for audit
envs = ev.search("ext:env", fields="full_path", limit=500).fetchall()
paths = [Path(r.full_path) for r in envs]

# Export search results as JSON
cursor = ev.search("ext:rs dm:today", fields="all", sort="modified", descending=True, limit=50)
data = [row.to_dict() for row in cursor]
Path("results.json").write_text(json.dumps(data, indent=2))

# Duplicate detection — find files with same name
dupes = ev.search("dupe: ext:dll", fields="name,full_path,size", sort="name", limit=1000)
by_name: dict[str, list[str]] = {}
for row in dupes:
    by_name.setdefault(row.name, []).append(row.full_path)

# Conditional count before expensive operation
n = ev.count("ext:log size:>100mb")
if n > 0:
    for row in ev.search("ext:log size:>100mb", fields="full_path,size", sort="size", descending=True):
        archive(row.full_path)
```

## When to Use API vs CLI

| Scenario | Use |
|----------|-----|
| Find/list files in terminal | CLI (`ev`) |
| File search in a Python script/tool | API (`search()`, `Everything`) |
| One-off lookup from agent | CLI (`ev -l`) |
| Processing results programmatically | API (iterate `Cursor`) |
| Piping between shell commands | CLI (pipe composition) |
