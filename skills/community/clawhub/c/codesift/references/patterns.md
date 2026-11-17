# Systemic review patterns

Use these patterns to form testable candidates, not automatic findings.
The evidence/impact definitions in SKILL.md are authoritative.

## Contents

- Cross-language coding standards
- Reachability and zombie code
- Redundancy
- Gate effectiveness
- Cross-language and cross-service boundaries
- Performance reasoning
- Other systemic candidates
- External candidate generators
- Sources and case-study provenance

## Cross-language coding standards

Apply explicit user and repository rules in their stated scope. Use the criteria
below to investigate observable behavior and maintainability; do not turn them
into automatic token bans or impose one language's syntax on another.
All proposed changes still require the review-and-approval workflow in SKILL.md.

### Functions, types and comments

- Keep functions focused on one responsibility. Identify inputs, outputs,
  side effects, ownership and failure behavior. Prefer clear guard clauses over
  deeply nested branches when they improve the actual control flow.
- Make public parameter and return contracts explicit where the language supports
  useful declarations. Respect established inference for local expressions and
  callbacks; do not universally ban inferred types or idiomatic implicit returns.
- Use meaningful, consistent names and named constants for domain values.
  Prefer immutable values when mutation is unnecessary. Choose numeric types from
  precision, range, interoperability and measured resource needs, not a global
  preference for one floating-point width.
- Use function-level comments to explain purpose, non-obvious invariants and
  important error or resource contracts. Do not restate obvious operations.
  Function/file length is a review signal unless the project defines a binding
  limit; do not split coherent code solely to meet an invented line count.

### Responsibilities and proportionality

Check for existing implementations before adding code. Keep each business rule
in one owning implementation and prefer clear typed models or enums when they
represent stable domain concepts. Use declarative mappings for genuinely tabular
logic, and procedural code when ordering or side effects is clearer.

Prefer the smallest coherent change that resolves the root cause. Do not stack
fallbacks on a broken contract, or expand a local fix into an unrelated redesign.
Prefer existing files; justify a new module by a concrete responsibility rather
than adding scaffolding, documentation or examples without a task need.

### Errors, validation and data preservation

Use the project's error model: exceptions, Result-like values or explicit error
returns as appropriate. Distinguish a valid empty result from a failed operation.
Preserve useful diagnostic context without exposing secrets. Catch a failure only
to recover under a real contract, add context or translate it at a defined boundary.
Never fabricate success or silently substitute defaults to make a check pass.

Validate actual API, persistence and workload contracts. Justify added guards,
caps, retries and fallback paths in the approval plan, including their failure
behavior. Keep necessary authorization and integrity protections. Do not create
speculative security layers or a catalog of unreachable failure scenarios.
Data limits and truncation must be explicit and visible to consumers, with a
continuation or recovery path when complete data is required.

Use exact equality and ordinary data structures where they express the contract.
Do not invent cryptographic fingerprints or identity wrappers merely to replace
ordered keys or exact content comparison. Existing checksum/content-identity
contracts may justify them; ordinary hash-table use is not itself a finding.

### Resource and concurrency ownership

Define who closes resources and owns background work. Use the language's scoped
cleanup mechanisms, such as RAII, context managers, defer or try/finally, including
failure paths. Make cancellation and task completion observable. Check shared
mutable state, synchronization and driver thread-safety against actual usage.
Avoid unnecessary lock retention across slow I/O. Retries need a defined transient
failure and safe replay/idempotency contract; they must not hide persistent faults.

### Tests and scenario fidelity

Derive assertions from an external behavior contract, invariant or reproduced
bug. For behavior fixes, run a focused case and establish the expected failure
before changing production code when feasible. Record unavailable reproduction
as a limit; never call an environment failure a reproduced bug.

Verify the scenario the user requested at the relevant boundary. Backend tests
alone do not establish a frontend interaction. Keep test oracles independent of
the implementation strategy and use real integration cases where persistence or
concurrency behavior matters. Reuse the project's test framework rather than
creating a custom one without a demonstrated need.

Run the focused case and affected targets first. Run broader regression checks
when the related work is complete or unresolved impact requires them. For
documentation, translation and behavior-preserving refactors, use appropriate
existing checks; do not manufacture failing tests for unchanged behavior.

### Scope, dependencies and experiments

Define observable completion criteria and relationships between subtasks so work
does not drift into an unverifiable collection of changes. Read relevant library
documentation for the actual version and inspect implementation paths when their
semantics or capabilities matter; a superficial API match is insufficient.

Start optimization with a bottleneck hypothesis and finish with a justified
keep/revert decision. Preserve correctness, workload semantics, baseline behavior
and failed or slow measurements. Never hardcode answers, query another system's
oracle at runtime, shrink one side's workload, or edit results to create a gain.
Separate cold/warm cache and startup/steady-state measurements where relevant.
Change one explanatory variable at a time when isolating a cause; identify any
compound change in the approved plan and limit causal claims accordingly.

## Reachability and zombie code

**Question:** Can a supported production or external consumer reach this code?

1. Enumerate roots within the requested scope: binaries, API/CLI routes, public
   library exports, workers, scheduled jobs, plugins, callbacks, reflection,
   FFI, serialization hooks, migrations, build scripts and configuration/assets.
2. Separate production, test, generated, vendored and intentionally retained
   compatibility code. Tests calling a function do not establish production use.
3. Follow edges from roots. Search both incoming and outgoing references.
   Include configuration strings and registration tables as well as direct calls.
4. Examine disconnected strongly connected components: A calls B and B calls A
   can be an unreachable island despite both having callers.
5. Check build flags, platform variants, dynamic imports and external consumers.
   An exported library API with no local caller is unresolved until its contract
   and consumers are known. Zero observed coverage proves only non-observation.
6. For a deletion candidate, record scope, roots, source locations, references,
   exclusions, purpose and remaining uncertainty. If removal is authorized,
   validate relevant builds/tests, packaging and public contracts afterward.

Use existing analysis tools as supporting evidence: Knip for configured JS/TS
projects; Vulture for Python candidates; compiler unused/unreachable diagnostics
for native/Rust code. Check tool version/configuration and complete output.
Do not auto-install a tool or treat its confidence score as a proof.
Do not introduce broad whitelists solely to make the report green.
See External candidate generators for further tools and their limits.

**Report separately:** confirmed unused code, unresolved candidates, code used
only by tests, and intentionally retained public/compatibility paths. Count
files/symbols and analyzed scope; avoid a universal "too much dead code" percentage.

**Illustrative cases, not reproduced project findings:**

- An unregistered handler has no reachable caller or supported external entry:
  a deletion candidate after checking framework discovery and consumers.
- A decorated callback has no direct caller but is registered at import:
  reachable; deleting it would break behavior.
- Two legacy modules call each other but no active root reaches them:
  examine them as one island instead of clearing each because it has callers.
- A dormant emergency kill switch has an operational owner and tested effect:
  retention may be justified even if recent traffic never used it.

## Redundancy

Distinguish these situations before proposing extraction or removal:

| Candidate | Evidence / decision |
|---|---|
| Copy-paste drift | Same responsibility and contract, unintended behavior differences |
| Duplicate calculation/validation | Same input and invariant, overlapping cost, no intervening mutation/trust boundary |
| Thin wrapper | Remove only if it adds no stable interface, adaptation, ownership or isolation |
| Parallel implementations | Check platform, protocol and compatibility requirements before consolidation |
| Unused abstraction/configuration | Check consumers and deletion impact using the reachability procedure |

Line/block matches nominate pairs for inspection. Small wrappers, boilerplate
and similar tests can be intentional. Prefer one owning implementation when the
contract is truly shared; do not create a generic framework to eliminate a few lines.

For performance cost, measure duplicate work on the active path. For maintenance
cost, show the duplicated decision and observed or plausible drift mechanism.

## Gate effectiveness

Here, a gate includes CI checks, preconditions, runtime validation, feature flags,
readiness checks, release criteria and algorithm-selection thresholds.

For each relevant gate, identify:

| Field | Evidence to collect |
|---|---|
| Purpose | The protected invariant or operational decision and its owner/requirement |
| Input | Data/revision/configuration actually inspected, including freshness and scope |
| Decision | Predicate, threshold source, reachable pass and fail branches |
| Enforcement | Exit/status propagation and the consumer that blocks, retries or falls back |
| Cost | Latency, resources and maintenance relative to the risk it reduces |
| Lifecycle | Supported variants, rollback/kill-switch role and retirement condition |

Use contrasting cases: a valid input passes; a known violation fails; missing,
empty, skipped, timed-out or stale evidence does not silently satisfy the gate.
Run mutations/negative cases in a disposable fixture, not production.

**Common ineffective gates:**

- A check fails but `|| true`, broad exception handling or `continue-on-error`
  masks it before the decision-making consumer.
- "Tests passed" means only exit 0, zero tests, all skipped tests or a stub command.
- A benchmark gate has no equivalent baseline, ignores failed samples, or times
  unrelated work such as one command's build versus another's steady state.
- A regex checks that a function/configuration exists, not that it is reachable
  or enforces the intended behavior.
- A quality threshold has no stated requirement and no action tied to failure.
- A check emits a report that no downstream decision reads.
- A feature/configuration flag is never read, cannot affect the outcome, or guards
  an obsolete branch with no remaining supported use.

**Do not overcorrect:** authorization, input validation at separate trust
boundaries, idempotency, rate limits, integrity checks and rollout kill switches
may be necessary despite repetition or a high pass rate. A threshold without
documentation is a question to resolve, not automatically a useless gate.

For CI, inspect the full producer-to-consumer path: triggers, path filters,
conditions, matrix jobs, dependencies, final status and repository requirements.
GitHub documents different outcomes for a skipped workflow and a skipped job;
a green-looking check alone does not establish coverage of the requested revision.

Recommend one of: keep, repair, consolidate, retire, or investigate. Provide a
counterexample and affected requirement before calling a gate ineffective.
Remove a safeguard only when its obligation remains covered or has been explicitly retired.

## Cross-language and cross-service boundaries

**Question:** Do both sides of a boundary agree on ownership, shape, meaning and failure?

Each side of a boundary can look correct on its own, which is why defects here
survive single-language review. Read both sides, and compare definitions
mechanically where a tool can.

| Boundary | Check |
|---|---|
| FFI and native extensions | Who allocates and frees each buffer, and with which allocator; how long borrowed pointers stay valid; thread affinity; whether panics or exceptions can cross; GIL or runtime-lock rules |
| IDL and wire schemas | Protobuf/Thrift field numbers never reused, removed fields `reserved`, type changes treated as breaking, unknown enum values handled; schema-registry compatibility mode |
| HTTP and RPC APIs | OpenAPI/GraphQL schema against real handlers: required fields, status codes, error bodies, pagination and versioning; generated clients regenerated after changes |
| Frontend and backend types | Hand-written TypeScript types against server DTOs: optional versus nullable, enums, date formats, 64-bit integers beyond JavaScript's 2^53 safe range |
| Database schema | Migrations against ORM models and raw SQL: nullability, defaults, indexes for new queries, constraint names; old and new code sharing one schema during a rolling deploy |
| Configuration and environment | Every key read is defined in each deployment and every defined key is read; names and units match (timeout versus timeout_ms); string booleans parsed deliberately; defaults agree across services |
| Errors and status codes | Domain errors map to HTTP/gRPC status consistently; retries key on retryable codes; boundary code does not turn failures into success or generic 500s |
| Units, time and text | Seconds versus milliseconds, bytes versus characters, UTC versus local time and DST, naive versus aware timestamps, text encodings and normalization |

Language specifics worth checking:

- Rust: a panic that reaches an `extern "C"` function aborts the process (Rust
  1.81 and later; undefined behavior before). `extern "C-unwind"` opts into
  unwinding; `catch_unwind` at the boundary turns a panic into an error code.
- C++: an exception that propagates through C frames is not portable; translate
  it at the boundary.
- CPython extensions: a function that returns NULL must have set an exception;
  track new versus borrowed references. Free-threaded builds (3.13 and later)
  remove the GIL that some code relied on as an implicit lock.
- JNI: local references are freed when the native method returns and their
  capacity is limited; check for a pending Java exception before further JNI calls.

**String references are graph edges.** Route names, task and queue names, event
topics, feature-flag keys, dependency-injection keys, template names, config keys,
reflection targets and table names in raw SQL connect code that no call graph
shows. Include them in reachability, rename and deletion analysis. Meta's SCARF,
for example, combines per-language dependency graphs with usage signals such as
API endpoints, logs and template rendering before it proposes a deletion.

Useful mechanical comparisons when the project already uses the tool:
`buf breaking` for protobuf, `oasdiff` for OpenAPI, Pact contract tests,
`alembic check`, `makemigrations --check`, `prisma migrate diff`, and a diff of
environment keys read in code against keys defined in deployment manifests.
Treat their output like any candidate generator and confirm the reachable consequence.

## Performance reasoning

For serial stages measured against the same baseline, total time is the sum of
stage times. If baseline fractions are p_i and stage slowdown factors s_i,
the normalized total is sum(p_i * s_i), with unchanged fractions included.
Same-path membership is not a justification for multiplying slowdown factors.
Nested iteration can multiply work counts; establish its actual algorithm.

Example: two 10 ms stages each become 20 ms: total 20 → 40 ms, a 2x slowdown.
A stage occupying 1% of time becoming 5x slower gives 0.99 + 0.01*5 = 1.04x.

Validate comparable outputs and workload sizes; record environment, compiler
mode, warmup, samples, median/spread and relevant concurrency/cache state.
Use multiple sizes to investigate growth; a single ratio does not prove O(n)
or O(log n). CPU profiles alone do not account for blocked I/O wall time.
Use profiling and controlled changes to support causal attribution.

Do not weaken durability, isolation or authorization to win a benchmark.

## Other systemic candidates

- **Ghost fast path:** suitable inputs never reach the intended path. Verify
  dispatch and workload; some valid inputs should correctly take a slower path.
- **Contract drift:** callers rely on old return/error/default/serialization
  semantics. Inspect the actual interface boundary and affected variants.
- **Intent gap:** behavior disagrees with a documented requirement even though
  local tests pass. Do not infer domain requirements solely from function names.
- **Circular tests:** the oracle reuses the implementation under test, or a wrong
  implementation still passes. Try a targeted counterexample/mutation.
- **Dependency confusion:** declared identity, configured registry, resolved
  version and imported API disagree. Registry existence does not prove safety.
- **State rebuild / retry overhead:** repeated work or unbounded retries on a
  reachable path. Verify the reason, resource budget and failure behavior.

## External candidate generators

These tools nominate candidates; their output stays a **hypothesis** until the
evidence procedure in SKILL.md confirms a reachable consequence. Use a tool only
when the project already has it or the user approves installing it. Record its
version, configuration and complete output, and run it in a disposable copy when
it writes caches or reports into the tree.

| Tool | Adds | Limits |
|---|---|---|
| Go `deadcode` | Rapid Type Analysis from `main` packages; `-whylive` prints the call path that keeps a function alive; `-test` adds test executables | No roots in libraries without `main`; reflection, assembly and `go:linkname` need separate checks |
| `staticcheck` U1000, Knip, Vulture, compiler lints | Unused identifiers, files, exports and dependencies | Configuration and roots decide the result; apply the reachability procedure |
| jscpd | Token-based clone detection across many languages; its clone-type guide covers identifier- and literal-insensitive matching for renamed (Type-2) clones | Similar is not redundant; apply the redundancy table |
| Mutation testing: mutmut, cargo-mutants, Stryker, PIT | Whether tests detect deliberate faults; surviving mutants point at weak oracles | Equivalent mutants survive legitimately; run on focused targets, not the whole repository |
| Race detectors: TSan, `go test -race`, loom | Data races and explored interleavings | Only paths the run executes or the model enumerates |
| Static analyzer plus LLM triage | Fewer false positives from CodeQL-style results, or extra candidates from inferred specifications | Triage can drop true positives and degrades on long contexts and chained conditions; keep dropped items visible |
| SCIP indexes: scip-python, scip-typescript, scip-java, scip-clang, rust-analyzer | Precise cross-file definitions and references for the structural-tools step | Built for one build configuration; stale after edits |

## Sources and provenance

Primary sources checked on 2026-11-03:

- [Knip entry files](https://knip.dev/explanations/entry-files) and
  [graph interpretation](https://knip.dev/explanations/how-knip-works):
  root/configuration gaps can cascade into false unused-code reports.
- [Vulture documentation](https://github.com/jendrikseipp/vulture):
  Python's dynamic behavior requires reviewing candidates and specific whitelists.
- [rustc dead_code](https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html#dead-code):
  unused, unexported items; this is not a whole-system public API usage proof.
- [GitHub required-check semantics](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)
  and [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax):
  trace skipped/failed jobs and their consumers.
- [Feature Toggles](https://martinfowler.com/articles/feature-toggles.html):
  distinguish flag purpose and lifecycle before retirement.
- [USENIX Security 2025 package-hallucination study](https://www.usenix.org/system/files/usenixsecurity25-spracklen.pdf):
  19.7% of recommended package references in that experiment were hallucinated,
  not 19.7% of all code samples or current code. Historical motivation only.

Additional sources consulted for the November 2026 revision:

- [SWR-Bench](https://arxiv.org/abs/2509.01494): review recall falls as the number
  of issues per change grows; aggregating independent runs raised recall.
- [OpenCodeReview](https://arxiv.org/abs/2608.09290): deterministic per-file dispatch
  and a falsification-only reflector that sees the diff, not the reviewer's context.
- [CR-Bench-v2](https://arxiv.org/abs/2611.02566): leading systems found roughly a
  third of known defects; self-reflection improved detection.
- [Trail of Bits differential-review](https://github.com/trailofbits/skills/tree/main/plugins/differential-review):
  size-tiered review depth and caller-count blast radius.
- [Meta SCARF](https://engineering.fb.com/2023/10/24/data-infrastructure/automating-dead-code-cleanup/):
  dead-code removal over a combined cross-language dependency graph.
- [Meta ACH](https://arxiv.org/abs/2501.12862): mutation-guided test generation;
  line coverage alone would have rejected about half of the tests that killed mutants.
- [Go deadcode](https://go.dev/blog/deadcode), [jscpd clone types](https://jscpd.dev/guides/clone-types),
  [IRIS](https://arxiv.org/abs/2405.17238), [LLM false-positive reduction](https://arxiv.org/abs/2601.18844)
  and [SCIP](https://github.com/scip-code/scip): candidate generators listed above.

A real case study needs a source URL, revision, workload and evidence artifact.
Never present invented file locations, timings or profiles as reproduced results.
