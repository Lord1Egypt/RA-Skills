# Skills Catalog — Template

Exact section structure every `<Tool>-Skills-Catalog.md` must follow. Read during Step 6 of the parent SKILL.md.

---

## File header

```markdown
# <Tool> Skills Catalog

> **Rated, persona-sorted catalog of <Tool> skills / extensions / plugins / rules / MCP servers.**
> Last updated: <today>. Research window: <since_date> → <today>.
> Companion files: [the five sibling files]

---
```

---

## Required sections (in order)

### 1. Primer — `<Tool>`'s extensibility surface

Table mapping primitive → file/location → what it does. Example primitives:

- Skills (SKILL.md directories)
- Plugins (native code bundles)
- Rules (e.g., Cursor `.mdc`, Gemini `GEMINI.md`, Codex `AGENTS.md`)
- Memory files (Claude `CLAUDE.md`, Codex `AGENTS.md`, OpenClaw `MEMORY.md` / `SOUL.md` / `HEARTBEAT.md`)
- MCP servers
- Gems (Gemini) / Notepads (Cursor) / Artifacts (Claude)
- Hooks

Also a one-paragraph note on `agentskills.io` cross-tool compatibility.

### 2. Install & management commands

Copy-pasteable. Cover: install, search, list, update, disable, remove, publish. Every command must actually exist — don't invent flags.

### 3. Rating legend

Either copy the legend from [`rating-system.md`](./rating-system.md) inline, or link to it. Inline is preferred for standalone readability.

### 4. Built-in / official foundation skills

Skills that ship with the tool or are maintained by the vendor's own GitHub org. All should be ✅ Verified by definition.

### 5. Marketplaces / meta-collections

Curated lists, awesome-lists, registries, meta-skills. Rate each as a collection (not its individual contents).

### 6. Skills by persona

Sub-sections 6.1 through 6.8, in the same persona order as `personas.md`:

- 6.1 PhD / research students
- 6.2 Solopreneur / startup founder
- 6.3 Marketer / growth / agency
- 6.4 Designer
- 6.5 Video / podcast / creator
- 6.6 Software developer
- 6.7 Personal productivity / PKM / student
- 6.8 Sales / finance / ops

Each sub-section: a table with columns `Skill | URL | Rating (validity + stars) | Role`.

Minimum 5 entries per persona if meaningful coverage exists; fewer is acceptable with an honest note.

### 7. Cross-tool skills

Skills that honor `agentskills.io` and work across ≥ 2 of the five tools in this series. These are disproportionately valuable — flag them specifically.

### 8. Unusual / frontier skills

Mirror section 12 of the playbook but with install commands. Show the tail of the skill distribution.

### 9. Starter kits by persona

Copy-paste-able install blocks. Example:

````markdown
### Developer starter
```bash
<install-cli> install <skill-a>
<install-cli> install <skill-b>
...
```
````

One starter kit per persona that has meaningful coverage. Plus one "safety-first starter" (install these BEFORE any other skills).

### 10. Creating your own skill

Minimal viable SKILL.md example for this tool (YAML frontmatter shape, trigger terms, publishing command). Link to the vendor's official skill-authoring doc.

Include meta-skills for building skills if any exist (e.g., Anthropic's `skill-creator`, OpenClaw's `agentskills-io`).

### 11. Safety / vetting protocol

Specific to tools with system access (all five to varying degrees). Include:

- Install-gate skills (e.g., `azhua-skill-vetter` for OpenClaw)
- Sandbox options
- Audit logging options
- Cost monitoring
- Prompt-injection screening

### 12. Tier-1 must-installs

A single table, 5–8 items max, with the rationale for each. This is the section most users will read. Be ruthless — no sympathy picks.

### 13. Cross-catalog navigation

Links to the four sibling catalogs with a one-line description each. Reminds the user that `agentskills.io`-compliant skills are portable.

### 14. Master source index

Same groupings as the playbook's section 16: Official, Curation, How-to, Context/culture.

### 15. (Optional) Appendix A — Ratings summary

Appendix table of all skills in the catalog with their ratings, useful for quick scanning. Optional if ratings are already inline everywhere.

---

## Table formatting contract

Every skill table has at minimum:

| Column | Required | Example |
|---|---|---|
| **Skill** | yes | `steipete/github` |
| **URL** | yes | clickable Markdown link to canonical source |
| **Rating** | yes | `✅ ★★★★★` or split into two columns |
| **Role / Why** | yes | 6–12 words, not a sentence |

Do not add columns that would be empty for most rows.

---

## Diff-friendly rules

- Alphabetical order within each persona table (or by descending usefulness rating — pick one convention per file and stick with it)
- Heading text identical across runs
- Every skill entry one row, one line (no multi-line rows)
- Ratings as literal characters `✅ 🟢 🟡 🔴 ★` — not images or HTML
- Dates always `YYYY-MM-DD`

---

## Length guide

| Section | Target lines |
|---|---|
| Header + sections 1–3 | 40–80 |
| Section 4 (foundation) | 20–60 |
| Section 5 (marketplaces) | 20–50 |
| Section 6 (personas, all 8) | 150–300 |
| Sections 7–11 | 30–80 each |
| Section 12 (tier-1) | 15–30 |
| Sections 13–14 | 30–60 |
| Optional appendix | 30–80 |
| **Total body** | **400–800 lines** |

Skills catalogs can justifiably be longer than playbooks because they're reference material. Users read them in chunks.
