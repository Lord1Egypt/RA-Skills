# Runtime Operations (NL ⇄ DB)

After the build phase (staged loop) completes, the skill enters **runtime mode**: the user issues database creates, reads, updates, and deletes in natural language; the agent handles intent recognition → SQL generation → execution → natural-language reporting.

## Trigger Rules (agent self-detection)

Enter runtime mode when any of the following signals appears in a user message:

| Signal type | Examples |
|---|---|
| Entity + operation word | "Add a row to the orders table…" "Delete that user" "Look up last week's sales" |
| Data question words | "How many…?" "Which…?" "What's the largest…?" |
| Mutation verb + data context | "Update / modify / mark / cancel / disable…" |
| Anaphora | "Look at that table again" "Delete it" (referring to an entity from earlier) |

**Do not trigger** (avoid false positives): casual chat, discussing "database concepts", requests to change the schema structure (that's build/migration mode — follow the methodology).

**Disambiguation priority**: the database already operated on in this conversation > a database in the project directory > ask the user "which database".

## Runtime Loop (per request)

```
User natural language
   │
   ▼
1. Intent classification → SELECT / INSERT / UPDATE / DELETE / DDL / aggregate / unclear
   │  unclear → ask once ("do you want to query or modify?"); never guess
   ▼
2. Load schema context (mandatory on first use: read schema.sql / \d output / PRAGMA table_info)
   │  cache for the session; reload when the schema changes
   ▼
3. Generate SQL (rules below)
   ▼
4. Pre-check + execute (safety rules below)
   ▼
5. Natural-language report (templates below)
```

## SQL Generation Rules

- **Read the schema before writing SQL**: column names, types, and constraints come from the schema; never guess column names from memory
- **Parameterization**: user values are never concatenated into SQL strings (prevents injection + type errors); in the agent context, declare "these values come from user input" before generating
- **UPDATE/DELETE must carry WHERE**: self-check after generation — a mutation without WHERE is refused execution and reported
- **Make fuzzy conditions explicit**: "recent orders" → first confirm the sort column (created_at) and time window, restate to the user, then execute
- **Aggregate mapping**: "how many" → COUNT, "average" → AVG, "top N" → ORDER BY + LIMIT, "by …" → GROUP BY
- **JOIN basis**: JOIN only on foreign keys that actually exist in the schema; never guess by name similarity

## Safety Rules (all must hold before execution)

| Operation | Gate |
|---|---|
| SELECT | Execute directly |
| INSERT | Execute directly; when a constraint is violated, translate the database error into plain language |
| UPDATE / DELETE | ① Run the same-condition SELECT first to show affected row count ② ≤ 5 rows: execute directly ③ > 5 rows or no WHERE: restate the conditions and wait for user confirmation |
| DROP / TRUNCATE / ALTER | Always confirm; ALTER follows the methodology's expand-and-contract migration flow |
| Bulk operations | Execute in batches; report progress |

**Error translation table** (database error → plain language):

- `duplicate key value violates unique constraint` → "This record already exists (value Y of column X is duplicated)"
- `violates foreign key constraint` → "The record it references does not exist / other data still depends on it"
- `violates not-null constraint` → "Column X is required; you didn't provide it"
- `check constraint` → "The value Y of X is outside the allowed range"

## Natural-Language Report Templates

**Query**: conclusion first, then data, then a lead for next steps.

> Found: 34 orders last month, totaling ¥4,520.
> | Date | Amount | Status | …
> (Full results saved to output/; say the word if you want a CSV export.)

**Mutation**: state exactly what changed, how many rows, and whether it's reversible.

> Added 1 subscription (Netflix, ¥65/month, billed on the 5th).
> Deleted 3 expired subscription records. This operation is irreversible — pre-deletion backup is at /tmp/backup_xxx.csv.

**Empty result**: never just say "nothing found"; proactively offer next steps.

> No orders found for "last week". Widen the range to all of October? Or did you mean 10/13–10/19 by "last week"?

**Ambiguous request**: restate your understanding + list the options.

> By "tidy up the users table" — I understand this could mean:
> ① inspect the current structure ② clean up invalid users ③ export a backup. Which one?

## Post-Change Visualization Delivery (run automatically after every modification)

After any write operation (INSERT/UPDATE/DELETE/DDL), in addition to the text report, automatically generate a delivery package for the user:

| Deliverable | Content | How it's generated |
|---|---|---|
| Database itself | `data.db` (SQLite default) or `dump.sql` (PostgreSQL) | SQLite is naturally a single file; PG uses pg_dump |
| Structure diagram | Mermaid ERD + mermaid.live online rendering link | Generate erDiagram from the schema, URL-encode into `https://mermaid.live/view#<encoded>` |
| Data snapshot | `snapshot.html`: top 20 rows per table + total row counts + key aggregates | Script exports a self-contained HTML (inline CSS, opens directly in a browser) |

**Engine choice guidance**: for personal/small-team scenarios default to SQLite at build time (zero install, single file, directly sendable); switch only when the user explicitly asks for Postgres/Supabase or needs multi-user concurrency — after switching, the deliverable becomes a pg_dump export + snapshot.

**Frequency control**: for a run of consecutive small modifications, merge into one final delivery (intermediate changes get text reports only) to avoid file spam. When the user says "send me a copy", generate the package unconditionally.

**Interactive snapshot (optional, not default)**: in addition to the static snapshot, an sql.js interactive HTML can be generated (data.db embedded, self-service queries in the browser) — but **read-only exploration only**, with write operations disabled. Rationale: a static HTML has no sync channel; anything the user edits there is only an in-browser memory copy — it never reaches data.db nor the agent — creating a "edited but nothing happened" illusion. The only channel for data changes remains: user tells the agent → agent modifies the database → re-deliver. The default package excludes the interactive version; generate it only when the user explicitly asks.

## Session Memory

- Cache the schema summary on first interaction (table list + column names + foreign keys); do not re-read afterwards
- Record the change history executed in this session so "undo what I just did" can be located
- Preferences the user corrected once (e.g. "always show times in Beijing time") go into the session context
