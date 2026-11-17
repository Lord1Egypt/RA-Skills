---
name: audit
description: Audit a codebase through every lens its stack calls for, verify each finding, cluster them by root cause, deliver the fixes as a ticketed map, and untangle the structure.
disable-model-invocation: true
argument-hint: "[path] [--lens a,b] [--since REF] [--fix] [--untangle [area|ticket]] [--out DIR]"
metadata:
  openclaw:
    homepage: https://github.com/OrenSegal/codebase-audit
    requires:
      bins: [python3, git]
---

Run an adversarial audit of this codebase and finish it. Report and deliver first; change source code only with `--fix` or once the user picks fixes.

You are the **adversary**. Every lens asks one question from a different angle: what input, timing, user or attacker makes this code give a wrong answer, lose data, leak data, or strand the user?

This folder holds everything the audit needs. Resolve these paths from this file's directory:

- `lenses/<lens>.md`: one per lens. Its `Fires:` line says when the lens runs (`always`, or `when <condition>`). Each probe is either **unconditional** (always answered) or marked `(when <condition>)` (answered when the condition holds, otherwise closed as not applicable). Then the artifact the lens produces, and its done line.
- `scripts/scan.py`: fingerprints the repo, routes lenses, and lists the project's own analyzers to run. `scripts/signals.tsv`: every detection and seed pattern; `scripts/tools.tsv`: every analyzer it knows. A project adds its own rows in `docs/agents/audit-signals.tsv`.
- `scripts/verify.py`: checks findings files against the lens files. `scripts/cochange.sh`: files that change together.
- `DELIVER.md`: hand-off notes, the audit map and its tickets.
- `UNTANGLE.md`: the structural refactor, for `--untangle` and for structural tickets.

## 1. Scope

- Arguments: a path (default: repo root); `--lens a,b` to run only those; `--since REF` to audit what changed since a ref (a PR base, or the last audit's commit); `--fix`; `--untangle [area|ticket]` to skip straight to `UNTANGLE.md`; `--out DIR` (default `.audit/`).
- When no answer can arrive (CI, `claude -p`), unanswered questions stay on `HANDOFF.md` as open questions, delivery goes to the local tracker only, and source stays untouched unless a ticket is on the `approved:` line.
- Create the output directory with a `.gitignore` containing `*`, so the audit touches no tracked file. When starting a new run (never when resuming), first move an earlier run's `RUN.md`, `REPORT.md` and `findings/` to `<out>/history/<its date>/`, so the new run can compare against it.
- **Resume**: if `<out>/HANDOFF.md` exists, continue from its `next` phase, leaving the run's files where they are. Tickets on its `approved:` line are cleared for source changes without asking again; work the first one on the frontier, one ticket per session, as `DELIVER.md` says. Any other ticket goes back to the user first. If an earlier run exists in `history/`, offer `--since <its commit>` and carry `refuted.md` forward.

Every phase below ends by rewriting `<out>/HANDOFF.md` as `DELIVER.md` describes.

## 2. Scan and recon

Run `python3 scripts/scan.py <path> [--since REF] [--lens a,b] > <out>/SCAN.md`, so `SCAN.md` is the script's raw output: stacks, packages, which lenses fire and why, hot spots, the execution plan, the analyzers to run, candidate sites per probe (hottest files first), and special-case counts.

Run each analyzer listed under **Tools** whose command is available, saving its output to `<out>/tools/<tool>.txt`. Their warnings are leads for the lens each row names, the same as scan sites; a tool that is missing or fails is noted in `RECON.md`, never installed.

Then write `<out>/RECON.md`, completing what a script cannot see. Finish only when every heading has an answer or `none`:

- **Boundaries**: every place outside data enters (HTTP, webhooks, DB reads, files, env, deep links, push payloads, model output, user input).
- **Persistence**: local stores, server DB, caches, queues, and which one owns each fact.
- **Critical paths**: money, auth, data deletion, migrations, anything safety-related, the main user loop.
- **Commands**: build, test, lint, run; whether tests pass now.
- **House rules**: `CLAUDE.md`/`AGENTS.md`; the domain language in `GLOSSARY.md` (or `GLOSSARY-MAP.md`), used for every name in findings and fixes; ADRs, whose accepted risks stay settled unless the risk changed; the issue tracker in `docs/agents/`.
- **Conditions**: for each firing lens, which conditional probes hold here, with evidence.
- **Lens overrides**: a lens the scan skipped that recon shows is needed, or one fired by a false signal, with the reason.

Write `<out>/RUN.md`: commit, date, arguments, final lens list.

## 3. Hunt

Follow the scan's plan: **sequential** runs each lens here, one after another; **parallel** gives each lens a subagent, and a sharded lens one subagent per listed package. A host that caps concurrency runs waves, pairing the lenses with the fewest sites; a host without subagents runs everything in sequence.

Subagents start with no skills and none of this conversation, so each brief stands alone. It names: the lens file, this file (for **Methods** and **Finding format**), `RECON.md`, the lens's section of `SCAN.md`, the scope, and the output path `<out>/findings/<lens>[-<package>].md`. Hunters are read-only leaves: they read code, run tests, scripts and the app, write only their findings file and repros, and return to the main context, which alone dispatches.

### Methods

- **Pre-mortem**: three months after launch, the top 1-star review is about this area. Write it, then find the code that caused it.
- **Inversion**: how would you make this feature fail as badly as possible? Check the code blocks each way.
- **Assumption ledger**: for each function on a critical path, list what it assumes. Which does a type or constraint enforce, and which rely on hope?
- **Chesterton's fence**: before calling a guard, special case or odd line a bug, find why it exists (`git log -L`, blame, the PR). A fence with a live reason is not a finding.
- **Candidates are leads**: a scan site is a place to start reading. A probe with zero sites is still answered, and a site becomes a finding only with a concrete scenario.

### Finding format

```
### <LENS>-<n> <the claim in under 60 chars>
- where: path:line
- probe: <probe id from the lens file>
- scenario: <concrete input, state or timing> → <wrong outcome a user or system sees>
- severity: critical | high | medium | low
- detectability: loud (crash, alert, test fails) | quiet (wrong answer someone may notice) | silent (nobody will notice)
- verdict: CONFIRMED (<the test, script, query or screenshot that reproduced it>) | PLAUSIBLE (reasoned, not run)
- fix family: <the kind of change, not the patch>
```

**Severity**: critical loses or corrupts data, breaches security or privacy, gets money wrong, or risks safety; high shows a wrong answer or strands the user on a common path; medium does so on a rare path or degrades quality; low is hygiene. Severity is set by who can trigger it today in the shipped configuration: a critical or high scenario names that person (any visitor, any signed-in user, an attacker holding X); a path only an operator or a dead config reaches drops a level.

**Redact**: findings, repros, reports and tickets get shared. Write `<REDACTED>` in place of any secret, token or personal data, and point at where it lives instead of quoting it.

A findings file opens with the lens's artifact. Every probe ends in at least one finding or one `clean:` line: `clean: <probe> — <evidence>`, or for a conditional probe whose condition does not hold, `clean: <probe> — n/a: <why>`. A hunter is done when its done line holds and `python3 scripts/verify.py <out> --root <path> --lens <lens>` passes.

## 4. Verify

1. **Merge duplicates** across lenses: when two findings share a location and mechanism, keep the more severe block, add `- also: <the other ids>` to it, and delete the other block, so each problem appears once.
2. **Refute**: every critical or high finding gets a fresh refuter; the rest are batched by lens. A refuter gets the finding block only, never the hunter's reasoning. For a `PLAUSIBLE` finding it tries to kill the claim: a guard upstream, a constraint in the DB, an unreachable path, a fence with a reason. For a `CONFIRMED` finding it checks the repro: does it go red for the stated reason, through code a real user or attacker reaches? When the host offers a different model, refuters use it, since shared biases make same-model agreement weak evidence.
3. **Promote by evidence**: survived and reproduced → `CONFIRMED`; survived on reasoning → `PLAUSIBLE`; killed → `<out>/refuted.md` with the reason.
4. **Coverage critic**: one fresh subagent gets `RECON.md`'s critical paths and every lens's `clean:` lines, and names each critical path whose evidence is thin (a sentence where a trace or a test was needed) or that no lens reached. Each one goes back to the matching lens for a second look before the report.

A repro is a **tight** feedback loop that goes **red** on this finding and no other: a failing test at the nearest seam, a script, a query. Build one wherever it costs under ten minutes, in `<out>/repro/`, against local, branch, sandbox or test-mode systems only. A finding killed by a reason that will hold next quarter (an accepted risk, a deliberate trade-off) belongs in an ADR, offered at delivery, so later audits read it in recon.

## 5. Report

Write `<out>/REPORT.md`:

1. **Summary**: counts by severity and lens, and the three fixes to make first, with why.
2. **Fixes**: cluster findings by root cause, each fix written above the findings it solves; look for the one fix behind several findings, which often looks nothing like them. Tag each `structural` (coupling, duplication, a missing type, a shallow module, a misplaced seam) or `local` (one place, one change), and describe structural fixes in the deep-module vocabulary: **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**, the **deletion test**.
3. **Unclustered findings**, ranked by severity, then detectability (silent first), then reach.
4. **Coverage**: every lens's `clean:` lines, skipped lenses with their reasons, analyzers run or missing, and what the coverage critic sent back.
5. **Since last audit**, when `history/` holds an earlier run: fixed, still open, new, and regressed (fixed before, back now).

```
- Make the server the only writer of `scan_count`, decremented atomically with `where scan_count > 0`, so the client cannot drift, double-spend or reset it. [structural, critical]
  - MONEY-2 `ScanQuota.swift:40` decrements locally before the upload, and again on retry.
  - MONEY-3 reinstalling the app resets `scansUsed` in local storage to 0.
  - STATE-5 the weekly quota resets on the device's local Monday, so flying west grants a second week.
```

Run `python3 scripts/verify.py <out> --root <path>`; the report is final when it passes. When the host renders structured findings (a `ReportFindings` tool), also report every surviving finding there, most severe first.

**Tune** the funnel for this project: a seed row whose sites all ended refuted or clean, or a finding no seed pointed at, is a proposed row for the project's `docs/agents/audit-signals.tsv`. List the proposals in the report; they are written only when the user accepts them.

## 6. Deliver and hand off

Read `DELIVER.md`. Chart the report as an audit map with one ticket per fix, typed, with blocking edges, on the repo's issue tracker (local `.scratch/` when none is configured; confirm before posting to a remote tracker). Then ask which fixes to start as one **grilling** round: number each as a question with your recommended answer, worded so "yes" accepts it. With `--fix`, take every recommendation. Record the approved ticket numbers on `HANDOFF.md`'s `approved:` line.

Route each ticket by its shape. The named skills are mattpocock-skills; call one with the Skill tool when available, and otherwise do its step inline:

| Ticket shape | Route |
|---|---|
| Needs a decision first: where a seam goes, an ADR it contradicts, a fuzzy domain term, a risk to accept | `grill-with-docs`, which records the answer as an ADR and glossary terms |
| Structural, one module, worth exploring with the user before committing | `improve-codebase-architecture` on that area |
| Structural, competing interface designs | `codebase-design`, its design-it-twice pattern |
| Structural, the way is clear and it fits one session | `UNTANGLE.md`, with the ticket and `REPORT.md` as its starting list |
| Structural, larger than one session | `wayfinder`, charting decision tickets toward the destination |
| Many fixes to slice for agents working unattended | `to-tickets` (tracer-bullet slices, blocking edges, wide refactors as expand–contract), then `implement` |
| Local fix | `tdd`: the repro is the first red test, at a seam agreed with the user; the full suite stays green |
| `PLAUSIBLE` and critical, no repro yet | `diagnosing-bugs` phase 1: build the tight loop first |

When the frontier is empty, re-audit with `--since <the audit commit>`. The audit's destination is a re-audit that verifies with no surviving critical or high finding.

## Done when

- Every firing lens has a findings file that meets its done line, and `verify.py` passes on the whole output.
- Every surviving finding has a location, probe, scenario, severity, detectability and verdict; every killed one is in `refuted.md`.
- `REPORT.md` places every finding under a fix or in the unclustered list, the map holds one ticket per fix, and `HANDOFF.md` names the next ticket.
