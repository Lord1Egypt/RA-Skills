# Contributing

Skills are markdown files. Adding a new one means writing a short, opinionated entry point that teaches a lens or methodology, then submitting a pull request.

---

## Where skills live

```
community-skills/
├── probe/         — Idea generation (thematic, supply-chain, alt-plays)
├── dive/          — Company deep analysis (business model, forensics, earnings)
├── track/         — Position tracking (watchlist, thesis check, event radar)
└── landscape/     — Macro & economic research (yield curve, trade flows, labor)
```

Pick the folder that matches what your skill helps with. If none fit, propose a new folder in your PR description.

Skills are intent-routed through the project's `CLAUDE.md` — there's no slash command or auto-discovery. When a user's request matches a skill, Claude reads the file and follows it. New skills become discoverable by adding a one-line entry to the capability map in `CLAUDE.md`.

---

## Two kinds of skill files

**Skill card (`<topic>.md`)** — Short. Teaches a lens. Why it matters, what it reveals that standard analysis misses, how to invoke it. About 200-400 words. Ends with a "What you can ask" list of example user questions.

**Deep workflow (`<topic>-workflow.md`)** — Optional companion to a skill card. Contains the formalized procedure: which MCP tools to call (e.g., `get_ticker_info`, `get_price_history`, `get_hkex_disclosures`), which SEC filings to search, the scoring rubric, the output format. Used when the user wants the full systematic version.

Most contributions are skill cards. Add a workflow only when there's a specific procedure worth formalizing.

---

## Skill card template

```markdown
# [Topic Name]

[One-sentence opener that frames the lens.]

[2-3 paragraphs explaining why this approach reveals something standard analysis misses, what the analyst is actually looking for, and what's non-obvious about it. No SQL. No procedure. No engineering language. Write like a sharp colleague explaining their own framework.]

**What you can ask:**
- "[Example natural-language question 1]"
- "[Example natural-language question 2]"
- "[Example natural-language question 3]"
```

---

## Deep workflow template

```markdown
# Skill: [Topic Name]

**Input:** [what the user provides — usually a ticker or theme]
**Output:** [what gets produced]

---

## Step 1 — [Stage name]

[Description of what to do, with concrete MCP tool calls like `get_ticker_info("0700.HK")`, `get_price_history("AAPL", period="1y")`, or `run_sql` queries against the local cache.]

```sql
SELECT ...
FROM ...
WHERE ticker = '<TICKER>'
```

## Step 2 — [Stage name]

...

## Output Format

[Concrete structure of what the analysis should produce — tables, scoring rubrics, etc.]
```

---

## What good skills look like

- **Specific over generic.** "Track non-GAAP gap widening over 3 years" beats "look at financials carefully."
- **Why-first.** Lead with what the analyst is actually trying to learn, then the how.
- **Analyst voice.** Read like a senior investor talking to a junior, not a tutorial.
- **Honest about limits.** If the approach has known weaknesses or fails in certain conditions, say so.

---

## What to avoid

- Don't restate what the data shows. Skills teach the lens, not the answer.
- Don't write tutorials about MCP server internals or Claude Code itself.
- Don't add procedural ceremony. If the skill can be expressed as one paragraph, write one paragraph.
- Don't include SQL in skill cards (only in `-workflow.md` files).

---

## Submitting

1. Fork the repo
2. Add your file in the right folder
3. Open a PR with a brief description: which folder, what lens, why it's worth adding
4. Be open to feedback — the bar for inclusion is whether a working analyst would find it genuinely useful

If your skill is highly opinionated or domain-specific (e.g., a particular sector lens), that's fine — say so in the file and the PR.

---

## Translated READMEs

`README.md` is the canonical source. Localized versions live alongside it: `README.ja.md` (Japanese), `README.zh-CN.md` (Simplified Chinese). If you change the English README in a way that affects substance — not just typo fixes — please update the translations in the same PR, or flag it in the PR description so a native-speaker maintainer can follow up. Translations are allowed to localize examples (tickers, market references) where natural, but section structure should stay aligned across files.
