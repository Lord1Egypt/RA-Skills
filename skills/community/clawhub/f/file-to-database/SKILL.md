---
name: file-to-database-skill
version: 1.1.1
description: "Use when the user wants to build a database from data files (CSV/Excel/JSON/JSONL/TSV), design a schema from raw data, or turn flat files into tables — AND when the user later talks to that database in natural language (add, query, update, delete records; 'how many...'; 'show me...'). Scans files, infers column types, detects candidate foreign keys, applies the methodology in references/methodology.md to produce DDL, ERD, seed scripts, and validation; runtime operations follow references/operations.md (intent → SQL → safe execution → natural-language report). Do NOT use for ORM code generation or pure database concept discussions."
---

# Database Generator Skill

Turn data files (CSV / Excel / JSON / JSONL / TSV) into a validated database:
**scan → infer → model → DDL → verify**, following the pluggable methodology in `references/methodology.md` throughout.


## Onboarding (First Use)

When the user first triggers this skill and `memory/file_to_database_state.json` doesn't exist, run a one-time setup:

1. **Introduce capability** (one sentence): _"I can turn CSV/Excel/JSON data files into a validated database, then let you operate it in natural language."_

2. **Quick configuration:**

1. **Default database engine**(Default: SQLite)
   - SQLite(zero-install, single-file, personal projectsrecommended)
   - PostgreSQL(Multi-user / cloud deployment)
2. **Enable runtime natural-language operations**(Default: Yes)
   - Yes (CRUD in natural language after database is built)
   - No (build database only, skip runtime mode)

3. **Write initial state file** `memory/file_to_database_state.json`(JSON format, with `onboarded: true` and timestamp)

4. **Confirm completion**: _"Setup done! Just use it from now on. Say 'reset settings' anytime to reconfigure."

**Onboarding runs exactly once.** Subsequent activations read the state file directly. When the user says "reset settings", delete the state file and re-run setup.

---

## Startup Flow

1. Read `references/methodology.md` (the methodology is the soul of this skill; read it first, always)
2. Detect the runtime environment:
   - `python3 --version` ≥ 3.8 → script engine available
   - Unavailable → fall back to pure LLM mode (the agent analyzes file samples itself; slightly lower precision, inform the user)
3. Ask the user for file paths (or a directory) and confirm the target engine (default: SQLite; PostgreSQL/Supabase when multi-user concurrency or cloud is needed; MySQL and MongoDB supported)

## Intake Triage (required reading for non-data files)

When the user provides files that are **not** CSV/Excel/JSON/JSONL/TSV (e.g. PDF textbooks, PPTX, DOCX, images), never enter the build pipeline directly and never refuse service — follow the triage in `references/intake.md`:

- Intent already clear (e.g. "build a database from this book's exercises") → take the structuring path: LLM extracts to a JSONL intermediate format (with page numbers for traceability) → show a 10-item sample for user confirmation → return to the standard pipeline
- Intent unclear → ask once with options: ① extract content and build a database ② read/summarize only ③ did you mean to send a different file; **never guess the task for the user**
- File type determines capability boundaries; user intent determines the workflow

## Main Flow (staged loop; each stage leaves a checkable artifact)

### Step 1: Scan & Profile (scripts/infer_schema.py)
Generate a statistical profile for every data file:
```bash
python3 scripts/infer_schema.py --input <file-or-dir> [--sample N] --json
```
Output: per-column type inference (int/float/bool/date/uuid/text), null rate, cardinality, uniqueness, max length, sample values.
**Done when**: one profile per file; the agent reviews ambiguous columns (mixed types, overlong text).

### Step 2: Relation Discovery (scripts/detect_relations.py)
```bash
python3 scripts/detect_relations.py --profiles <profiles.json> --json
```
Output: primary-key candidates, foreign-key candidates (name matching + value-set containment, with confidence scores).
**Done when**: every FK candidate carries confidence and evidence; low-confidence ones are listed for the user — never silently guessed.

### Step 3: Data Modeling (execute per methodology.md)
- Entity identification: one file → one table (whether to normalize wide tables follows the split rules in the methodology)
- Cardinality annotation: 1:1 / 1:N / N:M (N:M requires an explicit junction table)
- 3NF by default; denormalize only for queries named in the methodology, and always annotate which query is served
- Open-questions list: the methodology requires listing every question the spec leaves unanswered for the user — no silent invention

### Step 4: Produce Deliverables
Output per the layout in `references/output-format.md`:
1. `schema.sql` (DDL: tables, constraints, indexes — each index annotated with the query it serves)
2. `ERD` (Mermaid erDiagram)
3. `seed.py` or `seed.sql` (script importing data from source files, including type conversions)
4. `migrations/` (reversible migrations, expand-and-contract mode)

### Step 5: Verification (run against a database when available; manual walkthrough otherwise)
```bash
# With a local Postgres / Docker / Supabase branch:
psql -f schema.sql && python3 seed.py
# One negative test per constraint: insert a forbidden row, assert rejection
# EXPLAIN the key queries to confirm the planned indexes are actually used
```
Without a database: walk through the Step 7 checklist from the methodology item by item and output the walkthrough report.

## Runtime Mode (after the database is built)

Once the database exists, the skill enters **runtime mode**: the user issues creates, reads, updates, and deletes in natural language; the agent handles **intent recognition → SQL generation → safe execution → natural-language reporting**. Full rules in `references/operations.md` (trigger rules, SQL generation rules, safety gates, reporting templates). Key points:

- Trigger on "entity + operation word / data question / mutation verb / anaphora"; pure concept discussions do not trigger
- UPDATE/DELETE: run the same-condition SELECT first to report affected rows; more than 5 rows or no WHERE requires user confirmation
- Translate errors into plain language (unique violation → "this record already exists"; FK violation → "the referenced record does not exist")
- Query results: conclusion first, then the table; change reports state affected rows and reversibility
- **Automatically deliver a visualization package after every change**: the database file itself (SQLite single file by default) + Mermaid ERD (with a mermaid.live online link) + snapshot.html data snapshot — rules in the "Post-Change Visualization Delivery" section of `references/operations.md`

## Engineering Hardening Layer (references/engineering.md)

On top of the base build-and-run flows, read and enforce these four items from `references/engineering.md`:

1. **Migration ledger**: `.applied.json` prevents duplicate or out-of-order execution; a historical migration whose checksum changed must halt with an error; rehearse one rollback for real before delivery
2. **Data quality gates**: automatic post-seed assertions (row counts, PK nulls, dangling FKs, value drift); stop on failure and show samples
3. **Incremental import**: when a file is updated, never rebuild — profile diff → structural changes go through a new migration / pure new rows go through UPSERT (PK conflicts skipped and recorded by default)
4. **Permissions & security**: credentials only via environment variables, never in any file; SQLite 0600 / PG least-privilege roles / Supabase RLS; PII columns flagged + snapshots masked; every write operation logged to audit.log and shipped with each delivery

**Honest boundary** (generate but do not execute): production deploys, monitoring, load testing, capacity planning, credential custody.

## Failure & Fallback

| Situation | Handling |
|---|---|
| File too large for a full scan | `--sample N` sampling + inform the user that confidence dropped |
| Python unavailable | Pure LLM mode: read the first 100 lines of each file and profile by hand |
| FK relationship undeterminable | List candidates and ask the user; never choose silently |
| DDL execution failure | Print the full error + locate the column; fix and re-run verification |

## Environment Awareness

- Infer the target engine from `docker-compose.yml` / ORM config / a Supabase project; ask when inference fails
- When the user already has a migration tool (Prisma/Drizzle/Alembic) → match its migration file format; do not start a parallel convention
