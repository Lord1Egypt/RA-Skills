# Building Your Own — Files, Then SQLite

A one-person CRM in plain files is not a compromise; for a few hundred contacts it beats every hosted tool on speed of entry and costs nothing to leave. It fails at exactly two things: concurrent writes and real queries. This file covers building it, querying it, and migrating it when those two arrive.

Applies when `crm_tool` is `files` or `sqlite`. The data lives in `~/Clawic/data/crm/db/`, backups in `db/backups/` (`memory-template.md`).

**Contents:** [The File Version](#the-file-version) · [The JSON Version](#the-json-version) · [The SQLite Schema](#the-sqlite-schema) · [Queries That Earn Their Keep](#queries-that-earn-their-keep) · [Migrating Files To SQLite](#migrating-files-to-sqlite) · [Backups](#backups) · [Sync Across Devices](#sync-across-devices) · [Helper Scripts Worth Having](#helper-scripts-worth-having) · [When To Stop](#when-to-stop)

**Before editing the database**, read `## System` in `~/Clawic/data/crm/memory.md` for the schema in force and `## Boxes` for what exists. Before any bulk write, copy the file into `db/backups/` with today's date (SKILL.md Rule 9).

## The File Version

Smallest thing that works, and the one most people should stay on:

```
~/Clawic/data/crm/db/
├── contacts.md        # one table, the identity key is the email
├── deals.md           # open deals; closed ones live in ../closed-deals.md
└── backups/
```

Interactions do **not** go here — they are already `~/Clawic/data/crm/interactions/<year>.md`, which is append-only and cut by year for exactly this reason (`memory-template.md`).

A markdown table stays workable to roughly 200 rows: past that, every edit is a scroll and every alignment breaks. That is the signal for JSON or SQLite, not the row count in itself.

## The JSON Version

Preferred when a script will touch the data, because a markdown table has no types.

```json
{
  "id": "9f2c1b7e-...",
  "name": "Ana Ruiz",
  "email": "ana@northwind.com",
  "org": "northwind.com",
  "role": "Head of Ops",
  "channel": "email",
  "tier": "A",
  "source": "referral",
  "tags": ["e-commerce", "conference-2026"],
  "suppressed": false,
  "created": "2026-03-04",
  "updated": "2026-07-24"
}
```

- **One JSON array per entity, one file per entity** — `contacts.json`, `deals.json`. Nesting interactions inside a contact means rewriting the whole contact to log a call, and it makes "everything that happened last week" unanswerable.
- **UUID ids** (`schema.md`), generated at creation. Never array position, never an incrementing counter.
- **ISO dates, lowercased emails, money as a number plus a `currency` field.** These four conventions are what make the eventual SQLite import a straight copy.
- Pretty-print with a stable key order and one record per line block, so a diff is readable and version control is useful.
- Write atomically: write to a temp file, then rename over the original. A crash mid-write on the whole-file rewrite pattern is how a file CRM loses everything.

## The SQLite Schema

One file, four tables, foreign keys on:

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE orgs (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  domain TEXT UNIQUE,
  segment TEXT,
  created TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE contacts (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE COLLATE NOCASE,
  org_id TEXT REFERENCES orgs(id),
  role TEXT,
  channel TEXT,
  tier TEXT CHECK (tier IN ('A','B','C')),
  source TEXT,
  suppressed INTEGER NOT NULL DEFAULT 0,
  created TEXT NOT NULL DEFAULT (date('now')),
  updated TEXT
);

CREATE TABLE deals (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  org_id TEXT REFERENCES orgs(id),
  contact_id TEXT REFERENCES contacts(id),
  value REAL,
  currency TEXT,
  stage TEXT NOT NULL,
  stage_entered TEXT NOT NULL,
  close_date TEXT,
  close_date_asof TEXT,
  next_step TEXT,
  next_step_date TEXT,
  source TEXT,
  result TEXT CHECK (result IN ('won','lost') OR result IS NULL),
  reason TEXT,
  created TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE interactions (
  id TEXT PRIMARY KEY,
  date TEXT NOT NULL,
  contact_id TEXT NOT NULL REFERENCES contacts(id),
  deal_id TEXT REFERENCES deals(id),
  type TEXT CHECK (type IN ('call','meeting','email','note')),
  direction TEXT CHECK (direction IN ('in','out')),
  summary TEXT NOT NULL,
  next_step TEXT
);

CREATE INDEX idx_int_contact_date ON interactions(contact_id, date DESC);
CREATE INDEX idx_deals_stage ON deals(stage, stage_entered);
```

Details that matter later: `COLLATE NOCASE` on email makes the identity key case-insensitive at the database level, so a duplicate cannot be inserted by mistake (`hygiene.md`); `PRAGMA foreign_keys = ON` is **per connection** and off by default in SQLite, so a script that forgets it will happily create orphans; `stage_entered` is what makes the stall rule computable (`pipeline.md`); dates as ISO text sort and compare correctly without a date type.

## Queries That Earn Their Keep

These four replace most of what a hosted CRM's UI is for.

```sql
-- Overdue: open deals whose next step has passed, or that have none
SELECT title, stage, next_step, next_step_date FROM deals
WHERE result IS NULL AND (next_step_date < date('now') OR next_step IS NULL)
ORDER BY next_step_date;

-- Stalled: no stage change in stall_days (21 by default)
SELECT title, stage, stage_entered FROM deals
WHERE result IS NULL AND julianday('now') - julianday(stage_entered) > 21;

-- Gone quiet: contacts with no interaction in stale_days, no open deal
SELECT c.name, c.email, MAX(i.date) AS last_touch FROM contacts c
LEFT JOIN interactions i ON i.contact_id = c.id
WHERE c.suppressed = 0
  AND c.id NOT IN (SELECT contact_id FROM deals WHERE result IS NULL)
GROUP BY c.id
HAVING last_touch IS NULL OR julianday('now') - julianday(last_touch) > 90
ORDER BY last_touch;

-- Win rate and median-ish cycle by source, from closed deals only
SELECT source,
       COUNT(*) AS closed,
       SUM(result = 'won') AS won,
       ROUND(100.0 * SUM(result = 'won') / COUNT(*)) AS win_pct
FROM deals WHERE result IS NOT NULL GROUP BY source ORDER BY won DESC;
```

Thresholds come from `config.yaml` (`stale_days`, `stall_days`) — a query with the number baked in stops matching the skill's rules the day the user changes one.

## Migrating Files To SQLite

1. Back up the files, dated, to `db/backups/`.
2. Create the schema above.
3. Load orgs, then contacts, then deals, then interactions — the dependency order (`import.md`). Keep any old id in a `legacy_id` column.
4. Reconcile counts per table *and* the sum of open deal value.
5. Keep the files read-only for one cycle, then archive them into `db/backups/`.
6. Update `crm_tool` in `config.yaml` and `## System` in `memory.md` in the same turn — the record of truth moved, and anything that still writes to the old files is now creating a second truth (SKILL.md Rule 1).

## Backups

- A backup is a **file copy with a date in the name**, into `db/backups/`, taken before every bulk operation and on the quarterly `## Due` row.
- For SQLite, copy while nothing is writing, or use SQLite's own backup/`.dump` path — copying a database mid-write can capture a torn file, and the corruption is silent until the day you need it.
- **Verify on the day you make it**: open the copy, count the rows. An unverified backup is a belief.
- Keep a plain-text export (CSV or JSON) alongside the binary one. A `.db` file is only readable by the tool that made it; a CSV is readable in ten years.
- Prune old backups on the retention schedule in `privacy.md` — an erasure request that leaves the person in twelve backups has not been honored.

## Sync Across Devices

| Method | Works for | Breaks when |
|---|---|---|
| Cloud folder (Dropbox, iCloud, Drive) | Files, one device at a time | Two devices edit the same file — cloud folders resolve by making conflict copies, and a SQLite file can be corrupted outright by mid-write sync |
| Git repository | Text files, technical users, real history | Binary `.db` files, which do not diff and bloat the repo |
| Neither: one device is the writer | Everyone else | Nothing — this is the honest answer for a single-person CRM |

If two devices genuinely need to write, that is the trigger to leave the self-built path (`tools.md`), not a problem to solve with sync.

## Helper Scripts Worth Having

Only three are worth writing, and only after the manual version has been done twenty times:

- **Quick add**: one line in, a validated record out, with the duplicate check on the identity key. Removing friction from entry is worth more than any report (`adoption.md`).
- **Today's list**: the overdue query above, printed. This is the script that gets run daily.
- **Backup and export**: dated copy plus CSV, one command, so the quarterly `## Due` row is never skipped for being tedious.

Anything else — dashboards, a web UI, a mobile app, authentication for a single-user database — is a project competing with the work the CRM exists to support. A web UI for a personal CRM is the most common way this system dies before it is useful.

## When To Stop

Leave the self-built path when a second person needs to write, when a query you need weekly requires a script you have to maintain, or when you have lost data once. Volume is not a reason: SQLite handles more rows than you will ever type (`tools.md`).

**After any schema change, migration, or bulk operation**, write to `## System` in `~/Clawic/data/crm/memory.md` (schema in force, where the file lives, backup cadence), stamp `## Due` for the backup, and record counts in `## Data Health` (`memory-template.md`). Add a `## Boxes` line the first time `db/` exists.
