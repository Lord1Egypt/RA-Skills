# Fact producers: when to run them, how, and how to read the output

> This skill ships two **deterministic measurements**, provided by a zero-dependency Node CLI.
> They answer questions the model cannot compute accurately — **not** "what vulnerabilities exist".
>
> This page is the operations manual: when you must run them, how to write the commands, and which section of the output decides what conclusion you may draw.
> For what you can and cannot infer from a fact once you have it, see `fact-contract.md`.

---

## 1. First, where the commands live

The CLI is **not in the skill directory** — it is a separate program of this project. In order of availability:

| Situation | How to write it | Notes |
|---|---|---|
| Installed | `euthyna audit …` | `euthyna` is the command name declared by the package |
| Project checkout available | `node <euthyna repo>/bin/euthyna.js audit …` | the most common form |
| Neither | — | **mark the criterion as "not evaluable"**; do not substitute a manual estimate |

### ⚠️ A real pitfall: relative paths only work inside the euthyna repository

`node bin/euthyna.js …` only works **when the current directory happens to be the euthyna repository**.
When auditing, your current directory is the **audited project**, so:

```
Error: Cannot find module 'D:\axe-core\axe-core\bin\euthyna.js'
```

`history` has `--repo` — pass the repository path explicitly and it runs from any directory:

```powershell
node <euthyna repo>/bin/euthyna.js history --base <rev> --repo <audited repo>
```

- `--repo` refers to the **audited repository**, not the euthyna path
- `--base` / `--head` both resolve relative to the **audited repository**, independent of the current directory
- the coverage command has no `--repo` — write the coverage file as an **absolute path**

Both commands were verified: run from `D:\` with `--repo` pointing at another repository, exit codes matched expectations.

---

## 2. `history` — the origin of deleted code

### When you must run it

| Trigger scenario | Corresponding stage |
|---|---|
| Reviewing a change (PR / diff / commit) where **code was deleted** | Stage B |
| The user asks "did this change weaken some protection" | Stage B |
| You need to determine whether some code was "removed and added back" | Stage B |

**If the diff contains deleted lines, run it first.** This is not optional: a diff that looks "very clean" because a check was deleted
is exactly what a security regression usually looks like, and a model cannot blame hundreds of deleted lines one by one and then trace back through commit history.

**Usually you do not need to run it alone** — `euthyna audit` (section 1) already runs history (with origin tracing on by default)
and deps in one pass. Run `history` alone to compare against a different `--base`, or when you want history without deps.

### Commands

```powershell
# basic: which commits do this change's deleted lines come from, and do those commits look like security fixes
# (origin tracing is on by default: deleted lines are attributed to the commit that "originally introduced" the content)
node <euthyna repo>/bin/euthyna.js history --base <pre-change revision> --repo <audited repo>

# additionally check for "removed and added back" lines (has a probe cap; slower than the basic version)
node <euthyna repo>/bin/euthyna.js history --base <pre-change revision> --pickaxe --repo <audited repo>

# disable origin tracing and fall back to blame's "last modified" semantics (faster; the output states this)
node <euthyna repo>/bin/euthyna.js history --base <pre-change revision> --no-origins --repo <audited repo>
```

`--base` is the **pre-change revision** (the PR's fork point); `--head` defaults to `HEAD`.
Omitting `--base` infers it as `merge-base(<the audited head>, origin/main)`, marks the range line as inferred
and adds a `range-inferred` entry to the criteria not evaluated. An inferred range reaches **the
fork point only** — nothing earlier; when neither ref resolves the run stops with a usage error
instead of guessing `HEAD~1`. This is what lets a slash command arrive with no arguments, so
**the first thing to do with `range-inferred` is check the fork point**, not accept it.
When the fork point is uncertain, use the result of `git merge-base <target branch> HEAD`.

### Attribution semantics (two inherent approximations; established ≠ exact)

`history`'s attribution and classification each carry a **hard-coded approximation** — know them before reading the output:

1. **Attribution: `git log -S` traces the "original introducer" by default; blame's "last modified" is the fallback.** If a security-fix line was later touched by formatting/refactoring (moved, copied), blame attributes the origin to the last commit that touched it — tracing the introducer exists precisely to avoid that trap. Origin tracing uses `git log -S <line content>` to locate the commit that **originally introduced** the content; when it differs from blame, the fact writes out both commits (`detail.blameCommit` = last modified, `evidence.commit` = originally introduced) and states so. Tracing applies only to lines ≥ 12 characters long (for overly generic lines, `-S` would point at the first commit of the entire history, which is not the origin); traced lines are probe-capped, and when the cap is hit the remaining lines keep their blame attribution, stated under "criteria not evaluated"; disabling it explicitly with `--no-origins` is likewise stated there.
2. **Classification: look at the commit message first, then the commit diff, then the deleted line itself.** When the message is vague ("update utils") but the diff touches a dangerous API, or the deleted line is itself security code (e.g. `if (!authorized) return`), it is marked `security` — the basis is recorded in `detail.classificationBasis` (`message` / `diff` / `deleted-line`). The deliberately wide bias is intentional: missing a security commit is more dangerous than over-reporting.

### What the output looks like (real capture)

```
euthyna-history — attribution and security classification of deleted code
Target: D:/axe-core/axe-core
Range: 8390a5a9…..397f5fce…

Established (8)
  • This change deleted 4 lines of code from commit ab877f9d70, spread across 2 files. Commit message: "fix(link-in-text-block): don't match style or script text (#3775)", classification: fix
       Evidence: lib/checks/color/link-in-text-block-evaluate.js (ab877f9d70)
       Reproduce: git blame --porcelain -L 104,104 -L 114,114 8390a5a9… -- lib/checks/…

⚠ Criteria not evaluated (missing data is not clean):
  • reintroduction: --pickaxe not enabled; reintroduced lines were not checked

Evaluated criteria:
  • history: 105 (euthyna-history)
```

### How to read it

| What you see | What it means |
|---|---|
| `classification: security` under "Established" | **Raise the risk to maximum**, unless you can prove that code is no longer needed |
| `classification: fix` | Not a security fix, but **read the commit message itself** — the classifier is biased wide; do not rely on the label alone |
| `spread across N files` | The file in the evidence **does not contain all** deleted lines. Do not assume only that one file is affected |
| The "⚠ Criteria not evaluated" section at the bottom | When this section is non-empty, you **must not** read this run as "checked, no problem" |
| `Established (0)` with an empty not-evaluated section | There really are no deleted lines. This is a **completed measurement**, not a failure |

**Do not run `git blame` yourself and read commit messages by eye.** The machine adjudicates the same diff twice with identical results; a human may read it twice with different results.

---

## 3. `coverage` — symbol invocation counts

### When you must run it

| Trigger scenario | Corresponding stage |
|---|---|
| The report will say "this function **has test coverage**" | Stage B / C |
| The report will say "this function **has no test coverage**" | Stage B / C |
| A conclusion depends on "that path was exercised by tests" | Stage C |

In other words: **run it before writing anything about "tested or not tested"**.

### Commands

```powershell
node <euthyna repo>/bin/euthyna.js coverage `
  --coverage <absolute path to coverage file> `
  --symbol <symbol name> --symbol <symbol name>
```

`--symbol` is repeatable — query several at once. Add `--file` to restrict to a single file.
Go profiles additionally need `--source` (see below).

**Five coverage formats are read** (auto-detected, no parameters needed):

| Format | Source | Notes |
|---|---|---|
| c8 / v8-to-istanbul `coverage-final.json` | JS projects (c8 lands at `coverage/coverage-final.json` by default) | Per-file `fnMap` + `f` (invocation-count array) |
| classic istanbul `coverage-final.json` | jest's default provider, nyc | The same `fnMap` + `f` plus a `hash` field (c8 has no `hash`); both resolve through the same code path |
| coverage.py JSON (format 3) | Python projects (produced by `coverage json`) | Top-level `{meta, files}`; in `functions`, "function name → list of executed lines", **no invocation counts**. Functions never called are still in the list with empty `executed_lines` |
| Go `-coverprofile` (text) | Go projects (produced by `go test -coverprofile`) | A `mode:` header plus one line per block (`path:startL.startC,endL.endC stmts count`), **no function names**. `--source <module root>` is required: the producer reads top-level `func` declarations in the source to map line ranges back to functions |
| lcov tracefile (text) | Rust projects (produced by cargo-llvm-cov / cargo-tarpaulin); gcov / llvm-cov produce the format too | `SF:` opens a record, `end_of_record` closes it; `FN:<line>,<symbol>` and `FNDA:<count>,<symbol>` give a function name and its invocation count (**two separate runs, not adjacent pairs**); **the symbol names are mangled**, and the producer anchors the `module::function` path you write against the `<decimal length><name>` tail segments of Rust v0 mangling, never inside a longer `<length><name>` pair — a query for `get` does not answer for `cfg_3get` |

The Go production commands (Go targets):

```bash
go test ./<package>/ -coverprofile=<absolute path>.out -run <test name>
node <euthyna repo>/bin/euthyna.js coverage `
  --coverage <absolute path>.out --symbol <symbol> --source <Go module root>
```

> Go-specific notes (measured in the act case study):
> 1. **A file absent from the profile is not "never executed"** — its package may not have
>    been compiled into the test binary at all. The producer reports this as "not evaluated",
>    never as "not covered". To measure a package, use `-coverpkg=<package>` or run that
>    package's tests directly.
> 2. Profile paths are module import paths (`module/pkg/file.go`); point `--source` at the
>    module root containing go.mod, and the producer maps import paths back to disk files.
> 3. `mode: set` is enough — the two-state semantics (invoked / never invoked) do not need
>    the exact counts of `count`/`atomic`.

The coverage.py production commands (Python targets):

```powershell
uv run --with coverage python -m coverage run `
  --include="*/src/<package>/<file>.py" `
  -m pytest <test-file> -o addopts="" -p no:randomly
uv run --with coverage python -m coverage json -o <output path>.json
```

> Two Python-specific caveats (measured in the crewAI case study):
> 1. **Disable xdist** (`-o addopts=""`) — coverage does not collect subprocess traces by default, so with `-n auto`
>    the report is empty. Override the repository's xdist defaults with `-o addopts=""`.
> 2. Restricting by file path with `--include` is more reliable than `--source` for src layouts (`--source=<package name>` may report
>    `module-not-imported`).

Where the coverage file comes from: if the project produces one, use it. When the project does not, **either run its tests once with the project's own tooling to produce it, or mark the criterion as "not evaluable"**.

The lcov production commands (Rust targets, measured on this machine):

```powershell
# 0. llvm-cov / llvm-profdata are not on PATH; locate rustc's own copies first
$bin = (rustc --print sysroot) + "\lib\rustlib\x86_64-pc-windows-msvc\bin"
# 1. instrumented build + run the tests
$env:RUSTFLAGS = "-C instrument-coverage"
$env:LLVM_PROFILE_FILE = "<absolute path>\prof\probe-%p-%m.profraw"
cargo test
# 2. merge the profraw files, then export lcov from the test binary
& "$bin\llvm-profdata.exe" merge -sparse <absolute path>\prof\*.profraw -o <absolute path>\probe.profdata
& "$bin\llvm-cov.exe" export --format=lcov --instr-profile=<absolute path>\probe.profdata `
  "<target\debug\deps\<crate>-<hash>.exe>" --sources src > <absolute path>\lcov.info
# 3. query (lcov needs no --source: the function names are in the FN: lines)
node <euthyna repo>/bin/euthyna.js coverage `
  --coverage <absolute path>\lcov.info --symbol <module::function> --file <absolute path>\src\lib.rs
```

> lcov-specific caveats (measured on a probe crate):
> 1. **The symbol names are mangled and this producer does not demangle them** (no usable demangler on this machine: `llvm-cov --Xdemangler` was tried with `rust` / `rustfilt` / `llvm-cxxfilt` / `c++filt`, and all four report `could not find the demangler`). Matching relies on the `<decimal length><name>` tail segments of **Rust v0 mangling** (what `-C instrument-coverage` implies), so write the query as `module::function` (split on `::`, matched per segment). Each segment's name must start at a boundary — the start of the name, right after the mangling's own `_` separator, or at a proven pair boundary — and never strictly inside a longer pair: a query for `get` does not answer for `cfg_3get`. A qualified query is a subsequence test, not a path-exact one. `nested::dup` matches only `6nested3dup`, while a bare `dup` also matches the same-named function in an outer module — each hit is reported as its own fact carrying its own mangled name. An already-mangled query (starting with `_R`/`_Z`) is matched exactly and **never half-decoded**.
> 2. **One file may carry several `FN:` lines pointing at the same line** (generic monomorphisation, closures). That is not a duplicate record. A generic function instantiated twice yields two facts, each carrying its own mangled name.
> 3. When an `FN:` line exists and its `FNDA:` is missing, the result is "not evaluated", **never a default of 0** — inventing a "never invoked" out of thin air is the one direction this producer must not fail in.
> 4. When one `SF:` appears in several records (or several same-named `FNDA:` lines exist), the counts are **summed**; summing can never turn a non-zero into zero, which is what keeps the only actionable conclusion (a count of 0) safe.
> 5. A file absent from the tracefile is reported as **"not evaluated"** (llvm-cov / gcov only emit records for instrumented targets, and `--sources` filters further) — deliberately the opposite of c8's "file absent from the data = never executed".
> 6. The newer `FNL:`/`FNA:` encoding is **explicitly refused** rather than read out of a guessed shape; `SF:` paths are absolute (backslash-separated on Windows).
> 7. Three spellings the specification allows are read rather than refused: **comment records** (`#` in column 0) may appear anywhere, and `geninfo --comment` writes one at the top by default; **`KF:` is a synonym for `SF:`**; and **`FN:<start>,<end>,<name>`** is the shape gcc 9+ emits — the end line is discarded but must be *consumed*, or `14,` sticks to the symbol name and splits one function into a record with a line and no count plus one with a count and no line, the first of which then reports a spurious not-evaluated. An indented `#` is still refused.

### What the output looks like (real capture; one query hitting both result kinds)

```
euthyna-coverage — symbol invocation counts (can only falsify)

Established (1)
  • Symbol cleanup was never invoked in this test run (invocation count 0) — any behavior depending on it was never exercised
       Evidence: …\src\handlers.js:29

Unknown (1)
  • Symbol checkPermission was invoked 2 time(s), but a non-zero invocation count **cannot** prove any specific call site ran — this fact can only falsify, never confirm
       Evidence: …\src\authz.js:4
```

### How to read it (this section is the easiest part of the whole tool to misuse)

| Fact | What it lets you infer |
|---|---|
| Count 0, `status: established` | ✅ **Really never invoked**. You may say "this path was never exercised" on that basis |
| Count > 0, `status: unknown` | ❌ **Nothing can be inferred**. Having entered the function ≠ the specific call site you asked about ran |

The reason is fully explained in `fact-contract.md`: the underlying coverage data reports **call sites that never executed as covered**
(straight-line code after a thrown exception is the classic case), so the "covered" direction is unreliable in itself.
**The producer has no "executed" output at all — this is deliberate.**

Corollary: **do not** use "non-zero count" to close a "not tested here" concern. To prove something actually executed,
only a demonstration that truly reaches that call site can do it (Gate 4 of Stage C).

---

## 4. Exit codes: what to do with each code

| Code | Meaning | What you should do |
|---|---|---|
| `0` | Measured, no security-related findings | Continue. **But remember to read the "Criteria not evaluated" section** |
| `10` | Measured, at least one `security`-classified fact exists | **Raise priority**, then run each one through Stage C. Do not treat it as a conclusion directly |
| `1` | Usage error | Fix the command (`--base` mistyped, empty symbol name, etc.). This is not a measurement result |
| **`2`** | **Could not measure at all** | **Must not be read as clean**. Either switch measurement methods or mark the relevant criteria as "not evaluable" |

The difference between `2` and `0` is the essence of why this contract exists: **failing to measure and measuring clean are two different things.**

### Common situations that reach `2`

| Situation | What the output says | Handling |
|---|---|---|
| The directory is not inside a git repository | Not evaluated: not in any git repository | Switch to a real repository, or mark not evaluable |
| The coverage file does not exist | Not evaluated: `ENOENT`, tests not run | Produce coverage, or mark not evaluable |
| The symbol name is misspelled / does not exist | Symbol not found | Verify the symbol name; if it truly does not exist, state that it is outside the measurement scope |

**None of these count as "clean".** The report must write them into "Criteria not evaluated" with the reason stated.

---

## 5. Where they fit into the workflow

```
Stage B (change-surface audit)
  ├─ first command ───────────► audit              → history + deps in one pass
  │                                              → deleted lines present: the result decides whether risk is raised to maximum
  ├─ regression judgment ──────► history --pickaxe  → the result decides whether to treat it as a "regression"
  └─ test coverage to discuss ─► coverage           → can only falsify; a non-zero count is not evidence

Stage C (claim verification)
  └─ conclusion depends on "tested or not" ──► coverage → it constrains the truth of Gate 4 (demonstration)
```

**Producers give facts, not verdicts.** They say "this line comes from a security-fix commit",
**not** "deleting it is a vulnerability" — the latter is Stage C's business.

---

## 6. `gate` — programmatic gate validation (not a measurement)

`history` / `coverage` produce facts; `gate` **does not measure** — it checks whether an audit report's self-declaration
conforms to the 6-gate contract. The report format is in SKILL.md's "adjudication format" section.

```powershell
node <euthyna repo>/bin/euthyna.js gate <report file>
node <euthyna repo>/bin/euthyna.js gate <report file> --verify --cwd <audited repo>
```

| What you see | What it means |
|---|---|
| Exit code `0` | Every finding carries the evidence it should: TP has `path:L123` evidence + reproduce command + impact + all six gates passed; FP has a FAIL gate; INCONCLUSIVE has a not-evaluated gate |
| Exit code `10` | Some finding was **downgraded to "observation"** — missing evidence / missing reproduction / gates contradicting the verdict. Read the downgrade reason; fill the gap or change the conclusion to an observation |
| Exit code `2` | The report cannot be read, or contains no verifiable findings. **Not clean** |
| `--verify`'s reproduction-check ✗ | The reproduce command actually ran but did not succeed — "says it reproduces" does not count |

`gate` only validates what the report itself says; it does not audit the target repository. So it cannot replace adjudication — it only guarantees
that a conclusion without evidence is not handed over wearing the face of "established".

---

## 7. Known limits (do not use beyond them)

- `history`'s classifier is **biased wide**: missing a security commit is more dangerous than over-reporting, so it would rather report `fix` too. The classification is a **lead** — read the commit message yourself.
- `history`'s attribution **traces the "original introducer" by default** (`git log -S`, probe-capped, only lines ≥ 12 characters); to fall back to blame's "last modified" semantics use `--no-origins` (faster; the output states this). Both approximations are documented in this file's "Attribution semantics" section.
- `history` only covers **deleted lines**. It does not handle newly added code (except with `--pickaxe`).
- `--graph` only **draws** the attributions above (Mermaid source, not an image): the range → the last modifier → the commit that first introduced the content. It measures nothing new and draws no severity — a graph carries measured states and line counts, and that is the contract too, not an omission.
- **The absence of the second edge does not mean the content never moved.** A traced origin is dropped two ways: a generic short line (`}`, `return x;`) or `--no-origins` is written as the dotted `history-origins` edge, while an origin commit the classifier does not read as security-relevant is dropped **silently** — no edge and no note. Read a missing edge as a neutral fact, not as a clearance.
- `coverage` **can only falsify**. See above.
- `coverage` relies on invocation counts and **does not handle dynamic dispatch, reflection, or string-based calls**. Conclusions of count 0 must be discounted when such mechanisms exist.
- The two halves of `audit` **do not read the same thing**: `history` takes the commits named by `--base`/`--head`, while `deps` takes the manifest **currently checked out at the root of the repository** `--repo` points into (manifests are located from the root only). So the criterion is **content**: when the manifest measured differs from the one at `--head`, or does not exist in that commit at all (a gitignored lockfile is exactly that), *Criteria not evaluated* gains an entry naming the file and `--head`. The `code` (`manifest-not-head` / `manifest-unverified`) appears only on the `--json` channel. **Seeing one means checking out an end of the range and re-running** — the declaration keeps the trap from being silent; it does not measure the fact for you.
- Neither **produces scores, severity, or fix suggestions**. That is the contract, not an omission.
