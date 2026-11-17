# Evidence helper contracts

Python 3.11+ is required on macOS, Linux and Windows 10/11. The Python entry
points run directly in PowerShell 5.1 or 7; Bash is only needed for the legacy
.sh wrappers and explicitly trusted Bash programs. The commands below use two
documentation variables: CODESIFT_SKILL, this skill's absolute directory, and
REVIEW_ROOT, the selected package. No helper installs tools. Pass --root
explicitly, or run from the reviewed package root.

The .sh entry points run "${CODESIFT_PYTHON:-python3}". Set CODESIFT_PYTHON when
the default python3 is older, as macOS /usr/bin/python3 (3.9) is, and run the .py
helpers with the same interpreter. An older interpreter exits 2 with a message
naming its version and path instead of a traceback. Direct Python invocations
use the selected interpreter, with -B to avoid bytecode artifacts.

The review-and-approval workflow in SKILL.md governs how the agent uses these
helpers. Before plan approval, use read-only helpers or isolated reproductions;
do not let a project command write into the reviewed working tree.

```bash
python3 -B "$CODESIFT_SKILL/scripts/lib/source_checks.py" facts --root "$REVIEW_ROOT" --output json
python3 -B "$CODESIFT_SKILL/scripts/lib/source_checks.py" duplicates --root "$REVIEW_ROOT" --lang python --json
python3 -B "$CODESIFT_SKILL/scripts/dependency_audit.py" --root "$REVIEW_ROOT" --json
python3 -B "$CODESIFT_SKILL/scripts/verify_packages.py" --root "$REVIEW_ROOT" --offline --json
python3 -B "$CODESIFT_SKILL/scripts/lib/check_runner.py" correctness --root "$REVIEW_ROOT" --lang python --json
```

In Windows PowerShell, use the same Python files and options:

```powershell
$CodeSiftPath = Join-Path $HOME '.agents\skills\codesift'
$ReviewRoot = 'C:\my project'
py -3 -B (Join-Path $CodeSiftPath 'scripts\lib\source_checks.py') facts --root $ReviewRoot --output json
py -3 -B (Join-Path $CodeSiftPath 'scripts\lib\check_runner.py') correctness --root $ReviewRoot --lang python --json
py -3 -B (Join-Path $CodeSiftPath 'scripts\smoke_test.py')
```

--lang accepts auto, c, cpp, rust, python, javascript, go and java. Auto reports
mixed projects rather than silently choosing one root manifest. For execution or
dependency inspection, select a package and language. Native C/C++ sources alone
are treated as cpp when C++ sources exist.

## Results and exit codes

| Exit | Meaning |
|---|---|
| 0 | Requested operation completed; inspect status and evidence scope |
| 1 | Observed command/test failure, explicit dependency cap exceeded, benchmark output mismatch, or name absent from the default public registry |
| 2 | Invalid invocation, missing prerequisite or old interpreter, incomplete/unknown evidence, timeout, parse/scan/network error, or a name missing only from a mirror |
| 130 | Ctrl+C cancellation; command cleanup is attempted before the report is emitted |

Test success requires status=passed and complete=true. Benchmark completion uses
status=measured; it establishes command timings, not workload equivalence.
A file inventory with complete=true covers its stated scan policy, not all
framework entry points.

--allow-no-tests is an explicit compatibility escape: exit 0 but status=no_tests,
complete=false. It must never satisfy a correctness gate. No other error is waived.

Scripts using --json emit one structured report. Argument-parser errors go to
stderr with exit 2. A failed command's output and exit code remain in the report.
The report keeps the last 256 KiB of command output (output_truncated marks a cut)
and output_sha256 over the full output. JSON uses lossless ASCII escapes, so a
local output code page cannot discard a report containing Unicode paths. Text
and Markdown visibly escape characters unsupported by stdout. Test summaries are parsed from the full
output up to 32 MiB (output_parsed); larger output needs fresh JUnit evidence
via {report}.

## Repository facts and review units

collect_facts.sh reports:

- `units`: one entry per directory that holds a package or build manifest
  (Cargo, Python, npm, Go, Maven/Gradle, CMake, Meson, Make, vcpkg or Conan),
  with its languages and manifests. Nested native build files inside a detected
  native tree belong to that tree. Units under test, eval, example, docs or bench paths
  carry likely_non_production. More than 200 units makes the report incomplete.
- `project`: language is the selected language, or mixed/unknown under auto
  when several or no languages are found; detected_languages comes from root
  manifests, and repository_languages covers the root plus every unit whatever
  --lang says.
- `dependency_inventories`: one per unit and language that has a reader, with
  counts, warnings and errors; an error in any inventory makes the facts report
  incomplete. coverage.dependency_languages_without_reader lists the rest, such
  as go and java.
- `entry_point_candidates`: source patterns such as main functions and
  `__main__` blocks, plus manifest fields (package.json main/module/bin/exports/
  scripts; pyproject scripts, gui-scripts, entry-points and Poetry scripts; Cargo
  bin and lib). These are heuristics; framework and configuration roots still
  need inspection.
- `coverage`: the default exclusion policy, every pruned directory with its
  reason (default_exclude or symlink; the first 100 plus a count), and files
  decoded with a fallback encoding.

--include-dir NAME, repeatable, scans a directory name that is excluded by
default, such as build or vendor, when it holds in-scope code. --output md
renders the same report as Markdown.

Sources are decoded as UTF-8 (a BOM is accepted), then GB18030, then UTF-8 with
replacement characters, so no file is silently dropped. Files that needed a
fallback are listed under coverage.decoded_with_fallback; check their real
encoding before quoting them.

## Correctness

Automatic adapters use existing local runners only:

| Language | Adapter and limits |
|---|---|
| Python | Current helper interpreter's pytest; fresh temporary JUnit, basetemp and cache |
| Rust | cargo test --locked --offline --no-fail-fast, plus --workspace when the root declares [workspace]; temporary target; existing lockfile/dependencies required; tests.rust_targets lists the targets that ran |
| Go | go test -count=1 -json ./... with GOPROXY=off; the module cache must already be populated |
| JS/TS | Existing npm test script, CI=true; a recognized Jest/Vitest, node:test (TAP or spec) or mocha summary required |
| C/C++ | Existing CTest directory, CTest 3.21+, --no-tests=error and fresh JUnit |

There is no JVM adapter; see references/polyglot.md. No automatic configure/build,
direct execution of test_*.py, or npx tool download. Select the project's
interpreter/build through an explicit command when needed:

```bash
python3 -B "$CODESIFT_SKILL/scripts/lib/check_runner.py" correctness --root "$REVIEW_ROOT" \
  --command '.venv/bin/python -m pytest --junitxml {report}' --json
```

Legacy --command is parsed with POSIX shlex on every platform and executed
without a shell. Prefer --command-argv (a JSON string array) or
--command-argv-file (a UTF-8 or UTF-8-BOM JSON array) for portable exact
arguments. The three inputs are mutually exclusive; relative argv-file paths
resolve under --root. Empty string arguments are valid, but an empty executable,
non-string members and NUL characters are rejected. {report} and {metrics}
expand after argument parsing, so paths with spaces remain one argument.

For example, a Windows argv file can contain:

```json
["C:\\my project\\.venv\\Scripts\\python.exe", "-m", "pytest", "--junitxml", "{report}"]
```

```powershell
py -3 -B (Join-Path $CodeSiftPath 'scripts\lib\check_runner.py') correctness --root $ReviewRoot --command-argv-file 'test-command.json' --json
```

--trust-command explicitly authorizes shell syntax in a correctness --command;
--shell powershell or --shell bash selects the interpreter. The default is
PowerShell on Windows (pwsh.exe, then powershell.exe) and Bash on POSIX. Shell
mode uses no user profile and does not change global execution policy. Use
CODESIFT_REPORT_PATH and CODESIFT_METRICS_PATH environment variables for paths
inside trusted shell programs (for example $env:CODESIFT_REPORT_PATH in
PowerShell). Brace placeholders are rejected in this mode because their safe
quoting depends on the surrounding shell syntax. Invoking a reviewed script
through direct argv is also supported.

Windows resolves native executables with PATH/PATHEXT. The automatic npm test
adapter supports the fixed npm.cmd test invocation through an explicit Windows
batch compatibility path. Other .cmd/.bat targets need an explicitly trusted
shell command; arbitrary batch arguments do not have the native argv contract.
Project npm script-shell configuration remains unchanged.

--output-encoding selects how child output is decoded (default utf-8). Raw-byte
hashes and benchmark comparisons do not change with this option. Undecodable
bytes remain visible in escaped form with output_decode_error=true; text-only
test evidence is incomplete, while a valid fresh JUnit report can still establish
test counts. The helper does not rewrite a project's locale or console code page.

Zero executed tests, all skipped cases, missing/malformed reports and unrecognized
success output are incomplete evidence. JUnit failures override a misleading exit 0.
Text summaries are added up across every block, because workspace and multi-target
runs print several: tests.formats and tests.summary_blocks show what was counted,
and a failure in any block fails the run.

The default --timeout is 300 seconds per command (120 per benchmark run). A
timeout stops the command's owned process group/job, reports status=timed_out, and
names the limit that was hit; raise --timeout for long suites. SIGTERM or SIGHUP
sent to the helper also stops the child process group and removes temporary
files on POSIX; the helper then exits 128 plus the signal number. Windows keeps
the shared console Ctrl+C behavior, gives the command bounded cleanup time, and
then terminates its Job. A second interrupt can shorten that grace period.

Windows creates each command suspended with a non-inherited KILL_ON_JOB_CLOSE
Job supplied through STARTUPINFOEX JOB_LIST, so it is managed from creation;
only selected standard handles are inherited. The command resumes only after
launch resources are ready. Failed setup does not run the command or fall back
to unowned execution. stop/close require Job membership to reach zero; POSIX
cleanup is limited to members of the owned process group. Normal completion also
cleans remaining owned descendants. Process creation, Job setup and owned-process
cleanup are included in command timings; no extra Python worker is launched.
An OS-level hard kill cannot execute Python finally blocks, so temporary directory
removal is guaranteed only while the helper can run its cleanup path.

A failed or incomplete run carries failure_kind, with matching output lines in
failure_evidence:

| failure_kind | Meaning |
|---|---|
| timeout | The command exceeded --timeout |
| cleanup | Owned-process cleanup failed; exit 2 and incomplete evidence |
| tool_missing, spawn_error | The runner could not start |
| environment | Missing modules or packages, disabled downloads, missing toolchains |
| build | Compilation or test collection failed |
| assertion | Tests ran and at least one failed |
| unknown | No recognized signature |

An environment failure is a missing prerequisite, not a reproduced defect; hint
suggests a next command, such as the project's .venv interpreter. A build failure
is a defect only under the project's supported toolchain and configuration.

The runner snapshots file sizes and modification times under --root, up to 20,000
files and outside default-excluded directories, before and after the command.
workspace_mutations lists created, modified and deleted paths (the first 50 of
each) with a total, and a warning is added. The test verdict itself is unchanged,
so treat any mutation as a reason to rerun in a disposable copy.

--scale N exports TEST_SCALE and CODESIFT_METRICS_PATH; PCR_METRICS_PATH is set to
the same path for older harnesses. To complete a scale request, the harness must
process the requested size and write {"observed_scale": N} to that path (also
available as {metrics}). The helper checks the value; the reviewer checks that the
harness measures actual processed input. No matching observation means incomplete
even if ordinary assertions passed.

## Comparative benchmark

Both commands are mandatory and are timed as whole processes. Prepare/build
outside timing unless startup/build time is the research question.

```bash
python3 -B "$CODESIFT_SKILL/scripts/lib/check_runner.py" benchmark --root "$REVIEW_ROOT" \
  --project-cmd './build/app --fixture data.json' \
  --baseline-cmd './build/reference --fixture data.json' \
  --workload 'same fixture and validated output' --runs 5 --warmup 1 \
  --compare-output --json
```

Runs alternate project/baseline order. Every warmup and sample must succeed.
Missing either side, failed commands and timeouts cannot become measured.
Reports include individual timings, medians, the median absolute deviation
(mad_seconds), ranges and the ratio. spread.verdict is inconclusive when the two
sides' sample ranges overlap and separated otherwise; separated ranges still do
not establish comparability. --compare-output requires byte-identical combined
output from every run of both sides; a mismatch reports status=output_mismatch
and exits 1. Profiling and algorithmic complexity still need review.

Default commands are argv strings, not shell programs. Literal metacharacters
are arguments. Each side also accepts --project-argv/--baseline-argv or
--project-argv-file/--baseline-argv-file, mutually exclusive with its string
input. For reviewed shell syntax only, --trust-project-cmd and
--trust-baseline-cmd explicitly run that side through Bash with pipefail on
POSIX or PowerShell on Windows; --shell selects a supported shell explicitly.
PowerShell scripts must check each important native exit code and exit explicitly;
a successful shell exit alone cannot prove every pipeline stage succeeded.
These flags are execution authorization, not input sanitizers.

## Dependency and registry limits

Shared parsing lives in lib/dependencies.py. Inventory retains names, source,
group, manifest and specifier. It does not execute builds, install dependencies,
compute usage or claim a transitive dependency count.

Supported inputs:

- Cargo dependencies, aliases, targets and workspace inheritance.
- Python: PEP 621 dependencies and optional groups; Poetry, including legacy
  dev-dependencies and custom sources; uv sources and indexes; requirements files
  (requirements*.txt, *-requirements.txt, requirements/*.txt) with -r includes
  inside the root, continuation lines, comments, -e and direct references, index
  options and --hash pins (marked hash_pinned); setup.cfg; Pipfile; and literal
  setup.py declarations, which are read even next to requirements files.
- npm declarations and aliases, with scoped registries from the project .npmrc
  and npmRegistryServer from .yarnrc.yml. pnpm-workspace.yaml and lerna.json
  produce a warning; audit member packages with their own --root.
- vcpkg and conanfile.txt declarations.

A malformed line is an error that names file:line and the redacted line, and the
other lines are still parsed. Credentials in URLs are redacted in every report.
Dynamic definitions, overrides, private registries and native executable build
logic produce explicit coverage limits.

--max-deps N is an opt-in policy chosen by the caller. Exceeding it returns 1.
No universal cap or arbitrary reference-tool ratio is imposed.

Registry results use registry_match, not verified. A 404 or 410 from the default
public registry is not_found there, not proof of hallucination. Network and server
errors are error; names left after the circuit breaker trips are not_checked.
Path/git/URL/workspace sources are not_applicable: validate them with their
resolver or build.

Registry selection, reported under registry.base and registry.selected_by:

1. --registry-base URL (http or https, without credentials);
2. --mirror cn: TUNA for PyPI and the crates.io index, npmmirror for npm;
3. a public mirror found in effective configuration: platform pip.conf/pip.ini files, PIP_INDEX_URL and
   UV_INDEX_URL, .npmrc registry entries, or Cargo source replacement;
4. the default: the PyPI simple index, registry.npmjs.org and the index.crates.io
   sparse index.

registry.configured lists every configured registry with the file or variable it
came from and whether it is a known public host. A private or unknown registry
keeps the affected names unresolved and names its origin; --public-registry
confirms that the public default is authoritative anyway.

Pip discovery follows global, user, actual interpreter site (sys.prefix), explicit
PIP_CONFIG_FILE and option environment precedence for supported index settings.
Windows includes ProgramData, legacy home and APPDATA pip.ini locations. An
existing explicit config skips user config; PIP_CONFIG_FILE=os.devnull disables
config files, while environment options remain effective. configured retains
historical origins with active flags; only effective values affect checks. An
INI file with a UTF-8 BOM is read as UTF-8; otherwise its decoding follows the
helper interpreter's UTF-8 mode or preferred locale encoding, as pip does.
Invalid bytes remain explicit configuration errors. An
active private extra-index-url/find-links remains unresolved even if index-url
is public. Ambiguous install/download settings, another target interpreter or
unreadable config are explicit coverage limits; this is not a full pip resolver.

A non-default registry must first answer 200 for a known package and 404 for a
random name. If it does, a miss is mirror_not_found (exit 2), because mirrors can
lag the upstream registry; if it does not, misses are unresolved. Confirm a mirror
miss upstream before treating the name as missing.

Checks run four at a time with a per-request --timeout (default 10 seconds).
Three consecutive network errors trip a breaker; the remaining names are
not_checked. Reasons name the host and the proxy host:port, never proxy
credentials. Crates are checked through the sparse index rather than the
crates.io API, which keeps within the crawler policy.

The helper never sends registry credentials. Queries reveal package names to the
selected registry; use --offline when that is unsuitable.

## Read-only scans and redundancy

File scanning prunes documented generated/vendor/build directories, lists what
it pruned, and does not follow symlinks. --max-files bounds work and reports
truncation as incomplete. This is not .gitignore-aware whole-repository coverage.

Duplicate detection indexes ordered blocks of nontrivial lines once, avoiding
quadratic repeated file reads and process creation. Tuple keys compare complete
normalized blocks directly; no cryptographic digest substitutes for equality.
Adjacent matching windows merge into one maximal block, and non-overlapping
copies inside one file are reported too. Comment lines are recognized per
language, so lines such as `*p = 1;` or `--count;` in C stay code.
--threshold sets block size;
--max-results bounds output. Matches are review candidates, not a duplication
percentage, merge gate or instruction to extract an abstraction.

Whole-program dead-code and gate judgments use patterns.md and project-aware
tools; these helpers deliberately make no universal reachability claim.

## Cleanup and regression tests

Helpers own temporary reports/logs and remove them on normal completion,
exceptions and catchable termination signals. Timeouts terminate the owned process group/job.
Project commands can write their own artifacts: inspect workspace_mutations and
use a disposable checkout when needed. Do not overwrite global /tmp filenames or
delete pre-existing user artifacts.

Run python3 -B "$CODESIFT_SKILL/scripts/smoke_test.py" (or py -3 -B with the same
file from PowerShell). Fixtures and child caches live
inside automatically removed temporary directories; no registry network calls are
made. The wrapper delegates to smoke_test.py so static analysis can inspect the
tests. Shared tests call Python directly; Bash-only tests remain POSIX-specific,
and Windows has its own console/Job lifecycle cases. Tests assert actual outcomes,
counts, failure causes and descendant PIDs rather than arbitrary nonzero exit
codes. Optional real-tool tests are reported as skipped if unavailable. The native
cross-platform CI and explicit PowerShell 5.1 job are defined in
../.github/workflows/cross-platform.yml; only completed runs establish platform
verification for a revision. Evals' scaffold scripts retain their separate Bash
requirement and are not needed to run the bundled helpers on Windows.

## Changes from the previous helper interface

- Use explicit --lang/--root flags; legacy positional arguments are removed.
- Benchmarks require both --project-cmd and --baseline-cmd; automatic unrelated
  benchmark-suite discovery is removed.
- The ineffective --reference-tool label is removed. Dependency caps now affect exit status.
- Registry JSON uses per-package statuses, not verified/hallucinated lists.
- lib/detect_lang.py is the single language/scanning implementation.
  The duplicate shell library has been removed; public .sh command paths remain.
- collect_facts.sh reports dependency_inventories per unit instead of one
  dependency_inventory, and its complete flag includes their errors.
- Default timeouts rose from 30 seconds to 300 (tests) and 120 (benchmark runs).
- CODESIFT_METRICS_PATH replaces PCR_METRICS_PATH, which is still set.

Primary runner semantics:
[pytest](https://docs.pytest.org/en/stable/reference/exit-codes.html),
[CTest](https://cmake.org/cmake/help/latest/manual/ctest.1.html),
[go test -json](https://pkg.go.dev/cmd/test2json).
