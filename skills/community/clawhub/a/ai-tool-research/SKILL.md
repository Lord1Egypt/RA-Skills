---
name: ai-tool-research
description: >-
  Researches how people are using an AI tool (Claude Desktop, Cursor, OpenAI
  Codex, Google Gemini, or OpenClaw) and generates a Productivity Playbook
  plus a Skills Catalog in a consistent, rated, month-over-month format. Use
  when the user asks for a monthly research update on one of these tools, a
  productivity playbook, a skills catalog, a "what's new this month" report on
  an AI coding/agent tool, or wants to regenerate any of the files named
  `<Tool>-Productivity-Playbook.md` or `<Tool>-Skills-Catalog.md`. Also use if
  the user wants to run the same research cycle across all five tools.
---

# AI Tool Research Skill

Generates two Markdown artifacts for a given AI tool, updated for the last N days:

1. **`<Tool>-Productivity-Playbook.md`** — how real people are using it (personas, use cases, unusual examples, links).
2. **`<Tool>-Skills-Catalog.md`** — rated list of skills / extensions / plugins / rules / MCP servers with persona mapping.

The skill is **runtime-agnostic**. It works in Cursor, Claude Desktop, ChatGPT (web), Codex, Gemini CLI, and OpenClaw. See [Usage across runtimes](#usage-across-runtimes).

---

## When to invoke

Trigger on requests like:

- "Update the Cursor playbook with what happened this month"
- "Do the same research for Claude / Codex / Gemini / OpenClaw"
- "Run the monthly AI tool research"
- "Rebuild `<Tool>-Skills-Catalog.md` with fresh ratings"
- "Do all five tools for this month"

---

## Supported tools

| Tool key | What it is | Primary sources |
|---|---|---|
| `claude` | Claude Desktop + Claude Code + Anthropic Skills | anthropic.com, `anthropics/skills`, `obra/superpowers`, ComposioHQ |
| `cursor` | Cursor AI IDE + Rules / Skills / Plugins | cursor.com, cursor.directory, `awesome-cursorrules` |
| `codex` | OpenAI Codex (CLI + IDE + App + Cloud) | openai.com/codex, `openai/skills`, `openai/codex-plugins` |
| `gemini` | Google Gemini app + Gemini CLI + Code Assist + NotebookLM + Gems | ai.google.dev, `gemini-cli-extensions`, `Piebald-AI/awesome-gemini-cli-extensions` |
| `openclaw` | Peter Steinberger's OpenClaw local AI agent | openclaw.ai, `openclaw/clawhub`, `VoltAgent/awesome-openclaw-skills` |

All five honor the [agentskills.io](https://agentskills.io) open `SKILL.md` standard, so skills from one ecosystem often work in another — this is called out in every catalog.

---

## Inputs

Gather these before starting:

| Input | Required? | Default |
|---|---|---|
| `tool` | yes | ask the user: one of `claude` / `cursor` / `codex` / `gemini` / `openclaw` / `all` |
| `since_date` | no | 30 days before today (monthly cadence) |
| `output_dir` | no | current working directory |
| `existing_file_mode` | no | `rewrite` (default) or `append-appendix` (preserves body, adds "Updates since YYYY-MM-DD" appendix) |

If `tool = all`, loop through the five tools and produce ten files total.

**Always print today's date and the `since_date` used at the top of every generated file** so the user can verify the time window later.

---

## High-level workflow

Copy this checklist into the conversation and track progress:

```text
Research Progress:
- [ ] 1. Confirm inputs (tool, since_date, output_dir, mode)
- [ ] 2. Check existing files — if present, read them to avoid regressions
- [ ] 3. Research phase — search primary sources with since_date filter
- [ ] 4. Rating phase — apply validity + usefulness rubric to every item
- [ ] 5. Compose Productivity Playbook using playbook-template.md
- [ ] 6. Compose Skills Catalog using catalog-template.md
- [ ] 7. Verify link integrity + date stamps
- [ ] 8. Write files
- [ ] 9. Append run log entry
```

Do not skip any step. Step 2 is important — if the files already exist, you must read them so your update reflects genuine "what's new" signal, not repeated evergreen content.

---

## Step 1 — Confirm inputs

If a tool isn't specified, ask with a quick multi-choice question. Example:

> Which tool should I research this month?
> 1. Claude Desktop
> 2. Cursor
> 3. OpenAI Codex
> 4. Google Gemini
> 5. OpenClaw
> 6. All five

Default `since_date` = `today - 30 days`. If the user already ran this skill recently, prefer `since_date = last_run_date` from the run log (see Step 9).

---

## Step 2 — Check existing files

Check for these files in `output_dir`:

- `<Tool>-Productivity-Playbook.md`
- `<Tool>-Skills-Catalog.md`
- `research-log.md` (created by Step 9)

If any exist:

- Read them. Note the existing structure, tone, and skill ratings.
- Preserve link references that are still valid.
- In the new file, explicitly list **what changed since the last run** in a "Changes since `<last_run_date>`" section near the top.
- If `existing_file_mode = append-appendix`, do NOT rewrite the body. Add a new appendix called `Updates — <YYYY-MM-DD>` at the end with only the deltas.

---

## Step 3 — Research phase

### Source categories to cover (in order of trust)

1. **Official** — the tool vendor's own docs, blog, changelog, release notes
2. **Official GitHub orgs** — e.g., `anthropics/`, `openai/`, `getcursor/`, `google-gemini/`, `openclaw/`
3. **Curated "awesome" lists** — usually the fastest signal for new skills / rules / plugins
4. **Community marketplaces** — ClawHub, cursor.directory, Composio, geminicli.com/extensions
5. **X.com / Twitter** — search `<tool> since:YYYY-MM-DD` for fresh real-user workflows
6. **Dev blogs** — dev.to, Medium, Substack, HackerNoon, Pragmatic Engineer, The New Stack
7. **Reddit** — r/ClaudeAI, r/cursor, r/ChatGPTCoding, r/Bard
8. **YouTube** — transcripts of creator tutorials (last 30 days)

**For the exact search-query library per tool, read [`research-queries.md`](./research-queries.md).**

### Time filter

Apply date filtering to every search:

- Google / Web: `after:<since_date>` (e.g., `after:2026-03-21`)
- X.com: `since:<since_date>`
- GitHub: filter by `pushed:>=<since_date>` on repo search; for issues/PRs use `updated:>=<since_date>`

### What to collect per item

For every skill / rule / plugin / use case you plan to include, capture:

- Canonical name and author/org
- **Canonical URL** (prefer the GitHub repo or the vendor's doc page — not a random blog)
- One-sentence "what it does" description
- Last-update date (for validity rating)
- Install count / stars / endorsements if available
- Persona fit (from [`personas.md`](./personas.md))

### Minimum coverage bar

A single-tool run should surface:

- ≥ 10 new or updated skills / rules / plugins since `since_date`
- ≥ 6 new real-world use-case stories (X threads, case studies, blog posts)
- ≥ 1 officially announced product/feature change (release notes / changelog)
- ≥ 3 community discussions (Reddit / HN / Discord)

If you can't hit this bar, state so explicitly in the final file and lower the confidence claims.

---

## Step 4 — Rating phase

Apply the rating system from [`rating-system.md`](./rating-system.md) to **every** skill / rule / plugin entry.

Quick version (details in the reference file):

**Validity** = is it real + maintained?

- ✅ **Verified** — Official, OR GitHub push in last ~90 days AND ⭐ > 500 or installs > 1k
- 🟢 **Likely-valid** — confirmed repo, moderate traction, recent activity
- 🟡 **Early / Niche** — real but new, low traction
- 🔴 **Unverified** — mentioned but canonical source couldn't be confirmed

**Usefulness** = editorial 1–5 stars based on breadth, docs, persona fit, time-to-value.

- ★★★★★ must-install
- ★★★★ weekly use
- ★★★ niche but excellent
- ★★ narrow fit
- ★ experimental / novelty

Be honest. If something is hyped but you couldn't confirm maintenance, rate it 🔴 and say so. Do not give sympathy stars.

---

## Step 5 — Compose the Productivity Playbook

Use the **exact section structure in [`playbook-template.md`](./playbook-template.md)**. Do not renumber or rename sections — this is what makes month-over-month diffs useful.

**Personas**: always cover all eight from [`personas.md`](./personas.md) in the same order (PhD/research, solopreneur, marketer, designer, video/creator, developer, PKM/student, sales/finance/ops). If a persona has nothing meaningful for this tool, write one honest paragraph explaining why and move on.

**Tone rules**:

- Third person, not "you can…"
- Concrete verbs, no marketing fluff
- Every claim cites a link
- No emojis (except ratings badges)
- Prefer tables over prose for comparisons

**Length**: 300–600 lines is the healthy range. Longer than 700 = you're padding.

---

## Step 6 — Compose the Skills Catalog

Use the **exact section structure in [`catalog-template.md`](./catalog-template.md)**.

Mandatory sections (skipping any breaks month-over-month consistency):

1. Primer — what are the tool's extensibility primitives
2. Install commands — copy-pasteable
3. Rating legend (link to or copy from `rating-system.md`)
4. Built-in / official foundation skills
5. Marketplaces / meta-collections
6. Skills by persona (all eight)
7. Cross-tool skills (agentskills.io-compatible, works in ≥ 2 ecosystems)
8. Starter kits (one per persona, copy-paste-able)
9. How to create your own skill — minimum viable SKILL.md
10. Safety / vetting protocol
11. Tier-1 must-installs (5–8 items)
12. Cross-catalog navigation (links to sibling catalogs)
13. Master source index

Ratings appendix at the end is encouraged but not required if ratings are already inline.

---

## Step 7 — Verify

Before writing files, run these checks:

- [ ] Every skill has a name + URL + one-line description + both ratings
- [ ] Every URL resolves (when a WebFetch-type tool is available, sample-test a handful)
- [ ] `Last updated:` line exists near the top of each file
- [ ] `since_date` and `today_date` are both printed
- [ ] Sibling catalog links use correct relative paths (`./Claude-Skills-Catalog.md`, etc.)
- [ ] No invented repo URLs or fake GitHub orgs
- [ ] Persona order matches `personas.md`
- [ ] Rating badges render correctly in Markdown (no broken emojis)

If any check fails, fix before proceeding to Step 8.

---

## Step 8 — Write files

Write to `<output_dir>/<Tool>-Productivity-Playbook.md` and `<output_dir>/<Tool>-Skills-Catalog.md`.

File-naming rules:

- `<Tool>` capitalization: `Claude`, `Cursor`, `Codex`, `Gemini`, `OpenClaw`
- **For Claude specifically**, the playbook is historically `Claude-Desktop-Productivity-Playbook.md` (note the "Desktop"). Preserve that exact name when updating — the skill catalog drops "Desktop" and is just `Claude-Skills-Catalog.md`.

If `existing_file_mode = append-appendix`, append to the existing files instead of overwriting.

---

## Step 9 — Append run log

Append a row to `<output_dir>/research-log.md` (create it if missing):

```markdown
# AI Tool Research — Run Log

| Date run | Tool | since_date | Mode | New skills found | New use cases | Notable changes |
|---|---|---|---|---|---|---|
| 2026-04-21 | cursor | 2026-03-21 | rewrite | 14 | 9 | Composer 2 GA; 3 new MCP servers |
```

This is the source of truth for "when did I last run this" on future invocations.

---

## Output contract (what the user sees in chat)

When finished, reply with:

1. One-line summary: "Generated `<Tool>-Productivity-Playbook.md` (N lines) and `<Tool>-Skills-Catalog.md` (M lines), covering <since_date> → <today>."
2. **Top 5 what's-new bullets** — what the user should actually care about this month.
3. Any sources where you hit rate-limits or had to downgrade confidence.
4. Run-log row that was appended.

Do NOT dump the full file contents into chat. The file exists — let the user open it.

---

## Usage across runtimes

### Cursor

1. Put this whole folder in `.cursor/skills/ai-tool-research/` (project-local) or `~/.cursor/skills/ai-tool-research/` (personal).
2. Ensure Skills are enabled in Cursor settings.
3. Ask: "Run the AI tool research skill for Cursor this month."

### Claude Desktop / Claude Code

1. Put this folder in `~/.claude/skills/ai-tool-research/` (or the Anthropic Skills path on your OS).
2. In Claude Desktop, enable the skill under Settings → Skills.
3. Ask: "Use the ai-tool-research skill to update the Codex playbook."

### ChatGPT (web — no file system)

1. Start a new conversation.
2. Paste this `SKILL.md` as the first message, preceded by: `You are an agent following this skill definition. Apply it to my next request.`
3. Also paste the five supporting files (`playbook-template.md`, `catalog-template.md`, `personas.md`, `rating-system.md`, `research-queries.md`) in subsequent turns — ChatGPT will keep them in context.
4. Then say: "Run it for Gemini this month."
5. ChatGPT will return the two Markdown files as assistant messages; copy them into `.md` files locally.

### Gemini CLI

1. Put this folder in `~/.gemini/skills/ai-tool-research/` (or whichever Skills path your Gemini CLI is configured with — see `GEMINI.md`).
2. Ask: "Use ai-tool-research to update the OpenClaw skills catalog."

### OpenAI Codex (CLI / IDE / Cloud)

1. Put this folder in `~/.codex/skills/ai-tool-research/`.
2. Reference in `AGENTS.md` if you want it auto-loaded per project.
3. Ask: "Run ai-tool-research for Claude this month."

### OpenClaw

1. Put this folder in `~/.openclaw/workspace/skills/ai-tool-research/`.
2. Restart the gateway if needed.
3. Message the agent (on WhatsApp / Telegram / Slack): "Run the ai-tool-research skill for all five tools and DM me a summary."

---

## Reference files (read only when needed — progressive disclosure)

- [`playbook-template.md`](./playbook-template.md) — exact section structure + tone guide for the Productivity Playbook
- [`catalog-template.md`](./catalog-template.md) — exact section structure for the Skills Catalog
- [`personas.md`](./personas.md) — the 8 consistent personas, use-case angles, and what "good coverage" looks like per persona
- [`rating-system.md`](./rating-system.md) — the full validity + usefulness rubric with decision flowcharts
- [`research-queries.md`](./research-queries.md) — reusable search-query templates per tool, per source type

Read these **only when the step requires it** — they're progressive disclosure to keep this top-level SKILL.md lean.

---

## Examples of past output

If available, the user's own previous files in `output_dir` are the best examples:

- `Claude-Desktop-Productivity-Playbook.md` + `Claude-Skills-Catalog.md`
- `Cursor-Productivity-Playbook.md` + `Cursor-Skills-Catalog.md`
- `Codex-Productivity-Playbook.md` + `Codex-Skills-Catalog.md`
- `Gemini-Productivity-Playbook.md` + `Gemini-Skills-Catalog.md`
- `OpenClaw-Productivity-Playbook.md` + `OpenClaw-Skills-Catalog.md`

Match their voice, section numbering, and level of detail. If the user's versions differ from the templates in this skill, **prefer the user's version** — their file is the source of truth for their stylistic preferences.

---

## Anti-patterns to avoid

- ❌ Inventing repos or URLs. If you can't confirm it, rate 🔴 or drop it.
- ❌ Copying the previous month's file and changing the date. Always verify what actually changed.
- ❌ Giving five stars to everything. The rating system is useless if everything is ★★★★★.
- ❌ Marketing-speak ("revolutionary", "game-changing", "unlock"). Use concrete verbs.
- ❌ Long prose where a table would communicate faster.
- ❌ Skipping persona sections because "nothing new this month" — write one honest paragraph instead.
- ❌ Mentioning the skill file internals to the user. They just want the output files.

---

*This skill is intentionally portable — no hard-coded paths, no runtime-specific features. It works because Claude, Cursor, Codex, Gemini, and OpenClaw all honor the agentskills.io open spec.*
