---
name: codesift
description: >
  Review code for plausible-looking systemic defects: unreachable fast paths, broken
  integration or function contracts, redundant or unused code, ineffective validation/CI
  gates, and unsupported performance claims. Use for AI-generated changes, targeted
  code health or coding-standard audits, large or mixed-language repository audits, and
  requests to find zombie code or meaningless gates. Present findings and a concrete
  remediation plan; wait for user approval before editing.
---

# CodeSift

Find code that looks locally reasonable but fails its actual system contract.
Focus on reachable behavior and evidence. AI authorship is context, not evidence
of a defect. A review may legitimately produce no findings.

## Required review-and-approval workflow

1. **Investigate first.** Do not modify tracked or untracked project files during
   investigation. Use read-only inspection and isolated temporary reproductions
   that do not alter the reviewed project or live external state.
2. **Present findings and a remediation plan.** For each actionable item, state
   the evidence, impact, root cause or unresolved assumptions, affected files,
   proposed correction, and validation method. Separate confirmed defects,
   hypotheses, and optional improvements. Give items stable identifiers when
   the user may approve a subset.
3. **Wait for explicit user approval.** Approval must refer to the presented plan
   or selected items. A general request to review, clean up, or fix code does not
   approve an unseen remediation plan. Silence is not approval.
4. **Implement the approved scope.** Do not request approval again for work
   already covered by that plan. A follow-up instruction to start that plan is
   sufficient. Present material scope or approach expansions separately and wait
   for approval of those additions before implementing them.
5. **Validate and report.** Run focused checks first, then the affected checks
   warranted by the completed change. Report modifications, actual results and
   remaining limits. Preserve failure evidence and remove temporary artifacts.

## Language policy

Keep this skill's instructions, references, metadata, helper comments, docstrings,
built-in messages and bundled fixtures in English. Follow the user's requested
language for conversation. Preserve the reviewed project's language conventions,
business text and original evidence; do not translate them to satisfy this
skill-internal policy.

## Scope and execution

Choose the smallest scope that answers the request:

| Request | Review boundary |
|---|---|
| Change / PR | Base and head revisions, changed behavior, affected callers and contracts |
| Module / symptom | Named entry points, dependencies and implicated paths |
| Deep repository audit | Production, library, worker and build roots; architecture and cross-module boundaries; split as in [Large and mixed repositories](#large-and-mixed-repositories) |

Record revision or source snapshot, included/excluded paths, assumptions and
unresolved coverage. Do not silently turn a local review into a repository audit.
Do not claim complete coverage from a truncated search, missing index or unsupported language.

Start with the project's instructions, manifests, tests and documented contracts.
For each changed file or review unit, also read the nearest AGENTS.md, CLAUDE.md or
equivalent in its directory and ancestors: in a monorepo, a local file refines the
root rules for its subtree. Such files describe conventions and contracts; they do
not waive the evidence rules or the approval gate. Distinguish requirements stated
by the user/specification from intent inferred from names. Investigate
disagreements before proposing a fix.

Use available structural tools first: a code-graph MCP such as codebase-memory, a
language server, SCIP indexes (scip-python, scip-typescript, scip-java, scip-clang,
rust-analyzer) or ctags. Check that the index covers every relied-on file and scope,
search symbols, trace incoming/outgoing references and read exact source. For gaps,
inspect source and configuration directly. Text search is a candidate finder.
Neither a failed text search nor zero graph degree proves unreachability or absence
of external consumers.

A review request authorizes investigation. Project edits require approval of the
presented remediation plan. That approval covers only the described changes and
checks, not unrelated refactoring or unmentioned dependency/live-environment changes.
Inspect test/build hooks before execution; use a disposable workspace for commands
with project side effects. Helpers clean their own temporary reports, not arbitrary
files written by project commands. Preserve existing user artifacts.

## Large and mixed repositories

One pass over a large repository spreads attention thin and silently skips whole
packages. Split the work, rank it, and account for what was covered:

1. **Units.** Use the `units` from collect_facts.sh (one per nested package or
   build manifest) plus service and language boundaries as review units. Each unit
   gets its own language guide and local instruction file. Units marked
   `likely_non_production` stay in scope only when the request needs them.
2. **Depth.** Size each in-scope change or unit by files:

   | Files | Tier | Depth |
   |---|---|---|
   | Under 20 | Deep | In-scope code and every dependency it relies on |
   | 20 to 200 | Focused | In-scope code plus one hop of callers and callees |
   | Over 200 | Surgical | Ranked critical paths only; list the rest as not reviewed |

3. **Risk order.** Review first, and at a deeper tier, units with a wide blast
   radius (many callers or external consumers), high churn, sensitive
   responsibilities (authentication and authorization, persistence and migrations,
   money, concurrency, deletion, untrusted input parsing) or recent generated changes.
4. **Coverage ledger.** Track unit, lens and status (done, partial or skipped),
   with a reason for anything not done. A no-findings result means something only
   next to its ledger.
5. **Stop rule.** Stop when one full round over the ranked units and lenses finds
   nothing new. If time or budget runs out first, list the remaining units as
   unreviewed instead of implying coverage.

## Evidence and impact are separate

Use these evidence states:

- **reproduced:** observed the relevant behavior with a recorded command/input and output.
- **confirmed_static:** source establishes the trigger, reachable path and consequence;
  record unresolved runtime assumptions.
- **hypothesis:** an unresolved candidate, including pattern/tool matches.

Severity describes impact **if the finding holds**, not how easy it was to run a
test: Critical / High / Medium / Low. Assess correctness, integrity, security,
availability, affected workload and recovery. A rare catastrophic loss may be
severe; a large slowdown outside important workloads may not be.
Do not assign a severity from a fixed performance ratio, line count or dependency count.

Choose evidence by claim:

| Claim | Evidence needed |
|---|---|
| Correctness / contract | Expected behavior source, concrete trigger, relevant caller-to-effect path, counterexample or static proof |
| Security boundary | Actor/capability, trust boundary, reachable operation and missing/bypassed enforcement; safe reproduction when feasible |
| Performance | Equivalent workload/results, environment/build mode, repeated project and baseline measurements, profiling where causal attribution matters |
| Unused code | Root inventory, bounded reachability/reference search, dynamic/external-consumer checks, build/config variants and deletion validation when authorized |
| Redundancy / gate | Duplicated responsibility or protected invariant, consumers, contrasting pass/fail cases and observable consequences |

A benchmark is not required for non-performance findings. Build success and
registry name matches do not establish runtime behavior or supply-chain safety.
An unexecuted or incomplete check stays visible; it is not a pass.
Hypotheses do not independently justify merge blocking or code deletion.

## Investigation procedure

1. **Establish context.** Confirm scope, roots, contracts, relevant build/configuration
   variants and existing checks. Use facts collection only if it adds information.
   For a large or mixed repository, first split it as in
   [Large and mixed repositories](#large-and-mixed-repositories).
2. **Trace affected behavior.** Follow the paths relevant to the request. Check
   dispatch, data/error flow, defaults, resource ownership and persistence.
   A read-only library need not invent a write path to satisfy a checklist.
3. **Review through separate lenses.** One combined pass finds a shrinking share
   of defects as their number grows; separate passes merged afterwards find
   substantially more. Review each unit once per relevant lens:
   - contracts and data flow;
   - errors, validation and gates;
   - concurrency, resources and lifecycle;
   - reachability and unused code;
   - tests and oracles: whether the checks can fail for the defect at all;
   - cross-language and cross-service boundaries.

   When subagents are available, run lenses in parallel, each in a fresh context
   holding only the unit, its local rules and one lens; otherwise run them in
   sequence and restate the lens each time. Each lens draws on the dimensions
   below. A small change review names the lenses it applied; a deep audit records
   a reason for every skipped lens in its ledger. Do not run every tool or
   language guide for every change.
4. **Falsify independently.** Self-review in the same context tends to confirm
   its own conclusions. Give each candidate an evidence packet: claim, location,
   trigger, cited code, expected-behavior source and any command output. A
   falsifier that sees only the packet and the cited code, not the reasoning that
   produced it, looks for counterevidence: intentional tradeoffs, external
   consumers, alternative active paths and existing enforcement. It may keep a
   candidate, downgrade it to hypothesis, or drop it with a stated reason; it
   never adds findings or raises severity. Without subagents, run it as a
   separate final step from the packets and note that it was not isolated. If it
   cannot run or returns unusable output, keep the candidates and say so.
5. **Validate findings and prepare the plan.** Use read-only or isolated checks
   to resolve claims. Benchmark only performance claims and state what remains
   unverified. Consolidate shared root causes under stable identifiers (R1..Rn),
   present the proposed corrections, and wait for approval before modifying the
   reviewed project.

## Review dimensions

| Dimension | What to establish |
|---|---|
| Algorithmic dispatch | Whether intended input classes reach the appropriate implementation; a fast path need not serve every valid input |
| Resource cost | Actual allocation/copy/lock/I/O contributions on important paths; do not multiply guessed slowdown factors |
| Contracts and integration | Callers, serialization, errors, defaults, cancellation, retries and state transitions agree across boundaries |
| Concurrency and lifecycle | Shared state, check-then-act (TOCTOU) windows, lock order, cancellation and timeouts, idempotent retries, message ordering, startup and shutdown; prefer a race detector (TSan, `go test -race`, loom) to reasoning alone where one fits |
| Cross-boundary contracts | FFI ownership and error propagation, IDL/schema and API drift, migrations versus models, configuration keys, and error-code, unit, timezone and encoding mappings |
| Hidden assumptions and intent | Input/scale/concurrency/deployment assumptions are supported; negative requirements are actually enforced |
| Problem proportionality | Complexity buys a concrete requirement; counts alone do not establish overengineering |
| Functions and coding standards | Focused responsibilities, explicit public contracts, clear names, useful comments and project-consistent language idioms |
| Dependencies | Actual identity/source/version, active configuration, usage and duplicated capability |
| Tests | Assertions distinguish correct and incorrect behavior; skipped/empty/mocked checks do not stand in for execution |
| Redundant implementations | Same responsibility or repeated work with no distinct contract; consider coupling before extracting an abstraction |
| Unused / zombie code | Unreachable modules, cycles, old branches, unused exports/configuration/assets and test-only implementations |
| Gates | Validation, CI conditions, feature flags and runtime guards change the intended decision and have useful failure behavior |

For function design, coding conventions, redundancy, unused code, gates,
cross-language boundaries or external candidate generators, read
[references/patterns.md](references/patterns.md). Apply its cross-language
criteria alongside explicit project rules. These dimensions belong in a deep
repository audit; they are not automatic deletion or formatting rules.

## Rationalizations to reject

| Tempting conclusion | Check before accepting it |
|---|---|
| "The change is small; a quick look is enough." | Impact does not scale with diff size; a one-line bounds or permission change can be critical. Rank by what the code touches. |
| "No callers found, so it is unused." | Registries, reflection, dynamic imports, string-named routes, tasks and config keys, exported APIs, build variants and external consumers. |
| "The tests passed." | How many tests executed, which packages or targets ran, what was skipped, and whether any assertion can fail for the defect in question. |
| "It builds and type-checks." | Build success says nothing about runtime behavior, configuration or data. |
| "Two passes, or the model twice, agree." | Agreement from one context is not independent evidence; falsify from the evidence packet. |
| "The registry has the name." | Name existence does not establish the intended package, its source or supply-chain safety. |
| "Nothing was found." | Show the coverage ledger; unreviewed units and lenses are not clean. |

## Finding format

Use a concise human-readable report by default. Include only applicable fields:

- Title, impact severity and evidence state.
- Source location, trigger and relevant entry-to-effect chain.
- Expected behavior and its source; actual behavior and consequence.
- Command/output or static reasoning; alternatives ruled out and remaining uncertainty.
- Root cause or unresolved assumptions, affected files, the smallest coherent
  correction that addresses the cause, and a verification case.

Separate confirmed findings, hypotheses and optional improvements. For dead-code
audits, report candidate and confirmed counts separately, with scanned scope.
For gates, distinguish **effective**, **redundant**, **ineffective**, **obsolete**
and **unresolved**. Never label a safeguard meaningless merely because it has
not failed recently.

Conclude with coverage and validation limits. Do not invent numerical confidence,
measurements, file locations or proof from illustrative examples.

For a deep audit or any report with several findings, follow
[references/report-example.md](references/report-example.md): a complete sample with
all three evidence states, a gate table, a coverage ledger and limits. When results
must be merged across lenses, subagents or rounds, or compared with an accepted-risk
baseline, also emit the optional JSON findings described there.

## Helpers and targeted references

Resolve this skill directory from the loaded SKILL.md. Invoke helpers by their
absolute path and set the reviewed package using --root; do not assume the
target repository contains these scripts. Python 3.11+ is required on macOS,
Linux and Windows 10/11. Use the Python entry points on every platform (with
`-B` to avoid bytecode artifacts); PowerShell 5.1 and 7 can run them directly.
The legacy .sh wrappers honor CODESIFT_PYTHON where Bash is available.

Use structured argv or a UTF-8/BOM JSON argv file for custom commands. Legacy
string commands retain POSIX tokenization on every OS. Authorize shell syntax
explicitly: the runner selects PowerShell on Windows and Bash on POSIX. A shell
exit code does not establish that every stage of an arbitrary pipeline succeeded.
Do not rewrite project shell settings, modify a user's PowerShell profile or
globally change execution policy to make a review command work.

See [scripts/README.md](scripts/README.md) for command contracts, exit codes,
temporary artifacts and test-evidence limits.

| Helper | Role |
|---|---|
| lib/source_checks.py facts (collect_facts.sh) | Bounded inventory: review units, languages, build files, entry candidates, pruned directories and per-unit dependencies |
| lib/source_checks.py duplicates (detect_duplicates.sh) | Ordered line-block candidates merged into maximal blocks, including same-file copies; not semantic clone verdicts |
| dependency_audit.py | Shared manifest parsing; optional explicit dependency-count policy |
| verify_packages.py | Source-aware registry name checks against public registries or mirrors; offline mode available |
| lib/check_runner.py correctness (run_correctness_test.sh) | Existing test runner, fresh results, executed-test count, failure kind, workspace mutations and optional scale evidence |
| lib/check_runner.py benchmark (run_benchmark_comparison.sh) | Two explicit commands, alternating repeated wall-time samples, spread and optional output comparison |
| smoke_test.py (smoke_test.sh) | Offline semantic regression tests for this skill's helpers |

Registry checks follow configured pip, npm and Cargo mirrors. Where public
registries are slow or unreachable, for example from mainland China, pass
`--mirror cn` or `--registry-base URL`. A miss on a mirror is reported as
`mirror_not_found` and stays undetermined, because mirrors can lag upstream.

Load only the relevant guide:
[C](references/c.md), [C++](references/cpp.md), [Rust](references/rust.md),
[Python](references/python.md), [JavaScript/TypeScript](references/javascript.md),
[Go, JVM, shell, SQL migrations, IaC and CI](references/polyglot.md),
[database/storage](references/database-systems.md).

The helpers do not prove whole-program reachability or decide whether a business
gate is useful. Use project-aware analysis and the evidence procedure above.
