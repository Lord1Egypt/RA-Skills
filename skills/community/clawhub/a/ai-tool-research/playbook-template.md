# Productivity Playbook — Template & Tone Guide

The exact section structure every `<Tool>-Productivity-Playbook.md` must follow. Read this during Step 5 of the parent SKILL.md.

---

## File header (always identical shape)

```markdown
# <Tool> Productivity Playbook

> **How people are actually using <Tool> to run their lives / ship code / operate businesses.**
> Last updated: <today>. Research window: <since_date> → <today>.
> Companion files: [other four playbooks]

---
```

---

## Required sections (in order)

Do not renumber these across runs. Month-over-month diffs depend on stable numbering.

### 0. Why `<Tool>` is different from the other four

One-table comparison vs. the sibling tools. Always 2–4 rows max. Example axes: interface, runtime, execution layer, orchestration role, registry scale.

### 1. Foundation — what is `<Tool>` + install + file anatomy

- Origin, maintainer, scale signals (stars, install counts, notable adopters)
- Install command(s) — copy-pasteable
- File / config anatomy — what lives where on disk

### 2. What's new since `<since_date>`

**This section is the point of monthly re-runs.** Bullet list of:

- Product / feature announcements from the vendor
- Notable new skills / extensions / plugins
- Community workflows that gained traction
- Deprecations or breaking changes

If empty, say so honestly. Don't pad.

### 3. The flagship workflow / killer pattern

The single most-cited or most-copied workflow for this tool. Steinberger's 6,600-commit/month pattern for OpenClaw, Composer 2's parallel agents for Cursor, Codex CLI subagents, Gemini Deep Research Max, Claude's Artifacts + Skills combo, etc.

Pick the one that's **actually being copied on X**, not the one the vendor markets hardest.

### 4–11. Persona sections (all eight, in this order)

See [`personas.md`](./personas.md). Each persona gets:

- 2–5 concrete workflows with links
- Real names / handles / case studies when available
- A table or bullet list — not a paragraph

The eight personas are fixed:

4. PhD / research students
5. Solopreneur / startup founder
6. Marketer / growth / agency
7. Designer (app / web / brand)
8. Video / podcast / creator
9. Software developer
10. Personal productivity / PKM / student
11. Sales / finance / ops / back-office

If a persona has nothing meaningful this month, write one honest paragraph and move on. Do not skip the heading — that breaks consistency.

### 12. Unusual / frontier use cases

3–8 genuinely weird examples from X / Reddit / blogs. The purpose is to show the range of the tool, not to pad. Aim for stories that are either:

- High-impact (car purchase negotiation, $X reclaimed, millions earned)
- Surprising (AI VTuber, agent imageboard, theology bot)
- Technically novel (cross-tool orchestration, new primitive)

### 13. Compared to the other four tools in this series

One table mapping scenario → best tool. Be honest about where `<Tool>` loses.

### 14. Four-week getting-started plan

Broken into Week 1 / Week 2 / Week 3 / Week 4 with concrete installs and practices. Do not write "explore the docs" — write "install X, Y, Z and build workflow A".

### 15. Safety & security

Non-optional for tools with system access (OpenClaw, Cursor with shell, Codex in agent mode, Claude Code, Gemini CLI).

- Trust model
- Sandboxing / approval options
- Audit tooling
- Cost guardrails
- Specific red-flag skills/behaviors to avoid

### 16. Master link index

Grouped:

- Official — vendor docs / homepage / GitHub org
- Community — awesome lists, marketplaces, directories
- Setup guides — by channel / OS / scenario
- Best articles / interviews — editorial picks from the research window
- Deep how-to content — linked guides

Every link must be canonical and verified-live.

### 17. Final take

Short. 3–5 sentences. Honest assessment:

- Who is this tool actually for?
- When would another tool be better?
- One-line positioning vs. the other four.

Then a pointer to the sibling Skills Catalog:
`See the companion file — [<Tool>-Skills-Catalog.md](./<Tool>-Skills-Catalog.md) — for the rated, persona-sorted skill install list.`

---

## Tone rules

- Third person. Never "you can…" or "we recommend…" — use "people use it to…" / "this is the pattern that…"
- Every factual claim cites a link in parentheses or via Markdown link.
- Tables > bullets > prose. In that order.
- Concrete verbs. Banned: "leverage", "unlock", "empower", "revolutionize", "seamlessly", "cutting-edge".
- No emojis in body text. Rating badges (✅🟢🟡🔴★) are fine in catalog files, not here.
- Numbers > adjectives: "6,600 commits in January" not "highly productive".
- Names > roles: "Peter Steinberger" not "the founder".

---

## Length guide

| Section | Target lines |
|---|---|
| Header + section 0 | 20–40 |
| Sections 1–3 | 40–80 each |
| Persona sections (4–11) | 30–80 each |
| Section 12 (unusual) | 30–60 |
| Sections 13–17 | 30–80 each |
| **Total body** | **300–700 lines** |

Longer than 750 = padding. Shorter than 250 = insufficient research.

---

## Diff-friendly formatting

Since this file will be regenerated monthly:

- Keep heading text identical run-to-run (`## 5. Solopreneur / startup founder`, not `## 5. Solopreneurs & Founders`).
- Date stamps always `YYYY-MM-DD`.
- Link lists in alphabetical order within each subsection.
- Table rows in stable order (alphabetical by skill name or by descending usefulness rating).

This makes `git diff` between monthly versions actually useful for the human reader.
