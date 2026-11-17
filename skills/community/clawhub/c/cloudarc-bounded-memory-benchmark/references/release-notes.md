# CloudArc Bounded-Memory Benchmark 1.4.2

**Release date:** 2026-09-12

## Highlights

- Removed the hard CPython 3.11 gate in `core/semantic.py`; a native semantic
  backend is now decided by a real import plus the published
  `cloudarc.native-semantic-v1` capability, so it works on 3.12 (or any CPython
  with a matching build).
- Failed imports are classified: a probe now reports which build tags exist next
  to the module and which one is required.
- The archive index records `semantic.status: ready` with `model_id` and
  `dimensions` when a native backend answers a descriptor probe; previously it
  always said `unavailable`, even while semantic search worked.
- New regression suite `tests/test_native_capability.py` (10 tests); product
  suite 152 -> 162 tests.

## Verification

- `runtime --json` on Python 3.12 with a cp312 ViBo build:
  `semantic_available: true`, `api_version: cloudarc.native-semantic-v1`.
- `search --mode semantic`: `mode_used: semantic`, no fallback, expected document
  ranked first.
- Without a core build the executor degrades to lemmatised matching and reports
  that engine honestly.

# CloudArc Bounded-Memory Benchmark 1.4.1

**Release date:** 2026-09-11

## Highlights (1.4.1)

- The Yandex Disk provider accepts tokens issued with only
  `cloud_api:disk.app_folder`: set `YANDEX_DISK_ROOT=app:/` and every request
  stays inside the application folder (the default root is `disk:/`). A 401/403
  now explains both scopes instead of guessing.
- Root scope and permission errors are covered by tests (29 provider tests).

## Highlights (1.4.0)

- **A restore rebuilds the tree, not just the contents.** Every manifest entry now
  carries `kind` (`file` / `symlink` / `dir`), `mode`, `mtime_ns`, and symlink
  entries carry `target`. Permission bits, timestamps, empty directories and
  links survive a round trip; before this the modes came back as `644` and
  symlinks were skipped.
- The input directory itself is an entry, so the root's mode and timestamp are
  restored too.
- Unpack is two-pass (files and directories, then links, then directory modes),
  and an archive that declares a symlink and anything below it is refused
  (`archive writes through a symlink`).
- Archive `format_version` is 2 when directories or links are present: a 1.3.x
  reader refuses such an archive (`unsupported VIBO format version`) instead of
  restoring a directory as an empty file and a link as a text file.
- New flags: `--no-metadata` (contents-only pack/unpack) and `--allow-system`
  (deliberate backups of `/var/log` and friends; protected names stay refused).
- `scripts/verify_restore.py` checks a restore entry by entry (kind, hash, mode,
  mtime) against the original tree.
- `pack --dry-run` leaves no staging directory behind; only `kind == "file"`
  entries enter the lexical search index.
- A file that is still being written (a live log) no longer aborts the archive:
  it is skipped and reported (`reason: changed`), or
  included as a torn snapshot with `--accept-changing` (`changing: true` in the
  manifest plus a warning). Verified on a live `/var/log`: 5.8 GB, 234 files,
  21.8 s, 32 MB peak RSS.
- The Yandex Disk provider is implemented (REST API v1, OAuth token from the
  environment or a file, streamed uploads, size-verified downloads, HTTP Range
  reads for remote `open`/`fetch`); Google Drive stays a fail-closed placeholder.
- Product suite: 85 -> 120 tests. Review round (two independent reviewers) found
  and closed seven defects, each with a regression test.

## Highlights (1.3.0)

**Release date:** 2026-09-11

- zstd for text (optional package, baked into binary builds): the CI text profile
  archive drops 114973 -> 18461 KiB (6.2x), pack 22.2 -> 26.6 MiB/s. A missing
  zstandard is reported as a warning instead of a silent deflate fallback.
- Process-pool packing by file (`--workers N`), chosen by measurement: used only
  above 16 MiB total and >= 2 files (2.33x at 16.4 MiB, 3.55x at 4x32 MiB,
  3.69x at 8x24 MiB); below that sequential wins (0.76x on 50 tiny files).
  Peak tree RSS with the pool 45 -> 155 MiB (inside the 256 MiB SLO), warned
  when used, fail-safe fallback if the pool cannot start.
- Files vanishing mid-run are reported as `skipped: vanished`.
- Adaptive buffer measured and rejected (8 MiB is slower than 1 MiB).
- Product suite: 76 -> 83 tests.

## Highlights (1.2.3)

- Files that vanish mid-run (SQLite `-shm`/`-wal` siblings, rotating logs) are now
  reported as `skipped: vanished` instead of aborting the archive. Found by
  backing up a live 2.2 GB data set: the pack died on `/root/.hermes/kanban.db-shm`.
- Skipped reasons: `protected`, `system`, `symlink`, `vanished`.
- Product suite: 76 -> 78 tests.

## Highlights (1.2.2)

- Version drift fixed: `cloudarc.py version` reported `0.1.0-mvp` while
  `pyproject.toml` said 1.2.1. `core/version.py` is now the single source of
  truth and `tests/test_version.py` fails the build on any mismatch.
- Product suite: 71 -> 76 tests.

## Highlights (1.2.1)

- Dogfooding a 556-file heterogeneous tree exposed three defects, all fixed in the
  product: paths containing a `bin`/`var`/`etc` component were rejected anywhere
  (any Node or Python CLI project lost its `bin/` directory); skipped files were
  never reported (556 files in, 356 out, no signal); one symlink inside a
  directory aborted the whole walk.
- `pack --no-index` added: 169 MiB -> 29.7 MiB peak RSS on the same 64.1 MiB text
  tree, archive and restore unchanged, `search.index_built = false`.
- `pack`/`analyze` return `skipped`, `skipped_count`, `skipped_by_reason`; the CLI
  warns on stderr about files that did not enter the archive.
- README and `docs/LARGE_PACKAGE_SLO.md` now carry the measured heterogeneous-tree
  RSS numbers next to the streaming 256 MiB SLO.
- Product test suite: 59 -> 71 tests (`tests/test_safety_and_skips.py`),
  `tests/check_suite.py` inventory guard OK, helper smoke PASS.

## Highlights (1.2.0)

- Helper `doctor`, `selfcheck` and `badge` commands; `[zstd]`/`[semantic]` extras;
  lazy `zstandard` import.

# CloudArc Bounded-Memory Benchmark 1.1.0

**Release date:** 2026-09-10

## Highlights

- Added `scripts/cloudarc_benchmark.py` with three safe entry points:
  `smoke`, `manual`, and `check-telemetry`.
- Added explicit `--yes` protection for the manual 1/5/10 GiB profile.
- Added strict checks for positive RSS and non-zero bytes when telemetry
  reports successful range or sidecar reads.
- Added post-run validation of JSON schema/status, multi-file cardinality, and
  matching Markdown `PASS` reports before the helper exits successfully.
- Updated the pull request CI workflow to invoke the helper and upload JSON and
  Markdown smoke artifacts.
- Kept the large manual workflow separate from normal CI and preserved the
  single-file and multi-file SLO boundaries.

## Verification

- Skill validation: passed.
- CloudArc test suite: 51/51 passed.
- Helper smoke profile: passed on the reference Windows environment.
- Installed profile copy verified with the helper's range and sidecar telemetry
  checks.

## Upgrade note

Replace older copies of `cloudarc-bounded-memory-benchmark` with this package.
The skill does not enable cloud credentials or activate the native ViBo
backend.
