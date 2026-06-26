---
name: fargo
description: Look up pool player ratings and handicap data from FargoRate. Use when the user asks about a pool player's rating, FargoRate ID, match odds, race-to recommendations, handicaps, top-ranked pool players, or rating changes over time. A local db can be enabled to track rating changes across runs. Contact fields in the db are local-only and never sent to an API.
version: 0.4.1
metadata:
  openclaw:
    emoji: "🎱"
    homepage: https://github.com/rgstephens/fargo-skill
    requires:
      bins:
        - fargo
    install:
      - kind: brew
        tap: rgstephens/fargo
        formula: fargo
        bins:
          - fargo

---

# FargoRate

Look up pool player ratings, match odds, and handicap data from [FargoRate](https://fargorate.com) using the `fargo` CLI tool.

---

## Commands

### `search` — Search players by name or FargoRate ID

```bash
fargo search <name or id>
```

```bash
fargo search "John Smith"
fargo search 12345
```

### `lookup` — Lookup a player by FargoRate ID

Alias for `search` that accepts a single ID.

```bash
fargo lookup <id>
```

```bash
fargo lookup 12345
```

### `bulk` — Lookup multiple players at once

```bash
fargo bulk <id1> [id2 ...]
fargo bulk --group <name>
```

```bash
fargo bulk 12345 67890 11111

# Use a saved group (see `group` command)
fargo bulk --db --group monday-league
```

| Flag             | Description                                                               |
|------------------|---------------------------------------------------------------------------|
| `--group <name>` | Use a saved group of player IDs instead of listing them (requires `--db`) |

Uses the configured custom list ID (see `setup`). Defaults to the built-in list ID.

### `odds` — Calculate match odds

```bash
fargo odds <rating1> <rating2> <race1> <race2>
```

```bash
# Player rated 550 (races to 7) vs player rated 480 (races to 9)
fargo odds 550 480 7 9
```

### `races` — Get recommended race lengths

```
fargo races <rating1> <rating2> [--type 0|1|2] [--length N]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--type` | `1` | Race type: `0`=Scotch Doubles, `1`=Singles, `2`=Team |
| `--length` | — | Fix the total race length; omit to auto-recommend |

```bash
# Recommended singles race lengths for two players
fargo races 550 480

# Scotch doubles race recommendation
fargo races 550 480 --type 0

# Singles races that fit within a total of 15 games
fargo races 550 480 --length 15
```

### `top` — View top 10 ranked players

```bash
fargo top [--ranking World|US] [--gender M|F]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--ranking` | `World` | `World` or `US` |
| `--gender` | `M` | `M` or `F` |

```bash
fargo top
fargo top --ranking US --gender F
```

### `setup` — Configure the tool

```
fargo setup [--list-id ID]
```

Saves a custom list ID used by the `bulk` command to `~/.nanobot/workspace/fargorate/config.json`.

```bash
# Interactive prompt
fargo setup

# Non-interactive
fargo setup --list-id myCustomListId
```

### `group` — Manage named groups of player IDs

Groups let you save a named list of FargoRate IDs so you don't have to type them every time. All group commands require `--db`.

```bash
# Create or replace a group
fargo --db group set monday-league 12345 67890 11111

# List all groups
fargo --db group list

# Show members of a group (shows cached name/rating if player has been looked up)
fargo --db group show monday-league

# Delete a group
fargo --db group delete monday-league
```

Groups can then be used with `bulk`:

```bash
fargo --db bulk --group monday-league
fargo --changes --db bulk --group monday-league
```

### Version

```bash
fargo --version
```

---

## Global Flags

These flags work with every command:

| Flag          | Description                                                              |
|---------------|--------------------------------------------------------------------------|
| `--json`      | Output raw JSON as received from the API                                 |
| `--db [path]` | Save retrieved player data into a SQLite database                        |
| `--changes`   | Only output players whose rating or robustness changed (requires `--db`) |

---

## Database (`--db`)

The `--db` flag enables a local SQLite database that persists player data across runs. It works with `search`, `lookup`, and `bulk` — any command that retrieves player records from the API.

### Usage

```bash
# Use the default database file (fargo.db in the current directory)
fargo --db search "John Smith"
fargo --db bulk 12345 67890

# Use a custom path (requires = syntax)
fargo --db=~/data/fargo.db search "John Smith"

# Combine with --json (outputs raw JSON AND updates the database)
fargo --json --db search "John Smith"
```

### Behavior

- The database file is created automatically if it does not exist.
- Player rows are inserted or updated on each run — existing records are refreshed, new ones added.
- `previous_rating` is updated automatically whenever the rating changes.
- A row is appended to `rating_history` only when the player is **new** or their **rating has changed**, avoiding duplicate history entries.

### Schema

```sql
CREATE TABLE players (
    id                      TEXT PRIMARY KEY,
    first_name              TEXT NOT NULL,
    last_name               TEXT NOT NULL,
    location                TEXT,
    rating                  INTEGER NOT NULL DEFAULT 0,
    previous_rating         INTEGER NOT NULL DEFAULT 0,
    provisional_rating      INTEGER NOT NULL DEFAULT 0,
    robustness              INTEGER NOT NULL DEFAULT 0,
    last_update_timestamp   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email                   TEXT,
    mobile                  TEXT,
    telegram                TEXT,
    discord                 TEXT,
    preferred_communication TEXT CHECK(preferred_communication IN ('email','mobile','telegram','discord'))
);

CREATE TABLE rating_history (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id          TEXT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    timestamp          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    rating             INTEGER NOT NULL,
    provisional_rating INTEGER NOT NULL,
    robustness         INTEGER NOT NULL
);

CREATE TABLE fargo_groups (
    name       TEXT PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fargo_group_members (
    group_name TEXT NOT NULL REFERENCES fargo_groups(name) ON DELETE CASCADE,
    player_id  TEXT NOT NULL,
    PRIMARY KEY (group_name, player_id)
);
```

> **Note:** Contact fields (`email`, `mobile`, `telegram`, `discord`, `preferred_communication`) are stored in the database but are not populated by the FargoRate API. They can be set directly in the database and are included in `--changes` output when a player's rating changes.

---

## Change Detection (`--changes`)

The `--changes` flag filters output to only players whose **rating or robustness changed** since the last run. It requires `--db` and works with `search`, `lookup`, and `bulk`.

All fetched players are still written to the database on every run — `--changes` only affects what is printed.

### Examples

```bash
# Report only players whose rating or robustness changed
fargo --changes --db search "John Smith"
fargo --changes --db bulk 12345 67890 11111

# Custom DB path
fargo --changes --db=~/data/fargo.db bulk 12345 67890

# Machine-readable JSON output of changes (useful for bots)
fargo --changes --json --db search "John Smith"
```

### Example output

```text
1 change(s) detected:

Name       : John Smith
ID         : 12345
Rating     : 480 → 495 (provisional: 0)
Robustness : 200 → 215
Location   : Phoenix AZ
Email      : john@example.com
Preferred  : email
---
```

New players (not previously in the database) are marked `[NEW]` and show their current values without a `→` arrow.

### JSON output example (`--json --changes`)

```json
[
  {
    "firstName": "John",
    "lastName": "Smith",
    "id": "12345",
    "rating": 495,
    "provisionalRating": 0,
    "robustness": 215,
    "location": "Phoenix AZ",
    "isNew": false,
    "previousRating": 480,
    "previousRobustness": 200,
    "email": "john@example.com",
    "preferredCommunication": "email"
  }
]
```

Contact fields (`email`, `mobile`, `telegram`, `discord`, `preferredCommunication`) are omitted from JSON output when empty.

When no changes are detected, the output is:

```text
No changes detected.
```
