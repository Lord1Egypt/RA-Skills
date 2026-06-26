---
name: agented
version: 1.3.0
binary: ae
description: A text editor for LLMs, not humans.
metadata:
  openclaw:
    requires:
      bins:
        - ae
    homepage: https://github.com/frane/agented
    emoji: "📝"
    install:
      - kind: brew
        tap: frane/tap
        formula: agented
        bins: [ae]
---

# agented (binary: `ae`)

`ae` is a stateful editor controlled by command-line verbs. State persists across sessions in a SQLite-backed workspace (`.agented/state.db`). Every edit is versioned in an undo tree — you can branch, jump to any past state, and never lose work.

## Use this tool when

- You need to edit one or more files in a repo across multiple steps and want a durable history.
- You want to leave notes for your future self or other agents (annotations) attached to specific files.
- You want safe multi-file refactors with all-or-nothing semantics (transactions).

## Don't use this tool for

- Reading repo overview / architecture (use plain `cat`/grep).
- Single one-shot edits where you don't care about history (use the platform's built-in editor).
- Anything that isn't text (no binary file support).

## How the editor enforces correctness for you

Every read returns a `state_token`. Pass it to your next write with `--expect`. If the file changed under you, the write is rejected (exit code 3) and the response includes the new content and the new token. Retry with the new token.

You don't need to "view before write" — the editor will tell you if your assumption is stale. You don't need to "branches before undo" — undo's error includes the branches if there's ambiguity. You don't need to "status before edit" — every operation's response carries the state you'd want to check.

The default is `concurrency.require_expect: warn`: writes without `--expect` succeed and emit a stderr warning. For multi-agent setups, set `require_expect: writes` in `.agented/config.json` to enforce strict pre-write checks. In either mode, an actual conflict (a stale `--expect` value) is rejected with exit 3 and the recovery payload — the tree never silently loses work.

**Short forms are the default in agent contexts.** Long forms exist for documentation and human readers; agent calls should use the shorter form to save tokens. `ae s foo.go -r 12:14 -w "..." -x ab12cd34` is the canonical shape, not `ae replace foo.go --range 12:14 --with "..." --expect ab12cd34`.

**For multi-line content, pipe via `-i` (--from-stdin) or use `-f <path>` (--text-file).** Stdin is auto-detected when piped, so `cat patch.txt | ae s foo.go -r 12:14 -i` and `echo "..." | ae i foo.go -A 0 -i` work without quoting tricks.


## The first-touch rule

The first time you touch a file in a session, do it through `ae open <path>`. Not `Read`, not `Edit`, not `cat`. The response is the input to the rest of the session.

`ae open` returns six things: the file's id, line count, head_edit_id, content_hash, state_token, and any active annotations inline. Treat that response as authoritative. Annotations were left by a prior session for you to read. Read them. The state_token threads forward into your next write. The line_count tells you whether your assumptions about the file's shape match.

`ae open <new-path>` is also the file-creation primitive. If the path doesn't exist on disk, ae creates an empty file there and registers it in the workspace. No `touch` first, no `--create` flag. The new-file flow is `ae open foo.go` → `ae i foo.go -A 0 -i` (insert content from stdin) → `ae w foo.go`. The same call covers "open this existing file" and "create this new file"; the response shape is identical either way.

Skipping this step costs you. If you `Read` first, the agent runtime has the bytes, but the editor doesn't know you've seen the file. Subsequent writes through `ae` will treat your context as a fresh actor and may surface conflicts that wouldn't have happened otherwise. If you read via `ae open`, the editor knows your starting point, your writes thread cleanly, and the workspace history shows your session as a coherent sequence of edits rather than a stranger's drive-by.

The trained habit ("read before write to be safe") doesn't apply here. ae reports drift via full-content rejection payloads. Read once at session start. Edit forward.

## Round-trip economy: don't over-fetch

Most LLMs were trained on `Read → Edit → Read → Edit` and reach for the same shape with ae. Don't. ae's contract eliminates almost every "look first to be safe" round-trip. Specific anti-patterns:

- **Don't `ae view` before `ae replace`/`insert`/`delete`.** You already know the line range from `ae open` (or `ae search`). If you're wrong, the write rejects with the current content attached (exit 3); you reconcile and retry. One trip on success, one trip on conflict. View-first burns a trip every time, success or not.
- **Don't `ae view` before `ae search`.** Search returns `line\tcol\ttext` per match. That's the answer. View only after if you need surrounding context.
- **Don't `ae load` before reading.** Auto-load on drift is on by default. Every write verb stat-s the file and reconciles disk changes itself. `ae load` is only for the rare case where you specifically want to capture a disk snapshot as an edit without modifying anything else.
- **Don't `ae status` just to refetch a state_token.** Every write returns the new token in the result. Thread it forward. The only reason to call `ae status` is when you explicitly need workspace-level info (open files, dirty flags, current actor).
- **Don't `ae open` more than once per file per session.** The first-touch rule covers the registration. Subsequent reads/writes auto-resolve the same FileInfo. Auto-open also kicks in transparently if you forget — `ae search foo.go` registers the file silently when needed.

- **Don't pipe ae output through `| head`/`| tail`/`| grep`.** Every read verb has `--range`, `--limit`, or `--pattern` to bound output server-side, and `--range` accepts Python-slice syntax: `1:10` for first 10, `-10:` for last 10, `5:-5` for middle slice (skip first 5 and last 5), `:20` for first 20, `-50:-20` for the lines 50-from-end through 20-from-end. Pipe-trimming after the fact wastes the round trip's setup cost.
- **Don't append `2>&1`.** ae uses exit codes — 0 success, 3 conflict (with full content payload on stdout), 1/2 for errors. Stderr is ae's own diagnostic noise; merging it into stdout means you parse around it. Just read stdout.

Translation: the canonical loop is `open → search/find → replace/insert/delete → repeat`. Three calls per logical edit, sometimes two. Not five.
## What this editor does that Read/Edit/Write can't

These are the operations that motivate reaching for `ae` over the built-ins.

- **Read once, edit forever.** Your local model of the file (built from the `ae open` response and every subsequent edit) is the source of truth. The editor reports drift via full-content rejection payloads, not via "Read before every Write" rituals. Verb: `ae open <path>`, then any number of writes without re-reading.
- **Branching tree, not stack.** Walking back is `ae undo`; jumping to any prior state is `ae head -e <edit_id>`. Both branches stay addressable; the wrong path is never lost. Verb: `ae br <path>` to list leaves, `ae head <path> -e <id>` to jump.
- **Three-way merge.** Reconcile two diverged branches with structured conflict responses. Auto-resolve via `--prefer a|b`; resolve specific ranges via `--resolve start:end=a|b|"text"`. Verb: `ae merge <path> -l <leafA> -l <leafB>`.
- **Atomic batches.** `ae apply` consumes JSON-lines on stdin and applies every operation inside one transaction. Replaces N Edit calls with one. Verb: `cat ops.jsonl | ae apply <path>`.
- **Atomic move.** `ae move` cuts a range and inserts it elsewhere — same file or cross-file — in one transaction. No partial-success risk. Verb: `ae move <path> --from S:E --to N` (same-file) or `--to-file <other> --to-line N` (cross-file).
- **Atomic extract.** `ae extract` cuts a range out of one file and writes it to another, creating the destination if absent and optionally saving both files in one call. The canonical refactor primitive. Verb: `ae extract <path> -r S:E --to <new-or-existing> [--to-line N] [--save]`.
- **Regex replace with capture groups.** `ae replace --pattern` does sed-style replacement in a single tool call. Verb: `ae s <path> -p '<re>' -w '<expansion>' [-L <max>] [-n]`. **Always single-quote `-w`** when using `$1`/`$2` backrefs — bash expands `$1` as the first positional arg (empty in most shells), so `-w "$1.foo"` silently inserts an empty string. Single quotes (`-w '$1.foo'`) pass `$1` through to ae, which expands per Go regexp.ExpandString semantics.
- **Range-based addressing.** Every write targets a line range or insertion point, not a string. Edit's "string appears multiple times" failure mode doesn't exist here. Verb: any of `ae s/i/d` with `-r S:E`.
- **Annotations as cross-session memory.** Per-file notes that persist across processes and across agents. Verb: `ae an <path> a -t "..."` to write; reading is automatic on `ae open`.
- **Transactions with auto-rollback.** `ae begin` opens a logical group; `ae commit` finalizes; `ae rollback` reverts. Forgotten transactions auto-rollback after the configured idle window. Verb: `ae begin / ae commit / ae rollback`.
- **Cross-agent shared state.** A Claude Code session and a Codex session both reading the same `.agented/state.db` see the same head, branches, annotations, and marks. The workspace is the durable thing; the agent identity is incidental.

## Reading verbs (idempotent, cheap)

**Bound output server-side, always.** Every read verb has `--limit`/`-L`, `--range`/`-r`, or `--pattern`/`-p` to cap the result set before it leaves the daemon. Do not pipe through `head`/`tail`/`grep` to truncate; the bytes are already on the wire by then. ae prints a stderr nudge when stdout is piped without a bound flag (silence: `AE_NO_NUDGE=1` env or `output.nudge_on_pipe: false` in config).
| Verb     | Short | Args                          | Output (tab) suffix       | Use when                              |
|----------|-------|-------------------------------|---------------------------|---------------------------------------|
| `view`   | `v`   | `<path> [--range S:E] [--raw]` | `state_token\t<hex>`      | Inspect a file or range. `--range` is Python-slice: `1:10` first 10, `-10:` last 10, `5:-5` middle slice, `:20` first 20, `42:50` window. **Multi-range** in one call: comma-separated, e.g. `--range 100:120,140:160` — output concatenates each window with `...` between non-contiguous gaps and one trailing `state_token`. Two view trips collapse into one. `--raw` emits verbatim bytes (no line-num prefix, no token) for piping to another tool |
| `search` | `/`   | `<path> --pattern <re>`       | `state_token\t<hex>`      | Find matches; output `line\tcol\ttext`|
| `diff`   | `df`  | `<path> [--from N --to M]`    | unified diff + token      | Inspect what an edit changed          |
| `log`    | -     | `<path> [--limit N]`          | tab-delimited audit rows  | See history of operations             |
| `branches` | `br` | `<path>`                     | `id\tts\tactor\tcmd\tis_head` | Discover alternative leaves     |
| `list`   | `ls`  | `[--all|--closed|--stale]`    | per-file summary          | What files are open                   |
| `status` | `st`  | `[<path>]`                    | workspace or file summary | Get state_token for next write        |
| `mark get` | -    | `<path> <name>`             | `name\tline\tsnapped\t...`| Jump back to a known anchor           |
| `annotate list` | -| `<path>`                       | `id\tts\tactor\tcontent`  | Recall notes from prior sessions      |
| `show`   | -     | `<path> [--edit <id>] [--no-color]` | colored, syntax-highlighted unified diff | Display a change to the user. NOT for tool result chains; lean tab format is the default everywhere else |
| `symbols` | `sy` | `[<path>] [--kind <k>] [--pattern <re>]` | `sym\t<kind>\t<file>:<line>:<col>\t<name>` | List symbols (file or workspace). IDE mode only; falls through to `lsp_unavailable` when daemon is off |
| `diag`   | -     | `[<path>] [--severity errors\|warnings\|all\|none] [--wait-ms N]` | `diag\t<sev>\t<file>:<line>:<col>\t<msg>\t<source>` | Pull LSP diagnostics on demand — one file, or the whole workspace when path is omitted. `--wait-ms` polls past the LSP's async publish lag. IDE mode only |

## Writing verbs (use `--expect <state_token>`)

| Verb       | Short | Args                                          | Conflict response | Use when             |
|------------|-------|-----------------------------------------------|-------------------|----------------------|
| `replace`  | `s`   | `<path> --range S:E --with TEXT --expect TOK` | exit 3 + content  | Change lines         |
| `insert`   | `i`   | `<path> --after N --text TEXT --expect TOK`   | exit 3 + content  | Add lines            |
| `delete`   | `d`   | `<path> --range S:E --expect TOK`             | exit 3 + content  | Remove lines         |
| `save`     | `w`   | `<path>`                                      | -                 | Write head to disk   |
| `load`     | `e`   | `<path>`                                      | -                 | Reload from disk     |
| `move`     | `mv`  | `<path> --from S:E --to N` (or `--to-file P --to-line N`) | exit 3 + content | Move a range; cross-file dst auto-created |
| `extract`  | -     | `<path> --range S:E --to <new-or-existing> [--save]` | -            | Refactor a range into a sibling file (atomic) |

Every successful write prints `edit_id=<n>\thead_edit_id=<n>\tline_delta=<d>\tline_count=<n>\tstate_token=<hex>`. Use the new token for the next write.
**Auto-save and auto-load are on by default.** Every write verb (replace/insert/delete/move/extract) and history verb (undo/redo/head) flushes the resulting head to disk in the same call. The result includes `saved: true` to confirm. Before the write, ae stat-s the file: if `(mtime, size)` match the stamp from our last save, the call proceeds; if disk was touched externally, ae loads the disk content as a new edit on the tree (so external changes are recoverable via `ae undo`/`ae head`) and applies your edit on top. The result includes `loaded_from_disk: true` and `drift_reason` when this happens.

Config knobs: `concurrency.auto_save = clean | off | force` (default `clean`), `concurrency.auto_load_on_drift` (default `true`). Env override: `AE_AUTO_SAVE=off`, `AE_AUTO_LOAD_ON_DRIFT=false`.

`ae save <path>` and `ae load <path>` still exist for granular control. They are not part of the normal write flow.
`ae save <path>` and `ae load <path>` still exist for granular control: `save` flushes head when auto-save was off, `load` pulls disk content into the workspace as a new edit (useful when an external editor diverged the file). Neither belongs in the normal write flow.

## History verbs

- `ae undo <path> [--count N]` — walk head pointer back N edits. Errors with branch info if ambiguous.
- `ae redo <path>` — walk forward along the most recently created child.
- `ae head <path> --edit <id>` — jump to a specific edit (use after `branches` shows alternatives).
- `ae branches <path>` — list leaf edits (alternatives that exist in the tree).

### Worked example: backtracking after a wrong direction

```
ae view foo.go --range 10:20            # state_token=A1B2
ae replace foo.go --range 12:14 --with "..." --expect A1B2   # state_token=B3C4
ae replace foo.go --range 18:18 --with "..." --expect B3C4   # state_token=C5D6
ae undo foo.go --count 2                # head moves back two; new state_token=A1B2-ish
ae replace foo.go --range 12:14 --with "DIFFERENT" --expect <new>  # creates branch B
ae branches foo.go                       # shows two leaves: original C5D6, and branch B's leaf
ae head foo.go --edit <C5D6_id>          # jump back to original branch's leaf
```

## Marks

Marks are named line anchors that survive edits. The editor recomputes a mark's line on every edit (deletes shift it down, inserts shift it up; if a delete includes the mark's line, it snaps to the start of the deletion and the `snapped` flag is set).

### Worked example: mark a return point before a multi-edit refactor

```
ae open auth.go                              # state_token=T1
ae mark auth.go add return_point --line 240
ae replace auth.go --range 100:140 --with "..." --expect T1   # state_token=T2
ae mark auth.go get return_point             # line is now 100+(new lines)-(40 deleted)
```

## Annotations — durable cross-session memory

Annotations are how a session leaves context for the next one. They live in the workspace, not in your context window. `ae open` returns active annotations inline so reading them is free — there is no separate "load memory" step.

These four behaviors are mandatory, not optional:

**1. On opening any file with annotations, read them before doing anything else.** They are the prior session's input to the upcoming task. Parse them, factor them into your plan, reference them when making decisions. Do not skip. Do not skim. They were left specifically because the prior session thought the next session needed them.

```sh
ae open auth.go
# response: annotation\t14\t...\tprev-actor\tauth path uses signed cookies; do not weaken
# response: annotation\t15\t...\tprev-actor\trefactor in progress, lines 80-130 half-done
# read both before issuing any edit
```

**2. On finishing substantive work on a file, leave an annotation.** "Substantive" means more than three or four edits, or any logical unit of work — "implemented X", "refactored Y", "fixed bug Z". Summarize what was done, what remains open, and any decisions that aren't visible in the code. Skip annotations only for truly trivial fixes (single-line typo, config tweak with no broader implication).

```sh
ae an auth.go a -t "implemented refresh-token rotation; remaining: revoke endpoint and key-rotation cron. token storage is at line 47 — do not move without auditing the audit log."
```

**3. On encountering a non-obvious invariant or constraint while reading code, annotate it before moving on.** If the next session would benefit from knowing it without re-deriving it, capture it now.

```sh
ae an scheduler.go a -t "the dispatcher in run() must remain pure — it's called during init() before the metrics package is loaded"
ae an fixtures_test.go a -t "tests depend on the exact ordering of map iteration in this fixture; do not switch to map-iteration-order-independent assertions"
```

**4. Do not annotate trivia.** Don't write "this is a Python file", "this function returns a string", "imports". Don't repeat what a docstring already says. Don't annotate something obvious from three lines of the function. Useless annotations train the next session to skim them — that's how you lose the high-signal ones.

## Transactions

`ae begin [path]` opens a transaction. All subsequent edits attach to it. `ae commit` finalizes; `ae rollback` reverts every edit back to the pre-transaction head on each affected file (the reverted edits remain visible in `ae log` as a closed branch, never lost).

If you forget to commit/rollback, the editor auto-rolls-back idle transactions per `transactions.auto_rollback_idle_for` (default 10m). You don't need to handle abandoned transactions defensively; the editor cleans up.

### Worked example: multi-file refactor with rollback safety on test failure

```
ae begin                                                  # tx_id=42
ae search auth.go --pattern 'oldName\\('                   # find call sites
ae replace auth.go --range 12:12 --with "newName(" --expect T1
ae replace auth.go --range 80:80 --with "newName(" --expect T2
ae replace caller.go --range 40:40 --with "newName(" --expect U1
# run tests externally; if green:
ae commit
# else:
ae rollback
```

## Worked examples

### 1) Read-modify-verify a function

```
ae view auth.go --range 50:80          # capture state_token=T1
ae replace auth.go --range 60:65 --with "func ..." --expect T1   # state_token=T2
ae diff auth.go                         # confirm intended change
```

### 2) Backtracking (see history verbs section above).

### 3) Leaving context for the next session

```
ae annotate auth.go add --text "Migration 0042 must run before this lands; coordinate with infra"
```

### 4) Picking up where another session left off

```
ae open auth.go              # response includes annotations and state_token in one shot
                             # immediately use --expect <returned_token> on the next write
```

### 5) Search-then-targeted-edits

```
ae search foo.go --pattern 'TODO'      # state_token=T1; matches show line/col
ae replace foo.go --range 12:12 --with "..." --expect T1   # state_token=T2
ae replace foo.go --range 47:47 --with "..." --expect T2   # state_token=T3
```

### 6) Multi-file refactor with rollback (see transactions section).

### 7) Atomic batch via `ae apply`

```
cat <<'OPS' | ae apply auth.go
s 12:12 newName(\n
s 40:40 newName(\n
i 80 // see ADR-0042\n
OPS
# all-or-nothing; on any failure the response identifies the failing op
# and the head is unchanged.
```

### `ae apply` input formats

`ae apply` reads operations from stdin in any of three formats. The format is detected automatically; no flag is needed.

**Shortform.** What you reach for when writing batches yourself.

```
s 12:14 new content
i 80 header line
d 67:69
m foo 50
```

**Longform.** Same density, fuller names. Use when the batch will be reviewed.

```
replace range=12:14 with=new content
insert after=80 text=header line
delete range=67:69
mark name=foo line=50
```

**JSON-lines.** Use when piping from another tool, especially `ae find --json`.

```
{"verb":"replace","range":"12:14","with":"new content"}
{"verb":"insert","after":80,"text":"header line"}
{"verb":"delete","range":"67:69"}
```

The decision rule: shortform when typing it yourself and you want the token economy, longform when the batch goes anywhere a human will read it, JSON-lines when piping from a tool that produces structured output.

Cross-file batches: shortform and longform use `@<file>` lines as separators. JSON-lines uses a `"file"` field per line.

State tokens: shortform appends `! <token>` at end of line, longform uses `expect=<token>`, JSON-lines uses an `"expect"` field.

### 8) Three-way merge with one resolved conflict

```
ae br auth.go
# leaves: 47 (refactor branch), 52 (bug-fix branch), head=52
ae merge auth.go -l 47 -l 52
# conflict response shows ranges modified by both branches
ae merge auth.go -l 47 -l 52 -R '20:22=a' -R '47:47=b'
# all conflicts resolved => commit a merge edit; head moves to the new id
```

### 9) LSP-driven structural navigation (IDE mode on)

```
ae find -R HandleAuth                  # who calls it?
# ref  auth.go:47:12   call         HandleAuth(ctx, req)
# ref  middleware.go:128:8   call   HandleAuth(ctx, r2)
# ref  test.go:34:5    import       HandleAuth

ae find -s HandleAuth                  # where is it defined?
# def  auth.go:47:1    HandleAuth   func

ae sy auth.go --kind func              # list functions in this file
# sym  func    auth.go:47:1    HandleAuth
# sym  func    auth.go:89:1    parseToken

# now do the actual edit, with the line number from the ref output
ae view auth.go --range 47:60          # state_token=T1
ae replace auth.go --range 50:50 --with "..." --expect T1
# response includes diag lines if gopls flags anything new
```

Reach for these instead of `grep` when the question is structural ("who calls", "where is X defined", "what does this file expose"). Reach for `ae search` / `ae find` (regex) for free-text in comments, strings, TODOs.


## IDE mode

When `ide.enabled: true` is set in `.agented/config.json`, IDE features are available:

- `ae symbols [path]` (short `ae sy`) lists symbols in a file or workspace
- `ae find --symbol <name>` (`ae / -s`) finds where a symbol is defined
- `ae find --references <symbol>` (`ae / -R`) finds all use sites
- `ae find --definition <symbol> --at <file>:<line>:<col>` (`ae / -D -A`) resolves a definition at a cursor position

When IDE mode is on, prefer these over `grep`/Glob for structural questions: "where is X defined", "who calls X", "what does this file expose". `ae find -R Foo` is one structured call with usage classification (call/read/write/import/definition); a grep is text-only and forces you to disambiguate matches in your head. The trained `grep -rn` reflex still applies for free-text searches over comments, strings, and TODOs; structural queries belong on the LSP.

You don't need to manage the daemon yourself. If config has IDE enabled, ae ensures the daemon is running when you invoke any IDE-relevant verb. The first invocation in a session may take a second or two while the LSP starts up; subsequent calls are fast.

The user may instruct you to enable or disable IDE mode for a specific task, overriding the config. Honor those instructions for the duration of the conversation.

When IDE features aren't available (config disabled, no instruction override, daemon crashed), LSP-dependent verbs return:

  error    lsp_unavailable    <reason>

Don't retry; proceed without those capabilities. Don't try to start the daemon yourself unless the user explicitly told you to.

When the user asks why IDE features aren't working, run `ae lsp doctor [language]` and report what it says. The output is tab-delimited rows of `doctor <lang> <check> <subject> <result> <detail>` where result is `ok | warn | fail | info`. Doctor reads-only; it can't fix anything, but the `fail` and `warn` rows usually identify the issue (missing binary, missing `package.json`/`Cargo.toml`/`tsconfig.json`, eslint without `.eslintrc`, pyright without an activated venv).

When IDE mode is active, mutating verbs (`ae save`, `ae replace`, `ae apply`, etc.) may include diagnostic lines in their responses:

  ok    state_token=ab12cd34
  diag  warn  foo.go:89:4   unused variable x   lint
  diag  error foo.go:47:12  undefined: bar      compile

Diagnostics are informational. The operation succeeded; the diagnostics report current LSP findings on the file. Decide whether to act on them based on the task.

The absence of diag lines does not mean the file is clean. It means either there are no diagnostics, the LSP hasn't analyzed yet, the language has no LSP configured, or the daemon isn't running. Don't infer file health from absence of diagnostics. If the user asks "is this file clean?", answer "no diagnostics returned" rather than "the file is clean."

To pull diagnostics on demand instead of waiting for them to ride along on an edit, use `ae diag [path]` — omit the path for a workspace-wide sweep across all open files. Language servers publish asynchronously (often a second or two after a change), so pass `--wait-ms <N>` to poll until diagnostics appear or the timeout elapses; this is the reliable way to confirm an edit parsed without falling back to a full compile. Filter with `--severity errors|warnings|all|none`. Over MCP the same diagnostics also ride inline on every tool response that touched a file (a `diag` field on the JSON result), and `ae_diag` is exposed as a dedicated tool (with `wait_ms`).

A language can run multiple LSP servers. The first listed answers symbol/reference/definition queries; all of them publish diagnostics, tagged by source server in `diag` lines:

  diag  error foo.ts:14:3   Cannot find name 'bar'.   ts
  diag  warn  foo.ts:14:3   'bar' is not defined.       eslint

The last column is the source-server label (e.g. `tsserver`, `eslint`, `pyright`, `ruff`, `gopls`). When you see two `diag` lines at the same location with different sources, treat them as independent findings — the type checker and the linter looking at the same code from different angles.

Default server lists (when the language has `auto_start: true` and the binaries are installed):
- `go`: `gopls`
- `typescript`: `tsserver` + `eslint`
- `python`: `pyright` + `ruff`
- `rust`: `rust-analyzer`

### Severity, kind, and usage vocabularies

| Severity | LSP origin |
|----------|------------|
| `error`  | LSP severity 1 |
| `warn`   | LSP severity 2 |
| `info`   | LSP severity 3 |
| `hint`   | LSP severity 4 |

| Kind     | Examples |
|----------|----------|
| `func`   | top-level function |
| `method` | method on a type |
| `type`   | type alias, struct |
| `class`  | class (Python, TS) |
| `interface` | interface |
| `var`    | local or package variable |
| `const`  | constant |
| `field`  | struct/class field |
| `module` | package or namespace |

| Usage    | When |
|----------|------|
| `call`   | `name(...)` |
| `read`   | name appears, no other label fits |
| `write`  | `name = ...` or `name := ...` |
| `import` | import statement |
| `definition` | the line that defines the symbol |
| `other`  | catch-all |

## Errors and recovery

| Error substring          | What it means                                        | Next action                                           |
|--------------------------|------------------------------------------------------|-------------------------------------------------------|
| `state_token mismatch`   | Head moved or you didn't pass `--expect`             | Use the `current_token` from the conflict response    |
| `branch ambiguous`       | undo/redo would have to choose among siblings        | Read the branches list in the response, then `head --edit` |
| `transaction <id> owned by` | Another actor's tx is open; writes are blocked      | Wait, or pass `--no-transaction` to bypass            |
| `transaction auto-rolled-back` | The editor reverted an idle tx automatically       | Check `ae log <path>`; the auto_rollback row identifies what was reverted |
| `mark name exists`       | Mark name collision                                   | Pick a different name or `mark remove` first          |
| `file not registered`    | The path was never `ae open`'d                       | Run `ae open <path>` first, or pass `--auto-open`     |
| `pattern compile error`  | RE2 syntax issue                                     | Fix the pattern (Go's `regexp` syntax)                |
| `range out of bounds`    | Line range exceeds file                              | Re-`view` to get the current line count               |
| `skill out of date`      | Installed SKILL.md major-mismatches binary           | `ae skill install`                                    |

## Anti-patterns

- **Reaching for `Read`/`Edit`/`Write` because they're familiar.** When editing a file you'll edit more than once, ae is the right verb. Defaulting to the built-ins is path-of-least-resistance, not a technical case. The exceptions are bootstrap (the project doesn't build, ae can't be invoked) and one-shot inspection of files outside any project (`~/.zshrc`, configuration files in `/etc/`). Everywhere else, ae.
- Discarding `state_token` between calls (forces unnecessary conflicts on every write).
- Ignoring the conflict response payload (the new content is right there; use it instead of running `view` again).
- Calling `redo` after intentionally creating a new branch — `redo` will fail with branch ambiguity. Use `head --edit <id>` instead.
- Useless annotations ("this is a function").
- Unescaped regex special characters in `search` patterns.
- Skipping the annotations on `ae open`. They were left for you on purpose; reading them is free.
- Using Read/Edit/Write on a file ae already manages. They bypass the tree, the annotations, and the conflict detection; the agents that share this workspace will see drift they cannot recover from.
- Inferring file health from absence of `diag` lines. Diagnostics absence has multiple causes (no findings, LSP not analyzed yet, language not configured, daemon not running).
- Trying to start `ae lsp` yourself unless the user has explicitly authorized it. The auto-start handles it when config says enabled.

## Output format reference

All output is tab-delimited (`\t`) with one record per line.

- `view`: each line `<line_num>\t<content>`. Trailer (when `output.include_state_token` is on): `state_token\t<hex>`.
- `search`: each match `<line>\t<column>\t<text>`. Trailer: `state_token\t<hex>`.
- `replace`/`insert`/`delete`: a single line `edit_id=<n>\thead_edit_id=<n>\tline_delta=<d>\tline_count=<n>\tstate_token=<hex>`.
- `undo`/`redo`/`head`: a single line `head_edit_id=<n>\tline_count=<n>\tstate_token=<hex>`.
- `branches`: `<edit_id>\t<created_at>\t<actor>\t<command>\t<is_head>`.
- `open`: header line `<file_id>\t<path>\t<line_count>\t<head_edit_id>\t<annotation_count>\t<state_token>`. Then for each annotation: `annotation\t<id>\t<created_at>\t<actor>\t<content>`.
- `status` (workspace): `workspace\tactor=...\topen_files=...`. (file): `file\tid=...\tpath=...\tline_count=...\thead_edit_id=...\tstate=clean|dirty\tstate_token=...`.
- `log`: `<created_at>\t<actor>\t<command>\t<result>\t<edit_id>`.
- Conflict response (exit code 3, on stdout): `conflict\tfile_id=...\tcurrent_token=...\thead_edit_id=...\thead_actor=...\tline_count=...` then `note\t...` then `---current-content---` then literal content then `---end---`.

For programmatic parsing, pass `--json` to any verb and you'll get a stable JSON object instead of tabs.

## Verb shortcuts

| Long       | Short | Long       | Short |
|------------|-------|------------|-------|
| view       | v     | branches   | br    |
| search     | /     | open       | o     |
| replace    | s     | close      | x     |
| insert     | i     | list       | ls    |
| delete     | d     | save       | w     |
| undo       | u     | load       | e     |
| redo       | r     | diff       | df    |
| mark       | m     | status     | st    |
|            |       | annotate   | an    |
| symbols    | sy    | lsp        |       |
| --symbol   | -s    | --references | -R  |
| --definition | -D  | --at       | -A    |
| --diagnostics | -G | --no-diagnostics | -N |
| --background | -B  |            |       |

## Configuration awareness

The editor's behavior is influenced by the project's `.agented/config.json`:

- `concurrency.require_expect`: `writes` | `warn` | `off`. Default `writes`. Determines whether writes without `--expect` are rejected, warned, or silently allowed.
- `transactions.auto_rollback_idle_for`: how long an idle transaction can sit before auto-rollback. Default `10m`.
- `auto_prune.*`: whether and when the editor prunes stale history. You don't need to think about it.
- `output.include_state_token`: default `true`. Adds the `state_token\t<hex>` trailer to read verbs' output. Don't turn this off for agent use.
- `workspace.auto_create`: `root-only` (default) | `true` | `false`. Auto-creates `.agented/` at the project root on first use; you almost never need `ae init` in the normal flow.

When unsure where ae is resolving paths, run `ae status -W`. The first line includes `cwd=<dir>\tworkspace_dir=<dir>` so you can confirm the editor is pointing at the workspace you expect.

`ae config show` prints the resolved configuration if you want to know what's active. The agent does not modify config; the human sets it.
