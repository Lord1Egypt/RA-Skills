# Changelog

All notable changes to agented are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com), and the project follows [Semantic Versioning](https://semver.org).


## [v0.5.0] - 2026-06-23

### Features

- **`ae diag` verb + diagnostics over MCP.** `agented` already ran language servers and cached their diagnostics, but the MCP surface never exposed them — an agent editing through `mcp__agented__ae_*` got `saved: true` with no way to tell whether the edit even parsed, short of a full `go build` / `cargo check`. This release closes that gap:
  - New **`ae diag [path]`** verb (MCP tool `ae_diag`): pull LSP diagnostics for one file, or the whole workspace when the path is omitted. Flags: `--severity errors|warnings|all|none`, `--limit`, and `--wait-ms <N>` to poll past the language server's asynchronous publish lag.
  - **Inline diagnostics on MCP responses** that touch a file: edit / open / save tool results now carry a `diag` field with the file's current diagnostics, at parity with the CLI's `diag` lines.
  - Language-agnostic — gopls, tsserver, eslint, pyright, ruff, rust-analyzer, or any configured LSP, routed by file extension. Each diagnostic is self-describing: severity, range, message, source, rule id, source server, and path.

## [v0.4.9] - 2026-06-01

### Features

- **`ae permissions disable-internals --strict`** (and its `enable-internals --strict` pair). The nuclear option: extends the built-in tool denies with shell-command denies for the obvious editor/reader fallbacks an agent reaches for via Bash / run_shell_command / Codex shell:

  `cat, sed, awk, head, tail, vi, vim, nano, less, more, ed, emacs, code`

  Discovery + version-control tools (`grep`, `find`, `ls`, `git`) stay allowed. Per-target output:

  | Target | What `--strict` writes |
  |---|---|
  | claude | `Bash(<cmd> *)` entries appended to `permissions.deny` in the same settings.json |
  | codex | new file `~/.codex/rules/agented-strict.rules` with `prefix_rule(..., forbidden)` calls (Starlark) |
  | gemini | new file `~/.gemini/policies/agented-strict.toml` with `run_shell_command` + `argsPattern` rules |
  | openclaw | n/a |

  Pair with the existing `disable-internals` (which already denies Read/Edit/Write/NotebookEdit). The strict flag is additive and reversible — `enable-internals --strict` removes both layers cleanly.


## [v0.4.8] - 2026-05-13

### Fixes

- **`ae permissions disable-internals --help` was stale.** The long description still claimed Claude was the only supported target, even though v0.4.6 added Gemini and v0.4.7 added Codex. The string was last touched in v0.4.5 and never updated when the other two targets landed. Now reflects the full per-target matrix.


## [v0.4.7] - 2026-05-08

### Features

- **`ae permissions disable-internals` now writes a Codex deny rule too**, completing the Claude / Gemini / Codex matrix. Codex's only edit primitive at the public surface is `apply_patch`, so the implementation maps the canonical Read/Edit/Write/NotebookEdit input down to one TOML line — `apply_patch = false` under a `[tools]` table in `~/.codex/config.toml` — written idempotently with our own minimal section editor (no external TOML lib).

  Honesty caveat: Codex accepts `tools.apply_patch = false` via `-c` parsing without error, but the published config docs don't explicitly state that this disables the tool at runtime. Treated as **experimental** — the docs flag it, the rule gets written, and users can verify the behavior in their own Codex session.

  | Target | Mechanism | File |
  |---|---|---|
  | claude | `permissions.deny` array | `~/.claude/settings.json` (global) or `.claude/settings.local.json` (project) |
  | codex | `tools.apply_patch = false` (experimental) | `~/.codex/config.toml` (global) |
  | gemini | Policy Engine TOML rules | `~/.gemini/policies/agented-deny.toml` (global) |
  | openclaw | n/a — managed at agent level | — |

### Documentation

- `docs/permissions.md` per-target table updated with Codex's row and the experimental caveat.


## [v0.4.6] - 2026-05-08

### Features

- **`ae permissions disable-internals` now covers Gemini.** v0.4.5 shipped Claude only; this iteration adds Gemini support via its Policy Engine. Writes `~/.gemini/policies/agented-deny.toml` with `decision = "deny"` rules for `read_file`, `edit`, `write_file` (mapped from the canonical Read/Edit/Write/NotebookEdit names). Codex still skips: per OpenAI's docs, the `.rules` file covers shell-command sandboxing and there's no documented schema for denying built-in tools.

  Per-target summary now exposed via the same `--target all` flow:

  | Target | What `disable-internals` writes |
  |---|---|
  | claude | `permissions.deny` in `~/.claude/settings.json` |
  | gemini | `~/.gemini/policies/agented-deny.toml` (Policy Engine TOML) |
  | codex | skip (no upstream schema) |
  | openclaw | skip (managed at agent level) |

- **`docs/permissions.md`** updated with a per-target schema table and example invocations for each.


## [v0.4.5] - 2026-05-08

### Features

- **`ae permissions disable-internals`**. New subcommand that writes deny-rules for the built-in file tools (`Read`, `Edit`, `Write`, `NotebookEdit`) into the agent's permission config. Once these are in place, agents that have the agented skill installed are forced to drive `ae` from Bash instead of falling back to the built-ins out of training-data habit. Pair with `ae permissions install` (the existing allow-rules for `Bash(ae *)`).

  Today writes only Claude Code's `permissions.deny` array in `~/.claude/settings.json` (global) or `.claude/settings.local.json` (project). Gemini and Codex are skipped with a clear "deny-list schema not yet known" reason — their config schemas don't have a documented public deny-list field; we'll fill it in once they do.

  ```sh
  ae permissions disable-internals             # write deny rules to project scope
  ae permissions disable-internals -s global   # to global scope
  ae permissions disable-internals --dry-run   # preview
  ae permissions enable-internals              # remove the deny rules
  ```


## [v0.4.4] - 2026-05-08

### Features

- **Multi-range view**. `ae view -r 100:120,140:160` returns both windows in one call instead of two trips. Output concatenates each window with a `...` separator on non-contiguous gaps and one trailing `state_token` line. Single-range syntax is byte-identical to v0.4.3 — no existing call shape changes. The MCP tool gains a `ranges` arg with the same comma-separated format.

- **MCP parity for the four missing core verbs**. Previously the MCP server exposed 30 tools but skipped `apply`, `move`, `extract`, and `merge` — three of them ae's headline atomicity primitives, the fourth its three-way merge. They're now first-class:
  - `ae_apply` (`path`, `ops`, `multi_file`, `expect`, `expect_workspace`) — atomic batch ops; `ops` accepts the same JSON-lines / shortform / longform input the CLI reads from stdin.
  - `ae_move` (`path`, `from_start`, `from_end`, `to_line`, `to_file`, `expect`, `auto_open`) — same-file or cross-file atomic move.
  - `ae_extract` (`path`, `from_start`, `from_end`, `to_file`, `to_line`, `save`, `expect`) — the canonical refactor primitive: cut a range out of one file, write it to another (auto-created if absent), optionally save both.
  - `ae_merge` (`path`, `leaf_a`, `leaf_b`, `prefer`, `abort`) — three-way merge between two leaf edits; fine-grained per-range `--resolve` specs remain CLI-only for now.

  Brings the MCP tool count to 34 and closes the parity gap CLI agents had over MCP agents.

### Tests

- `TestViewSingleRangeBackwardCompat` pins the v0.4.3 single-range output byte-for-byte.
- `TestViewSingleRangeViaRanges` confirms passing one element via the new `Ranges` field produces identical output to the legacy `Start/End` path.
- `TestViewMultiRangeNonContiguousEmitsSeparator`, `TestViewMultiRangeAdjacentNoSeparator`, `TestViewMultiRangeOverlapMerges`, `TestViewMultiRangeOutOfOrderSorts` cover the new behaviors.

### Deferred to v0.4.5

- Multi-range `delete` and `search` — same pattern, more code; kept out of v0.4.4 to ship the high-leverage view + MCP-parity bits cleanly.
- LSP-backed MCP tools (`ae_diagnostics`, `ae_hover`, `ae_references`) — design discussed in the v0.4.0 notes; implementation pending.

## [v0.4.3] - 2026-05-07

### Features

- **Claude Code plugin distribution**. agented is now publishable as a Claude Code plugin via a marketplace at the repo root (`.claude-plugin/marketplace.json`). After tagging, users install with:

  ```sh
  /plugin marketplace add frane/agented
  /plugin install agented@frane-agented
  ```

  The plugin layout under `plugin/` ships the embedded `SKILL.md` plus `.mcp.json` (registers `ae serve`). The `ae` binary still has to be on PATH (Homebrew or curl); plugins don't ship cross-platform binaries.

- **Codex CLI plugin manifest**. Same plugin directory carries `plugin/.codex-plugin/plugin.json` for OpenAI Codex CLI. Codex's marketplace mechanism is still per-user (`~/.agents/plugins/marketplace.json`); users add the plugin manually via that file until the official Codex directory opens up.

- **Gemini CLI extension manifest**. Same directory carries `plugin/gemini-extension.json` plus `plugin/GEMINI.md` (Gemini insists on the `.md` being named `GEMINI.md` rather than `SKILL.md`). Distributable via `gemini extensions install <github-url>`.

- **`make stage-plugin` + drift guard**. `internal/skill/SKILL.md` stays the canonical copy; `make stage-plugin` mirrors it into the three plugin paths (`plugin/skills/agented/SKILL.md`, `plugin/GEMINI.md`) and rewrites the three manifests with the current git tag. `internal/skill/plugin_sync_test.go` runs in `go test ./...` and fails CI if any of the three skill copies drifts from the canonical, so a release can't ship a stale plugin.

## [v0.4.2] - 2026-05-07

### Fixes

- **`ae apply` shortform now rejects `\<whitespace>` as content prefix** instead of silently embedding the literal `\` in the file. Users hit this thinking `\` was an escape for leading whitespace; it never was. The new error names two valid alternatives: drop the `\` (shortform preserves leading whitespace verbatim after the line-number separator) or use the heredoc form `i N <<<` for content that begins with `\` legitimately.
- **Auto-load drift is no longer silent**. When ae detects that the on-disk content has diverged from workspace head (an external editor wrote in between ae calls) and folds the disk content in as a new edit before applying the user's write on top, the CLI now prints a `warning: drift reconciled` line to stderr explaining what happened and noting that the disk version is recoverable via `ae undo` / `ae head`. Previously the reconciliation only surfaced via the `loaded_from_disk: true` JSON field, which was easy to miss in tab-mode output.

### Documentation

- **SKILL.md note on shell-quoting `-w` for capture groups**. `-w "$1.foo"` in bash silently expands `$1` as the first positional arg (empty in most contexts), inserting an empty string instead of the captured submatch. Single-quote (`-w '$1.foo'`) to pass `$1` through verbatim to ae's Go-regexp expander. The previous "regex replace with capture groups" entry didn't flag this; now it does.

## [v0.4.1] - 2026-05-07

### Breaking

- **Removed tier-3 global-workspace fallback.** When ae could not find an existing `.agented/` above cwd and could not auto-create one (no project-root signal, or `auto_create=false`/`--no-auto-workspace`), it used to silently fall back to `~/.agented/`. That meant any number of unrelated projects ended up sharing a single SQLite database, with the same actor names and intermingled state — exactly the "no isolation" footgun. ae now errors with a message naming the three explicit options: run `ae init` here, pass `--workspace-dir <path>`, or set `workspace.auto_create=true` in config.

  Migration: if you have edits in `~/.agented/` from prior versions, they remain readable via `ae --workspace-dir ~/.agented <verb>`. Most users will simply run `ae init` per project (or leave the project-root auto-create to handle it on first call). The few who relied on a true global scratch workspace can flip the new config knob.

## [v0.4.0] - 2026-05-06

### Features

- **Multi-workspace MCP**. `ae serve` is no longer locked to a single workspace at startup. A new `cmd.Pool` lazily resolves an Engine per `.agented/` dir, keyed by the absolute path argument on each tool call, so one global MCP server registration (Claude Desktop, Codex Desktop, Cursor) handles every project the user touches. Tool calls without an absolute path fall back to a default workspace (the one resolved from cwd at startup, when there is one). Paths outside any project workspace error loudly with a `run \`ae init\`` suggestion instead of silently using the global fallback.
- **Per-workspace LSP daemons**. The LSP daemon model follows the same shape: each workspace gets its own daemon, lazily spawned on the first write that targets it. `lsp.SpawnBackground` and `lsp.EnsureDaemon` are now in the `lsp` package (used by both CLI and MCP), and spawn explicitly with `--workspace-dir <wsDir>` so the daemon attaches to the right project regardless of the parent process's cwd. New `Engine.NotifyLSPIfWrite` hook is invoked from MCP after every successful tool call.
- **Per-LSP `init_options` pass-through**. `IDEServerCfg.InitOptions` (a free-form `map[string]any`) is forwarded verbatim as the LSP `initialize` request's `initializationOptions` field. ae does no validation; the schema is whatever the server accepts. Closes the recurring "rust-analyzer / clippy / linkedProjects" round-trip — users can drop `init_options: { check: { command: "clippy" } }` directly into ae's config instead of wrangling a separate `rust-analyzer.toml`.
- **Unified `internal/agents` registry**. The skill-target list (`internal/skill/targets.go`) and MCP-install-target list (`internal/mcpinstall`) used to duplicate per-agent definitions for Claude, Codex, Cursor, Gemini, OpenClaw. They now both build their slices from a single source of truth in `internal/agents/agents.go` — adding a new client is a one-place change.
- **Gemini CLI integration**. New target across both surfaces: `ae skill install --target gemini` writes to `~/.gemini/extensions/agented/GEMINI.md` plus a sibling `gemini-extension.json` so Gemini recognises the directory; `ae mcp install --target gemini` writes the agented entry to `~/.gemini/settings.json`.

### Fixes

- **rust-analyzer "Failed to discover workspace"**. `SpawnClient` now sets `cmd.Dir = workspaceRoot` on the LSP child process. rust-analyzer (and several other servers) discover the project from cwd, not from `rootUri` alone. The bug surfaced as silent diagnostic loss whenever `ae lsp` was started from a subdirectory; users would round-trip clippy errors through cargo because nothing came back as `diag` lines.
- **`ae lsp doctor` Cargo.toml message**. When the workspace dir doesn't contain `Cargo.toml`, the doctor used to say "missing in workspace root: …" which is misleading — Cargo.toml may exist higher up. Updated to point at the workspace-root mismatch and suggest either moving `.agented/` or using `init_options.linkedProjects`.

### Defaults

- **`ide.diagnostics.default` is now `warnings`** (was `errors`). The previous default dropped warn/info/hint lines, which silently hid the bulk of useful LSP output (clippy, unused imports, type warnings). Users who want the old strict-errors-only behavior can set it back, or pass `-G errors` per call.

### Documentation

- New section in `docs/ide.md` on per-server `init_options`, with the rust-analyzer/clippy example.
- New section in `docs/mcp.md` on workspace routing in multi-workspace serve mode.

### Tests

- `TestPoolMultiWorkspaceRouting`: one MCP server, two `.agented/` workspaces, paths route correctly; stray-path opens reject loudly.

## [v0.3.9] - 2026-05-01

### Fixes

- **`ae move` now flushes to disk** ([#3](https://github.com/frane/agented/issues/3)). Previously the store-layer move succeeded and reported success, but the new head was never auto-saved; `ae status` showed `state=dirty` immediately after the call. Both same-file and cross-file branches now run the standard autosave; cross-file flushes both source and destination. Result also gains `Edit.Path` and `Edit.Saved`.
- **`ae apply -M` is atomic across files** ([#4](https://github.com/frane/agented/issues/4)). Previously the per-op autosave fired before the next op had a chance to fail, so a failure in op N left ops 0..N-1 written to disk while the store rolled back. Apply now suppresses per-op autosave for the duration of the batch and flushes every touched file once after the implicit commit. On failure no disk writes happen.

### Tests

- `TestMoveAutosaveSameFile`, `TestMoveAutosaveCrossFile`: pin the autosave behavior for both move branches.
- `TestApplyMultiFileAtomicityOnFailure`: pin the multi-file rollback behavior using the bug-report repro.
- `TestApplyMultiFileSuccessFlushes`: confirm the success path still writes to disk for every touched file.

## [v0.3.8] - 2026-04-30

### Release engineering

- **Migrated to `homebrew_casks:` from deprecated `brews:`**. goreleaser deprecated formula generation in v2.10 in favor of casks. The cask path also gives us `postflight` hooks: a one-line `xattr -dr com.apple.quarantine` clears the macOS Sequoia provenance attribute that was SIGKILL-ing the brew-installed binary on first run. v0.3.7's formula at `frane/homebrew-tap/agented.rb` should be deleted; v0.3.8 ships the cask at `frane/homebrew-tap/Casks/agented.rb`.
- Cask `binary:` field renamed to `binaries: [ae]` per goreleaser v2.12.6 deprecation.

Same binary as v0.3.7; release-engineering only.

## [v0.3.7] - 2026-04-30

### Release engineering

- **Homebrew tap.** `brew tap frane/tap && brew install agented` now installs the signed/notarized release binaries; `brew upgrade` picks up future releases automatically. The goreleaser `brews:` block generates `Formula/agented.rb`, computes SHA256s, and commits to `frane/homebrew-tap` on every tag. macOS Sequoia users get the signed binary path with no SIGKILL surprises.
- **`make publish-skill` now declares brew as the preferred install** in the openclaw metadata block injected at stage time. Two install entries are emitted in order: `kind: brew` (tap `frane/tap`, formula `agented`), then `kind: go` as a fallback for users without brew. ClawHub's runtime tries them in order.

No code or behaviour changes to the binary itself; same build as v0.3.6.

## [v0.3.6] - 2026-04-30

### Fixes

- **Autosave race detection.** v0.3.2 swapped `atomicfile.Editor.Write` (with backup + readback verify) for `atomicfile.WriteSimple` to win 2.2× on the bench. The verify step would have caught "rename succeeded but disk content does not match what we wrote", which is exactly the symptom an active multi-actor session reported: matches=N, new state_token, but disk lagged. Added a stat-after-rename: if disk size disagrees with `len(head)`, re-read and confirm; on mismatch surface a clear error rather than silently claiming saved=true. Keeps the v0.3.2 speedup for the common case (single fsync, no readback) and only pays the read on the rare disagreement path.
- **Skill-version warning rate-limit.** "warning: installed skill version X differs from binary Y" used to fire on every command. Now writes a `.agented/.skill_warn` marker keyed on the `(installed, binary)` pair and skips subsequent warnings until either side changes. One warning per workspace per version drift, not one per call.
- **Empty-content guard on `--from-stdin` / `--text-file`.** When the resolved input yields zero bytes, write verbs (`replace`, `insert`, `apply`) now error with a clear message: "pipe content or use `ae delete` to remove a range". Catches the agent-wiring bug where an exec wrapper drops stdin and the underlying replace turns into a destructive delete. Pass `--allow-empty` / `-e` to override.
- **Makefile install on macOS Sequoia.** `make install` previously used `cp`, which preserves the `com.apple.provenance` xattr. The resulting binary at `~/.local/bin/ae` got SIGKILL-ed by Gatekeeper on Apple Silicon. Switched to `install -m 755` plus a best-effort `xattr -c` to clear residual attrs.

### Tests

- `TestReadTextInput*` (5 cases): empty stdin, empty file, --allow-empty bypass, non-empty unaffected.
- `TestShouldEmitSkillWarn`, `TestShouldEmitSkillWarnNoEngine`: marker rate-limit + nil-engine fallback.
- `TestAutoSaveVerifyHappyPath`: happy-path regression so the new verify does not produce false positives.

## [v0.3.5] - 2026-04-30

### Features

- **Pipe nudge.** Read verbs (`view`, `search`, `find`, `log`, `symbols`, `find -s/-R/-D`) now print a one-line stderr nudge when stdout is piped and no result-bounding flag was set: "use --limit/-L (or --range, --pattern) to bound output server-side; do not | head/tail/grep". Catches the common trained-reflex mistake (`ae sy foo.ts | head -40`) at runtime even when SKILL.md is skimmed. Disable per-call with `AE_NO_NUDGE=1` or globally via `output.nudge_on_pipe: false` in `.agented/config.json`.
- **`-Z` short** for `--no-auto-lsp` (the only v0.3-era persistent flag without a short).

### Documentation

- SKILL.md (1.2.6): a "Bound output server-side, always" callout sits at the top of the reading verbs table. Same rule that was buried in the anti-patterns list, hoisted into the verb reference where the agent looks first.

## [v0.3.4] - 2026-04-30

### Features

- **`ae lsp doctor [language]`** diagnoses LSP setup without starting the daemon. Per language, checks: server binary on PATH (with `--version` probe), language-specific config files (`go.mod`, `package.json` / `tsconfig.json` / `.eslintrc.*`, `pyproject.toml` / venv detection, `Cargo.toml`), `node_modules/` presence for typescript, daemon state from `lsp_status`. Output is tab-delimited `doctor <lang> <check> <subject> <result> <detail>` with results in `ok | warn | fail | info`. Read-only; doesn't fix anything, but the `fail` and `warn` rows usually identify the issue.
- Doctor covers all four supported languages: `go`, `typescript`, `python`, `rust`. Custom languages get a generic "no language-specific config checks defined" line.

### Documentation

- README: new "When the daemon doesn't behave: `ae lsp doctor`" section with sample output and a per-language check table.
- SKILL.md (1.2.5): the `lsp_unavailable` recovery flow now points the agent at `ae lsp doctor` first.

## [v0.3.3] - 2026-04-30

### Fixes

- **Skip auto-start servers whose binary is not on PATH.** Default config has `go.auto_start: true`, which crash-recorded a "gopls: file not found" row in `lsp_status` on machines without Go. The user could do nothing about it; the row was just noise muddying `ae lsp status`. The daemon now `exec.LookPath`-s each server's command before spawning. Misses log a single "skip <lang>/<name>: <bin> not on PATH" line and proceed.
- **Clear stale `lsp_status` rows on daemon start.** Old crashed/stopped rows from prior runs no longer linger.

### Tests

- New regression test `TestResolveIDETypescriptOverrideKeepsExtensions` for the user-reported config-merge case (project sets only `ide.languages.typescript`, embedded `extensions` map must survive). The merge already works; the test pins it.
- New `TestIDELanguageCfgResolvedServersLegacy` for the back-compat shim that synthesizes a one-element servers slice from the legacy single-server form.
- New `TestStartLanguagesSkipsMissingBinary` for the LookPath preflight behaviour.

### Notes for users hitting "no language server for .ts" on a TypeScript project

If `ae sy foo.ts` returns `error lsp_unavailable no language server for .ts` while you have `typescript-language-server` on PATH:

1. Confirm the resolved config: `ae config show ide.languages.typescript` should show `auto_start: true` and a `servers` list.
2. Inspect the daemon log: `cat .agented/lsp.log` shows spawn errors and the new "skip" lines for missing binaries.
3. Check the status table directly: `sqlite3 .agented/state.db "SELECT * FROM lsp_status"` reveals all rows including ones not in `ae lsp status`' formatted output.
4. Restart the daemon after editing `.agented/config.json`: `ae lsp stop && ae lsp --background`. The daemon reads config at startup; live config reload isn't supported.

## [v0.3.2] - 2026-04-30

### Features

- **Multiple LSP servers per language.** A language can now run a list of servers; the first answers symbol/reference/definition queries, all contribute diagnostics tagged by source. Lets you run a type checker (tsc, pyright) and a linter (eslint, ruff) in parallel and see findings from both on every save.
- **Sane multi-LSP defaults** in the embedded config:
  - `go`: `gopls`
  - `typescript`: `tsserver` + `eslint`
  - `python`: `pyright` + `ruff`
  - `rust`: `rust-analyzer`
  Set `auto_start: true` on the language to use them; install the LSP binaries first (`npm i -g typescript-language-server vscode-eslint-language-server`, `pip install pyright ruff`).
- **`ae lsp status`** shows one row per `(language, server)` pair: `lsp typescript tsserver ready pid=...`.

### Schema

- **Schema v4.** `diagnostics.source_server` column tracks which LSP published each diagnostic so multi-server setups don't trample. `lsp_status` rebuilt with `(language, server)` composite primary key. Existing v3 rows migrate cleanly: pre-existing `lsp_status` rows are preserved with `server = language` (single-server era).

### Backward compatibility

- Legacy single-server config form (`{"server": "gopls", "auto_start": true}`) from v0.3.0/v0.3.1 still works. When `servers` is empty, the legacy `server`/`args` fields are synthesized into a one-element list.

### Documentation

- README + SKILL.md (1.2.4): multi-LSP section, the four built-in defaults, the diag-line source label format.

## [v0.3.1] - 2026-04-30

### Fixes

- **Cross-platform build.** v0.3.0 release-build failed on `windows_amd64` because `internal/cli/lsp.go` used `syscall.Kill` and `syscall.SysProcAttr.Setsid`, both Unix-only. Split daemon-spawn into `lsp_unix.go` (Setsid) and `lsp_windows.go` (`CreationFlags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP`). `processAlive` likewise split: kill(0) on Unix, conservative on Windows.
- **`ae lsp stop`** now uses `os.Process.Signal(os.Interrupt)` instead of `syscall.Kill`. Same effect on Unix; works on Windows where `syscall.Kill` is undefined.

### IDE mode platform support

- **Native Windows 10 1803+ supported.** Unix sockets work on Windows since 1803 (April 2018) via Go's `net.Listen("unix", ...)`. The daemon spawns detached via `CreationFlags`. Older Windows: use WSL (the `linux_amd64`/`linux_arm64` binaries run there with full IDE support).
- macOS, Linux, WSL: unchanged.

### Documentation

- README and SKILL.md (1.2.3): IDE mode section gained concrete verb examples with sample output, daemon subcommand reference, and a "prefer LSP over grep for structural queries" worked example. Earlier prose-only treatment was undersold.

## [v0.3.0] - 2026-04-30

### Features

- **IDE mode (opt-in).** Set `ide.enabled: true` in `.agented/config.json` and `ae` exposes language-server-backed verbs through a daemon (`ae lsp`). Ships with `gopls` validated; `pyright`, `typescript-language-server`, and `rust-analyzer` are config-driven but not yet tested. Off by default — v0.2 behaviour is byte-identical when `ide.enabled` is false.
  - `ae symbols [path]` (`ae sy`) lists symbols in a file or workspace
  - `ae find --symbol <name>` (`-s`) finds where a symbol is defined
  - `ae find --references <symbol>` (`-R`) finds all use sites with usage classification (call/read/write/import/definition)
  - `ae find --definition <symbol> --at <file>:<line>:<col>` (`-D -A`) resolves a definition at a cursor position
  - Mutating verbs (`open`, `view`, `save`, `replace`, `insert`, `delete`, `move`, `apply`) emit `diag` lines from cached LSP diagnostics
  - `ae lsp [--background] [status] [stop] [logs]` manages the daemon; auto-start kicks in on first IDE-relevant verb when config has `ide.auto_start_daemon: true` (default)
  - Per-call severity filter via `--diagnostics`/`-G` (`errors|warnings|all|none`); `--no-diagnostics`/`-N` for suppression; `--no-auto-lsp` to skip auto-spawn
- **2.2× speedup on write-heavy scenarios.** Profile showed `autoSaveAfterEdit` was paying 2-3 fsyncs per edit inside the heavyweight `atomicfile.Editor.Write` (backup + readback verify). For autosave the SQLite store is the durable record, so the lite path `atomicfile.WriteSimple` (single temp+fsync+rename) is sufficient. Bench medians: 50 sequential replaces 750ms → 325ms; 1000 edits + reconstruction 15.4s → 6.8s; 30 undo+redo 380ms → 178ms. Read-only paths and one-shot installers (`ae skill install`, `ae permissions install`) unchanged.

### Documentation

- **SKILL.md 1.2.2.** New "IDE mode" section with severity/kind/usage vocabularies and a "prefer LSP over grep for structural queries when ide.enabled" rule. The first-touch rule now spells out that `ae open <new-path>` is the file-creation primitive (auto-creates an empty file; no `touch` or `--create` needed). Two new anti-patterns: don't infer file health from absence of `diag` lines; don't try to start `ae lsp` yourself unless authorized.
- **README** gained an "IDE mode (optional)" section documenting the opt-in flow.

### Schema

- **SQLite schema v3** adds `diagnostics` and `lsp_status` tables. Migration `003_lsp.sql`. Existing v1/v2 workspaces upgrade automatically on first open with the v0.3 binary; downgrading the binary requires manual schema rollback.

### Tests

- New regression tests for the three bugs caught while dogfooding v0.3 on the agented repo:
  - `TestDecodeRequestDoesNotBlockOnNonNotify`: simulates a live socket via `io.Pipe` (the buffer-based round-trip didn't catch this)
  - `TestReplaceDiagnosticsRejectsZeroFileID`: pins the FK guard
  - `TestReplaceDiagnosticsClearsAllRowsOnNilEditID`: pins the legacy-row cleanup behaviour
  - `TestEvalSymlinksFallbackResolvesTmp`: pins the macOS `/tmp` → `/private/tmp` invariant

## [v0.2.3] - 2026-04-29

### Features

- **`ae skill install` shows a version column** so it is clear which version is being installed (or has just been installed). `ae rules install` gained the same column. The "unchanged" status now means "on-disk content already matches the embedded version" — no longer ambiguous.
- **`--force` / `-f`** on `ae skill install`, `ae skill upgrade`, and `ae rules install`: re-write the file even when the on-disk content already matches the embedded copy. Useful for bit-for-bit re-installs after manual edits or to reset backups.
- **Skill version bumped to 1.1.0** and **rules section version bumped to v0.1.1** so re-running `ae skill install` / `ae rules install` after upgrading the binary actually flips status from "unchanged" to "updated". Previous releases shipped new SKILL.md content under the old version constants, leaving the binary unable to detect that disk and embedded content had diverged.

## [v0.2.2] - 2026-04-29

### Features

- **Auto-open in read verbs.** `ae search`, `ae view`, `ae find`, `ae diff`, `ae log`, `ae branches` and friends register the file in the workspace if it is not already open. Mirrors the auto-open already done by write verbs, so the canonical first-touch loop drops from `ae open + ae search` to just `ae search`.
- **Slice-syntax `--range`.** Negative indices and open ends now work everywhere `--range` is accepted: `1:10` first 10, `-10:` last 10, `5:-5` middle slice, `:20` shorthand for first 20, `-50:-20` lines 50-from-end through 20-from-end. Eliminates the need for `| head -N` / `| tail -N` after ae output.

### Documentation

- SKILL.md gained a "Round-trip economy" section: don't `view` before `replace`, don't `view` before `search`, don't `load` before reading, don't `status` just to refetch a state token, don't `open` more than once per file per session, don't pipe ae output through `head`/`tail`/`grep`, don't append `2>&1`. The canonical loop is `open → search/find → replace/insert/delete → repeat`.

### Infrastructure

- `release.yml` workflow pinned to `goreleaser: latest` and `mode: keep-existing` to avoid the asset-upload retry race that produced spurious "already_exists" errors on v0.2.1 (the artifacts uploaded successfully despite the workflow exit code).

## [v0.2.1] - 2026-04-29

### Features

- This release was tagged before some of the v0.2.2 work landed; in practice v0.2.1 contains an early version of `auto_load_on_drift` plus the same SKILL.md round-trip economy section. v0.2.2 adds slice-syntax ranges and the goreleaser fix.

## [v0.2.0] - 2026-04-29

### Features

- **Auto-save** by default on write verbs. `ae replace`/`insert`/`delete`/`move`/`extract` and the history verbs (`undo`/`redo`/`head`) atomically flush the new head to disk as part of the same call. Result includes `saved: true` to confirm. Config: `concurrency.auto_save = clean | off | force` (default `clean`). The five-call dance (`open + status + view + replace + save`) collapses to two for the common flow.
- **Auto-load on disk drift** by default. Before each write, ae stat-s the file. If `(mtime, size)` match the stamp recorded after the last save, no work; otherwise read + hash. On detected drift, the disk content is loaded as a new edit on the tree before the user's edit applies, so external changes are captured (recoverable via `ae undo` / `ae head`) instead of silently overwritten. Config: `concurrency.auto_load_on_drift` (default `true`). Env override: `AE_AUTO_LOAD_ON_DRIFT=false`.
- **`ae show <path>`** renders a Claude Code-style colored, syntax-highlighted diff (chroma-backed) for the most recent edit. Opt-in display command — write verbs return the lean tab format by default so agents pay no extra tokens.
- **Agent-centric `ae setup` wizard.** Detects which agents are present (claude / codex / cursor / openclaw), shows what's available, and asks per-agent which to install. `--yes` runs non-interactively for every detected agent. `--legacy` keeps the previous per-component flow.
- **Install gating symmetry.** `ae rules install` now skips undetected targets under `--target=all` (matching skill / permissions / mcp). Explicit `--target=<name>` still writes regardless. Cursor without a `.cursor/` dir and OpenClaw skip with explanatory reasons.
- **`ae rules show` rewritten.** Section body printed once at the top, followed by an aligned per-target status table. Previously duplicated the body across every target.
- **Tabwriter alignment** on `ae rules list`, `ae permissions list`, `ae mcp list`, and the `ae status -W` per-file table. Empty placeholders standardised to `—`.
- New env mappings: `AE_AUTO_SAVE`, `AE_AUTO_LOAD_ON_DRIFT`.

### Dependencies

- Added `github.com/alecthomas/chroma/v2` (and its transitive `github.com/dlclark/regexp2`) for the `ae show` command's syntax-highlighting backend. The README's "three deps" claim is now four.

## [v0.1.1] - 2026-04-29

### Bug fixes

- `atomicfile.Write` now preserves the original file mode (was hardcoding `0o644` and silently stripping the executable bit on shell scripts and similar). Default `0o644` is still used when creating a new file.
- `install.sh` archive-name case now matches goreleaser's lowercase output, and `mkdir -p` is run unconditionally on `AE_INSTALL_DIR`.
- CLI auto-workspace tests use a separate HOME from the project root to pass on Linux (where `/var → /private/var` symlink unmasking does not paper over path equality).

## [v0.1.0] - 2026-04-29

First public release.

### Features

- SQLite-backed editing workspace with persistent state across sessions
- Branching undo tree with `ae head --edit <id>` to jump to any prior state
- State token mechanism with full-content rejection payloads on conflicts
- `ae merge` for three-way merge with structured conflict resolution
- `ae apply` for atomic multi-edit batches. Three input formats (JSON-lines, shortform, longform) auto-detected from the first line
- `ae apply --multi-file` with `--expect-workspace` for cross-file atomic batches
- `ae move` for atomic moves within and across files. `--to-file` auto-creates the destination if absent
- `ae extract <src> --range S:E --to <dst>` cuts a range out of one file and writes it to another, the canonical refactor primitive. `--save` writes both files to disk in one call
- `ae find` for cross-file regex search with per-file and workspace state tokens
- `ae status -W` for the per-file workspace table. Output includes `cwd=<dir> workspace_dir=<dir>` so the agent always knows where ae is resolving paths
- `ae view --raw` emits content verbatim (no line-number prefix or state-token trailer) for piping to other tools
- `ae replace --pattern` for regex search-and-replace with capture groups
- Per-file annotations as cross-session memory
- Transactions with auto-rollback on idle
- Workspace discovery follows the file-path argument when absolute, so agents working from outside the project directory do not need `--workspace-dir`
- Auto-workspace creation at the project root on first use, controlled by `workspace.auto_create`
- `ae --version` flag (cobra root) and the existing `ae version` subcommand
- Parallel `ae open` calls handled via `busy_timeout=30s` and verified by 50-concurrent-opens test
- Skill installation across Claude Code, Codex, Cursor, OpenClaw, and the canonical `~/.agents/skills/` location
- Permission rule installation for Claude Code's `settings.local.json` (OpenClaw and Cursor handled via deliberate skip messages)
- MCP server (`ae serve`) exposing the same verbs over stdio
- `ae mcp install` writes the agented MCP-server entry into Claude Code, Claude Desktop, and Codex configs in one call

### Known limitations

- Codex permission schema not supported (manual setup required if needed beyond skill install)
- Cross-tool benchmark comparisons against built-in `Read`/`Edit`/`Write` not yet published. The in-process suite measures ae against itself