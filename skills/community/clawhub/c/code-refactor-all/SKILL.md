---
slug: code-refactor-all
displayName: "code-refactor"
version: 1.0.2
name: code-refactor
description: Refactor, rewrite, port, migrate, or modernize existing source code - read this skill FIRST, before searching files or planning, even if the named files are not in the workspace. Covers refactor (split a god module into a package, untangle circular imports, move modules, change a signature across callers, swap an internal API or library across a codebase step by step), rewrite (re-implement a component from scratch or on a new framework, e.g. JS to TS + NestJS), and port / translate code to another language (Python to Go or Rust, pyo3 extensions, TS to Go, Java to Kotlin, C to Rust behind an unchanged C header) with fixture parity. Triggers - refactor, restructure, split modules, rewrite, reimplement, port, convert to another language, migrate to a framework, modernize, 重构, 拆分模块, 重写, 代码迁移, 移植到 Rust, 把 Python 改成 Go. Not for tidying one function (simplify-code), type hints, bug fixes, features, perf, database/schema/cloud/infra migrations (e.g. Postgres RDS to Cloud SQL), dependency bumps, or prose translation.
license: MIT
metadata:
  version: "1.0.2"
---

# Code Refactor · Rewrite · Port

Change the *shape* or the *language* of code while keeping what it *does*. The promise: every caller, test, and observable output behaves as before unless the user approved a difference. To keep it, pin behavior down **before** editing, move in green steps, and report evidence rather than confidence.

Local cleanup of one function or snippet belongs to `simplify-code`. If the request is that small, say so and hand it over.

## Read first (hard rules)

Read this SKILL.md top to bottom before anything else, even when the workspace is empty or the files the user names are missing. A missing file is not a reason to skip the skill: pick the mode, say what is missing, and deliver what the mode allows (a plan, a contract, or a port of the code the user pasted).

1. **Stay in the workspace.** Read and write only inside the given working directory. Never search the disk for other projects, and never read, reuse, or write sibling/parent project folders or earlier runs' outputs, even if they look like a head start.
2. **No installs.** Do not `brew install`, `apt`, `pip install` toolchains, add rustup components, or download compilers/SDKs without the user's approval. If a toolchain is missing, write "Not run: <tool> unavailable (<exact command>)", verify what you can with the tools present, and still deliver the code.
3. **Finish, don't hand off.** Do not end with "state saved to RESUME.md" / "say the word and I'll continue" while work can still proceed. Stop early only for a Gate, a denial, or the budget below, and then deliver the full report for what exists.
4. **Plan-only means no files.** If the user asks for a plan, review, or assessment, edit and create nothing; put the plan in the reply (write a file only if asked).
5. **Denied means stop.** If a command or deletion is denied, do not get the same effect another way; list it in the report.

## Budget (time and steps)

Runs are time-limited; a correct port with no report counts as a failure.
- **Smallest verifiable slice first:** get the contract, one end-to-end path, and the given fixtures/compare script green before anything else.
- **Checkpoint: report before hardening.** The moment the given fixtures/compare script first pass, write the Output-format report to `PORTING.md` (or the plan) with the current N/M result *before* running any generated/differential inputs. Every later milestone only updates it.
- **Stay in the input domain.** Differential mismatches on inputs the fixtures and contract do not cover (wrong types such as bools or mixed int/float, huge magnitudes, float summation order, exotic Unicode) go under Follow-ups as "outside contract"; do not fix them unless the user asked for full-domain parity.
- **Cap exploration:** at most one modest differential/fuzz run (hundreds to a few thousand inputs) and at most 3 fix-and-rerun rounds per mismatch class. Do not re-derive language runtime internals, hand-build Unicode tables, or chase cases outside the given fixtures and contract; list them under Follow-ups.
- **Milestones:** (1) mode + contract, (2) baseline/fixtures captured, (3) first green slice, (4) full fixtures green + report written, (5) optional extra hardening. If you have used roughly two thirds of your steps or time, stop hardening and deliver the final report.

## Pick the mode

| Signal in the request | Mode |
|---|---|
| Same language, structure is the problem (god module, tangled imports, wrong boundaries, widely used API needs a new shape) | **refactor**: existing code survives and moves in mechanical steps |
| Same language, existing code not worth evolving (unreadable legacy, dead framework, "rewrite / from scratch") | **rewrite**: the old implementation becomes the *oracle* |
| Target language differs | **port**: numbers, strings, errors, ordering, and concurrency semantics shift, so prove parity |

Rules of thumb:

- Prefer **refactor over rewrite** whenever an incremental path exists, because rewrites discard encoded edge-case knowledge. Choose a rewrite only when the user asks for one or it is clearly cheaper, and say why.
- Framework migrations (Express→Fastify, Vue→React, callbacks→async across a codebase) are **rewrite** when components are re-implemented, **refactor** when the change can be done as a mechanical, staged transformation.
- Port + redesign ("port to Go and clean it up") is two projects: port first, then refactor as a separate later step.

State the chosen mode in one line before starting, with the reason.

## Safety gates (all modes)

The workflows below enforce seven gates:
1. contract first;
2. a green safety net before edits (characterization tests where coverage is thin, `references/safety-net.md`);
3. a plan with sign-off when the blast radius is large;
4. structure and behavior never share a step (bugs go under "Found, not fixed");
5. small, revertible green steps (revert and go smaller when red);
6. the same proof re-run at the end (N inputs / M differences for rewrite/port);
7. a finished migration (no leftover shims or second live paths).

Never claim a check you did not run. "Not run: no Go toolchain available" is useful; a false "verified" is not.

### Keep the proof proportionate

- **One solid check per contract item.** Use fixtures and targeted edge cases, then one modest differential/fuzz run (hundreds to a few thousand inputs). Stop once every contract line has green evidence. Million-input soaks, sanitizers, or Miri are only for real risk (unsafe/FFI code, concurrency), and then only once.
- **Use the toolchain that is already there** (PATH, version managers, keg-only prefixes such as `/opt/homebrew/opt/openjdk@21`), inside this workspace only. No installs (hard rule 2).
- **Keep scaffolding out of the deliverable.** Keep real tests where the project keeps tests. Put scratch material (drivers, oracle copies) in one named directory and say so. Never leave large downloads in the repo.
- **Write the contract down early.** For multi-step ports or rewrites, keep the contract and its running evidence in the plan or a short `PORTING.md`, so the record survives an interrupted session.

## Workflows

Run the steps in order, and start a step only when the previous step's **Done when** holds. At a **Gate**, stop and wait unless the user already told you to proceed. Every workflow starts after the mode line and ends with the "Output format" report.

### Mode: refactor

**Step 1 — Write the contract.**
- *Action:* List the public surface (exports, flags, routes, formats, error messages), side effects and their order, and what may change. Find every caller, including hidden coupling (dynamic imports, reflection, DI, string-keyed registries, config/templates, tests that patch internals).
- *Output:* a 3–6 line contract plus a list of callers and coupling points.
- *Done when:* each public name and each external caller is accounted for.

**Step 2 — Record the baseline.**
- *Action:* Run the existing tests, type-checker, and linter. Where the code you will move is poorly covered, add characterization tests that record what it does today, bugs included (`references/safety-net.md`).
- *Output:* the exact baseline commands with their results (pass/fail counts, warnings), plus any new characterization tests.
- *Done when:* the safety net is green on the untouched code and covers each contract item.

**Step 3 — Plan the target shape and path.**
- *Action:* Describe the end state (a few lines or a before/after tree). Pick a pattern (`references/refactoring-catalog.md`): parallel change (API with many callers), forwarding shim (move), branch by abstraction (swap a subsystem), consumer-owned interface (break a cycle). Order the steps: contracts/types → implementations → callers → tests → shim removal. Each step should be a single kind of move.
- *Output:* a plan (`references/templates.md`) listing the steps in order.
- *Done when:* every step is small, independently revertible, and has a verification command. **Gate:** cross-module moves, public API changes, or deletions.

**Step 4 — Execute one step at a time.**
- *Action:* Apply one planned step, using IDE/LSP or codemod tools where possible. No bug fixes, taste renames, or upgrades; log those under "Found, not fixed".
- *Output:* one green change per step, plus an entry in the step log.
- *Done when:* the build, type-check, and Step 2 commands are all green, and a grep for string references to moved/renamed symbols is clean. If red, revert to the last green state and split the step.

**Step 5 — Remove scaffolding.**
- *Action:* Delete forwarding shims and adapters once no caller uses them. If the surface is public, keep a deprecation path and state it.
- *Output:* the final tree, plus a list of any shims still alive and the reason for each.
- *Done when:* there is one live path per behavior.

**Step 6 — Verify and report.**
- *Action:* Re-run exactly the Step 2 commands.
- *Output:* the report in "Output format", with before/after results.
- *Done when:* the after-results equal or exceed the baseline, and every claimed check was actually run.

### Mode: rewrite

**Step 1 — Justify the rewrite and inventory the behavior.**
- *Action:* State why an incremental refactor is not chosen. Inventory features, flags, error cases, odd behaviors, the performance envelope, and operational hooks (`references/rewrite-checklist.md`).
- *Output:* a one-line justification, plus the inventory (this is the definition of done).
- *Done when:* each public entry point and quirk appears in the inventory.

**Step 2 — Turn the old code into an oracle.**
- *Action:* Freeze a copy of the old implementation. Write characterization/golden tests whose expected values come from *running* it, not from reading it.
- *Output:* the golden tests or fixtures, plus the command that runs them.
- *Done when:* they pass on the old code, and a deliberate one-line mutation turns them red.

**Step 3 — Plan the seam and cutover.**
- *Action:* Choose how old and new coexist: same interface, adapter, flag, or route. Write the plan with the approved differences, the rollback, and the deletion date.
- *Output:* the rewrite plan (`references/templates.md`).
- *Done when:* the plan names the seam, the rollback, and any approved differences. **Gate.**

**Step 4 — Build the new implementation behind the seam.**
- *Action:* Implement against the same contract in modern idioms, without changing behavior.
- *Output:* the new code, plus the Step 2 suite running against it.
- *Done when:* the Step 2 suite passes on the new code.

**Step 5 — Differential run and triage.**
- *Action:* Run the same inputs (fixtures plus a modest generated set with odd types and edges) through old and new, then diff. Triage: new-code bug → fix; old bug the user approves changing → record; out of scope → accepted difference.
- *Output:* "N inputs, M differences", with each difference classified.
- *Done when:* M is 0, or every remaining difference is approved or accepted in writing.

**Step 6 — Cut over, delete, report.**
- *Action:* Switch callers, keep the rollback for the agreed period, then remove the old code.
- *Output:* the report in "Output format".
- *Done when:* there is a single live implementation, or the remaining one has an owner and a date.

### Mode: port

Target: the same behavior, written as a native of the target language would write it.

**Step 1 — Write the parity contract.**
- *Action:* Fill in the `references/port-playbook.md` template: unit of parity (function, CLI call, HTTP response, file); must-match items (outputs, exit codes, error classes, numbers, relied-on ordering); allowed differences; how parity is measured; end state A (standalone replacement), B (permanent bindings), or C (temporary bindings).
- *Output:* the contract, kept in the plan or in a short `PORTING.md` next to the new code.
- *Done when:* every observable output has a must-match or allowed-difference line.

**Step 2 — Inventory and choose the seam.**
- *Action:* Map modules and dependencies. Order the work leaf-first. Pick the seam where both implementations can be called: a CLI, HTTP, or FFI boundary.
- *Output:* the port order, plus the seam.
- *Done when:* each module has a slot in the order, and the seam can run both sides. **Gate:** multi-module ports.

**Step 3 — Characterize the source.**
- *Action:* Capture source behavior as language-neutral fixtures (input → expected output), produced by running the source. Cover error paths and the traps listed for the pair.
- *Output:* fixtures, plus a runner such as `compare.py "<cmd>"` that prints N/M.
- *Done when:* the source passes its own fixtures (N/0).

**Step 4 — Map the constructs before translating.**
- *Action:* For every construct, decide the target idiom: types and nullability, numbers (overflow, division, rounding), strings (bytes/UTF-16/code points), collection order, errors, resources, concurrency, and each dependency's equivalent. Use the pair's section in `references/port-pairs.md` (Python↔Go, Python↔Rust, JS/TS↔Rust, TS↔Go, Java↔Kotlin, C↔Rust). For other pairs, use the generic procedure in `references/port-playbook.md` section 8.
- *Output:* a short mapping table of the decisions that affect behavior.
- *Done when:* every trap the pair section lists for this code has a decision.

**Step 5 — Translate module by module.**
- *Action:* Port leaf-first in target idioms and layout, using the target's formatter, linter, and test framework. Port the source's unit tests as well. Leave out source-language workarounds and note each omission.
- *Output:* target code plus ported tests for each module.
- *Done when:* each module builds, passes lint and its ported tests, and passes the Step 3 fixtures that reach it.

**Step 6 — Prove parity.**
- *Action:* Run the shared fixtures, plus one modest generated differential set, against both implementations.
- *Output:* "N fixtures / M diffs; K generated / L diffs", plus accepted differences, each with a reason.
- *Done when:* every remaining difference is listed as allowed in the Step 1 contract. Anything else goes back to Step 5.

**Step 7 — Cut over and report.**
- *Action:* Apply the end state: replace the source, keep permanent bindings, or remove temporary ones.
- *Output:* the report in "Output format", including test parity (each source test has a target counterpart or a stated reason).
- *Done when:* the end state from Step 1 is reached, or the remaining work is listed under Follow-ups.

Port anti-patterns: line-by-line transliteration, `clone`/`unwrap`/`!!`/`any`/`interface{}` added just to compile, porting class hierarchies instead of behavior, fixing source bugs mid-port, inventing tests instead of reproducing behavior (more in `references/port-playbook.md`).

## Output format

Report in the user's language. Keep it short and evidence-based.

```
Mode: <refactor | rewrite | port (source → target)> — <one-line reason>
Summary: <what changed>; behavior/API <unchanged | changes listed under Needs approval>
Plan: <steps taken or proposed, in order; mark the current stop point if waiting for sign-off>
Changes:
- <step>: <what and why, one line>
Parity / verification:
- Baseline: <commands + results before>
- After: <same commands + results>
- Differential/fixtures: <N inputs compared, M differences, how triaged>   (rewrite/port)
- Not run: <what and why>
Not changed: <tempting edits deliberately left out (scope, API, semantics)>
Needs approval: <proposed behavior/API differences with a concrete input that would differ>   (omit if none)
Found, not fixed: <bugs discovered, with location and reproduction>   (omit if none)
Follow-ups: <redesign ideas, cleanup left for later, shims still alive and why>
```

Then show the diff, the new files, or the plan. If the user only asked for a plan or assessment, edit and create nothing (no plan file unless asked), put the plan in the reply, and say so.

## References

| File | Read when |
|---|---|
| `references/safety-net.md` | Code is poorly tested; setting up characterization, golden, or differential tests |
| `references/refactoring-catalog.md` | Planning a refactor: patterns, moves, codemod tools, risk |
| `references/rewrite-checklist.md` | Rewrite: go/no-go, inventory, cutover, rollback |
| `references/port-playbook.md` | Port: contract template, phases, semantic traps, anti-patterns |
| `references/port-pairs.md` | Port: mapping for the specific language pair (read only that section) |
| `references/templates.md` | Writing a plan or parity contract |
| `references/sources.md` | The user asks where a practice comes from |
