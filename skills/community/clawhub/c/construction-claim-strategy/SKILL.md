---
name: construction-claim-strategy
description: Strategic planning framework for construction claim responses — plan direction, scope, arguments, and disclosure strategy BEFORE selecting clauses or drafting. Covers situation assessment, scope control, direction decisions, argument ranking, disclosure control, response architecture, and risk assessment for EOT, delay, disruption, variation, and payment claims under PSSCOC, FIDIC, NEC, SIA, and bespoke forms. Includes practical checklists, quantum calculation methods, ADR strategies, delay analysis methods, concurrent delay, disruption claims, arbitration tactics, expert engagement, notice compliance, and legal precedent guidance.
---

# Construction Claim Strategy

**Strategic planning framework for construction claim responses.**

Plan your direction, scope, arguments, and disclosure strategy **before** selecting clauses or drafting correspondence.

---

## Why use this?

- Stop jumping straight to clause selection — plan the strategy first.
- Rank arguments by strength (Textual Interpretation is strongest).
- Control what to disclose precisely, keep general, or defer.
- Choose proven response structures.
- Avoid common mistakes that weaken your position.

---

## Who this is for

- Contract managers
- Claims consultants
- Quantity surveyors
- Commercial managers
- Construction lawyers
- Anyone preparing responses to claims or formal queries under construction contracts

---

## What this skill does

Use this tool to systematically work through 7 key dimensions:

1. **Situation Assessment** — Understand exactly what you are responding to.
2. **Scope Control** — Decide what to address and what to avoid volunteering.
3. **Direction Decision** — Choose primary and fallback arguments, and what to avoid.
4. **Argument Strategy** — Select the strongest type of argument available.
5. **Disclosure Control** — Decide what to state precisely, keep general, or defer.
6. **Response Architecture** — Choose the most effective structure for your reply.
7. **Risk Assessment** — Identify counter-arguments, weak points, and timing risks.

Plus **practical tools and reference guides** covering:

- Record keeping checklists
- Claim preparation checklists (adjudication & arbitration)
- Notice requirements compliance
- Expert engagement guidance
- ADR strategy (negotiation, mediation, adjudication, arbitration)
- Concurrent delay strategic approach
- Disruption claims strategy
- Delay analysis methods (As-Planned vs As-Built, TIA, Collapsed As-Built, Windows)
- Arbitration tactics and prolongation strategies
- Quantum calculation worked examples (Eichleay, Hudson, Emden, Measured Mile, Actual Cost, Total Cost)
- Legal precedents overview (Prevention Principle, Common Law vs Civil Law)
- Common pitfalls and how to avoid them
- Risk assessment framework

---

## Supported contract forms

Works with any construction contract form:
- PSSCOC (Construction Works / D&B)
- FIDIC (Red, Yellow, Silver, Emerald)
- NEC (NEC3, NEC4)
- SIA Conditions
- JCT
- Bespoke contract conditions

---

## Working out the actual deadline

Most construction claim responses are time-bound. Before using this skill, identify the actual calendar deadline for your response.

For Singapore matters under the Building and Construction Industry Security of Payment Act (SOPA), or for contracts using calendar-day notice periods (PSSCOC, SIA, FIDIC, NEC), the deadline calculation is not just "today + N days". It must account for:

- **Calendar-day counting** — Saturdays count; Sundays and public holidays generally do not, per s.50(a) of the Interpretation Act
- **In-lieu Mondays** where a public holiday falls on a Sunday
- **Ad-hoc declared holidays** (e.g. Polling Day) which are not in the standard gazetted list

The companion skill **construction-law** includes a Singapore SOPA deadline calculator that handles these rules. Calculate the actual deadline there first, then provide the resulting date when prompted by this skill.

If your contract is governed by a different jurisdiction, apply the equivalent local rule. Do not assume "calendar day" means simple date arithmetic — it almost never does.

---

## Start here

### Quick Reference (all strategy patterns)

```bash
python3 scripts/strategy_advisor.py --reference
```

Outputs all argument types, disclosure levels, response patterns, scope control rules, and risk checklists in one view.

### Interactive Strategy Session (Recommended)

```bash
python3 scripts/strategy_advisor.py
```

The wizard walks you through all 7 dimensions and produces a structured strategy report.

### Non-Interactive (from JSON)

```bash
python3 scripts/strategy_advisor.py --file strategy_input.json --output strategy_report.md
```

### Save Strategy for Reuse

```bash
python3 scripts/strategy_advisor.py --save-strategy my_strategy.json
```

---

## Examples

The `examples/` folder contains a worked scenario demonstrating the full 7-Dimension workflow:

| File | Description |
|------|-------------|
| `strategy_input.json` | Sample JSON input — PSSCOC 2014 (7th Edition) EOT scenario |
| `strategy_report_sample.md` | Generated strategy report from the above input |

**Note:** The example uses **PSSCOC 2014** clause references (Clauses 12.5, 14.2(m), 14.2(n), 22.1(h), 22.1(i), 14.3, 23.1). The **7-Dimension methodology itself is contract-form neutral** — it applies equally to FIDIC, NEC, SIA, JCT, and bespoke contracts. Future versions will include additional worked examples for other contract forms.

---

## Key Concepts

### Argument Strength Ranking

1. **Textual Interpretation** (Strongest) — Argue from the actual wording of the relevant clause in the Contract.
2. **Factual Distinction** (Strong) — Show that the facts fall outside the clause's scope or trigger conditions.
3. **Concede-then-Distinguish** (Moderate-Strong) — Acknowledge the normal case, then distinguish the current situation.
4. **Implied Terms** (Weakest) — Use only as a last resort when no express clause wording supports the position.

### Disclosure Control Levels

| Level | Use for |
|-------|---------|
| **State Precisely** | Clause references, formal correspondence, key dates, and legal reasoning |
| **Keep General** | Operational context and high-level details |
| **Defer** | Detailed quantification and supporting analysis |

### Recommended Response Patterns

- **Standard Query Response** — acknowledge, pivot, argue, reserve, close
- **Risk Allocation Rebuttal** — concede ordinary application, distinguish, factual support, legal conclusion, mitigation evidence, close cooperatively
- **Chronology-Based Response** — state known facts, flag pending items, commit to supplement, reserve
- **Cost / Quantum Claim Response** — contractual basis, heads of claim, ongoing assessment, commit to detailed breakdown, reserve
- **Reservation of Rights Closing** — always recommended

### Scope Control Rules

1. **Limit to letter** — respond only to what was asked; do not volunteer unrequested information.
2. **Preserve future claims** — use "reserves its position" and "without prejudice" language.
3. **Keep operational details general** — do not name specific zones or quantities prematurely.

### Common Anti-Patterns to Avoid

- ❌ Citing the wrong clause (e.g., a clause for other contractors when the Employer caused the issue)
- ❌ Leading with "the clause doesn't apply" — this antagonises the other party
- ❌ Volunteering information about topics not yet raised
- ❌ Naming specific zones/quantities before they are finalised
- ❌ Reaching for implied terms when express clause text supports your case
- ❌ Hedging dates that have formal letter references behind them
- ❌ Quantifying costs before records are complete

---

## How to use

### CLI options

```
usage: strategy_advisor [-h] [--file INPUT_JSON] [--output FILE]
                        [--format {md,txt}] [--save-strategy PATH]
                        [--reference] [--version]

Strategy Advisor — Strategic planning framework for construction claim
responses. Plan your direction, scope, and argument strategy BEFORE selecting
clauses.

options:
  -h, --help            show this help message and exit
  --file INPUT_JSON     Non-interactive: read strategy inputs from a JSON
                        file.
  --output, -o FILE     Write report to file instead of stdout.
  --format, -f {md,txt}
                        Output format (default: md).
  --save-strategy PATH  Save the strategy data as JSON for reuse.
  --reference           Print all reference tables (argument types, patterns,
                        etc.) and exit.
  --version             show program's version number and exit
```

### Required JSON keys (for `--file` mode)

The following 6 keys are **required** in the input JSON. If any are missing, the tool exits with a clear error listing what’s needed.

| Key | Description |
|-----|-------------|
| `situation_type` | What you’re dealing with (e.g. “Responding to a rejection of our claim”) |
| `other_side_position` | The other party’s stated position |
| `trigger_event` | Key facts / what triggered this response |
| `primary_argument` | Your primary contractual argument |
| `chosen_argument_type` | Argument type (e.g. “Textual Interpretation”) |
| `chosen_pattern` | Response architecture pattern (e.g. “Risk Allocation Rebuttal”) |

All other keys are optional — the tool fills empty fields gracefully. See `examples/strategy_input.json` for a complete example with all 21 supported keys.

### Commands

```bash
# Show all reference tables
python3 scripts/strategy_advisor.py --reference

# Run interactive wizard
python3 scripts/strategy_advisor.py

# Non-interactive from JSON
python3 scripts/strategy_advisor.py --file input.json --output report.md

# Save strategy for reuse
python3 scripts/strategy_advisor.py --save-strategy strategy.json
```

---

## Reference Library

All reference documents are in the `references/` folder. These are standalone reading material for human use — the `strategy_advisor.py` script does not load them at runtime.

| Document | Description |
|----------|-------------|
| `seven_dimensions_guide.md` | Full guide to the 7-Dimension framework |
| `argument_ranking_guide.md` | Detailed argument types with examples |
| `worked_examples.md` | 4 complete worked strategy examples (Variation, EOT, Disruption, Combined) |
| `delay_analysis_study_guide.md` | Comprehensive delay analysis study guide — SCL Protocol 22 principles, 7 analysis methods, concurrent delay, pacing, float, disruption, force majeure, case law |
| `quantum_worked_examples.md` | 8 quantum calculation examples (Eichleay, Hudson, Emden, Measured Mile, Actual Cost, Total Cost) |
| `adr_overview.md` | ADR methods comparison and strategy recommendations |
| `arbitration_tactics.md` | Arbitration tactics and prolongation claim strategies |
| `concurrent_delay.md` | Concurrent delay — strategic approach within the 7-Dimension framework |
| `disruption_claims.md` | Disruption claims strategy — Common Law vs Civil Law |
| `delay_analysis_methods.md` | Delay analysis methods — strategic overview |
| `legal_precedents.md` | Legal precedents and the Prevention Principle |
| `notice_requirements_checklist.md` | Notice compliance checklist |
| `expert_engagement.md` | Expert engagement tips and best practices |
| `record_keeping_checklist.md` | Printable record keeping checklist |
| `claim_preparation_checklist.md` | Claim preparation checklist for adjudication & arbitration |
| `common_pitfalls.md` | 10 most common claim pitfalls and how to avoid them |
| `risk_assessment_framework.md` | Expanded risk assessment categories and practical questions |
| `response_template.md` | Letter template mapping strategy to formal response |
| `quick_reference_card.md` | One-page desk reference card |
| `blank_worksheet.md` | Printable blank 7-Dimension worksheet |
| `training_guide.md` | Workshop-ready training material |
| `strategy_patterns.md` | All strategy patterns reference |

---

## How to use with the construction-law companion skill

This skill is designed to pair with **construction-law**, which handles clause analysis, notice drafting, and deadline calculation. The typical end-to-end workflow uses both skills in sequence:

1. **Identify the applicable clause and notice period** — use construction-law to look up the relevant contract clause (e.g. EOT notice provision, SOPA payment response window) and the prescribed time limit.

2. **Calculate the actual deadline** — use construction-law’s SOP calculator (or its equivalent for your contract form) to compute the calendar date, accounting for weekends, public holidays, and statutory roll-forward rules. Do not rely on simple date arithmetic.

3. **Plan the response strategy** — use this skill to work through the 7 strategy dimensions. Pass the calculated deadline as the `response_deadline` input.

4. **Draft the response** — return to construction-law for clause-level drafting and formal correspondence templates, using the strategy from step 3 as input.

Keeping strategy and execution in separate skills produces more commercially realistic outputs than trying to combine them. Each skill stays focused on what it does well: this one decides the direction; construction-law executes the analysis and drafting.

---

## Requirements

- Python 3.10+
- Standard library only — no third-party dependencies

## Tests

```bash
python3 -m unittest tests.test_smoke
```

---
## Security & Safety

- ✅ No network access
- ✅ No external calls
- ✅ No subprocess execution
- ✅ No dynamic code loading
- ✅ No telemetry: this tool does not collect or transmit usage data
- ✅ Safe for use with confidential project information
- ✅ **Safe to install and use** 🛡️

### Files written

This tool writes files **only** when you pass explicit flags:

| Flag | What is written | Format |
|------|----------------|--------|
| `--output FILE` | Strategy report | UTF-8 (Markdown or plain text) |
| `--save-strategy PATH` | Strategy data for reuse | UTF-8 JSON |

If neither flag is provided, output is printed to stdout. No files are created, modified, or read beyond the `--file` input (when given).

---

## Changelog

### v1.7.6 (May 2026)
- **Docs:** Added "Working out the actual deadline" section — explains calendar-day counting, s.50(a) roll-forward, ad-hoc holidays; points users to construction-law SOP calculator before running strategy
- **Docs:** Replaced "Companion skill" section with "How to use with construction-law" — 4-step end-to-end workflow (identify clause → calculate deadline → plan strategy → draft response)
- **Wizard:** Response deadline prompt sharpened to nudge toward specific calendar dates and reference the SOP calculator
- **Design decision:** No cross-skill code coupling. Date math stays in construction-law; strategy planning stays here. Skills are paired via documentation, not imports.

### v1.7.5 (May 2026)
- **Security:** Sanitised test docstrings and comments — removed function-call patterns (e.g. `compile(...)`) that ClawHub static analysis flagged as `suspicious.dynamic_code_execution`. The actual detection logic uses `ast.parse` and was never affected; the scanner was pattern-matching against English text in comments.

### v1.7.4 (May 2026)
- **Security:** Replaced string-grep forbidden-imports check with `ast.parse` tree-walking — properly catches `compile(...)`, `exec(...)`, `eval(...)` regardless of whitespace or indirection; no longer false-positives on comments, docstrings, or strings containing those words

### v1.7.3 (May 2026)
- **Security:** Rewrote `test_smoke.py` to avoid `subprocess.run()` entirely — now imports `main()` directly and patches `sys.argv`. Resolves ClawHub ClawScan `suspicious.dynamic_code_execution` false positive on the test file
- **Security:** Tightened forbidden-imports list: `urllib.request`/`urllib.error` (not blanket `urllib`), added `importlib`, `pickle`, `marshal`, `compile(`
- **Performance:** Tests now run in ~0.01s (was ~0.2s with subprocess overhead)

### v1.7.2 (May 2026)
- **Fix:** Interactive mode now wraps file writes (`--output`, `--save-strategy`) with friendly error messages (consistent with non-interactive mode)
- **Added:** Required-key validation for `--file` JSON input — missing keys produce a clear error listing what's needed, instead of empty fields
- **Added:** `_safe_write` helper — unified error handling for all file output paths
- **Docs:** Added `--help` output to SKILL.md so users can evaluate CLI flags without installing
- **Docs:** Added explicit "No telemetry" statement in Security section
- **Docs:** Added "Files written" section documenting exactly what is written and when
- **Docs:** Documented the 6 required JSON keys for `--file` mode
- **Docs:** Changed test instructions to recommend `python3 -m unittest` (stdlib) over `pytest`

### v1.7.1 (May 2026)
- **Security:** Added `test_no_forbidden_imports` — enforces the "no network / no subprocess" claim at test time by scanning for forbidden imports (subprocess, socket, requests, urllib, etc.)
- **Compatibility:** Updated Python requirement from 3.6+ to 3.10+ (reflects what is actually tested)

### v1.7.0 (May 2026)
- **Changed:** Replaced example scenario with a realistic PSSCOC EOT case (Contractor responding to SO rejection under Clause 13.2)
- **Changed:** `strategy_input.json` rewritten with correct flat-key schema matching all 7 dimensions
- **Changed:** `strategy_report_sample.md` regenerated from actual script output (not hand-written)
- **Changed:** Improved test docstrings and header matching

### v1.6.1 (May 2026)
- **Added:** JSON input validation for `--file` mode — checks file exists, valid JSON, root is a dict; warns on unrecognised keys (typo protection)
- **Added:** File I/O error handling — friendly messages for missing files, permission errors, and malformed JSON (no raw tracebacks)
- **Removed:** Dead code (`_prompt_yesno` function was defined but never called)

### v1.6.0 (May 2026)
- **Added:** `examples/strategy_input.json` and `examples/strategy_report_sample.md` — preview output before installing
- **Added:** `tests/test_smoke.py` — smoke test covering `--reference`, `--file`, and `--version` modes
- **Added:** `LICENSE` file (MIT-0) shipped at package root
- **Added:** Requirements section in SKILL.md (Python 3.6+, stdlib only)
- **Added:** Tests section in SKILL.md
- **Changed:** Vocabulary normalisation — replaced contract-form-specific terms ("Authority", "Engineer") with neutral language ("certifier", "the other party") for consistent applicability across PSSCOC, FIDIC, NEC, SIA, JCT, and bespoke contracts
- **Changed:** SKILL.md clarifies that `references/` is human reading material, not loaded by the script at runtime
- **Fixed:** Removed stale reference to `construction_law.py` in module docstring
- **Fixed:** Removed dead conditional branch in title block of `generate_report`

### v1.5.0 (May 2026)
- **Added:** Delay Analysis Study Guide — comprehensive reference covering SCL Protocol 22 Core Principles, 7 delay analysis methods (incl. Retrospective Longest Path), negative float & EOT entitlement, concurrent delay (Malmaison, North Midland, City Inn), pacing delays, disruption causation (Walter Lilly test), force majeure vs hardship, COVID-19 lessons, 15 key cases, and full definitions glossary
- Sanitised from project-specific study guide; all generic content with public case law citations
- Total reference documents: 22

### v1.4.0 (May 2026)
- **Major expansion:** Integrated full Construction Claim Strategy Practical Tools Guide v1.4
- Added: Notice Requirements Checklist
- Added: Expert Engagement Tips
- Added: Legal Precedents guide (Prevention Principle, Common Law vs Civil Law)
- Added: Concurrent Delay — Strategic Approach
- Added: Disruption Claims Strategy (with Common Law vs Civil Law comparison)
- Added: Delay Analysis Methods — Strategic Overview (As-Planned vs As-Built, TIA, Collapsed As-Built, Windows)
- Added: Arbitration Tactics & Prolongation Claim Strategies
- Added: ADR Overview with Adjudication vs Arbitration detailed comparison
- Added: Quantum Calculation Worked Examples (8 examples: Eichleay, Hudson, Emden, 2× Measured Mile, Actual Cost, Productivity Loss, Total Cost)
- Added: Common Claim Pitfalls (10 pitfalls with fixes)
- Added: Risk Assessment Framework (expanded categories and practical questions)
- Added: Record Keeping Checklist (printable)
- Added: Claim Preparation Checklist (printable, adjudication & arbitration)
- Total reference documents: 21

### v1.3.0 (May 2026)
- Added argument ranking guide, seven dimensions guide, worked examples
- Added response template, quick reference card, blank worksheet
- Added training guide and strategy patterns

### v1.1.0 (May 2026)
- Fully sanitized — all examples use generic/neutral language
- Improved interactive wizard with examples and input validation
- Better README for public listing
- Added review step before report generation

### v1.0.1 (May 2026)
- Removed all project-specific references
- Added disclaimer

### v1.0.0 (May 2026)
- Initial release — 7 strategy dimensions
- Interactive wizard mode
- Non-interactive JSON mode
- Reference tables dump
- Strategy save/reload

---

*This is a generic strategic planning tool. It does not constitute legal advice. Users should verify all information independently and seek qualified legal counsel before relying on any analysis for dispute resolution, adjudication, arbitration, or court proceedings.*
