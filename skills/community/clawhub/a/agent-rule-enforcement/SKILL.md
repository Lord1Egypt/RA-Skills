---
name: agent-rule-enforcement
description: "Audit whether an agent's written rules are actually enforceable: classify each rule as interception, exit gate, detection, or prompt-only, compute blocking coverage, and run behavioral checks over event logs. Use when a rulebook has grown, when someone asks whether rules are really followed, or after changing agent instructions. Tool-agnostic; works on Markdown rules and JSONL event logs."
license: MIT
---

# Agent Rule Enforcement

Rules are cheap to write and expensive to enforce. This skill separates three questions that usually get merged:

1. **What did we write?** (rulebook audit)
2. **What actually happens?** (behavior audit over logs)
3. **What would make it stick?** (conversion to an enforcement point)

> Developed through agent operation and corrected against real failures, not hand-authored as a prompt template.

## Applicability

**Use for**
- A rulebook or system prompt that has grown past what anyone can track.
- The question “are these rules actually followed, or just written?”
- Measuring whether a rules change improved enforcement rather than adding more text.

**Do not use for**
- Drafting new policy. This audits enforcement, not intent.
- Compliance certification. Coverage is a structural metric, not an assurance of correct behaviour.
- Rule sets with no execution surface at all (pure advice documents).

## Boundary

Required: a rule file in Markdown or plain text, and read access to execution artefacts (scripts, hooks, logs) if they exist.

Optional: an event log (JSONL) for the behavior audit; tool-policy configuration; exit-code gates.

Known limits:
- Tier classification is judgement. Keyword heuristics are a starting point, not a verdict.
- Coverage counts rules, not strength. One interception can matter more than twenty detections.
- A rule classified as “detected” may still be routinely violated; detection is not correction.
- This skill cannot prove safety or correctness; it can only show where enforcement is absent.

## Part A — Rulebook audit

### A1. Quantify the surface

Count must-clauses separately from descriptive prose. Only must/shall/required/never-style statements enter the audit.

**Completion criterion:** a number for must-clauses, plus the file and line range audited.

### A2. Inventory the executors

List everything that can actually stop or detect something: pre-action checks, tool policies, exit-code gates, scheduled audits, CI checks.

**Completion criterion:** each executor names the rules it covers.

### A3. Classify every must-clause into exactly one tier

| Tier | Test | Example |
|---|---|---|
| **Interception** | The action cannot complete without passing | tool not mounted, permission denied, sandbox boundary |
| **Exit gate** | A script returns non-zero and blocks “done” | deliverable check, linter, schema validation |
| **Detection** | A later scan can find it, but nothing stops it | transcript audit, log query, periodic report |
| **Prompt-only** | Written in the rule file, no checker anywhere | “ask when unsure” |

**Completion criterion:** every must-clause has one tier; counts sum to the total.

### A4. Compute blocking coverage

`blocking coverage = (interception + exit gate) / must-clauses`

Report detection coverage separately. **Never merge the two.** A rule that can be found afterwards is not a rule that is enforced.

**Completion criterion:** both percentages present, with the formula shown.

## Part B — Behavior audit

Structure inspection says what could happen; logs say what did. Run both, and keep the conclusions separate.

### B1. Define observable checks

A check must be a predicate over event fields, not a reading of intent. Good checks:

| Check | Predicate |
|---|---|
| Long task, no checkpoint | `duration_ms > threshold and checkpoint_count == 0` |
| Retry storm | `same tool called >= N times consecutively after errors` |
| Silent failure | `outcome == error and user_visible_message == false` |
| Unverified claim | `task produced claims and tool_calls == 0` |

**Completion criterion:** every check names the fields it reads and the threshold it uses.

### B2. Segment tasks

Group events into tasks by session and idle gap. State the gap and why; segmentation is a judgement that changes every count.

**Completion criterion:** segmentation rule written down; task count reported.

### B3. Run and report

Report per-check: hits, base (how many tasks were eligible), rate. Do not report a naked hit count.

**Completion criterion:** each check has hits / base / rate, and the log window is stated.

### B4. Calibrate before trusting

Run the audit on a period where you know the answer. If the checks fire on known-good runs, the checks are wrong — fix the predicate, not the threshold.

**Completion criterion:** at least one false-positive check documented and corrected, or an explicit note that calibration was not performed.

## Part C — Conversion

Order of leverage, most to least:

1. **Move the rule to an interception point** — tool policy, permission, sandbox. Cheapest and strongest.
2. **Add an exit gate** — a script that returns non-zero. Start as warning-only, promote after a clean week.
3. **Keep detection** — only where interception is impossible (e.g. judgement calls).
4. **Leave as prompt** — only for rules that genuinely need judgement, and accept that they will sometimes be missed.

Output at most three conversion proposals. Each must name the execution point: script, tool policy, or pre-action step. “Rewrite the rule more forcefully” is not a proposal.

**Completion criterion:** each proposal states where it executes and how it fails.

## Scripts

- `scripts/rule_scan.py <rules.md>` — counts must-clauses and emits a CSV skeleton for manual tier assignment. Heuristic suggestions only.
- `scripts/audit_events.py <events.jsonl>` — runs the built-in checks and prints JSON. Event schema is documented in `references/checks.md`.

## Discipline

- Enforcement improves by changing the execution point, not by adding clauses.
- Do not describe detection as blocking. That single confusion inflates every coverage number.
- Coverage counts rules, not strength. Report strong conversions separately from the percentage.
- Convert rules in small batches and re-measure; a rulebook rewrite without re-measurement is unverified.

## Final self-check

1. Must-clause count and audited file stated.
2. Every clause has exactly one tier.
3. Blocking and detection coverage reported separately.
4. Behavior checks name fields and thresholds.
5. Calibration performed, or explicitly marked as not performed.
6. At most three conversion proposals, each with an execution point.
