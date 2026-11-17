# awam-todo Optimization Roadmap (pending ideas)

> This file only **records** ideas that are not yet implemented — it never
> changes code. Each item states: current gap, goal, approach outline,
> priority, dependencies.
> Numbering continues from the sequence used when extracting lessons from the
> "学习目标管理台" (learning-goal dashboard) experience, so discussion context
> can be traced.
>
> Already implemented items are not listed here (schema versioning,
> blocker/counter contingency plans, overdue two exits, pin-with-reason,
> Monday week boundary, monthly archiving, overridable defaults, "today" view,
> both-end creation entries, three responsive tiers, semantic three-state
> colors, inline SVG, zero-external-library constraint — see SKILL.md).

---

## I. Data layer (determines what everything else can compute)

### 7 + 8. Progress-record layer + derived metrics (**top priority; many other items depend on it**)

- **Current gap**: `storage/YYYY-MM-DD.md` only stores each task's **current
  state** plus created/updated times — there is no record of "how much was
  done on which day". Therefore consecutive-day streaks, completion rate,
  projected finish date, minutes invested, and week-over-week comparisons are
  all impossible — `_projected_finish()` currently always returns `None` and
  the UI shows 「暂无推算」. This is a deliberate no-invention, not a defect.
- **Goal**: let a todo have **multiple progress records**, from which real
  progress and velocity can be computed.
- **Approach**
  1. Append record lines inside the task block, e.g.:
     ```
     进展: 2026-10-06 30分钟 60个 补记:false
     进展: 2026-10-04 25分钟 40个 补记:true
     ```
     Suggested format `进展: <date> [<minutes>分钟] [<amount><unit>] [补记:true]`;
     minutes and amount are both optional.
  2. New commands: `log <id> [--amount N] [--minutes N] [--date YYYY-MM-DD] [--makeup]`,
     and `unlog <id> <record-index>` to delete a single record
     (corresponding to "the last N records can be deleted").
  3. Make-up window limited to the last 6 days; make-up records carry a 「补」
     mark but still count toward streaks and velocity **by their true date**.
  4. Derived metrics are always computed live from records, never stored:
     completion rate, consecutive-day streak, last-7-day average pace,
     projected finish date.
  5. **Insufficient samples still show 「暂无推算」**
     (`PROJECTION_MIN_SAMPLES = 3`) — no invented numbers.
  6. Multiple records per day are allowed; records without minutes are not
     force-fitted into charts (see chart definitions in 18/19 below).
- **Priority**: P0 (blocks 18 and 19; also the prerequisite for actually
  honoring the "no-invention" principle #1)
- **Dependencies**: requires syncing `_parse_block` / `_write_block` /
  `_task_view` / `build_index`, plus `SCHEMA_VERSION = 3` + `migrate` rules
  (v2 → v3 only adds fields, backward compatible).

### 10. Export / import JSON (with overwrite confirmation)

- **Current gap**: data only lives in `storage/*.md` and `index.json`; there
  is no whole-dataset export channel — machine migration/backup means
  manually copying directories.
- **Goal**: one command exports all data to a single JSON file; import
  **explicitly warns that existing data will be overwritten** and requires
  confirmation.
- **Approach**
  1. `export [--out path] [--since YYYY-MM]`: exports
     `{schema_version, generated, files:[{date, archived, tasks}],
     archives:[{month, tasks}], env:{path_style, defaults}}`.
  2. `import <file> [--dry-run] [--force]`: by default prints the number of
     files and tasks that would be overwritten; only `--force` actually
     overwrites; before importing, the existing `storage/` is auto-backed up
     as `storage.bak-<timestamp>/`.
  3. Import follows the migration chain by `schema_version`; fields newer than
     the current version **error out instead of being silently dropped**.
- **Priority**: P1
- **Dependencies**: recommended after 7/8, otherwise the export format has to
  change again.

---

## II. Interaction & prompts

### 17. Behavior-triggered gentle nudges (instead of timed popups)

- **Current gap**: there is no "time to tidy/back up" reminder at all; a
  timed popup easily becomes nagging.
- **Goal**: trigger a one-time, immediately actionable nudge bar from
  **behavior thresholds**.
- **Approach**
  1. Thresholds as constants, overridable in `env.json`:
     `NUDGE_LOG_COUNT = 20` (total records), `NUDGE_DIRTY_PATCHES = 15`
     (unsaved changes), `NUDGE_STORAGE_FILES = 30` (un-archived day files).
  2. On trigger, a **gentle banner** appears at the top of the page (purple,
     not a red alert) with buttons on the right: 「导出备份」/「立即保存」/
     「归档旧记录」 — the nudge must carry its own exit.
  3. Dismissal is recorded in `localStorage`; the same threshold never
     repeats; the next prompt only after crossing the next magnitude.
  4. CLI side appends one same line at the end of `list` / `index` output
     (plain text, does not affect exit codes).
- **Priority**: P2
- **Dependencies**: export feature (10).

### 24. Sample data & "clear samples"

- **Current gap**: `storage/` holds real todos; there is no one-click
  restorable demo data — after a fresh install or a machine switch the UI is
  empty and you cannot see what overdue/stalled/contingency states look like.
- **Goal**: provide a sample dataset covering every boundary state that can
  be loaded and cleared in one click, without touching real data.
- **Approach**
  1. Sample data lives in `samples/` (not in `storage/`); `demo load` copies
     it into `storage/`, `demo clear` only deletes entries tagged 示例.
  2. Samples must cover: overdue by 3 days, consecutive missed logging
     (stalled), make-up records, blocker+counter, dependency-blocked,
     subtasks, completed-and-archived.
  3. **Never auto-inject samples into existing user data**: `demo load` must
     ask for a second confirmation when `storage/` is non-empty.
- **Priority**: P3
- **Dependencies**: 7 (demonstrating make-up records / consecutive days needs
  the record layer first).

---

## III. Periodic reviews

### 18. Weekly report (Monday→Sunday summary + same-boundary week-over-week)

- **Current gap**: only `week.created / week.done` two counters exist; no
  per-week history, no comparisons, no report text.
- **Goal**: one command produces this week's engagement overview and can
  review any historical week.
- **Approach**
  1. Boundary fixed: Monday 00:00 through Sunday 23:59 (already in
     `WEEK_START_ISO`, reuse as-is).
  2. `report [--week YYYY-Wxx | --date YYYY-MM-DD]`: summarizes invested
     amounts, check-in days, minutes, completed counts, and compares with
     **last week under the same boundary** (same metric, same unit; when last
     week has no data, show 「暂无环比」, never 0%).
  3. Historical weeks are browsable: keep one summary line per week in the
     index to avoid full recomputation every time.
- **Priority**: P1
- **Dependencies**: 7 (no records → no "invested amount / minutes").

### 19. Four-column review (keep / problem / try / next-week plan)

- **Current gap**: reviews only live in conversation; nothing is structured
  and persisted, so next week cannot look back.
- **Goal**: persist the weekly four-column free text with the weekly report,
  and fold it into the one-shot report text.
- **Approach**
  1. Storage suggestion: `storage/weekly/YYYY-Wxx.md` (not part of daily
     indexing, avoiding pollution of day files). Four columns:
     `保持` / `问题` / `尝试` / `下周预案`.
  2. `report --note 保持=xxx 问题=yyy` writes incrementally; the web side
     edits directly on the weekly-report page and saves immediately.
  3. `report --text` generates a plain-text weekly report in one go: this
     week's numbers + comparison + four-column content, directly pastable
     into a daily report or group chat.
- **Priority**: P2
- **Dependencies**: 18.

---

## IV. Experience details

### 22. Confetti animation on completion

- **Current gap**: marking a task 「结束」 only shows a toast; no sense of
  accomplishment.
- **Goal**: one lightweight positive feedback on completion that is
  **non-intrusive, non-blocking, dismissible**.
- **Approach**
  1. Pure inline implementation: `document.createElement` generates 20–30
     `div`s with CSS `transform` animation, removed after 1.2 s.
  2. Trigger condition: status changes from non-结束 to 结束, and the current
     operation touches ≤ 3 tasks (no confetti for batch completion).
  3. Respect `prefers-reduced-motion: reduce`; the web side provides a toggle
     stored in `localStorage`.
- **Priority**: P4 (pure experience; can be done anytime)

---

## V. Not recommended for now

- **Forcing a "total/unit/deadline" quantified-goal model into the todo core
  model**: a todo is a one-shot state machine (待开始/进行中/结束), while a
  quantified goal is a cumulative counter — the two semantics conflict. If
  support is wanted, it should be an **optional metering field**
  (`目标总量/当前/单位`) layered on top, or a separate view — not a change to
  the definition of todo.
- **Regressing to a pure-localStorage single-file design**: the current
  "files as source of truth + CLI/web same-source + revision merge + patch
  queue" architecture is more rigorous; do not regress for the sake of a
  "single file".


---

## VI. Implemented (v0.7.0)

### 23. Triage entry `triage` (pure rules, no LLM)

- Decides add / update / status / delete from one sentence: `scripts/todo.py triage --text "..."`.
  Read-only, rule-based; order delete > status > update > add; questions and
  verb-less sentences fall back to `unknown + need_confirm`; commitment leads
  (需要/要/必须/应该/记得…) are forced back to `add`; targets resolve by T-ID or
  text similarity (prefers unfinished tasks), with `candidates` /
  `fallback_action=add` when not locked. Extracts due / importance / urgency /
  note / tags / workspace / update text. JSON contract:
  `action, confidence, need_confirm, reasons, text (verbatim, unfiltered),
  target, candidates, status, fields, suggested_tags, fallback_action`;
  exit 3 when confirmation is required (delete always).
- Use in session: run triage on the user's sentence, confirm when needed, then
  execute the underlying command.

### 24. Capture service `capture` (hotkey → clipboard → triage → system dialogs)

- `scripts/capture.py` (stdlib only) runs **inside `web/server.py`**:
  - **No filtering** — the raw clipboard text is the task content;
  - Win32 global hotkey (default Ctrl+Alt+T; RegisterHotKey + message-loop
    thread) + CF_UNICODETEXT clipboard read;
  - Anything needing confirmation/input pops a **system dialog (tkinter)**:
    verdict, target candidates, deadline/tags/note/importance/urgency, new
    status; delete always confirms (toggleable); guarded operations offer
    "Force" in a second dialog;
  - Config lives in `env.json` under `capture` (enabled / hotkey /
    confirm_delete / toast / triage_types), managed from the new web UI
    **Settings** page, which also has a read-only "Try triage" box;
    API: `GET|PUT /api/settings`, `POST /api/capture/triage`.
- Boundary: Windows only (Win32 hotkey/clipboard); degrades gracefully without
  a GUI; a taken hotkey errors with a hint to change it.
