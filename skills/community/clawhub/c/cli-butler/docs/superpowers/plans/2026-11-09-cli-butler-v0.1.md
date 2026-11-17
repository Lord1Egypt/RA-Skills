# cli-butler v0.1 Implementation & Publish Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (inline, unattended) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement all six features (F1→F5→F6→F3→F4→F2), pass acceptance on real machine + CI, publish to GitHub as `kelegele/cli-butler` public repo.

**Architecture:** bash library split — `lib/common.sh` (ownership resolution, journal, output helpers) + `lib/channels.sh` (per-channel enumerate/route/desc). Six `bin/*.sh` entrypoints orchestrate. Tests drive real code paths via PATH-injected fake channel commands (fixtures), never env-var plumbing.

**Tech Stack:** POSIX bash, awk, zero third-party deps. CI: shellcheck + smoke on GitHub Actions.

**Spec:** `docs/REQUIREMENTS.md` (source of truth) + `docs/provenance.md` (channel model) + `docs/design.md` (conventions). Plan argues from these; executors read both plan and spec.

## Global Constraints (verbatim from spec)

- POSIX bash，零第三方依赖（无 jq 时降级纯文本输出）
- 渠道探测逐项容错：单渠道命令缺失/超时不阻塞整体
- F1 desc 只做本地查询，**禁止逐包联网**
- system（系统自带）项一律拒绝卸载；渠道管理的二进制**永不直接 `rm`**
- 卸载、覆盖安装一律先 dry-run，`--yes` 或交互确认才执行
- launchd 停用须挪 plist；app 内嵌软链只备份挪链（`.bak`）
- CLI 输出英文（开源规范）；提交信息英文祈使句，一个功能一个 commit
- 每次改动后跑 `tests/run.sh`；shellcheck 本地装了就跑，CI 必跑
- journal 必经 `BUTLER_JOURNAL_DIR` 重定向，测试不得写真实 journal

## Locked Interfaces

**CLI surface (all exit 0 success / non-zero + stderr on error):**
```
bin/list.sh      [--kv] [--channel <id>]
bin/refchain.sh  <cli>
bin/cap.sh       <cli>
bin/install.sh   <cli> [--channel <id>] [--yes]
bin/uninstall.sh <cli> [--yes]
bin/manage.sh    info <cli> | outdated | upgrade <cli> [--yes]
```

**lib/common.sh adds:**
- `realpath_safe <path>` → absolute resolved path (fallback: input, resolved via cd+pwd -P; macOS has no reliable `readlink -f`)
- `is_darwin` → exit 0/1 (`uname -s`, overridable `BUTLER_OS_OVERRIDE`)
- `is_system_path <abs>` → exit 0/1 (darwin: `/usr/bin /bin /sbin /usr/sbin`; overridable `BUTLER_SYSTEM_PREFIXES` for tests)
- `resolve_owner <name> <abs>` → stdout `<channel>|<category>`; order per provenance.md §归属判定; channel ∈ brew/npm/pnpm/pipx/uv/cargo/gem/apt/manual/system, category ∈ managed/manual/untracked/system
- `kv_field <k> <v>` → sanitized `k=v` + TAB (strip TAB/CR/LF from v)
- `du_size <path>` → bytes or `-`
- `hist_last_used <name>` → epoch or empty (zsh `: <epoch>:0;cmd` parse; fallback bash hist file mtime, flagged unreliable)

**lib/channels.sh (new):**
- `channel_available <id>` → exit 0/1
- `channel_enumerate <id>` → `name<TAB>version` lines (brew/npm/pnpm/pipx/uv/cargo/gem/apt parsers; fixture-driven in tests via PATH fakes)
- `channel_prefixes <id>` → space-separated install-prefix dirs (npm/pnpm/uv/pipx/cargo queried live + cached in run-global; brew/intel+arm; gem: none, query-routed)
- `channel_desc <id> <name> <path>` → one-line description or "" (brew desc / package.json / dpkg Summary / gem list -d; no network)
- `channel_upgrade_cmd|channel_uninstall_cmd|channel_install_cmd <id> <name>` → full command string (routing used by F2/F3/F4)

**--kv machine format (locked):** one line per CLI, TAB-separated fixed field order:
`name=…	version=…	channel=…	category=…	path=…	size=…	desc=…`

**Human format:** grouped sections `== <channel> (<n>) — <one-line channel blurb> ==` then `NAME  VERSION  SIZE  DESC` rows. Group order: managed channels in provenance order, then system (blurb: system-bundled, SIP-protected, not uninstallable), manual (journaled), untracked.

**Test harness:** `tests/fixtures/bin/` holds fake channel executables (brew, npm, pnpm, pipx, uv, cargo, gem, dpkg-query, whatis, uname, sleep-based slow probe) + `tests/fixtures/data/` static outputs. `tests/lib.sh` provides `t_ok/t_eq/t_contains` assert helpers and counts. Fakes resolve through PATH injection — no env-var plumbing beyond `BUTLER_JOURNAL_DIR` / `BUTLER_SYSTEM_PREFIXES` / `BUTLER_OS_OVERRIDE`.

## Review Focus

1. **desc with TAB/newline breaks --kv** → `kv_field` must sanitize; test: fixture desc containing spaces+TAB.
2. **macOS `readlink -f` missing** → `realpath_safe` portable loop; test: 3-deep symlink chain in fixture dir.
3. **One hanging channel blocks list** → probe timeout; test: fake npm sleeps 30s, full list must finish <10s.
4. **Linux system false-positive** → `is_system_path` gated on darwin; test: `BUTLER_OS_OVERRIDE=Linux` + /usr/bin-like path yields untracked (then distro-channel via query).
5. **uninstall of system item proceeds** → refuse before any dry-run; test: system-prefixed fake binary → exit≠0, stderr states reason, no rm invoked.

---

### Task 0: Preflight + task record

**Files:** Create `tasks/2026-11-09-impl-publish.md`; commit task file.

- [ ] Name dedup: `npm view cli-butler` (expect 404), `gh search repos cli-butler`, `webget https://skills.sh` search. If npm package or skills.sh entry `cli-butler` exists → switch all naming to `toolbutler`, record decision in REQUIREMENTS §名字 + HANDOVER. GitHub name collision alone → also prefer toolbutler (discoverability).
- [ ] `brew install shellcheck` if absent (skip gracefully if brew missing/slow; CI covers it).
- [ ] Write task record: owner=this session, goal, plan path, status=in-progress.
- [ ] `tests/run.sh` green; commit `chore: add implementation plan and task record`.

### Task 1: Test harness

**Files:** Create `tests/lib.sh`, `tests/fixtures/bin/*`, `tests/run.sh` (modify to source lib.sh).

- [ ] Write assert helpers + fake channel commands (static outputs in fixtures/data: brew formula+cask lists, npm ls + prefix, pipx, uv, cargo, gem, dpkg-query, whatis, uname=Darwin).
- [ ] Run: `tests/run.sh` — all existing smoke still green, new helpers self-test passes.
- [ ] Commit `test: fixture-driven harness with fake channel commands`.

### Task 2: common.sh primitives

**Files:** Modify `lib/common.sh`; Test: `tests/test_common.sh` (sourced by run.sh).

- [ ] Failing tests: realpath_safe 3-deep chain; is_system_path darwin yes / Linux no (BUTLER_OS_OVERRIDE); resolve_owner precedence (prefix > system > query > journal > untracked) with fixture PATH + journal; kv_field sanitization; du_size on fixture dir; hist_last_used on fixture zsh_history.
- [ ] Run → verify FAIL; implement; Run → PASS; full `tests/run.sh` green.
- [ ] Commit `feat: ownership resolution and portable path primitives`.

### Task 3: channels.sh enumerators

**Files:** Create `lib/channels.sh`; Test: `tests/test_channels.sh`.

- [ ] Failing tests per channel: enumerate parses fixture outputs into `name<TAB>version`; channel_available false when command absent (PATH without fake); channel_desc from brew/package.json/dpkg Summary/whatis fallback; route cmd builders exact strings (e.g. `brew uninstall --cask <name>` for casks).
- [ ] Run → FAIL; implement; Run → PASS; full suite green; shellcheck if present.
- [ ] Commit `feat: per-channel enumerate, describe, and route builders`.

### Task 4: F1 list

**Files:** Rewrite `bin/list.sh`; Test: `tests/test_list.sh`.

- [ ] Failing tests: PATH scan + channel enumeration merged, deduped by basename; system group from system prefixes; untracked detection (fixture bin not owned by anything); `--kv` exact field order + sanitization; `--channel brew` filters; slow-channel fake doesn't block (wall clock <10s); exit 0 with empty channel set.
- [ ] Run → FAIL; implement; Run → PASS.
- [ ] Commit `feat: grouped CLI inventory with descriptions (F1)`.

### Task 5: F1 real-machine validation

**Files:** fixes as needed in `lib/*.sh`; no new files.

- [ ] Run real `bin/list.sh` and `bin/list.sh --kv`; verify against known truth: docker (OrbStack symlink → brew cask orbstack), node/nvm chain, dsh residue (`.plist.off` → untracked/absent), homebrew packages, `/usr/bin` system group non-uninstallable blurb, user's pipx/uv/cargo/gem if present.
- [ ] Discrepancies → fix → re-run until list matches reality; append evidence to task record.
- [ ] Commit fixes `fix: list against real machine findings` (or skip commit if none needed).

### Task 6: F5 refchain

**Files:** Rewrite `bin/refchain.sh`; Test: `tests/test_refchain.sh`.

- [ ] Failing tests: five layers on fixture symlink chain (layer1 realpath+chain, layer2 owner line, layer3 PATH line from fixture shell-config dir overridable via `BUTLER_SHELL_CONFIGS`, layer4 fixture launchd dir via `BUTLER_LAUNCHD_DIRS`, layer5 grep hits in fixture config files); last-used from fixture zsh_history epoch; bash-fallback mtime path flagged.
- [ ] Run → FAIL; implement; Run → PASS.
- [ ] Real-machine: `/usr/local/bin/docker` chain (OrbStack), dsh `.plist.off` detection; evidence to task record.
- [ ] Commit `feat: five-layer reference chain with last-used (F5)`.

### Task 7: F6 cap

**Files:** Rewrite `bin/cap.sh`; Test: `tests/test_cap.sh`.

- [ ] Failing tests: fake cli with `--help` → usage line + top-level subcommands extracted; `-h` fallback when `--help` exits≠0; unparseable help → first paragraph raw; timeout kill; missing cli → exit≠0 stderr.
- [ ] Run → FAIL; implement; Run → PASS.
- [ ] Commit `feat: capability enumeration from help output (F6)`.

### Task 8: F3 install

**Files:** Rewrite `bin/install.sh`; Test: `tests/test_install.sh`.

- [ ] Failing tests: routing table (node tool→npm, system tool→brew/apt by OS) with fake channels — asserts constructed command, no execution without --yes… **decision:** new installs execute after printing plan unless `--dry-run`; overwrite (already installed) always dry-run first; `--channel` overrides; journal_add written on success (fixture journal dir); npm prefix check warns when `npm prefix -g` mismatch vs PATH npm; proxy: if `webget` present, export its proxy-url as HTTPS_PROXY for network steps, else note proxy vars.
- [ ] Run → FAIL; implement; Run → PASS.
- [ ] Real-machine: `bin/install.sh cowsay --channel brew --yes` succeeds; verify journal row + `brew list cowsay`.
- [ ] Commit `feat: channel-routed install with journal writeback (F3)`.

### Task 9: F4 uninstall

**Files:** Rewrite `bin/uninstall.sh`; Test: `tests/test_uninstall.sh`.

- [ ] Failing tests: system item → refuse, exit≠0, reason on stderr, no command runs; channel item → dry-run plan first, `--yes` executes route command (fake channel records invocation to fixture log); manual journaled item → refchain summary + dry-run → confirm → journal_del; untracked → require refchain pass, refuse without it; no `rm` of channel-owned paths anywhere in flow (grep guard test).
- [ ] Run → FAIL; implement; Run → PASS.
- [ ] Real-machine: dry-run uninstall of `cowsay` shows plan; `--yes` removes via brew; journal row gone. Manual flow on self-created fixture binary in temp dir (safe, not user data).
- [ ] Commit `feat: safe uninstall with dry-run and system refusal (F4)`.

### Task 10: F2 manage

**Files:** Rewrite `bin/manage.sh`; Test: `tests/test_manage.sh`.

- [ ] Failing tests: info prints path/chain/owner/size/launchd refs (reuses refchain internals); outdated lists per available channel; upgrade builds route cmd, dry-run default, `--yes` executes (fake channel log); unknown channel command → explicit error, no guessing.
- [ ] Run → FAIL; implement; Run → PASS. Real: `manage.sh info git`, `manage.sh outdated --channel brew` read-only.
- [ ] Commit `feat: per-CLI info, outdated, upgrade routing (F2)`.

### Task 11: Acceptance + hardening

**Files:** README examples, SKILL.md status, version bump.

- [ ] Walk REQUIREMENTS §验收标准 item by item; record pass evidence in task record.
- [ ] shellcheck all bin/*.sh lib/*.sh (local if installed; else verify CI does) → zero warnings.
- [ ] Full `tests/run.sh`; README usage examples refreshed with real output; SKILL.md status → stable; `BUTLER_VERSION=0.1.0`.
- [ ] Commit `chore: v0.1.0 acceptance pass and docs refresh`.

### Task 12: Publish

**Files:** none new (remote only).

- [ ] Re-run name dedup (state may have changed) → final name.
- [ ] `gh repo create kelegele/<name> --public --source . --push` (description + topics: cli, agent-skills, package-manager, homebrew, provenance).
- [ ] `gh run watch` until CI green (shellcheck + smoke).
- [ ] Tag `v0.1.0` + `gh release create v0.1.0` with notes.
- [ ] Verify `npx skills add kelegele/<name>` resolution path documented in README matches repo layout (skills.sh compatible: SKILL.md at root).
- [ ] HANDOVER.md final sync (published URL, version, evidence links); final report to user.

## Rollback / Failure Posture

- Any task failing after 3 fix attempts → stop, record blocker in task record + HANDOVER, report to user (unattended halt criterion).
- Publish step is the only external action; repo creation failure → report, do not retry with force.
- Name fallback (toolbutler) is pre-authorized by user HANDOVER §1.
