# Port Playbook — moving code to another language without losing behavior

## Contents
1. Principles · 2. Parity contract (template) · 3. End states and seams · 4. Phases · 5. Cross-language semantic traps · 6. Dependency and ecosystem mapping · 7. Test parity · 8. Unlisted language pairs · 9. Port anti-patterns

## 1. Principles

- **A port moves behavior, not structure.** The target should read as if a native speaker wrote it; similarity of file layout and function order to the source is a warning sign, not a virtue.
- **Behavior changes are a separate project.** Fixing a source bug during the port makes every difference ambiguous (fix or regression?). Record it; change it after parity, with approval.
- **Parity is measured.** Shared fixtures and differential runs, with numbers. "It compiles and the tests I wrote pass" is not parity.
- **Leaf first.** Port the modules with the fewest dependencies first so each can be tested for real.
- **Decide what not to port.** Dead code, workarounds for source-language limits, and abstraction layers that only existed to satisfy the source type system — each omission written down.

## 2. Parity contract (template)

Write this before translating; keep it in the repo or in the plan.

```markdown
## Parity contract — <component> (<source> → <target>)
- End state: <A replacement | B permanent bindings (target core, source-language API stays) | C temporary bindings removed at cutover>
- Unit of parity: <function call | CLI invocation (argv+stdin+env → stdout+stderr class+exit code) | HTTP request → response | file in → file out>
- Must match: <outputs byte-for-byte or semantically, exit codes, error classes, numeric results to N digits/exactly, ordering callers depend on, side-effect order>
- Allowed to differ: <log wording, timing, memory, help text, hash-map iteration order where unobserved, float formatting in debug output>
- Measured by: <fixture corpus location, harness command, CI job>; report = inputs compared / differences / triage
- Not ported (with reason): <dead code, source-language workarounds, deprecated flags>
- Known source bugs preserved: <list, each with the fixture that pins it>
- Owner of contract changes: <the user / named person>; changes are dated with a reason
```

## 3. End states and seams

| End state | Seam | Notes |
|---|---|---|
| A. Replacement (new binary/library, old deleted) | Process, CLI, HTTP, queue boundary | Simplest; differential harness compares two processes |
| B. Target-language core with permanent bindings (e.g. Rust core + Python package) | FFI / extension module | Binding layer is public API: versioning, error mapping, packaging for every platform the old package supported |
| C. Bindings as scaffolding (migrate piece by piece, remove bindings at the end) | FFI | Bindings can be crude, but deleting them is part of "done" |

Ask which end state the user wants if it is not obvious; a user porting a CLI usually wants A.

## 4. Phases

1. **Inventory and seam.** Module list with dependency direction; external dependencies; the seam where both implementations can be invoked; count of call sites crossing it.
2. **Characterize the source.** Language-neutral fixtures produced by running the source — including error paths and odd inputs. Existing source tests are inputs to this, not a substitute.
3. **Map.** For the pair at hand, read `port-pairs.md`. Write a short mapping note for non-obvious decisions: numeric types, error model, nullability, concurrency model, each dependency's replacement.
4. **Port leaf-first.** One module at a time; both implementations stay runnable; the module passes the shared fixtures before the next starts.
5. **Run both.** Differential run over the corpus (and shadow traffic for services if available). Triage every difference.
6. **Cut over and clean up.** Switch callers per the end state; delete the source implementation or scaffolding bindings; keep a tagged rollback.

## 5. Cross-language semantic traps

Check each relevant row with a concrete input; these differences compile fine and pass naive tests.

| Area | What differs between languages | Check with |
|---|---|---|
| Integer width & overflow | Arbitrary precision (Python, JS BigInt) vs fixed width; wraparound (Go, Java, Rust release with `wrapping_*`) vs panic (Rust debug) vs undefined behavior (C signed) | max/min values, sums that overflow 32/64 bits |
| Division & modulo | Floor division (Python `//`, `%` takes divisor's sign) vs truncation (C, Go, Java, JS, Rust `/` and `%` take dividend's sign) | `-7 / 2`, `-7 % 2` |
| Rounding | Banker's rounding (Python `round`, .NET default `Math.Round`) vs half away from zero (Go `math.Round`, Rust `f64::round`) vs JS `Math.round` (half toward +∞) | `0.5`, `1.5`, `2.5`, `-2.5` |
| Float formatting | `1.0` prints as `1.0` (Python `str`, Rust `{:?}`, serde_json) vs `1` (JS, Go `%v`, Rust `{}`); exponent thresholds differ | `1.0`, `1e21`, `0.1+0.2` |
| Strings | Code points (Python) vs UTF-8 bytes (Go `len`, Rust `len`) vs UTF-16 units (JS, Java, C#) for length, indexing, slicing; case mapping locale | `"é"`, emoji, `"İ".lower()` |
| Collections order | Insertion-ordered (Python dict, JS Map/object non-integer keys, Java LinkedHashMap) vs unordered (Go map, Rust HashMap, Java HashMap) vs sorted on serialization (Go `encoding/json` map keys, serde_json `Map` without `preserve_order`) | iterate/serialize a map with 3+ keys |
| Sorting | Stable (Python, Java objects, JS since ES2019, Rust `sort`) vs unstable (Go `sort.Slice`, Rust `sort_unstable`, C++ `std::sort`); JS default `sort()` compares as strings | equal keys; `[10, 9, 1]` |
| Equality & hashing | Value vs reference equality for objects/records; NaN equality; float keys | two equal structs, NaN in a set |
| Null/absence | `None`/`null`/`undefined`/`nil`/zero values/`Option` — zero values (Go) silently fill missing fields | missing JSON field, explicit null |
| Errors | Exceptions vs error returns vs `Result`; checked vs unchecked; error message text callers match | each error path in fixtures |
| Resource cleanup | GC + finalizers vs RAII/`Drop` vs `defer`/`with`/`using`; timing of close/flush | output flushed on error exit |
| Concurrency | GIL (CPython) vs true parallelism → data races appear; event loop (JS) vs threads; eager promises (JS) vs lazy futures (Rust); cancellation models | concurrent access tests, `-race`/TSan |
| Time | Epoch units (s vs ms vs ns), time zone defaults, monotonic vs wall clock, date format strings | DST boundaries, leap day |
| Regex | Backtracking engines (Python `re`, JS, Java, PCRE) vs RE2-style (Go `regexp`, Rust `regex`) without backreferences/lookaround; differing `\w`, `\d` Unicode semantics | patterns with lookahead, non-ASCII digits |
| Randomness & hashing | Seeds, algorithms, hash randomization — never compare outputs that depend on them; stub them | — |
| Paths & OS | Separators, case sensitivity, default encodings, newline handling | Windows path, CRLF input |

## 6. Dependency and ecosystem mapping

For each third-party dependency:
1. List what the code actually uses from it (often 5% of the library).
2. Prefer the target's standard library when it covers that subset; otherwise pick the target ecosystem's de-facto choice (well maintained, permissive license compatible with the project).
3. Check behavioral details that leak into outputs: JSON number/key formatting, date parsing leniency, HTTP client redirects/timeouts/retries, regex dialect, CSV quoting.
4. Record the mapping in the plan; flag any dependency with no reasonable equivalent early (it may decide the seam or end state).

Build and packaging: map the build (pyproject/npm/Maven/Gradle/Make/CMake → go.mod/Cargo/Gradle…), CI jobs, lint/format configs, and release artifacts (wheels, binaries per platform, containers).

## 7. Test parity

- Shared fixtures run against both implementations (primary evidence).
- Every source unit test gets a target counterpart, or a one-line reason it does not apply (e.g. "tests a Python-only duck-typing path removed by static types").
- Target-native additions: compile-time guarantees replace some runtime tests (nullability, exhaustiveness); add tests for target-only risks (overflow behavior, concurrency with race detector, FFI boundary null/ownership).
- Keep the source test suite running until cutover.

## 8. Unlisted language pairs

When the pair is not in `port-pairs.md`:
1. Read the target's official style guide and idioms; use its formatter and linter as the authority.
2. Walk the trap table in section 5 row by row and write the answer for this pair.
3. Map the error model, nullability, concurrency model, and module/visibility system explicitly.
4. Map each dependency (section 6).
5. Say in the report that the pair is not covered by a curated mapping, so reviewers look harder at idioms.

## 9. Port anti-patterns

| Anti-pattern | Tell | Instead |
|---|---|---|
| Transliteration | Same file names, function order, loop indices; source idioms in target syntax | Port behavior per module; write target idioms |
| Compile glue | `clone()`/`unwrap()` everywhere (Rust), `!!` (Kotlin), `any` (TS), `interface{}`/`any` (Go), blanket `catch (Exception)` | Model ownership, nullability, and errors properly; these are design decisions the port must make |
| Porting the abstraction | Interface/trait per source class, factories with one product, getters/setters around plain data | Port behavior; add abstractions when a second caller needs them |
| Fixing while porting | "port X and fix off-by-one" | Preserve; record; fix after parity |
| Fresh test suite | New tests reflect what the porter imagined | Fixtures recorded from the source |
| Narrowed errors | Error paths missing from fixtures; target rejects or panics where source returned an error | Fixtures for each error class; never panic on input the source handled |
| `unsafe`/raw pointers to mimic GC graphs (Rust) | Raw parent pointers, self-references | Indices/arenas/IDs; `unsafe` only with documented invariants |
| Harness rot | Differential job set to allow failure | Fix the difference or the contract — never mute the check |
| Leaving the source alive | Old implementation kept without owner/date after cutover | Tagged rollback, then delete |
