# AI Opportunity Discovery — AI Business Consultant Skill for AI Agents

**Find out where AI actually helps your business — and where it doesn't.**

An open-standard [agentskills.io](https://agentskills.io/specification) skill that turns any compatible AI agent into an AI opportunity-discovery consultant. It interviews a business owner or manager about their real workflows, tools, and pain points, then delivers a written AI opportunity assessment: prioritized use cases, complexity and data-readiness scores, risks, a build-vs-buy call, and a phased roadmap — including an honest "don't use AI here, use plain automation instead" section when that's the right answer.

100% self-contained. No API keys, no external services, no paid tools required — just structured interview logic and scoring rubrics the agent applies conversationally.

## Compatible with

- **Claude** (Claude Code, Claude apps, Claude Skills)
- **OpenClaw** / **ClawHub**
- **Hermes Agent** (Nous Research)
- Any other agent that supports the [agentskills.io](https://agentskills.io/specification) open standard (Cursor, Codex CLI, Gemini CLI, and 20+ others)

## What it does

1. **Interviews first.** Asks about the business, its workflows, repetitive tasks, document/data load, existing tools, cost centers, and constraints — before naming a single AI use case.
2. **Maps opportunities.** Screens workflows with the data-rich/process-heavy heuristic and a business-signal → solution-category reference table.
3. **Scores rigorously.** Every candidate gets a business-impact and feasibility score (data readiness, process documentation, decision complexity, error tolerance) on a 1–5 rubric.
4. **Applies a "no AI" filter.** Explicitly flags tasks better solved with plain automation, a rules engine, or off-the-shelf software — because AI isn't always the right call, and pretending otherwise is how AI projects fail.
5. **Recommends build vs. buy.** Commodity problems → buy; proprietary/differentiating workflows → build.
6. **Delivers a roadmap.** Executive summary, workflow map, prioritized opportunity table, "where not to use AI," and a phased plan (quick wins / mid-term / strategic bets).

## Frameworks it's built on

Not guesswork — grounded in documented methodology (full citations in `reference/framework-sources.md`):

- Peter Drucker's Seven Sources of Innovation
- Clayton Christensen's Jobs-to-be-Done
- The Impact–Feasibility / Value–Effort prioritization matrix used in AI and automation consulting
- The data-rich / process-heavy screening heuristic for AI use-case identification
- Standard AI-readiness scoring (data quality, process documentation, ownership, error tolerance)
- Build-vs-buy strategy heuristics (commodity vs. differentiator)

## Install

**OpenClaw / ClawHub**

```bash
clawhub install <your-handle>/ai-opportunity-discovery
```

or add this repo as a tap and install from source.

**Hermes Agent**

```bash
hermes skills install <your-handle>/ai-opportunity-discovery/skills/ai-opportunity-discovery
```

or drop the folder into `~/.hermes/skills/`.

**Claude**
Drop the `ai-opportunity-discovery/` folder into your Claude Skills directory, or upload it as a project skill.

## Usage

Ask your agent something like:

> "Analyze my business and tell me where I should — and shouldn't — use AI."

The agent will run the discovery interview in batches, then produce the full assessment once it has real answers — not before.

## Folder structure

```
ai-opportunity-discovery/
├── SKILL.md                          # entry point — frontmatter + workflow
├── reference/
│   ├── scoring-rubric.md             # 1-5 impact/feasibility rubric
│   └── framework-sources.md          # citations and methodology
└── README.md
```

## License

MIT — free to use, modify, and redistribute.

## Version

1.0.0 — initial release. A second skill (technical AI Integration Architect, for engineers who already know what they want to build) is planned as a companion, not included here.
