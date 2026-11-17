# Changelog

版本方案:**SemVer 2.0.0**(semver.org)——MAJOR=不兼容大改 / MINOR=向后兼容新功能 / PATCH=向后兼容修 bug;格式遵循 **Keep a Changelog**(keepachangelog.com):每版一节最新在上,日期 ISO 8601,改动按六类 Added/Changed/Deprecated/Removed/Fixed/Security。Unreleased 随做随记,发布时改版本号+日期,顶部重置空 Unreleased。

## [Unreleased]

## [0.99.0] - 2026-10-22

### Added
- **The design, published.** `references/memory-system.md` — the method behind
  the scripts, written so it can be copied into any agent setup with any file
  layout: the four layers (raw / working / reference / always-on) and the rule
  that one fact has exactly one home; the two orthogonal questions that decide
  where a memory lives (whose it is · which way time points); entry points
  (each event gets one landing place *and* one check that it happened);
  the budget rules; and an explicit "what this does not solve".
- **`scripts/memory_ledger.py`** — the always-read layer as a reviewable
  budget. One row per entry with `why`, `review_by`, `max_age_days` and
  `action_on_expiry`. `--check` reports missing files, incomplete rows,
  overdue reviews, stale rows and budget overruns, and exits non-zero so it
  can be wired into a hook. Hard byte budget 30000, target waterline 25000.
  Writes only its own `.changsheng/ledger.json`; never edits your memory files.
- **`scripts/recall.py`** — "why did we decide this?" across four surfaces
  (todos, journal, notes, archive), printing file and line. Every surface is
  reported even when it had zero hits, and "nothing could be searched" exits 3
  so it is never confused with "not found". Read-only, pure stdlib.

### Changed
- SKILL.md / README gained a "What kind of memory is this?" section (the
  whose/when table), a ledger section and a recall section; the key-command
  line, the file list, the security notes and the roadmap mention the two new
  scripts.
- Version bumped to 0.99.0 (SKILL.md frontmatter, `version`, README badge).
- **README marketing copy refreshed** (reviewed copy, shipped as reviewed):
  the hero line now leads with "your agent's memory, decoupled from the model";
  a new **Why is this free?** section states why the method is MIT and where the
  paid side actually is; a new **v0.99 — memory that never gets lost, three ways**
  section describes the three new pieces in user terms; the closing section is
  now **Going further** (full system + the sibling Mode Switch Kit).
- **The 1.0 bar is written down.** The roadmap now says exactly what 1.0 means
  — the write side closes the loop: capture without writing things down by hand,
  the ledger's expiry actions actually running, cross-machine recall over the
  archive, and the recovery-cost measurement re-run on the 1.0 build. Until
  those four hold, the version stays 0.99 (0.99 is a complete read-side skill,
  not a placeholder).

### Migration
- No behaviour change: same recovery flow, same commands, same config keys,
  same handover protocol. The two new scripts are optional — install and use
  them when you want a budget on your always-read layer, or want to look up
  the reason behind an old decision. Nothing to do when upgrading from 0.6.0.

## [0.6.0] - 2026-09-19

### Added
- **Dreaming — the write side.** Recovery is the read side; dreaming is the write side. On each
  pass the agent tidies what it has stored, with five moves that each carry a checkable
  criterion: merge duplicates, split look-alikes, retire stale entries, re-home new entries,
  escalate doubts. Rhythm: once per 3-day cycle. Output: a one-page dream report.
  The skill ships discipline and criteria only — it does not create jobs or scripts of its own;
  scheduling stays with the host's own timer.
- **Chinese reachability line.** Every H2 section now opens with a one-line Chinese summary
  (`**中文**: …`), so a Chinese reader (or a Chinese-speaking agent) can orient before the
  English body. The English body itself is unchanged.

### Changed
- Frontmatter gains `description_zh` / `description_en` (required by the WorkBuddy skill page).
- README badge and the roadmap section synced to 0.6.0.

### Migration
- No behaviour change: same recovery flow, same commands, same config keys, same handover
  protocol. Nothing to do when upgrading from 0.5.0.

## [0.5.0] - 2026-09-15

### Changed
- **Renamed: Evermind -> ChangSheng.** The published name sat too close to unrelated
  products already using it in this same space (an AI-agent-memory company, plus a
  trademarked name), which risked confusion with products we have nothing to do with.
  Everything user-visible now reads `ChangSheng`:
  - package / skill identifier: `evermind-ai-agent-memory` -> `changsheng-agent-memory`
  - display name: `Evermind` -> `ChangSheng`
  - runtime directory: `.evermind/` -> `.changsheng/` (`discovery.json`, `rules.json`, `handover.md`)
- Publisher attribution is unchanged: `TXJ · 天玄镜 (Tianxuanjing)`.

### Migration
- No behaviour change: same recovery flow, same commands, same config keys. Only names differ.
- Coming from 0.4.x: rename any existing `.evermind/` directory to `.changsheng/`, or just
  delete it — discovery runs again on the next use. If `rule_gate.py` is wired into a hook,
  update the path in that hook command.

## [0.4.4] - 2026-09-14

### Added
- `assets/agents-snippet.md` — a paste-in block for your project's instruction file. Hermes, OpenClaw and DeepSeek Harness all load that file at session start, so recovery then runs by itself: no code, no hooks, no config.
- README: "Make it automatic (3 lines, 3 platforms)" section + a per-platform table of which instruction file is loaded when.

### Changed
- README / platform table: the automatic route is now stated first; wiring a session-reset hook is no longer presented as the only way to automate. The manual route is unchanged and still supported — say "recover memory" (or 接着上次) at session start.

### Fixed
- `scripts/memory_index.py`: the change index **and its state file** are now written
  atomically (temp file + `os.replace`). An interrupted or failed run can no longer
  leave a half-written `memory_index.md` / `memory_index_state.json` behind — the
  previous good copy stays intact (parity with OpenClaw `memory-builtin` full-rebuild
  semantics). Verified: `--demo` E-block (first write / overwrite / failed write keeps
  the old file / no `.mma_tmp_` leak).

## [0.4.3] - 2026-09-12

### Changed
- Publisher attribution corrected: `author` read `Evermind`; it is now `TXJ · 天玄镜 (Tianxuanjing)`, matching the companion skill `mode-switch-machine-stack`. README footer and the ClawHub storefront title (`--name`) updated to match. No behaviour change.
- README: added a cross-link section to the companion skill, so the two published halves of the setup point at each other.

## [0.4.2] - 2026-09-11

### Added
- **User-tunable nudge thresholds (C30)**: context-switch nudges now read `nudge_thresholds` from `config.yaml` (default `[30, 50, 70]`) — users who want more headroom set e.g. `[35, 55, 75]`. SKILL.md documents the tuning knob; FAQ added to README (why nudged / how to change / handover ready / privacy).

### Changed
- **Storefront copy rewritten for scenario matching**: the ClawHub `description` (storefront summary) now opens with the capability + measured numbers and then lists 6 explicit "Use when" trigger scenarios, so an agent can match its current situation instead of reading ad copy; a Chinese trigger line (中文触发) is added for the same reason. Consumers stay separate — README top keeps the human-facing capability + numbers narrative, SKILL.md first screen carries the condensed use-when / key commands / cost. GitHub repo description cleared of the retired projection figure (measured ~70% / 55-75% only).

## [0.4.1] - 2026-09-08

### Changed
- **Single-source script refactor (0.4.1 pending)**: `scripts/memory_index.py` build/summary templates are now language-driven via a built-in zh/en word table — the published default stays English (`lang` defaults to en when absent), so external behaviour is unchanged from 0.4.0. The top-level `lang: en|zh` config key selects the display language, and the maintainers' private/internal layout (agent names, local paths, Chinese descriptors) moved entirely into their own private config file. Published package carries zero private content.

## [0.4.0] - 2026-09-08

### Added
- **Rules alignment (alignment layer)**: recovery now extracts the imperative rules from the user's rules files and restates them explicitly in the recovery report — the user sees that the do's and don'ts they set are loaded every session ("it remembered what I told it"). Honest "no hard rules found" when the rules file has none.
- **Action-time guardrail (enforcement layer)**: optional `scripts/rule_gate.py` reads `.evermind/rules.json` (written by the agent at recovery: id/text/keywords per rule) and blocks violating actions — `--check "description"` for scripts, or Claude Code PreToolUse JSON on stdin for hook wiring (example in SKILL.md). Exit 2 on a hit; pure stdlib; fails open (no rules file → pass); writes nothing.
- **Handover protocol**: say "handover" (交接/收尾) at any task break → agent writes `.evermind/handover.md` from `assets/handover-template.md` (✅ done · 📌 leftover · 🔗 pointers · ➡️ next). Recovery reads it if present as the fast pointer; authority stays with todos/journal.
- **Nudge upgrade (ready-signal hard rule)**: context checks now happen at every visible reading (usage jumps between turns — 29% one turn, 49% the next), with pre-nudge bands approaching each threshold (25–30 / 45–50 / 65–70) so a jump never passes in silence; and **any** nudge — pre or full — goes out only after `.evermind/handover.md` has been refreshed, so a user who switches right after a nudge loses nothing.

### Changed
- Storefront/SKILL.md copy adds "rule memory" and "one-line handover" to the value story; product positioning unchanged (memory first — rules are memory of the most important kind).

## [0.3.0] - 2026-09-04

### Added
- **Environment discovery** (fixes the "assumes our file layout" flaw): `memory_index.py --discover`/`--list` locate the user's memory carriers by community conventions (rules/identity/todos/journal) → `.evermind/discovery.json`. Fresh installs work with zero config.
- **Semantic roles**: config `roles:` maps rules/identity/todos/journal/profile → real files (file or directory; directory resolves to newest `YYYY-MM-DD.*`); extras stay L3/L2.
- **Context gauge + threshold nudges**: per-platform context-usage query table (Hermes `/status`, Claude Code `/context`, …); honest reporting — never invent a percentage; 30/50/70% switch nudges.
- `--mode internal|auto|manual` (internal = fixed-layout for the maintainers' own vault; published/community default = auto).

### Changed
- Recovery is honest about sources: reports which files each role resolved to, and **lists empty roles instead of claiming a full recovery** (fixes silent false-recovery).
- Discovery cache is stat-validated before reuse — a moved/deleted source triggers re-discovery (never reuse stale paths).
- Legacy 0.2.x config (`must_read`/`tracked_files`) migrates automatically, preserving L3/L2 semantics (never upgrades L2 to per-session reads).
- Storefront description updated to the finalized token-saving narrative — "the token-saving switch… save tokens, save money, save worry", with the measured 44K→12K (~70%) recovery comparison (author-approved copy; replaces the earlier benefit-first wording).
- Security wording updated for the discovery layer (name-only scan, no content reads); README/config/SKILL.md synchronized; root `version` file corrected (was stale 0.1.1).

### Fixed
- config.example.yaml key mismatches (`note:` vs code's `desc:`; `index_output` vs `output_index`) resolved by full rewrite.
- yaml-less fallback silently dropped legacy 0.2.x configs (0-file empty index, rc0, no stderr) — fallback no longer pre-seeds empty extras (which made migration never run), legacy `must_read`/`tracked_files` migrate for real (7eddf32).
- Fallback parser could not parse the shipped nested `roles:` shape — no-yaml + manual roles produced a silent empty index while the YAML interpreter indexed 2+ files; fallback now parses nested roles (inline `[a,b]`, block list, empty subkey) and errors out loudly (rc3 + stderr) on declared-but-empty roles instead of writing a silent empty index (6f03ea6).
- Fallback kept literal YAML quotes on scalar values (`"CLAUDE.md"` → path with quotes → `read failed` rows with content dropped while stdout still said OK rc0) — diverging from the YAML interpreter for the same config. `_unquote()` now strips one matching quote pair on every fallback value path (roles inline/block items, flat `role_*` items, extra dict path/name/desc, mode, scalar keys); quoted configs parse identically under both interpreters (890a35e).

## [0.2.2] - 2026-09-04

### Changed
- Positioning upgrade (user insight): headline benefit reframed as **free context switches** — cheap reliable recovery means users can switch sessions at any task boundary without losing state, instead of stretching one context until it breaks. README adds a "Why this changes your workflow" section; storefront description now leads with cross-session restore + switch-anytime + ~70% fewer tokens.
- README version badge corrected to 0.2.2 (was stale 0.1.1 through 0.2.0/0.2.1).

## [0.2.1] - 2026-09-04

### Changed
- Storefront description rewritten benefit-first: "Never re-explain yourself to your AI..." (value hook → quantified savings → platform list), replacing the mechanism-first wording — clearer what users get in the first 3 seconds.

## [0.2.0] - 2026-09-04

### Added
- L2 read policy split: index entries whose one-line description already answers the need (role cards / member summaries) now require only the **index summary line**, not a full-file read — full reads reserved for substantive docs.
- Single-source-of-truth note: index descriptions are display rows; authoritative role summaries live in the roles table (config/discovery); agents maintaining their own rules/identity files must log the change and refresh the table.

### Changed
- SKILL.md Usage step 2 & How-it-works L2 row updated to the split policy (previously "changed → read in full").
- Honest-numbers wording aligned to the measured 2026-09-04 range (~55-75% cumulative for host-injected identity; retired the 85%/6.5K projection phrasing).
- Install references updated to the final slug `evermind-agent-memory` (old working titles removed).

### Fixed
- (none)

## [0.1.1] - 2026-09-03

### Changed
- Renamed to **Evermind** (repo `evermind`; brand prefix dropped, low-key credit in README footer).
- README rewritten in English with per-platform install guide (Hermes / ClawHub / Claude Code / Cursor / generic SKILL.md agents).
- SKILL.md fully English; platform-support section added; frontmatter description extended (85%+ host-injection case).
- config.example.yaml comments and sample names in English.
- Script user-facing output (docstring, CLI messages, demo) localized to English.
- Chinese docs kept out of the published tree (archived locally).

### Added
- LICENSE file added (MIT-0).

## [0.1.0] - 2026-09-03

### Added
- Tiered progressive memory recovery (SKILL.md): L3 must-read / L2 conditional reads driven by a change index / L1 on-demand.
- Companion script `scripts/memory_index.py`: config-driven change-index generation, pure stdlib, hash-idempotent with a 24h freshness window.
- `config.example.yaml` template; README (pitch / how-it-works / install / safety / roadmap).
- Dual-compatible frontmatter (standard fields + Hermes `metadata.hermes`).
