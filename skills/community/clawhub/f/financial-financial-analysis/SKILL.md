---
name: financial-financial-analysis
version: 1.0.0
description: Core financial modeling and analysis tools: DCF, comps, LBO, 3-statement models, competitive analysis, and deck QC
source: anthropics/financial-services
---

# financial-analysis

Core financial modeling and analysis tools: DCF, comps, LBO, 3-statement models, competitive analysis, and deck QC

## 来源
来自 Anthropic 官方 financial-services 仓库的 financial-analysis 插件。
原始仓库: https://github.com/anthropics/financial-services

## 可用命令 (Commands)

### 3-statement-model

---
description: Fill out a 3-statement financial model template
argument-hint: "[path to template file]"
---

Load the `3-statement-model` skill and populate a 3-statement financial model (Income Statement, Balance Sheet, Cash Flow Statement).

If a file path is provided, use it as the template. Otherwise ask the user for their model template.


---

### competitive-analysis

---
description: Create a competitive landscape analysis
argument-hint: "[company or industry]"
---

Load the `competitive-analysis` skill and build a competitive landscape analysis for the specified company or industry.

If a company/industry is provided as an argument, use it. Otherwise ask the user what they want to analyze.


---

### Comparable Company Analysis Command

---
description: Build a comparable company analysis with trading multiples
argument-hint: "[company name or ticker]"
---

# Comparable Company Analysis Command

Build an institutional-grade comparable company analysis with operating metrics, valuation multiples, and statistical benchmarking.

## Workflow

### Step 1: Gather Company Information

If a company name or ticker is provided, use it. Otherwise ask:
- "What company would you like to analyze?"

### Step 2: Load Comps Analysis Skill

Use `skill: "comps-analysis"` to build the analysis:

1. **Clarify the analysis purpose**:
   - "What's the key question?" (valuation, efficiency, growth comparison)
   - "Who is the audience?" (IC, board, quick reference)
   - "Do you have a preferred format or template?"

2. **Identify peer group** (4-6 comparable companies):
   - Similar business model
   - Similar scale/market cap range
   - Same industry/sector
   - Geographic comparability

3. **Gather data** (prioritize MCP sources if available):
   - Operating metrics: Revenue, Growth, Gross Margin, EBITDA, EBITDA Margin
   - Valuation: Market Cap, Enterprise Value, EV/Revenue, EV/EBITDA, P/E
   - Additional metrics based on industry (Rule of 40 for SaaS, etc.)

4. **Build the analysis**:
   - Operating Statistics section with company data + statistics (Max, 75th, Median, 25th, Min)
   - Valuation Multiples section with same statistical summary
   - Notes & Methodology documentation

### Step 3: Create Excel Output

Generate Excel 

---

### DCF Valuation Command

---
description: Build a DCF valuation model with comps-informed terminal multiples
argument-hint: "[company name or ticker]"
---

# DCF Valuation Command

Build an institutional-quality DCF model that uses comparable company analysis to inform valuation ranges.

## Workflow

### Step 1: Gather Company Information

If a company name or ticker is provided, use it. Otherwise ask:
- "What company would you like to value?"

### Step 2: Run Comparable Company Analysis

**First, load the comps-analysis skill** to build trading comps:

Use `skill: "comps-analysis"` to:
1. Identify 4-6 comparable public companies
2. Pull operating metrics (Revenue, EBITDA, margins, growth)
3. Pull valuation multiples (EV/Revenue, EV/EBITDA, P/E)
4. Calculate statistical summary (median, 25th/75th percentiles)

**Key outputs to capture from comps:**
- Median EV/EBITDA multiple → informs terminal value exit multiple
- Median EV/Revenue multiple → sanity check on DCF output
- Peer growth rates → benchmark for revenue projections
- Peer margins → benchmark for margin assumptions

### Step 3: Build DCF Model

**Load the dcf-model skill** to construct the valuation:

Use `skill: "dcf-model"` to:
1. Gather historical financials and market data
2. Build revenue projections (Bear/Base/Bull cases)
3. Model operating expenses and FCF
4. Calculate WACC using CAPM
5. Discount cash flows and calculate terminal value
6. Bridge to equity value and implied share price

**Use comps to inform DCF assumptions:**

| Comp

---

### debug-model

---
description: Debug and audit a financial model for errors
argument-hint: "[path to .xlsx model file]"
---

Load the `audit-xls` skill with scope **model** and audit the specified financial model for broken formulas, balance sheet imbalances, hardcoded overrides, circular references, and logic errors — including the full model-integrity checks (BS balance, cash tie-out, roll-forwards, model-type-specific bugs).

If a file path is provided, use it. Otherwise ask the user for the model to review.


---

### lbo

---
description: Build an LBO model for a PE acquisition
argument-hint: "[company name or deal details]"
---

Load the `lbo-model` skill and build a leveraged buyout model for the specified company or deal.

If a company name is provided as an argument, use it. Otherwise ask the user for the target company and deal parameters.


---

### PPT Template Creator Command

---
description: Create a reusable PPT template skill from a PowerPoint template file
argument-hint: "[path to .pptx or .potx file]"
allowed-tools: ["Read", "Write", "Bash", "Glob"]
---

# PPT Template Creator Command

Create a self-contained PPT template skill from a user-provided PowerPoint template.

## Instructions

1. **Ask for the template file** if not provided:
   - "Please provide the path to your PowerPoint template file (.pptx or .potx)"
   - The template should contain the slide layouts and branding you want to use

2. **Load the ppt-template-creator skill**:
   - Use the `skill: "ppt-template-creator"` tool to load the full skill instructions
   - Follow the workflow in the skill to analyze the template and generate a new skill

3. **Gather additional info**:
   - Company/template name (for naming the skill)
   - Primary use cases (pitch decks, board materials, client presentations, etc.)

4. **Execute the skill workflow**:
   - Analyze template structure (layouts, placeholders, dimensions)
   - Generate skill directory with assets/ and SKILL.md
   - Create example presentation to validate
   - Package the skill

5. **Deliver the packaged skill** to the user


---

## 底层技能 (Skills)

### 3-statement-model

---
name: 3-statement-model
description: Complete, populate and fill out 3-statement financial model templates (Income Statement, Balance Sheet, Cash Flow Statement) . Use when asked to fill out model templates, complete existing model frameworks, populate financial models with data, complete a partially filled IS/BS/CF framework, or link integrated financial statements within an existing template structure. Triggers include requests to fill in, complete, or populate a 3-statement model template
---

# 3-Statement Financial Model Template Completion

Complete and populate integrated financial model templates with proper linkages between Income Statement, Balance Sheet, and Cash Flow Statement.

## ⚠️ CRITICAL PRINCIPLES — Read Before Populating Any Template

**Environment — Office JS vs Python:**
- **If running inside Excel (Office Add-in / Office JS):** Use Office JS directly. Write formulas via `range.formulas = [["=D14*(1+Assumptions!$B$5)"]]` — never `range.values` for derived cells. No separate recalc; Excel computes natively. Use `context.workbook.worksheets.getItem(...)` to navigate tabs.
- **If generating a standalone .xlsx file:** Use Python/openpyxl. Write `ws["D15"] = "=D14*(1+Assumptions!$B$5)"`, then run `recalc.py` before delivery.
- **Office JS merged cell pitfall:** Do NOT call `.merge()` then set `.values` on the merged range — throws `InvalidArgument` because the range still reports its pre-merge dimensions. Instead write value to top-left cell alone, then merge + format the full range: `ws.getRange("A1").values = [["INCOME STATEMENT"]]; const h = ws.getRange("A1:G1"); h.merge(); h.format.fill.color = "#1F4E79";`
- All principles below apply identically in either environment.

**Formulas over hardcodes (non-negotiable):**
- Every projection cell, roll-forward, linkage, and subtotal MUST be an Excel formula — never a pre-computed value
- When using Python/openpyxl: write formula strings (`ws["D15"] = "=D14*(1+Assumptions!$B$5)"`), NOT computed resul

---

### audit-xls

---
name: audit-xls
description: Audit a spreadsheet for formula accuracy, errors, and common mistakes. Scopes to a selected range, a single sheet, or the entire model (including financial-model integrity checks like BS balance, cash tie-out, and logic sanity). Triggers on "audit this sheet", "check my formulas", "find formula errors", "QA this spreadsheet", "sanity check this", "debug model", "model check", "model won't balance", "something's off in my model", "model review".
---

# Audit Spreadsheet

Audit formulas and data for accuracy and mistakes. Scope determines depth — from quick formula checks on a selection up to full financial-model integrity audits.

## Step 1: Determine scope

If the user already gave a scope, use it. Otherwise **ask them**:

> What scope do you want me to audit?
> - **selection** — just the currently selected range
> - **sheet** — the current active sheet only
> - **model** — the whole workbook, including financial-model integrity checks (BS balance, cash tie-out, roll-forwards, logic sanity)

The **model** scope is the deepest — use it for DCF, LBO, 3-statement, merger, comps, or any integrated financial model before sending to a client or IC.

---

## Step 2: Formula-level checks (ALL scopes)

Run these regardless of scope:

| Check | What to look for |
|---|---|
| Formula errors | `#REF!`, `#VALUE!`, `#N/A`, `#DIV/0!`, `#NAME?` |
| Hardcodes inside formulas | `=A1*1.05` — the `1.05` should be a cell reference |
| Inconsistent formulas | A formula that breaks the pattern of its neighbors in a row/column |
| Off-by-one ranges | `SUM`/`AVERAGE` that misses the first or last row |
| Pasted-over formulas | Cell that looks like a formula but is actually a hardcoded value |
| Circular references | Intentional or accidental |
| Broken cross-sheet links | References to cells that moved or were deleted |
| Unit/scale mismatches | Thousands mixed with millions, % stored as whole numbers |
| Hidden rows/tabs | Could contain overrides or stale c

---

### clean-data-xls

---
name: clean-data-xls
description: Clean up messy spreadsheet data — trim whitespace, fix inconsistent casing, convert numbers-stored-as-text, standardize dates, remove duplicates, and flag mixed-type columns. Use when data is messy, inconsistent, or needs prep before analysis. Triggers on "clean this data", "clean up this sheet", "normalize this data", "fix formatting", "dedupe", "standardize this column", "this data is messy".
---

# Clean Data

Clean messy data in the active sheet or a specified range.

## Environment

- **If running inside Excel (Office Add-in / Office JS):** Use Office JS directly (`Excel.run(async (context) => {...})`). Read via `range.values`, write helper-column formulas via `range.formulas = [["=TRIM(A2)"]]`. The in-place vs helper-column decision still applies.
- **If operating on a standalone .xlsx file:** Use Python/openpyxl.

## Workflow

### Step 1: Scope

- If a range is given (e.g. `A1:F200`), use it
- Otherwise use the full used range of the active sheet
- Profile each column: detect its dominant type (text / number / date) and identify outliers

### Step 2: Detect issues

| Issue | What to look for |
|---|---|
| Whitespace | leading/trailing spaces, double spaces |
| Casing | inconsistent casing in categorical columns (`usa` / `USA` / `Usa`) |
| Number-as-text | numeric values stored as text; stray `$`, `,`, `%` in number cells |
| Dates | mixed formats in the same column (`3/8/26`, `2026-03-08`, `March 8 2026`) |
| Duplicates | exact-duplicate rows and near-duplicates (case/whitespace differences) |
| Blanks | empty cells in otherwise-populated columns |
| Mixed types | a column that's 98% numbers but has 3 text entries |
| Encoding | mojibake (`Ã©`, `â€™`), non-printing characters |
| Errors | `#REF!`, `#N/A`, `#VALUE!`, `#DIV/0!` |

### Step 3: Propose fixes

Show a summary table before changing anything:

| Column | Issue | Count | Proposed Fix |
|---|---|---|---|

### Step 4: Apply

- **Prefer formulas over hardcoded cleane

---

### competitive-analysis

---
name: competitive-analysis
description: Framework for building competitive landscape decks — market positioning, competitor deep-dives, comparative analysis, strategic synthesis. Use when the user asks for a competitive landscape, competitor analysis, peer comparison, market positioning assessment, strategic review, or investment memo deck. Also triggers on "who are the competitors to X", "benchmark X against peers", "build a market map", or any request to systematically evaluate competitive dynamics across an industry.
---

# Competitive Landscape Mapping

Build a complete competitive analysis deck. This is a two-phase process: gather requirements and get outline approval first, then build.

## Environment check

This skill works in both the PowerPoint add-in and chat. Identify which you're in before starting — the mechanics differ, the workflow doesn't:

- **Add-in** — the deck is open live; build slides directly into it.
- **Chat** — generate a `.pptx` file (or build into one the user uploaded).

Everything below applies in both.

## Phase 1 — Scope the analysis

Competitive analysis means different things to different people. Before any research or slide-building, use `ask_user_question` to pin down what they actually want. Don't guess — a 20-slide peer benchmarking deck and a 5-slide market map are both "competitive analysis" and take completely different shapes.

Gather in one round if you can (the tool takes up to 4 questions):

- **Scope** — Single target company with competitors around it? Or multi-company side-by-side with no protagonist?
- **Competitor set** — Which companies are in scope? If the user names them, use exactly those. If they say "the usual suspects," propose a set and confirm.
- **Audience and depth** — Quick read for someone already in the space, or a full primer? This drives whether you need market sizing, industry economics, and history — or can skip to the comparison.
- **Investment context** — Do they need bull/base/bear scenarios 

---

### comps-analysis

---
name: comps-analysis
description: |
  Build institutional-grade comparable company analyses with operating metrics, valuation multiples, and statistical benchmarking in Excel/spreadsheet format.

  **Perfect for:**
  - Public company valuation (M&A, investment analysis)
  - Benchmarking performance vs. industry peers
  - Pricing IPOs or funding rounds
  - Identifying valuation outliers (over/under-valued)
  - Supporting investment committee presentations
  - Creating sector overview reports

  **Not ideal for:**
  - Private companies without comparable public peers
  - Highly diversified conglomerates
  - Distressed/bankrupt companies
  - Pre-revenue startups
  - Companies with unique business models
---

# Comparable Company Analysis

## ⚠️ CRITICAL: Data Source Priority (READ FIRST)

**ALWAYS follow this data source hierarchy:**

1. **FIRST: Check for MCP data sources** - If S&P Kensho MCP, FactSet MCP, or Daloopa MCP are available, use them exclusively for financial and trading information
2. **DO NOT use web search** if the above MCP data sources are available
3. **ONLY if MCPs are unavailable:** Then use Bloomberg Terminal, SEC EDGAR filings, or other institutional sources
4. **NEVER use web search as a primary data source** - it lacks the accuracy, audit trails, and reliability required for institutional-grade analysis

**Why this matters:** MCP sources provide verified, institutional-grade data with proper citations. Web search results can be outdated, inaccurate, or unreliable for financial analysis.

---

## Overview
This skill teaches Claude to build institutional-grade comparable company analyses that combine operating metrics, valuation multiples, and statistical benchmarking. The output is a structured Excel/spreadsheet that enables informed investment decisions through peer comparison.

**Reference Material & Contextualization:**

An example comparable company analysis is provided in `examples/comps_example.xlsx`. When using this or other example f

---

### dcf-model

---
name: dcf-model
description: Real DCF (Discounted Cash Flow) model creation for equity valuation. Retrieves financial data from SEC filings and analyst reports, builds comprehensive cash flow projections with proper WACC calculations, performs sensitivity analysis, and outputs professional Excel models with executive summaries. Use when users need to value a company using DCF methodology, request intrinsic value analysis, or ask for detailed financial modeling with growth projections and terminal value calculations.
---

# DCF Model Builder

## Overview

This skill creates institutional-quality DCF models for equity valuation following investment banking standards. Each analysis produces a detailed Excel model (with sensitivity analysis included at the bottom of the DCF sheet).

## Tools

- Default to using all of the information provided by the user and MCP servers available for data sourcing.

## Critical Constraints - Read These First

These constraints apply throughout all DCF model building. Review before starting:

**Environment: Office JS vs Python/openpyxl:**
- **If running inside Excel (Office Add-in / Office JS environment):** Use Office JS directly — do NOT use Python/openpyxl. Write formulas via `range.formulas = [["=D19*(1+$B$8)"]]`. No separate recalc step needed; Excel calculates natively. Use `range.format.*` for styling. The same formulas-over-hardcodes rule applies: set `.formulas`, never `.values` for derived cells.
- **If generating a standalone .xlsx file (no live Excel session):** Use Python/openpyxl as described below, then run `recalc.py` before delivery.
- The rest of this skill uses openpyxl examples — translate to Office JS API calls when in that environment, but all principles (formula strings, cell comments, section checkpoints, sensitivity table loops) apply identically.

**⚠️ Office JS merged cell pitfall:** When building section headers with merged cells, do NOT call `.merge()` then set `.values` on the merged range — Office JS st

---

### deck-refresh

---
name: deck-refresh
description: Updates a presentation with new numbers — quarterly refreshes, earnings updates, comp rolls, rebased market data. Use whenever the user asks to "update the deck with Q4 numbers", "refresh the comps", "roll this forward", "swap in the new earnings", "change all the $485M to $512M", or any request to swap figures across an existing deck without rebuilding it.
---

# Deck Refresh

Update numbers across the deck. The deck is the source of truth for formatting; you're only changing values.

## Environment check

This skill works in both the PowerPoint add-in and chat. Identify which you're in before starting — the edit mechanism differs, the intent doesn't:

- **Add-in** — the deck is open live; edit text runs, table cells, and chart data directly.
- **Chat** — the deck is an uploaded file; edit it by regenerating the affected slides with the new values and writing the result back.

Either way: smallest possible change, existing formatting stays intact.

This is a four-phase process and the third phase is an approval gate. Don't edit until the user has seen the plan.

## Phase 1 — Get the data

Use `ask_user_question` to find out how the new numbers are arriving:

- **Pasted mapping** — user types or pastes "revenue $485M → $512M, EBITDA $120M → $135M." The clearest case.
- **Uploaded Excel** — old/new columns, or a fresh output sheet the user wants pulled from. Read it, confirm which column is which before you trust it.
- **Just the new values** — "Q4 revenue was $512M, margins were 22%." You figure out what each one replaces. Workable, but confirm the mapping before you touch anything — a "$512M" that you map to revenue but the user meant for gross profit is a quiet disaster.

Also ask about **derived numbers**: if revenue moves, does the user want growth rates and share percentages recalculated, or left alone? Most decks have "+15% YoY" baked in somewhere that's now stale. Whether to touch those is a judgment call the user should ma

---

### ib-check-deck

---
name: ib-check-deck
description: Investment banking presentation quality checker. Reviews a pitch deck or client-ready presentation for (1) number consistency across slides, (2) data-narrative alignment, (3) language polish against IB standards, (4) visual and formatting QC. Use whenever the user asks to review, check, QC, proof, or do a final pass on a deck, pitch, or client materials — including requests like "check my numbers", "reconcile figures across slides", "is this client-ready", or "what am I missing before I send this out".
---

# IB Deck Checker

Perform comprehensive QC on the presentation across four dimensions. Read every slide, then report findings.

## Environment check

This skill works in both the PowerPoint add-in and chat. Identify which you're in before starting:

- **Add-in** — read from the live open deck.
- **Chat** — read from the uploaded `.pptx` file.

This is read-and-report only — no edits — so the workflow is identical in both.

## Workflow

### Read the deck

Pull text from every slide, keeping track of which slide each line came from. You'll need slide-level attribution for every finding ("$500M appears on slides 3 and 8, but slide 15 shows $485M"). A deck with 30 slides is too much to hold in working memory reliably — write the extracted text to a file so the number-checking script can process it.

The script expects markdown-ish input with slide markers. Format as:

```
## Slide 1
[slide 1 text content]

## Slide 2
[slide 2 text content]
```

### 1. Number consistency

Run the extraction script on what you collected:

```bash
python scripts/extract_numbers.py /tmp/deck_content.md --check
```

It normalizes units ($500M vs $500MM vs $500,000,000 → same number), categorizes values (revenue, EBITDA, multiples, margins), and flags when the same metric category shows conflicting values on different slides. This is the part most likely to catch something a human missed on the fifth read-through.

Beyond what the script flags, verify:

---

### lbo-model

---
name: lbo-model
description: This skill should be used when completing LBO (Leveraged Buyout) model templates in Excel for private equity transactions, deal materials, or investment committee presentations. The skill fills in formulas, validates calculations, and ensures professional formatting standards that adapt to any template structure.
---

---

## TEMPLATE REQUIREMENT

**This skill uses templates for LBO models. Always check for an attached template file first.**

Before starting any LBO model:
1. **If a template file is attached/provided**: Use that template's structure exactly - copy it and populate with the user's data
2. **If no template is attached**: Ask the user: *"Do you have a specific LBO template you'd like me to use? If not, I can use the standard template which includes Sources & Uses, Operating Model, Debt Schedule, and Returns Analysis."*
3. **If using the standard template**: Copy `examples/LBO_Model.xlsx` as your starting point and populate it with the user's assumptions

**IMPORTANT**: When a file like `LBO_Model.xlsx` is attached, you MUST use it as your template - do not build from scratch. Even if the template seems complex or has more features than needed, copy it and adapt it to the user's requirements. Never decide to "build from scratch" when a template is provided.

---

## CRITICAL INSTRUCTIONS FOR CLAUDE - READ FIRST

### Environment: Office JS vs Python

**If running inside Excel (Office Add-in / Office JS environment):**
- Use Office JS (`Excel.run(async (context) => {...})`) directly — do NOT use Python/openpyxl
- Write formulas via `range.formulas = [["=B5*B6"]]` — Office JS formulas recalculate natively in the live workbook
- The same formulas-over-hardcodes rule applies: set `range.formulas`, never `range.values` for anything that should be a calculation
- Use `range.format.font.color` / `range.format.fill.color` for the blue/black/purple/green convention
- No separate recalc step needed — Excel handles calculation native

---

### ppt-template-creator

---
name: ppt-template-creator
description: Creates self-contained PPT template SKILLS (not presentations) from user-provided PowerPoint templates. Use ONLY when a user wants to create a reusable skill from their template. For creating actual presentations, use the pptx skill instead.
---

# PPT Template Creator

**This skill creates SKILLS, not presentations.** Use this when a user wants to turn their PowerPoint template into a reusable skill that can generate presentations later. If the user just wants to create a presentation, use the `pptx` skill instead.

The generated skill includes:
- `assets/template.pptx` - the template file
- `SKILL.md` - complete instructions (no reference to this meta skill needed)

**For general skill-building best practices**, refer to the `skill-creator` skill. This skill focuses on PPT-specific patterns.

## Workflow

1. **User provides template** (.pptx or .potx)
2. **Analyze template** - extract layouts, placeholders, dimensions
3. **Initialize skill** - use the `skill-creator` skill to set up the skill structure
4. **Add template** - copy .pptx to `assets/template.pptx`
5. **Write SKILL.md** - follow template below with PPT-specific details
6. **Create example** - generate sample presentation to validate
7. **Package** - use the `skill-creator` skill to package into a .skill file

## Step 2: Analyze Template

**CRITICAL: Extract precise placeholder positions** - this determines content area boundaries.

```python
from pptx import Presentation

prs = Presentation(template_path)
print(f"Dimensions: {prs.slide_width/914400:.2f}\" x {prs.slide_height/914400:.2f}\"")
print(f"Layouts: {len(prs.slide_layouts)}")

for idx, layout in enumerate(prs.slide_layouts):
    print(f"\n[{idx}] {layout.name}:")
    for ph in layout.placeholders:
        try:
            ph_idx = ph.placeholder_format.idx
            ph_type = ph.placeholder_format.type
            # IMPORTANT: Extract exact positions in inches
            left = ph.left / 914400
   

---

### pptx-author

---
name: pptx-author
description: Produce a .pptx file on disk (headless) instead of driving a live PowerPoint document — for managed-agent sessions with no open Office app.
---

# pptx-author

Use this skill when running **headless** (managed-agent / CMA mode) and you need to deliver a PowerPoint deck as a **file artifact** rather than editing a live document via `mcp__office__powerpoint_*`.

## Output contract

- Write to `./out/<name>.pptx`. Create `./out/` if it does not exist.
- Return the relative path in your final message so the orchestration layer can collect it.

## How to build the deck

Write a short Python script and run it with Bash. Use `python-pptx`:

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation("./templates/firm-template.pptx")  # if a template is provided
# or: prs = Presentation()

slide = prs.slides.add_slide(prs.slide_layouts[5])    # title-only
slide.shapes.title.text = "Valuation Summary"
# ... add tables / charts / text boxes ...

prs.save("./out/pitch-<target>.pptx")
```

## Conventions (mirror the live-Office `pitch-deck` skill)

- **One idea per slide.** Title states the takeaway; body supports it.
- **Every number traces to the model.** If a figure comes from `./out/model.xlsx`, footnote the sheet and cell.
- **Use the firm template** when one is mounted at `./templates/`; otherwise default layouts.
- **Charts**: prefer embedding a PNG rendered from the model over native pptx charts when fidelity matters.
- **No external sends.** This skill writes a file; it never emails or uploads.

## When NOT to use

If `mcp__office__powerpoint_*` tools are available (Cowork plugin mode), use those instead — they drive the user's live document with review checkpoints. This skill is the file-producing fallback for headless runs.


---

### skill-creator

---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
license: Complete terms in LICENSE.txt
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks—they transform Claude from a general-purpose agent into a specialized agent
equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Claude needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.

**Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, o

---

### xlsx-author

---
name: xlsx-author
description: Produce a .xlsx file on disk (headless) instead of driving a live Excel workbook — for managed-agent sessions with no open Office app.
---

# xlsx-author

Use this skill when running **headless** (managed-agent / CMA mode) and you need to deliver an Excel workbook as a **file artifact** rather than editing a live workbook via `mcp__office__excel_*`.

## Output contract

- Write to `./out/<name>.xlsx`. Create `./out/` if it does not exist.
- Return the relative path in your final message so the orchestration layer can collect it.

## How to build the workbook

Write a short Python script and run it with Bash. Use `openpyxl`:

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active; ws.title = "Inputs"
ws["B2"] = "Revenue"; ws["C2"] = 1_250_000_000
ws["C2"].font = Font(color="0000FF")           # blue = hardcoded input
calc = wb.create_sheet("DCF")
calc["C5"] = "=Inputs!C2*(1+Inputs!C3)"        # black = formula
wb.save("./out/model.xlsx")
```

## Conventions (mirror `audit-xls`)

- **Blue / black / green.** Blue = hardcoded input, black = formula, green = link to another sheet/file.
- **No hardcodes in calc cells.** Every calculation cell is a formula; every input lives on an Inputs tab.
- **Named ranges** for any value referenced from a deck or memo.
- **Balance checks.** Include a Checks tab that ties (BS balances, CF ties to cash, etc.) and surfaces TRUE/FALSE.
- **One model per file.** Do not append to an existing workbook unless explicitly asked.

## When NOT to use

If `mcp__office__excel_*` tools are available (Cowork plugin mode), use those instead — they drive the user's live workbook with review checkpoints. This skill is the file-producing fallback for headless runs.


---
