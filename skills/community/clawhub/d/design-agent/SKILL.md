---
name: design-agent
description: Design consultation skill for AI agents. Invoke when another agent, skill, or user requests design review, design tokens, or UI美化 (UI beautification). Provides structured design prompts, DESIGN.md files, color systems, typography rules, spacing conventions, and component patterns. Use when building UI, generating HTML/React, writing newsletters, or any output where visual design matters. Also triggered by "make it look better", "apply design", "improve the UI", or "add design context".
---

# Design Agent — Structured Design for AI Outputs

## What This Skill Does

When another agent or skill produces UI output, it can call this skill to get a **structured design brief** — real design tokens, color systems, typography, spacing — that transforms generic AI output into distinctive, intentional design.

## Design Prompt Sources

Use these tools to generate a DESIGN.md for a given project or style:

| Tool | Use |
|---|---|
| [design-extractor.com](https://www.design-extractor.com) | Paste any URL → structured DESIGN.md with tokens |
| [design/prompts](https://lnkd.in/gy8z4XRF) | Browse 31+ rendered design styles, grab AI prompts |
| [typeui.sh](https://www.typeui.sh) | `npx typeui.sh pull [style]` — CLI, 57+ design skills |
| [awesome-design-md](https://lnkd.in/ghx8RddV) | Real DESIGN.md files from Stripe, Linear, Vercel etc. |

## Core Design System (defaults — override per project)

Stored in `references/design-tokens.md`:
- Color palette (hex + use)
- Typography scale
- Spacing system
- Component patterns
- Animation/transition defaults

## Workflow

```
Another agent requests design improvement
         │
         ▼
1. Identify the output medium (HTML/React/Newsletter/PDF/etc.)
2. Identify the target aesthetic or reference site
3. Use design-extractor.com or typeui.sh to generate design tokens
4. Merge with references/design-tokens.md base system
5. Write a DESIGN.md into the project or skill directory
6. Downstream agents read DESIGN.md → apply consistently
```

## VLM Review Loop (MANDATORY before finalising)

Before any design is marked complete, run it through a VLM review iteration:

### Step 1 — Generate initial output
Apply design tokens → produce HTML/React/PDF/etc.

### Step 2 — Capture screenshot
Use `canvas` tool to snapshot the rendered output:
```
canvas(action=snapshot, node=<target>, width=1280)
```

### Step 3 — VLM review
Send the snapshot to the vision model with the design brief:
```
Review this against the DESIGN.md tokens:
- Are colors consistent with the palette?
- Is typography on-scale (no arbitrary sizes)?
- Is spacing on the 8px grid?
- Are component states correct (hover, active)?
- Any visual anti-patterns (orphaned text, broken hierarchy)?
Flag specific issues and suggested fixes.
```

### Step 4 — Iterate
If VLM flags issues → apply fixes → resnapshot → re-review.
Repeat until VLM returns "design is consistent with tokens" or all flagged issues resolved.

### Step 5 — Final sign-off
Only mark complete when VLM confirms token consistency.
Log iteration count in the DESIGN.md.

```
Iteration log:
- v1: Initial render — 3 issues flagged (orphaned h3, wrong accent color, spacing off grid)
- v2: Fixed accent + orphaned h3 — spacing still off
- v3: All clear. Approved.
```

### VLM Review Prompts (by output type)

**HTML/Newsletter:**
```
Check: color palette, typographic hierarchy, spacing grid alignment,
component borders, dark/light mode if applicable. Flag any ad-hoc values.
```

**PDF (rendered as screenshot):**
```
Check: font sizes on scale, line spacing, margin consistency,
image placement, page break handling. Note any text overflow or orphans.
```

**React/UI Component:**
```
Check: button/input sizes match tokens, color applied from palette,
hover/active states visible, spacing between elements on grid.
```

## Creating a Project DESIGN.md

```bash
# Extract design from a reference URL
# (use design-extractor.com manually, paste result into project)

# Or pull a known style from typeui
npx typeui.sh pull minimal    # clean typographic
npx typeui.sh pull editorial  # magazine/longform
npx typeui.sh pull brutalist  # high contrast, raw
npx typeui.sh pull luxury     # dark, gold accents
```

## Design Review Checklist (before shipping UI)

- [ ] Colors match design tokens (no ad-hoc hex values)
- [ ] Typography uses defined scale (no arbitrary font sizes)
- [ ] Spacing follows the system (8px grid or defined scale)
- [ ] Component states covered (hover, active, disabled, error)
- [ ] Dark mode / light mode if applicable
- [ ] Responsive breakpoints defined
- [ ] Animation durations defined (no magic numbers like `0.3s` without tokens)

## Integration with Other Skills

This skill is **designed to be called by other skills**. Any skill that produces visual output should reference this skill before generating UI.

See `references/integration-guide.md` for how other skills should call design-agent.

## Key Files

| File | Purpose |
|---|---|
| `references/design-tokens.md` | Base design token system |
| `references/integration-guide.md` | How other skills call design-agent |
| `assets/design-prompt-template.md` | DESIGN.md template for new projects |
| `assets/example-design-standards/` | Example extracted from Vercel/Linear/Stripe |
