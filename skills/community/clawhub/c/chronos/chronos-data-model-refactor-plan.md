# Chronos data-model refactor plan

## Bottom line

Chronos should stop treating `entries` as a second-class scheduling system. The target model should be:

- `tasks` (rename/evolve from current `periodic_tasks`) = canonical task definition table for **all** Chronos-managed work
- `task_occurrences` (rename/evolve from current `periodic_occurrences`) = per-date execution/reminder state
- `entries` = legacy inbox/one-shot scratchpad only during migration, then read-only compatibility, then retired from Chronos paths

That is the right cut for this codebase because the current pain is not abstract purity — it is that `todo.py` already contains dual-path logic for list/add/complete/skip/show/complete-overdue, while `periodic_task_manager.py` only understands one side of the world.

## What the current codebase is actually doing

### 1. There are already two scheduling systems

Current runtime DB (`/home/ubuntu/.openclaw/workspace/todo.db`) has:

- `entries(id, text, status, group_id, created_at, updated_at)`
- `groups(id, name, ...)`
- `periodic_tasks(...)`
- `periodic_occurrences(task_id, date, status, reminder_job_id, is_auto_completed, completed_at)`

And the code splits responsibility like this:

- `skills/chronos/scripts/periodic_task_manager.py`
  - creates/manages `periodic_tasks`
  - creates occurrences
  - schedules/removes cron reminders
  - maintains `monthly_n_times` quota state
- `skills/chronos/scripts/todo.py`
  - merges `entries` + periodic tables for listing
  - routes `add once` into `entries`
  - routes non-`once` into `periodic_task_manager`
  - handles `complete`, `skip`, `show` through two separate storage paths
  - recently added `complete-overdue`, which has to manually scan both `periodic_occurrences` and recurring-looking `entries`

That last bullet is the smell: the system now needs heuristics (`RECURRING_ENTRY_PATTERNS`, `TIME_PATTERN`, `META_REVIEW_PATTERN`) to guess whether a legacy `entries.text` row is really a scheduled task.

### 2. `entries` is no longer just “simple todo”

Tests and live data show `entries` has been carrying scheduled/system semantics:

- Meta-Review fallback task
- `每 4 小时：同步 subagent 记忆 (memory_manager.py sync)`
- older time-encoded recurring reminders embedded in free text

So Chronos is already paying the migration tax, just in runtime logic instead of schema.

### 3. There is schema drift inside the “new” side too

Two concrete signs:

- Live DB contains `periodic_tasks.cycle_type = 'monthly_dates'`, but code only advertises/supports:
  - `once`, `daily`, `weekly`, `monthly_fixed`, `monthly_range`, `monthly_n_times`
- `periodic_tasks` has `dates_list`, but scheduler/model code does not actually implement that path

So the refactor is not just `entries` cleanup. It also needs to normalize the target schema before more data gets piled onto it.

### 4. `once` is in the wrong place conceptually

`todo.py add` currently sends:

- `cycle_type != 'once'` -> `periodic_tasks`
- `cycle_type == 'once'` -> `entries`

That split is exactly why the system can never fully unify behavior. A one-shot scheduled task is still a scheduled task. If it has a date/time, completion semantics, reminder semantics, and overdue semantics, it belongs in the canonical task model.

## Target model

Use a two-layer model:

1. **Task definition**: what should happen, on what cadence, with what reminder/delivery policy
2. **Occurrence/execution record**: what happened for a concrete scheduled date/time

Keep `groups` or replace it with category fields, but stop using `entries` as a scheduler.

### Proposed canonical tables

## `tasks` (phase 1 can keep the physical name `periodic_tasks`)

Recommended columns:

- `id`
- `title` (`name` compat alias during migration)
- `category`
- `kind` — enum-like text:
  - `scheduled`
  - `routine`
  - `system`
  - `ad_hoc`
- `schedule_type` — normalized successor of `cycle_type`:
  - `once`
  - `daily`
  - `weekly`
  - `monthly_fixed`
  - `monthly_range`
  - `monthly_n_times`
  - `monthly_dates` (only if we intentionally keep and implement it)
- schedule parameter columns:
  - `weekday`
  - `day_of_month`
  - `range_start`
  - `range_end`
  - `n_per_month`
  - `dates_list` (JSON text or comma list; only if `monthly_dates` is kept)
- `start_date` nullable
- `end_date` nullable
- `time_of_day`
- `timezone`
- `is_active`
- `quota_state_json` nullable — optional future-proof place for more complex counters; keep `count_current_month` initially for compatibility
- `count_current_month`
- `source` — `chronos`, `legacy_entries_migrated`, `system_seeded`, etc.
- `legacy_entry_id` nullable unique — back-reference during migration
- `special_handler` nullable:
  - `meta_review_fallback`
  - `subagent_memory_sync`
  - etc.
- `handler_payload` nullable JSON
- `reminder_template`
- `delivery_target` nullable
- `delivery_mode` nullable
- reminder health fields already present:
  - `last_reminder_error`
  - `reminder_error_count`
  - `last_reminder_error_at`
- `created_at`
- `updated_at`

### `task_occurrences` (phase 1 can keep the physical name `periodic_occurrences`)

Recommended columns:

- `id`
- `task_id`
- `scheduled_date`
- `scheduled_time` nullable (copy from task at generation time if needed for audit)
- `scheduled_at` nullable ISO timestamp for future richer scheduling
- `status`:
  - `pending`
  - `reminded`
  - `completed`
  - `skipped`
  - optional later: `failed`, `canceled`
- `completion_mode` nullable:
  - `manual`
  - `auto_quota`
  - `fallback_handler`
  - `migration`
- `special_handler_result` nullable JSON/text
- `reminder_job_id`
- `delivered_at` nullable
- `completed_at`
- `is_auto_completed`
- `legacy_entry_id` nullable (for migrated rows if needed)
- unique `(task_id, scheduled_date)` for date-based schedules

## What to do with `entries`

Do **not** immediately delete it.

Use a three-step phase-out:

1. **Phase A: compatibility source**
   - Chronos still reads legacy rows from `entries`
   - new scheduled tasks no longer write there
2. **Phase B: read-only legacy mirror**
   - migrated rows are marked/linked
   - `todo.py` stops treating plain `entries` rows as schedulable unless explicitly legacy-compatible
3. **Phase C: Chronos stops querying `entries`**
   - only non-Chronos consumers may still use it
   - eventually archive or leave as separate generic todo feature

## Concrete schema proposal for the current codebase

Minimal practical path: evolve existing tables instead of hard renaming first.

### Phase 1 schema patch

Keep physical table names for now, but change semantics.

#### `periodic_tasks`

Add:

- `task_kind TEXT NOT NULL DEFAULT 'scheduled'`
- `source TEXT NOT NULL DEFAULT 'chronos'`
- `legacy_entry_id INTEGER UNIQUE`
- `special_handler TEXT`
- `handler_payload TEXT`
- `start_date TEXT`
- `delivery_target TEXT`
- `delivery_mode TEXT`

Constrain/fix:

- formalize allowed `cycle_type` set in one shared place
- either:
  - **implement** `monthly_dates` in `core/scheduler.py`, `core/models.py`, parser/docs/tests
  - or migrate all `monthly_dates` rows to a supported type and forbid it

Recommendation: implement `monthly_dates` only if there is real live use. Since live DB already has one row and `dates_list` exists, the least surprising option is to support it properly instead of pretending it does not exist.

#### `periodic_occurrences`

Add:

- `completion_mode TEXT`
- `special_handler_result TEXT`
- `scheduled_time TEXT`
- `scheduled_at TEXT`
- `legacy_entry_id INTEGER`

Keep existing unique `(task_id, date)` and FK.

#### `entries`

Do not mutate heavily. At most add:

- `migrated_task_id INTEGER`
- `chronos_legacy INTEGER DEFAULT 0`

But even that is optional if we store `legacy_entry_id` on `periodic_tasks` and maintain a migration ledger.

## Migration strategy

### Step 0: freeze the write path

Before touching data, make one behavioral change:

- `todo.py add` must stop writing scheduled/dated one-shot tasks into `entries`
- if the user uses Chronos, create a row in `periodic_tasks` even for `once`

For phase 1, `once` can mean:

- one task definition row with `cycle_type='once'`
- one generated occurrence row for the target date

If the CLI currently lacks explicit date for `once`, add one. Without a date, it is just a generic inbox item and should not pretend to be schedulable.

### Step 1: inventory legacy `entries`

Classify existing `entries` into buckets:

1. **pure inbox/manual todo**
   - no schedule semantics
   - leave in `entries`
2. **legacy recurring/system task**
   - detected by current heuristics or explicit curated rules
   - migrate into `periodic_tasks`
3. **ambiguous**
   - has a time like `21:00` but no recurring semantics
   - do not auto-migrate unless user/system explicitly marks it

This matters because current `complete-overdue` deliberately ignores future one-shots like `给朋友发消息 21:00`. The migration must preserve that safety bias.

### Step 2: create migrated task definitions

For each legacy recurring/system entry:

- create `periodic_tasks` row with:
  - `source='legacy_entries_migrated'`
  - `legacy_entry_id=<entries.id>`
  - `special_handler` when applicable
- map group -> `category`
- derive schedule fields from text only when deterministic
- if schedule cannot be safely parsed, do not auto-migrate

### Step 3: seed occurrences

For migrated recurring/system tasks:

- create occurrence for today/current due window if needed
- optionally backfill recent occurrences only if needed for quota continuity

Do **not** blindly backfill entire history. Current code only really needs current-month state and today’s execution state.

### Step 4: mark legacy rows as migrated

Options, best to worst:

1. set `entries.status='done'` with an audit note in text or side ledger — ugly
2. add `migrated_task_id` or maintain external migration ledger — better
3. stop listing migrated entries in Chronos queries using a join on `legacy_entry_id` — best with minimal user-facing noise

Recommendation: do **not** overload `status` to mean migration. Use linkage, not fake completion.

### Step 5: remove dual-path operational logic

Once migrated enough:

- delete `get_simple_pending()` from Chronos list path or limit it to true inbox mode
- delete `get_overdue_legacy_entries()` heuristics from `todo.py`
- move overdue logic to occurrence-based queries only
- move special handler execution to task/occurrence metadata instead of text regex

## Special system tasks: Meta-Review fallback semantics

This is the sharpest edge, so encode it in the model instead of hiding it in text matching.

Current behavior in `todo.py`:

- recognize Meta-Review by regex on `entries.text`
- when overdue, run `run_meta_review_fallback()`
- log a note to `memory/YYYY-MM-DD.md`
- only then mark the legacy entry done

That behavior is correct. The storage location is the problem.

### Proposed representation

Create a normal task row:

- `task_kind='system'`
- `cycle_type='daily'`
- `time_of_day='02:00'`
- `special_handler='meta_review_fallback'`
- `handler_payload` can include:
  - review scope (`days=1`)
  - primary executor (`meta_auditor.py analyze`)
  - fallback source files (`PREDICTIONS.md`, `FRICTION.md`)
  - required side effect (`append memory log`)

When its occurrence is completed:

1. try primary path if still desired
2. if primary path fails/hangs/disabled, execute fallback handler
3. write handler result into occurrence (`completion_mode='fallback_handler'`, `special_handler_result=...`)
4. then mark occurrence completed

### Why this is better

- no regex dependency on task title text
- fallback becomes an explicit contract, not a coincidence
- audit trail lives with the occurrence, not only in memory log side effects
- future system tasks can reuse the same mechanism

### Other system tasks

The live legacy row `每 4 小时：同步 subagent 记忆 (memory_manager.py sync)` should be treated similarly:

- either migrate it into a proper system task with explicit cadence/handler
- or keep it out of Chronos if another orchestrator owns it

The wrong answer is the current in-between state where it is stored as plain text but receives scheduler-like treatment.

## Command and API compatibility story

Do not break the human-facing CLI. Break the storage split underneath it.

### Keep these identifiers stable

- `FIN-<occurrence_id>` for occurrence-level actions
- `ID<entry_id>` only for true legacy `entries` rows during migration

### CLI behavior after refactor

#### `todo.py add`

Current:

- recurring -> `periodic_tasks`
- once -> `entries`

Target:

- any scheduled Chronos task -> canonical task table
- true unscheduled inbox note -> `entries` or a future inbox table

Concretely:

- `todo.py add "买牛奶"` with no date/time/cycle can still go to `entries`
- `todo.py add "周五抢券" --cycle-type weekly --weekday 4 --time 10:00` goes to canonical task table
- `todo.py add "周五 10:00 提醒我" --cycle-type once --date 2026-03-27 --time 10:00` also goes to canonical task table

#### `todo.py list`

During migration:

- list canonical occurrences first
- list unmigrated legacy `entries` second
- optionally label legacy rows as `[legacy]`

After migration:

- default list should be occurrence-driven
- legacy inbox items can remain in a separate section if desired

#### `todo.py complete`

No command change.

Implementation change:

- `FIN-*` stays occurrence-based
- `ID*` only for actual legacy rows
- eventually allow task-level completion by semantic command, but not required now

#### `todo.py complete-overdue`

Current:

- merges periodic occurrences + regex-detected legacy recurring entries

Target:

- query overdue occurrences only
- if occurrence has `special_handler`, run that handler before final completion

This removes the current brittle text heuristics.

#### `todo.py skip` / `show`

Same CLI, unified backing model for Chronos-managed tasks.

### Internal API cleanup

Introduce one service module and stop duplicating sqlite logic inside `todo.py`:

- `core/task_repo.py` or `core/task_service.py`

It should own:

- create task
- create occurrence
- list pending/today/overdue
- complete occurrence
- skip occurrence
- migrate legacy entry
- resolve identifier

Right now completion/quota logic exists in both `todo.py` and `periodic_task_manager.py`. That duplication will bite again.

## Safe phase-out plan for `entries`

### Phase A — now

- Add compatibility doc and schema plan
- Stop new scheduled writes to `entries`
- Add task metadata for special handlers
- Normalize `cycle_type` support, especially `monthly_dates`

### Phase B — migration release

- Add migration script: `skills/chronos/scripts/migrate_legacy_entries.py`
- Script outputs:
  - migrated rows
  - ambiguous rows requiring manual review
  - skipped pure inbox rows
- Add dry-run first, apply second
- Add tests covering Meta-Review + memory sync migration cases

### Phase C — cutover

- `complete-overdue` no longer scans `entries`
- `list/show/skip/complete` only touch `entries` when identifier is truly legacy
- docs stop describing `entries` as a normal Chronos storage path

### Phase D — retirement

- remove `RECURRING_ENTRY_PATTERNS`, `META_REVIEW_PATTERN`, and legacy text-time inference from `todo.py`
- optionally archive old migrated `entries` rows to `entries_archive` or external dump

## Implementation order I would actually use

1. **Fix schema drift first**
   - decide on `monthly_dates`
   - centralize allowed cycle types
2. **Unify service layer**
   - move DB writes/reads from `todo.py` into core service/repo helpers
3. **Change `once` behavior**
   - scheduled `once` -> canonical task + occurrence
4. **Add explicit special-handler metadata**
   - especially `meta_review_fallback`
5. **Ship dry-run migration for legacy recurring entries**
6. **Cut `complete-overdue` over to occurrences-only**
7. **Retire legacy heuristics**

That order minimizes user-visible breakage while removing the worst source of complexity first.

## Non-goals

- Do not rename tables on day one. Semantic unification matters more than pretty names.
- Do not try to auto-parse every historical `entries.text` line. Ambiguous rows should stay legacy until reviewed.
- Do not delete `entries` before CLI compatibility is stable.

## Recommended acceptance criteria

The refactor is successful when all of these are true:

- new scheduled one-shot tasks no longer land in `entries`
- `complete-overdue` uses occurrence data only
- Meta-Review fallback is driven by explicit task metadata, not regex on free text
- quota accounting (`monthly_n_times`) still works after migration
- `todo.py` no longer duplicates core completion logic already present in `periodic_task_manager.py`
- live DB has no unsupported `cycle_type` values
- legacy `entries` remaining in DB are genuinely unscheduled inbox items or explicitly quarantined legacy rows

## Recommended first patch set

If I were patching this repo next, I would do exactly this:

1. add support or migration for `monthly_dates`
2. add `task_kind`, `source`, `legacy_entry_id`, `special_handler`, `handler_payload` to `periodic_tasks`
3. add `completion_mode`, `special_handler_result` to `periodic_occurrences`
4. move complete/skip/identifier resolution into shared core helpers
5. change `todo.py add --cycle-type once` to use canonical task storage when a schedule is present
6. write a dry-run legacy migration script
7. convert Meta-Review from legacy `entries` row to explicit system task

That gets Chronos out of the current half-migrated limbo without a risky big-bang rewrite.
