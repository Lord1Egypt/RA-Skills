# 🗄️ File to Database

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.1.0-green)
![Platform](https://img.shields.io/badge/platform-OpenClaw%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Codex%20%7C%20Gemini%20CLI-purple)
![ClawHub](https://img.shields.io/badge/ClawHub-draft-yellow)

**English** | **[中文](README.zh-CN.md)**

Turn raw data files (CSV / Excel / JSON / JSONL / TSV) into a validated database — then keep operating it in natural language: queries, inserts, updates, and deletes with safety gates, audit logs, and a visual delivery package after every change.

**7 reference docs** encode the full engineering loop. **6 file formats** supported. **0 dependencies** (stdlib Python only; openpyxl optional for xlsx).

**The problem:** "Send the files to Cursor and it builds a database" works once, but every new project means re-explaining your design rules, the agent guesses foreign keys and indexes differently each time, and after the DDL you're on your own. File to Database fixes all three: your design methodology lives in `references/methodology.md` (swap it to change the design style), every generated schema follows it verbatim, and the runtime mode keeps the agent as the database's natural-language operator afterwards.


## Table of Contents

<details>
<summary>Click to expand</summary>

- [How It Works](#how-it-works)
- [The Staged Loop](#the-staged-loop)
- [Runtime Mode (After the Database Exists)](#runtime-mode-after-the-database-exists)
- [Engineering Hardening](#engineering-hardening)
- [Non-Data Files (Intent Triage)](#non-data-files-intent-triage)
- [Pluggable Methodology](#pluggable-methodology)
- [Install](#install)
- [Quick Start](#quick-start)
- [Tested End-to-End](#tested-end-to-end)
- [Files](#files)
- [Compatibility](#compatibility)
- [License](#license)

</details>

## How It Works

```
data files ──▶ infer_schema.py ──▶ column profiles
                                        │
             detect_relations.py ◀──────┘
                    │
                    ▼
          methodology.md (your rules)
                    │
                    ▼
      schema.sql + ERD + seed + migrations
                    │
                    ▼
      constraint tests + EXPLAIN verification
```

1. **Profile** — `infer_schema.py` scans each file: types (int/float/bool/date/uuid/text via 90% voting), null rates, cardinality, uniqueness, max length, samples.
2. **Relate** — `detect_relations.py` finds PK candidates (fully unique columns) and FK candidates (name match + value containment), each with a confidence score and verdict: `adopt` / `ask_user` / `ignore`.
3. **Model** — the agent applies your methodology: 3NF by default, denormalization only for named queries, constraints in DDL not app code.
4. **Deliver** — `schema.sql`, Mermaid ERD, `seed.py`, reversible migrations.
5. **Verify** — constraint negative tests (insert forbidden rows, assert rejection) + `EXPLAIN` the key queries to confirm index hits.

## Runtime Mode (After the Database Exists)

The skill doesn't stop at DDL. Once the database is built, the agent becomes its **natural-language operator**: intent detection → SQL generation → safe execution → human-language reporting.

```
"Add an order for Alice, amount 59"
    → parameterized INSERT → execute
    → "Added 1 order (Alice, $59)."

"Delete all expired subscriptions"
    → SELECT first to preview affected rows (12)
    → over the 5-row threshold, wait for user confirmation
    → "Deleted 12 expired subscriptions; backup at /tmp/backup_xxx.csv"
```

Full rules in `references/operations.md`: trigger conditions (entity + operation words, data questions, mutation verbs, anaphora), SQL generation rules, safety gates (UPDATE/DELETE require row-count preview; confirmation above 5 rows or without WHERE), error translation (unique violation → "this record already exists"), and reporting templates (conclusion first, then data, then next-step hints).

## The Staged Loop

Every stage leaves a checkable artifact, so correctness rests on tests and query plans — not on reading generated SQL:

| Stage | Artifact | Done when |
|---|---|---|
| 1. Scan | `profiles.json` | every file profiled, ambiguous columns flagged |
| 2. Relate | FK list with evidence | low-confidence candidates asked, never silently chosen |
| 3. Model | decision record | open questions listed for the user |
| 4. Deliver | DDL + ERD + seed | every index annotated with the query it serves |
| 5. Verify | test output | all constraint tests pass, EXPLAIN hits planned indexes |

## Pluggable Methodology

`references/methodology.md` is the soul of the skill. The bundled one encodes the Cursor-community staged loop: constraints in the database, query-driven indexes, expand-and-contract migrations, and a fixed two-checkpoint ask-user pattern (after profiling and before modeling — evidence-based multiple-choice questions, never open-ended). To enforce your house style — say, "always use surrogate keys and soft deletes" — edit that one file. The skill reads it at startup and follows it verbatim; no code changes needed.

## Engineering Hardening

`references/engineering.md` adds what real data engineers do, sized for personal use:

- **Migration ledger** — `.applied.json` with checksums; reordered or edited history migrations halt with an error; rollback is actually rehearsed before delivery
- **Data quality gates** — post-seed assertions (row counts, PK nulls, dangling FKs, value drift); failures stop the pipeline with offending samples
- **Incremental import** — file updated? Never rebuild: profile diff → schema changes go through new migrations, new rows go through UPSERT (PK conflicts skipped to `skipped.csv` by default)
- **Security** — credentials only via environment variables (never in code/reports/chat), SQLite 0600 / PG least-privilege roles / Supabase RLS, PII columns flagged and masked in snapshots, every write logged to `audit.log` shipped with each delivery
- **Honest boundary** — production deploys, monitoring, load tests, capacity planning: the skill generates configs and scripts, but does not pretend to run them

## Non-Data Files (Intent Triage)

Hand it a PDF textbook, a PPTX, an image? The skill neither force-builds a database nor refuses: `references/intake.md` routes by user intent — extract to structured JSONL (with page-number traceability and a 10-sample human check) → standard pipeline, or just read/summarize without a database, or "did you mean to send something else?" File type decides capability; user intent decides workflow.

## Tested End-to-End

Full pipeline battle-tested with synthetic data across three formats (CSV / JSONL) including planted dirty rows (dangling FKs):

- type inference: all columns correct; FK detector caught the planted dangling references and downgraded confidence → asked the user
- quality gate: dirty rows blocked by FK enforcement, quarantined to `skipped.csv`
- constraint negative tests: duplicate PK / invalid quantity / deleting a referenced product — all correctly rejected
- runtime mode: NL query, UPDATE preview → row-count threshold → execute → audit log, error translation to plain language
- two real bugs found and fixed during testing (SQLite FK pragma per connection; seed transaction boundaries) — now encoded in `references/engineering.md` §4.5

## Install

```bash
# ClawHub
clawhub install file-to-database-skill

# Or from source
git clone https://github.com/Thomaszhou22/file-to-database-skill.git
cp -r file-to-database-skill ~/.openclaw/skills/
```

Requires Python 3.8+ (stdlib only). `openpyxl` optional for `.xlsx`.

## Quick Start

```bash
# 1. Profile your files
python3 scripts/infer_schema.py --input ./data/ --out profiles.json

# 2. Detect relationships
python3 scripts/detect_relations.py --profiles profiles.json --out relations.json

# 3. Ask your agent: "build a database from ./data following the skill methodology"
```

Then the agent (OpenClaw / Claude Code / Cursor) takes over: modeling, DDL, ERD, seed, validation.

## Files

```
file-to-database-skill/
├── SKILL.md                        # entry point: staged loop + runtime mode + hardening
├── references/
│   ├── methodology.md              # ⭐ pluggable design methodology + ask-checkpoint pattern
│   ├── operations.md               # ⭐ runtime mode: NL intent → SQL → safe exec → NL report + visual delivery
│   ├── engineering.md              # migration ledger, quality gates, incremental import, security
│   ├── intake.md                   # non-data files (PDF/PPTX/…): intent triage before anything
│   ├── output-format.md            # deliverable layout & report template
│   └── other-engines.md            # MySQL / SQLite / MongoDB / Supabase notes
└── scripts/
    ├── infer_schema.py             # column-level profiler (CSV/TSV/JSON/JSONL/xlsx)
    └── detect_relations.py         # PK/FK candidate detection with confidence verdicts
```

## Compatibility

| Environment | Status |
|---|---|
| OpenClaw | ✅ primary target |
| Claude Code | ✅ drop into `~/.claude/skills/` |
| Cursor | ✅ use as a Project Rule + run scripts in terminal |
| Codex CLI | ✅ drop into `~/.codex/skills/` or reference via AGENTS.md |
| Gemini CLI | ✅ reference SKILL.md in GEMINI.md; scripts run standalone |
| Any LLM agent | ✅ scripts are standalone (any agent that can read files and run Python) |

## License

MIT
