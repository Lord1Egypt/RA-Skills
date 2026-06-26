---
name: film-production-assistant
version: 1.0.1
description: "Pre-production assistant for filmmakers. Generates script breakdowns, shot lists, call sheets, production schedules, and budget estimates from scene descriptions. Built by a working film director with 20 years on set."
requires:
  binaries:
    - pandoc
  optional: true
---

# Film Production Assistant — SKILL.md

## Overview

A complete pre-production toolkit for indie and professional filmmakers. Generates industry-standard production documents from screenplay scenes and project parameters, using AI-driven prompt templates validated against real industry reference structures.

**Designed for:** Indie directors, student filmmakers, ADs, producers, and anyone managing a narrative film production with limited resources.

**No external APIs required.** All prompts are self-contained — paste into Claude, ChatGPT, or any capable LLM.

---

## When to Use This Skill

Trigger this skill when David (or any user) asks for:
- "Break down this scene for production"
- "Make a shot list for this scene"
- "Generate a call sheet for [shoot day]"
- "Build a shooting schedule from these scenes"
- "Estimate the budget for this project"
- "What do I need to produce this scene?"
- Any film pre-production planning request

---

## Available Tools

### 1. Script Breakdown Generator
**File:** `prompts/script-breakdown.md`
**What it does:** Analyzes a screenplay scene and produces a complete breakdown sheet — cast, props, set dressing, wardrobe, SFX, VFX, stunts, sound notes, production flags, and continuity concerns.
**Input required:** Scene text (paste directly)
**Output:** Production-ready breakdown sheet, one page per scene

### 2. Shot List Generator
**File:** `prompts/shot-list-generator.md`
**What it does:** Creates a complete, director-ready shot list for a scene with shot size, movement, angle, lens, equipment, estimated time, and priority ratings (A/B/C).
**Input required:** Scene text + director's tonal/visual notes + available hours
**Output:** Shot list table + coverage strategy + lighting notes + risk flags

### 3. Call Sheet Formatter
**File:** `prompts/call-sheet-formatter.md`
**What it does:** Generates a professionally formatted call sheet for a single shoot day — cast call times, crew grid, location details, emergency contacts, catering, advance schedule.
**Input required:** Shoot day details (scenes, cast, crew, location, weather, transport)
**Output:** Full formatted call sheet, ready to distribute

### 4. Production Schedule Builder
**File:** `prompts/production-schedule-builder.md`
**What it does:** Builds a complete shooting schedule from a scene list, optimizing for location groups, cast availability, and production efficiency. Produces one-liner schedule, DOOD chart, and scheduling flags.
**Input required:** Scene list with Int/Ext, location, pages, cast + constraints
**Output:** Day-by-day one-liner + DOOD chart + flags + contingency recommendations

### 5. Budget Estimator
**File:** `prompts/budget-estimator.md`
**What it does:** Generates a realistic line-item budget estimate with ATL/BTL breakdown, fringe calculations, contingency, and budget notes including what to cut vs. what never to cut.
**Input required:** Project parameters (pages, days, location, union status, key elements)
**Output:** Full budget with subtotals + budget notes + cost-reduction options

---

## Document Export (.docx) — Optional

If the user explicitly asks to save or export the output, use pandoc to generate a Word document.

**Requires:** `pandoc` must be installed on the host (`brew install pandoc` on Mac). If not available, deliver the output as text only.

**Only export when the user asks.** Do not automatically save files without confirmation.

```bash
# Only run this when user explicitly requests a file export
echo "{{output}}" > /tmp/film-output.md
pandoc /tmp/film-output.md -o "{{user-specified-path}}/{{ProjectTitle}}-{{DocumentType}}.docx"
```

**Naming convention:**
- Script Breakdown: `ProjectTitle-Scene01-Breakdown.docx`
- Shot List: `ProjectTitle-Scene01-ShotList.docx`
- Call Sheet: `ProjectTitle-Day01-CallSheet.docx`
- Production Schedule: `ProjectTitle-Schedule.docx`
- Budget: `ProjectTitle-Budget.docx`

**Ask the user for save location.** Do not default to `~/Desktop` without asking first.
Always confirm the file was saved and provide the full path.

---

## How to Use

### Option A: Direct Execution (Lilu handles it)

User provides a scene or project details. Lilu:
1. Reads the appropriate prompt template from `prompts/`
2. Fills in the template with the user's content
3. Runs it against the LLM (this session or sub-agent)
4. Returns formatted output
5. **Offers to export to .docx if user wants — does not save automatically**

### Option B: Template Delivery

Lilu delivers the filled prompt template to the user so they can paste it into their preferred tool (Claude.ai, ChatGPT, etc.).

### Option C: Full Pre-Production Package

For a complete project, run all 5 tools in sequence:
1. Script Breakdown → every scene
2. Shot List → key scenes
3. Production Schedule → full shoot
4. Budget Estimate → full project
5. Call Sheet → each shoot day (run day-before)

---

## Workflow: Scene → Production-Ready in 5 Steps

```
1. USER provides scene text
         ↓
2. Run SCRIPT BREAKDOWN → identify all elements
         ↓
3. Run SHOT LIST → director's visual plan
         ↓
4. Feed scenes into PRODUCTION SCHEDULE BUILDER
         ↓
5. Night before each shoot → generate CALL SHEET
```

---

## Reference Files

All structural knowledge is documented in `references/`:

| File | Contents |
|------|----------|
| `industry-templates.md` | Research summary — real call sheets, shot lists, breakdowns, schedules, budgets |
| `prompts.md` | All 5 prompt templates with example inputs and outputs |
| `call-sheet-structure.md` | Industry-standard call sheet anatomy (Celtx, CalArts) |
| `shot-list-structure.md` | Shot sizes, camera movements, shot list elements (StudioBinder) |
| `production-schedule-structure.md` | One-liner format, DOOD chart, stripboard colors |
| `script-breakdown-structure.md` | Category color codes, element definitions, full scene example |
| `budget-structure.md` | ATL/BTL categories, fringe rates, budget tiers, micro-budget example |

### Test Outputs (validated against "Bitter Coffee" — INT. COFFEE SHOP - DAY, Anna & Marcus confrontation, 3 pages)

| File | What It Tests |
|------|---------------|
| `test-outputs/01-script-breakdown.md` | Full breakdown sheet — coffee shop confrontation scene |
| `test-outputs/02-shot-list.md` | 17-shot list with coverage strategy and lighting notes |
| `test-outputs/03-call-sheet.md` | Day 2 of 3 call sheet — The Daily Grind location |
| `test-outputs/04-production-schedule.md` | 3-day schedule, DOOD chart, location groupings |
| `test-outputs/05-budget-estimate.md` | $8K-$14.8K short film budget with risk flags |

---

## Key Industry Concepts (Quick Reference)

### Page Eighths
1 script page = 8 sections. Scenes measured in eighths. 4 4/8 pages ≈ 4.5 pages ≈ ~4.5 min screen time.

### Budget Tiers
- Micro: $0-$50K | Ultra-low: $50K-$300K | Low: $300K-$1M | Mid-indie: $1M-$5M

### SAG ULB Rates (2025-2026)
$232-$241/day minimum. Under $300K total budget. +14.3% H&P fringes.

### Turnaround
Minimum 12 hours between company wrap and next call (union standard). Always note and protect it.

### Contingency
10% of BTL. Never remove. Ever.

### The Golden Rule of Scheduling
Group by location first. Then by cast. Interior before exterior. Complex scenes mid-production, not day one.

---

## David's Film Background Note

David has 20+ years of film and TV experience as a director/editor. He is cinematically literate. When working with him on production planning:
- Skip the basics — go straight to professional-level detail
- Flag creative concerns, not just logistical ones
- Reference his director's intent when making shot list suggestions
- If he gives a scene, he's thinking about how it cuts, not just how it shoots

---

## Token Cost

These prompts use Claude/GPT only when explicitly invoked — no background LLM calls. Each prompt run costs ~1,000-3,000 tokens depending on scene length and output detail. Covered by Claude Max subscription when run in this session.

---

## Sources

- StudioBinder (shot list, breakdown, schedule guides)
- CalArts 2 Pop (call sheet template structure)
- Celtx (call sheet elements)
- Saturation.io (indie budget template and fringe guide)
- Filmustage (script breakdown color system)
- No Film School (budget category reference)
- Industry standard 1st AD practices

*Skill built: March 27, 2026. Built by Lilu for David Apex.*
