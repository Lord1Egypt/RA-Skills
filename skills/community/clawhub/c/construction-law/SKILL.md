---
name: construction-law
description: "FIDIC (Red/Yellow/Silver), PSSCOC, SIA, and Singapore SOP Act toolkit. Generate notices, claims, EOT applications, and obligations registers. Computes statutory deadlines against eGazette-verified holiday data. Use when (1) analysing contract clauses, risk allocation, or obligations; (2) preparing or reviewing claims (delay, disruption, prolongation, EOT, loss & expense); (3) comparing contract forms or advising on procurement strategy; (4) drafting or reviewing notices, correspondence, or contract documents; (5) building obligations registers or notice calendars; (6) discussing dispute resolution (DAB/DAAB, adjudication, arbitration, mediation, CAB); (7) Singapore-specific construction law (SOP Act, BCA, SIArb); (8) MDB procurement frameworks (ADB, World Bank). NOT for: non-construction commercial contracts, pure property/real-estate conveyancing, or insurance law."
---

# Construction Law: FIDIC, PSSCOC, SIA & Singapore SOP Act

<!-- Remove v2.11.0 banner after 2026-08-17 -->
> **⚠️ v2.11.0 users — action required if you computed non-SG deadlines.**
> v2.11.0 shipped with bundled best-effort holiday data for AE, MY, and GB that was **not verified against authoritative sources**. If you ran the FIDIC Deadline Calculator against a non-SG seat using v2.11.0, **re-check those deadlines** against your jurisdiction’s official gazette. From v2.11.1 onward, only Singapore holidays are bundled (gazette-verified); other jurisdictions require `--holidays-file` with your own verified data. See the [FIDIC Deadline Calculator](#fidic-deadline-calculator) section for details.

Analyze construction contracts, claims, notices, payment timelines, risk allocation, and dispute pathways across major standard forms, with strong international and Singapore-focused coverage.

## Why install this?

- ✅ Avoid missed notice deadlines and time-bar mistakes
- ✅ Structure claims and EOT submissions faster
- ✅ Compare contract risk and obligations more consistently
- ✅ Prompts for the correct contract form **and edition** before analysis

## Who this skill is for

This skill is built for:

- Construction lawyers
- In-house counsel
- Contract managers
- Commercial managers
- Quantity surveyors
- Claims consultants
- Project managers

## What this skill does

Use this skill to:

- Identify the correct contract form and edition before analysis
- Review clauses for obligations, rights, risks, and time-bars
- Generate notice calendars and obligations registers
- Draft structured claim, EOT, variation, and payment templates
- Compare FIDIC forms across key topics
- Calculate Singapore SOP Act payment timelines
- Assess delay events, concurrency, EOT exposure, and LD risk
- Triage dispute resolution pathways

## Supported forms and frameworks

- FIDIC Red Book 2017 (Construction)
- FIDIC Yellow Book 2017 (Plant & Design-Build)
- FIDIC Silver Book 2017 (EPC/Turnkey)
- PSSCOC (Construction Works)
- SIA Conditions (9th Edition)
- NEC (NEC3, NEC4) — notice calendar only
- JCT — pending
- Singapore SOP Act workflows

## Why this skill matters

Construction outcomes often turn on details such as:

- the exact contract form and edition
- amended or bespoke clauses
- notice timing
- record quality
- causation
- quantification
- governing law

This skill helps you structure analysis quickly and consistently so you can spot risks early and avoid missing critical deadlines.

> 🇸🇬 **Singapore matters — BCA circular awareness:** BCA frequently updates SOP Act timelines, plan fees, CORENET-X procedures, BC1/structural codes, cost-sharing schemes, productivity grants, and buildability rules through circulars at https://www1.bca.gov.sg/resources/circulars/. If you maintain a local mirror (e.g. `bca-circulars/` in your workspace, refreshed via a weekly heartbeat task), check it before relying on general knowledge. See `references/singapore.md` for details.
>
> ℹ️ This skill does not fetch live BCA updates itself. If you maintain a local circulars mirror in your workspace, use it as an up-to-date reference alongside the skill.

## CLI overview

```
Construction Law Skill — Unified CLI

Usage: construction_law.py <command> [options]

Available commands:

  intake       🏗️ Matter intake — guided issue triage (recommended starting point)
  wizard       🧙 Interactive guided prompts for tools
  notices      Generate notice/obligations calendar for a contract form
  claims       Generate claim notice/EOT/VO/disruption letters
  sop          Singapore SOP Act payment timeline calculator
  compare      Compare FIDIC contract forms side-by-side
  obligations  Generate party-by-party obligations register
  register     Generate Excel workbook of obligations + notices
  delay        Delay analysis & EOT entitlement calculator
  deadline     FIDIC deadline calculator — Singapore bundled; bring-your-own-holidays for other seats

Run any command with --help for its specific options, e.g.:
  python3 construction_law.py notices --help
  python3 construction_law.py claims --help
```

---

## Start here

### Recommended for all users: Matter Intake

The intake mode triages a construction issue and produces a professional report with clause buckets, deadline checks, amendment warnings, confidence labels, and recommended next steps.

```bash
python3 scripts/construction_law.py intake
# or
python3 scripts/intake.py
```

Supports non-interactive mode for automation:
```bash
python3 scripts/intake.py --file matter.json --output report.md --save-matter answers.json
```

Use non-interactive mode for repeatable internal workflows, templates, or batch matter intake.

### Sample Matter Intake output

Example: delay / EOT issue under FIDIC Red 1999

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 MATTER INTAKE — OUTPUT REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Contract:   FIDIC Red 1999
Governing:  Singapore
Party:      Contractor
Issue:      Delay / Extension of Time (EOT)
Objective:  Both EOT and additional payment

1. ISSUE SUMMARY
This appears to be a delay / EOT issue arising from late
access to site. The likely focus is notice compliance,
EOT entitlement, causation, and supporting records.

2. LIKELY CLAUSE BUCKETS
- Clause 2.1   Right of Access to Site
- Clause 8.4   Extension of Time
- Clause 20.1  Contractor's Claims

3. DEADLINE / TIME-BAR CHECK
Trigger:   Awareness of delaying event
Deadline:  28 days from awareness
Status:    ⚠️ Notice not confirmed
Risk:      Potential time-bar if late notice applies

4. AMENDMENT SENSITIVITY FLAGS
- Notice periods may be amended
- EOT wording may be narrowed
- Particular Conditions may override the standard form

5. RECOMMENDED NEXT STEPS
- confirm exact clause wording and edition
- verify whether notice was served in time
- gather programme and contemporaneous records
- prepare claim narrative and supporting documents

6. CONFIDENCE LABELS
Deadline calculation:      High confidence
Clause identification:     High confidence
Entitlement position:      Needs review

This is a workflow and analysis aid only. It is not legal advice.
```

> 🎯 **For strategic claim planning**, see the companion skill `construction-claim-strategy` on ClawHub (v1.5.0). It covers the 7-Dimension strategy framework, argument ranking, delay analysis methods (SCL Protocol, TIA, Windows Analysis), concurrent delay strategy, disruption claims, quantum calculation examples (Eichleay/Hudson/Emden/Measured Mile), ADR strategy (adjudication vs arbitration), notice compliance, expert engagement, risk assessment, pacing delays, legal precedents, and 22 printable reference documents — all BEFORE you select clauses or start drafting.

### Interactive Wizard

For tool-specific tasks (notices, claims, SOP calculator, etc.), use the wizard:

```bash
python3 scripts/construction_law.py wizard
# or
python3 scripts/wizard.py
```

### For power users: Unified CLI

```bash
python3 scripts/construction_law.py --list
python3 scripts/construction_law.py notices --form fidic-red
python3 scripts/construction_law.py notices --form fidic-silver
python3 scripts/construction_law.py claims --form fidic-red --type disruption-claim
python3 scripts/construction_law.py claims --form fidic-yellow --type eot-application
python3 scripts/construction_law.py claims --form fidic-silver --type notice-of-claim
python3 scripts/construction_law.py sop --claim-date 2026-05-15
python3 scripts/construction_law.py compare --forms red,yellow,silver --topic claims
python3 scripts/construction_law.py obligations --form fidic-silver --party both
python3 scripts/construction_law.py register --form fidic-red --type both --output reg.xlsx
python3 scripts/construction_law.py register --form fidic-silver --type both --output silver.xlsx
python3 scripts/construction_law.py delay --baseline-start 2026-05-01 --baseline-end 2026-12-31
python3 scripts/construction_law.py deadline --seat SG --trigger 2026-05-15 --period 28 --mode exclude_ph
python3 scripts/construction_law.py deadline --seat AE --trigger 2026-03-18 --period 28 --mode exclude_ph --holidays-file ae_holidays.json
```

> 💡 **All three FIDIC colours supported:** `fidic-red`, `fidic-yellow`, `fidic-silver`. Also: `psscoc`, `sia`.

## Critical rule: always confirm the contract edition first

Before any clause analysis, confirm:

- contract form
- edition/year
- governing law
- amendments or particular conditions
- whether bespoke terms override the standard form

Do not assume the latest edition applies.

### Common editions still in use

- PSSCOC: 2017, 2020
- PSSCOC D&B: 2014, 2020
- FIDIC: 1999, 2017
- SIA: 9th Ed, 11th Ed
- NEC: NEC3, NEC4

## Core workflows

### 1. Clause analysis

For any clause question, this skill helps you:

- identify the relevant clause
- explain the obligation, entitlement, or risk
- flag notice periods and time-bars
- cross-reference related clauses
- highlight where amendments may change the default position

### 2. Claims and EOT analysis

For delay, disruption, prolongation, and related claims, use this structure:

1. Entitlement
2. Causation
3. Notice compliance
4. Substantiation
5. Quantification

### 3. Notice calendars

Build notice calendars that capture:

- clause reference
- trigger event
- notice period
- recipient
- consequence of non-compliance

### 4. Risk allocation review

Assess whether risk is allocated to the party best able to:

1. identify it
2. control it
3. mitigate it
4. absorb it

### 5. Delay and LD exposure

Review:

- delay event chronology
- criticality
- concurrency
- potential EOT entitlement
- potential liquidated damages exposure

## Included tools

### Interactive Wizard

Guided prompts for common tasks.

```bash
python3 scripts/wizard.py
```

### Notice Calendar Generator

Generate notice and obligations calendars.

```bash
python3 scripts/notice_calendar.py --form fidic-red --format md
python3 scripts/notice_calendar.py --form fidic-yellow --format md
python3 scripts/notice_calendar.py --form fidic-silver --format md
python3 scripts/notice_calendar.py --form psscoc --format csv --output notices.csv
```

### Claims Template Generator

Generate structured templates for claim notices and related submissions.

```bash
python3 scripts/claims_template.py --list
python3 scripts/claims_template.py --form fidic-red --type notice-of-claim --output notice.md
python3 scripts/claims_template.py --form fidic-yellow --type eot-application --output eot_yellow.md
python3 scripts/claims_template.py --form fidic-silver --type notice-of-claim --output notice_silver.md
python3 scripts/claims_template.py --form psscoc --type eot-application --output eot.md
```

### Obligations Register Generator

Create obligations registers by party and category.

```bash
python3 scripts/obligations_register.py --form fidic-red --party both --format md
python3 scripts/obligations_register.py --form fidic-yellow --party contractor --format md
python3 scripts/obligations_register.py --form fidic-silver --party both --format md
python3 scripts/obligations_register.py --form psscoc --party contractor --format csv --output obligations.csv
```

### SOP Act Payment Timeline Calculator

Calculate statutory payment deadlines from a Singapore payment claim date.

```bash
python3 scripts/sop_calculator.py --claim-date 2026-06-30
python3 scripts/sop_calculator.py --claim-date 2026-06-30 --response-period 14 --format csv --output timeline.csv
```

### FIDIC Contract Comparator

Compare FIDIC forms side by side.

```bash
python3 scripts/fidic_comparator.py --forms red,yellow,silver --topic risk
python3 scripts/fidic_comparator.py --forms red,yellow,silver --topic all --format csv --output comparison.csv
```

Topics: `overview`, `risk`, `claims`, `disputes`, `payment`, `termination`, `all`

### FIDIC Deadline Calculator (Seat-Aware)

Compute contractual deadlines based on the seat country's public holidays.

> The FIDIC Deadline Calculator supports Singapore out of the box, with holiday data verified against the eGazette. Singapore data covers gazetted years (currently 2025–2026); the 2027 entry is provisional until MOM gazettes it (expected late 2026). For projects with a seat in any other jurisdiction, you must supply your own holiday list — the tool will not ship pre-loaded holiday data for non-Singapore seats. This is deliberate: holiday calendars vary by sub-jurisdiction (Malaysian state, UK constituent country, individual emirate), shift by moon-sighting, and are gazetted by your own government's authoritative source. Use that source, not ours.

Supports three day-counting modes:
- **calendar** — calendar-day counting; use where the relevant clause defines or operates on calendar days
- **exclude_ph** — calendar days excluding public holidays of the seat country
- **working** — excludes weekends AND public holidays (for contracts defining "working day")

```bash
python3 scripts/fidic_deadline.py --list-seats
python3 scripts/fidic_deadline.py --seat SG --trigger 2026-05-15 --period 28
python3 scripts/fidic_deadline.py --seat SG --trigger 2026-05-15 --period 28 --mode exclude_ph
python3 scripts/fidic_deadline.py --seat AE --trigger 2026-03-18 --period 28 --mode exclude_ph --holidays-file ae_holidays.json
python3 scripts/fidic_deadline.py --seat MY --trigger 2026-02-15 --period 28 --mode working --holidays-file my_holidays.json
```

Bundled seat: `SG` (Singapore — gazette-verified). For any other jurisdiction, supply `--holidays-file`. See `docs/holiday-file-format.md` for the JSON schema and a worked example.

> 💡 **Which mode to use?** Check your contract's definition of "day". FIDIC 2017 standard = calendar days. If Particular Conditions amend this to exclude public holidays, use `exclude_ph`. If the contract uses "working days", use `working`.

### Delay Analysis Calculator

Assess delay events, concurrency, EOT exposure, and LD risk.

```bash
python3 scripts/delay_calculator.py --baseline-start 2026-05-11 --baseline-end 2030-05-10 \
  --add "Late access|2026-06-01|2026-06-30|employer|critical" \
  --add "Weather|2026-07-15|2026-07-25|neutral|critical"
```

### Excel Register Generator

Export notice calendars and obligations registers to .xlsx.

```bash
python3 scripts/excel_register.py --form fidic-red --type both --output contract_admin.xlsx --commencement 2026-05-11
python3 scripts/excel_register.py --form fidic-yellow --type both --output yellow_admin.xlsx
python3 scripts/excel_register.py --form fidic-silver --type both --output silver_admin.xlsx
python3 scripts/excel_register.py --form psscoc --type obligations --output obligations.xlsx
```

Requires: `openpyxl` (`pip3 install openpyxl`)

## Example outputs

### Notice calendar — concrete sample

```
Clause:    FIDIC 20.2.1
Trigger:   Event giving rise to claim
Deadline:  28 days from awareness
Recipient: Engineer
Risk:      Late notice may prejudice entitlement (time-bar)
```

### Notice calendar — fields

- Clause reference
- Trigger event
- Notice deadline
- Recipient
- Time-bar consequence

### Claims template

- Background
- Contract basis
- Event chronology
- Causation
- Notice compliance
- Relief sought
- Reservation of rights
- Supporting documents

### Obligations register

- Clause
- Obligation
- Responsible party
- Timing
- Priority
- Status
- Notes

## Best use cases

- preliminary clause review
- contract administration checklists
- claim structure and document preparation
- notice and deadline tracking
- form comparison
- SOP timeline calculation
- delay event triage

## Important limitations

This skill is a workflow and analysis aid. It is not a substitute for legal advice.

Use caution where:

- the contract is heavily amended
- bespoke EPC or project-specific drafting applies
- governing law may materially change the outcome
- local statutory regimes override standard form assumptions
- adjudication, arbitration, or court submissions require final review

Always verify:

- the contract edition
- amendments and particular conditions
- governing law
- notice requirements
- jurisdiction-specific treatment of concurrency, good faith, prevention, and time-bars

## Key principles

- Read the contract first
- Standard form positions mean little if amended
- Time-bars can be fatal
- Notice compliance should be checked before merits
- Concurrency treatment differs by jurisdiction
- Good faith is jurisdiction-specific
- Prevention issues may affect LD exposure
- Fitness for purpose and reasonable skill and care must be distinguished carefully

## Reference files

- references/fidic.md
- references/singapore.md
- references/claims.md
- references/disputes.md
- references/procurement.md

## Live knowledge sources (Singapore)

For up-to-date Singapore regulatory context, consult the **BCA circulars page** — the authoritative source for changes to SOP Act timelines, plan fees, CORENET-X, BC1/structural codes, cost-sharing schemes, productivity grants, and buildability requirements:

- **Source:** https://www1.bca.gov.sg/resources/circulars/
- **Recommended setup:** Maintain a local PDF mirror (e.g. `bca-circulars/` in your workspace) refreshed weekly via a heartbeat or cron task. Track seen titles in a `seen.json` index to detect new circulars.

When advising on Singapore matters touching SOP Act timelines, plan fees, CORENET-X, BC1/structural codes, cost-sharing schemes, productivity grants, or buildability requirements, **check the latest circulars first** before relying on general knowledge — BCA updates can change deadlines, rates, and procedural requirements.

If your local mirror looks stale (>2 weeks old), trigger a fresh fetch.

## 🔒 Security and safety

All Python scripts in this skill are designed as safe, local template and register generators.

- ✅ **No network access** — no API calls, no HTTP requests
- ✅ **No subprocess execution** — no shell commands, no external programs
- ✅ **No dynamic code loading** — sibling scripts are imported as plain Python modules (no `importlib`, no `exec`, no `eval`)
- ✅ **No telemetry from skill code** — the bundled scripts do not collect or transmit data. (Note: your LLM provider’s normal data handling still applies.)
- ✅ **No filesystem traversal** — only writes to the user-specified `--output` path
- ✅ **Read-only static reference data** — contract clauses bundled with the skill
- ✅ **ClawScan:** Benign
- ✅ **Static analysis:** Benign
- ℹ️ VirusTotal status is shown on the listing page

**Safe to install and use.** 🛡️

### Files written

Scripts write files **only** when you pass explicit output flags. If no output flag is provided, all output goes to stdout.

| Script | Flag | What is written | Format |
|--------|------|----------------|--------|
| Any script | `--output FILE` | Generated report/template/calendar | UTF-8 (Markdown, CSV, or plain text) |
| `excel_register.py` | `--output FILE.xlsx` | Obligations/notices workbook | Excel (.xlsx, requires openpyxl) |
| `claims_template.py` | `--output FILE.docx` | Claim letter | Word (.docx, requires python-docx) |
| `sop_calculator.py` | `--output FILE` | SOP payment timeline | UTF-8 Markdown or CSV |
| `fidic_deadline.py` | `--output FILE` | Deadline calculation | UTF-8 text or Markdown |

No files are created, modified, or read beyond the explicit input flags (`--file`, `--holidays-file`, `--events-csv`).

## Dependencies

Core scripts use only the Python standard library. Optional features require:

| Package | Required For | Install |
|---------|-------------|--------|
| `openpyxl` | Excel register output | `pip3 install openpyxl` |
| `python-docx` | Word document export | `pip3 install python-docx` |

Declared in `pyproject.toml` as optional extras:
```bash
pip3 install .[excel]    # Excel only
pip3 install .[all]      # Excel + Word
pip3 install .[test]     # pytest + hypothesis
```

## Testing

The skill includes a multi-layer test suite (73 tests):

**Layer 1 — Golden file** (`test_sop_golden.py`): 8 hand-computed scenarios frozen in `tests/data/golden_timelines.csv`. Covers CNY cluster, Vesak/Hari Raya Haji, Christmas/New Year cross-year, National Day in-lieu, baseline, claim-on-PH, 14-day response, and s.17(2) +7 extension.

**Layer 2 — Property-based** (`test_sop_properties.py`): Hypothesis tests over 2025–2027 date range. Properties: deadline never on PH, strictly monotonic, round-trip sop_days_between, adding a holiday can only push later, result ≥ N calendar days.

**Layer 3 — Boundary** (`test_sop_boundary.py`): End-of-month, end-of-year, s.17(2) extension (verified as SOP days with PH skipping), claim on PH, consecutive holidays (3+ non-SOP days), out-of-range year (fails loud), Silver Book fitness-for-purpose assertion.

**Register tests** (`test_registers.py`): All forms produce valid MD/CSV, Silver Book has no Engineer, entry structure validation.

```bash
cd skills/construction-law
pip3 install .[test]
python3 -m pytest tests/ -v
# or without pytest:
python3 -m unittest discover tests
```

## Changelog

### v2.11.5 (May 2026)
- **MUST-FIX:** `_check_year_coverage` now called from all public functions (`is_sop_day`, `add_sop_days`, `sop_days_between`) — previously only called from `calc_timeline`. Dates in uncovered years (e.g. 2028) now raise `ValueError` instead of silently treating all days as working days. Year-crossing within `add_sop_days` also checked.
- **Docs:** `is_sop_day` docstring clarifies: returns True for Saturdays/Sundays (they count as SOP days); raises ValueError for uncovered years (does not silently return False); ad-hoc holidays (e.g. Polling Day) require manual addition
- **Docs:** `add_sop_days(start, 0)` semantics documented (returns start unchanged; caller responsible for whether start is a working day)
- **Docs:** Ad-hoc holiday warning added to timeline output
- **Docs:** Error message now uses actual config path (`_HOLIDAY_JSON.name`) instead of hardcoded string
- **Tests:** 73 → 85. New: `TestSaturdayDeadline` (deadline on Saturday stays), `TestInLieuCollision` (synthetic collision sets exercise while-loop), `TestOutOfRangeYear` expanded (4 new: `add_sop_days`, `is_sop_day`, `sop_days_between`, year-crossing), golden row 9 (Saturday deadline + Labour Day PH skip)
- **Tests:** Property test date bounds tightened (`MAX_DATE_FOR_ADD = 2027-10-01`) to avoid crossing into uncovered 2028

### v2.11.4 (May 2026)
- **Security:** Sanitised test docstrings and comments — removed function-call patterns that static analysis scanners match against English text

### v2.11.3 (May 2026)
- **Security:** Replaced string-grep forbidden-imports check with `ast.parse` tree-walking — properly catches `compile(...)`, `exec(...)`, `eval(...)` regardless of whitespace or indirection; no longer false-positives on comments, docstrings, or strings containing those words

### v2.11.2 (May 2026)
- **Title:** Updated to "Construction Law: FIDIC, PSSCOC, SIA & Singapore SOP Act"
- **Advisory:** Added v2.11.0 user advisory banner for non-SG deadline re-check
- **Docs:** Added CLI overview (`--help` output) to SKILL.md so users can evaluate commands without installing
- **Docs:** Tightened "No telemetry" statement to distinguish skill code from LLM provider data handling
- **Docs:** Added "Files written" section documenting exactly what each script writes and when
- **Docs:** SKILL.md changelog backfilled with v2.10.0–v2.11.1 entries (CHANGELOG.md remained the source of truth; SKILL.md was out of sync)
- **Security:** Added `test_security.py` — scans all 13 scripts for forbidden imports (subprocess, socket, requests, urllib.request, http.client, importlib, pickle, marshal, os.system, exec, eval, compile), enforcing the no-network/no-subprocess/no-dynamic-code claim at test time
- **Docs:** Recommend `python3 -m unittest` (stdlib) alongside pytest

### v2.11.1 (May 2026)
- **Scope correction:** Removed bundled best-effort holiday data for AE, MY, GB — shipping unverified holiday data in a legal-deadline tool was the wrong call
- **FIDIC Deadline Calculator** now ships with **Singapore holidays only** (gazette-verified). Other jurisdictions: supply your own verified holiday data via `--holidays-file`
- Added `docs/holiday-file-format.md` with JSON schema, worked example, and source guidance
- Reduced golden deadline tests to Singapore-only; retained generic property tests

### v2.11.0 (May 2026)
- **New:** FIDIC Deadline Calculator (`fidic_deadline.py`) — computes contractual deadlines in three modes: `calendar` (calendar-day counting), `exclude_ph` (excludes public holidays only), and `working` (excludes weekends + public holidays)
- **Singapore calendar bundled and maintained** — verified against eGazette / MOM source data
- **Important:** Holiday data covers **Singapore only**. For all other jurisdictions, users must supply their own gazette-verified holiday file via `--holidays-file`. The tool will prompt clearly if a non-SG seat is used without one.

### v2.10.1 (May 2026)
- Reconciled CHANGELOG v2.8.1/v2.9.1 duplication
- Recategorized out-of-range ValueError as legal accuracy change
- Added per-year eGazette URL, MOM gazette cite, and holiday names to `data/sg_holidays.json`
- Added moon sighting notes for Hari Raya Puasa / Hari Raya Haji dates

### v2.10.0 (May 2026)
- **3-layer test suite (57+ tests):** golden-file, Hypothesis property-based, and boundary tests for SOP calculator; register tests for all forms
- **Out-of-range year protection:** Calculator now raises ValueError with a clear message when claim date's year has no holiday data (no silent wrong answers)
- **`pyproject.toml`** with optional extras (`[excel]`, `[word]`, `[all]`, `[test]`)
- **`data/sg_holidays.json`** as single source of truth with per-year provenance
- **Disclaimer injection** on all generated templates (visible text + HTML comment)
- **Deprecated:** `--add` pipe-delimited flag; replaced with `--add-event` (structured) and `--events-csv` (batch)
- **Added:** `CHANGELOG.md` with categorized convention

### v2.9.0 (May 2026)
- **FIDIC Silver Book (EPC/Turnkey) 2017 added as a fully-supported form.** All 7 claim templates now have fidic-silver versions (notice-of-claim, eot-application, variation-claim, interim-claim, disruption-claim, loss-and-expense, final-account). Templates are tailored to EPC/Turnkey context: no Engineer (Employer administers directly via Employer's Representative), narrower EOT grounds under Sub-Clause 8.5, Contractor's broader risk assumption, lump sum pricing, fitness for purpose obligations, and design responsibility under Sub-Clause 5.
- **fidic-silver obligations register added** — 33 contractor obligations (including EPC-specific design, fitness for purpose, higher physical conditions threshold) and 11 employer obligations.
- **fidic-silver notice calendar added** — 12 key notices (claims, design, variations, disputes, payment) with Silver Book-specific recipients (Employer, not Engineer).
- **Excel register now produces fidic-silver sheets** for both obligations and notices.
- Full support matrix is now **35 combos** (7 claim types × 5 forms: fidic-red, fidic-yellow, fidic-silver, psscoc, sia). NEC4 and JCT remain pending.
- Updated cross-references to companion skill `construction-claim-strategy` v1.5.0.

### v2.8.1 (May 2026) — SOP holiday correctness fix
- **Sunday → Monday in-lieu rule now applied automatically.** Under the Holidays Act 1998 s.4(2), when a public holiday falls on a Sunday the following Monday is a public holiday in lieu. The previous bundled holiday list missed four such Mondays (1 Jun 2026 — Vesak in-lieu; 10 Aug 2026 — National Day in-lieu; 9 Nov 2026 — Deepavali in-lieu; 8 Feb 2027 — CNY Day 2 in-lieu). The SOP day arithmetic now derives in-lieu Mondays from the gazetted Sunday holidays automatically, so future gazette updates won't drift.
- This affects any SOP timeline whose computed window crosses a Sunday public holiday — deadlines could be off by one day under v2.8.0 and earlier. Re-run any SOP timelines you generated previously if the period crossed those dates.

### v2.8.0 (May 2026)
- **FIDIC Yellow Book 2017 added as a fully-supported form.** All 7 claim templates now have fidic-yellow versions (notice-of-claim, eot-application, variation-claim, interim-claim, disruption-claim, loss-and-expense, final-account). Templates are tailored to Plant & Design-Build context: design responsibility (Cl. 5), Employer's Requirements (Cl. 1.9), milestone-based payment (Schedule of Payments), Tests after Completion (Cl. 12), and the 8.5 EOT grounds.
- **fidic-yellow obligations register added** — 33 contractor obligations (including design-specific clauses 5.1–5.8) and 12 employer obligations.
- **Excel register now produces fidic-yellow obligations sheets** in addition to notices.
- All new templates are edition-tagged in the HTML comment header and visible body.
- Full support matrix is now **28 combos** (7 claim types × 4 forms: fidic-red, fidic-yellow, psscoc, sia). NEC4 and JCT remain pending.

### v2.7.0 (May 2026)
- **6 new claim templates** filling the PSSCOC + SIA gap: `eot-application`, `variation-claim`, and `interim-claim` now have full PSSCOC (7th Ed., 2014 rev. 2020) and SIA (9th Ed., 2010 rep. 2016) versions.
- All new templates are **edition-tagged** in an HTML comment header and in the visible body, so users know exactly which standard form edition the clauses correspond to.
- Interim-claim templates explicitly dual-purpose as SOP Act s.10 payment claims with the s.10(3) requirements ticked off.
- Full support matrix is now **21 combos** (7 claim types × 3 forms).

### v2.6.0 (May 2026)
- **SOP calculator now holiday-aware.** Periods are computed in SOP days (excluding Singapore public holidays per SOP Act s.2 read with the Holidays Act 1998). Previously used calendar-day arithmetic which silently produced wrong dates around holiday clusters.
- **SOP timeline conceptual fix.** Removed misleading min/max determination and payment-due rows; replaced with single statutory deadlines and an explicit s.17(2) +7-day extension note.
- **Argparse no longer crashes** on `claims_template.py` for `fidic-yellow`, `nec4`, or `jct` — unsupported forms are now rejected at parse time with a pointer to `--list`. Unsupported (form, type) combos within registered forms also fail with a helpful message.
- **Excel register no longer writes half-empty workbooks.** Pre-flight coverage check refuses combos like `--form fidic-yellow --type obligations` and prints what is supported.
- **Version sprawl resolved.** New `scripts/version.py` is the single source of truth; intake.py / wizard.py / delay_calculator.py / sop_calculator.py footers all aligned to v2.6.

