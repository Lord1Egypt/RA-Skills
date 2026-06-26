# Career Spotlight Finder

Turn your past projects into a clear career story — with resume bullets, LinkedIn copy, and a positioning strategy you can actually use.

## Who This Is For

You've done real work — repos, papers, side projects, design docs — but when it comes to describing yourself, you draw a blank. Sound familiar?

- **"I don't know what my strengths are called."** You've built ETL pipelines, but you'd never think to write "data pipeline orchestration" on your resume.
- **"I can't explain what I do."** You know you're good, but turning that into a pitch feels impossible.
- **"My work looks all over the place."** Your projects seem unrelated, but you suspect there's a thread connecting them.
- **"I don't fit one clean label."** Maybe your real edge is the combination of things you do, not any single one.

This skill solves all four.

## Install

**Via [skills.sh](https://skills.sh):**

```bash
npx skills add RealZST/career-spotlight-finder
```

**Via [ClawHub](https://clawhub.ai):**

```bash
clawhub install career-spotlight-finder
```

**Manual:**

Clone into the skills directory for your agent:

```bash
# Claude Code
git clone https://github.com/RealZST/career-spotlight-finder.git ~/.claude/skills/career-spotlight-finder

# Codex
git clone https://github.com/RealZST/career-spotlight-finder.git ~/.codex/skills/career-spotlight-finder

# Gemini CLI
git clone https://github.com/RealZST/career-spotlight-finder.git ~/.gemini/skills/career-spotlight-finder

# Cursor / Windsurf / other agents
# Clone into the agent's skill directory, or use `npx skills add` with the --agent flag
```

## Quick Start

Point the skill at your projects and let it work:

```
Use career-spotlight-finder to analyze ~/projects/my-app and ~/papers/icml-2025.pdf
```

```
Use career-spotlight-finder on these repos and generate resume bullets and a LinkedIn summary:
- ~/work/data-pipeline
- ~/work/ml-serving
- https://myblog.com/building-rl-agents
```

You can also invoke it directly:

- **Claude Code:** `/career-spotlight-finder`
- **Codex:** `$career-spotlight-finder`

## What You Get

### Per-project analysis

Each project is examined across five dimensions — problem solved, methods used, scale achieved, hidden capabilities, and transferable patterns. The skill translates what you actually did into the industry terms that belong on a resume.

> You wrote "cleaned up messy JSON files" → the skill maps it to **"data quality engineering"** and **"ETL pipeline design"**

### Career positioning

The skill infers 2–3 plausible career directions from your work, then **recommends one** as your expert center. You don't have to figure out your own label — it does that for you.

If your edge comes from combining adjacent strengths (e.g., ML depth + systems intuition), it uses a **bridge framing** instead of forcing you into one narrow box.

### Ready-to-use copy

Four outputs, all generated from the same underlying story:

| File | What it is | Length |
|------|-----------|--------|
| `resume-bullets.md` | Action-verb bullets grouped by theme | 8–15 bullets |
| `elevator-pitch.md` | Spoken-tone self-intro | 80–120 words |
| `linkedin-summary.md` | Professional summary with embedded keywords | 150–300 words |
| `casual-intro.md` | Dinner-party version, zero jargon | 2–3 sentences |

### Aggregated report

One `report.md` tying everything together: positioning statement, distinctiveness thesis, term mapping table, narrative arcs, and cross-theme capabilities.

## Supported Inputs

| Input type | Examples |
|-----------|---------|
| Code repositories | Any repo with source files — Python, JS/TS, Go, Rust, Java, etc. |
| Research papers | PDF or LaTeX files with research-trajectory extraction |
| Documents | Design docs, reports, specs, postmortems |
| Word documents | `.docx` files (converted via pandoc or python-docx) |
| URLs | Blog posts, online articles, project pages |
| Mixed directories | Folders containing multiple independent papers or docs |

When you point it at a folder of papers, it automatically detects that they're separate documents and analyzes each one individually.

## Key Features

### It recommends, not asks

Most career tools hand the classification problem back to you. This one analyzes your work and tells you: "Based on your projects, here's where you should position yourself, and here's why." You confirm or redirect.

### It finds what you don't know you know

The five-dimension analysis surfaces hidden capabilities — things like reliability engineering, observability, or API governance that you've been doing but would never think to mention. These often become the strongest resume bullets.

### It connects scattered work into one story

The skill looks for threads across projects that seem unrelated on the surface. Two RL papers + two systems papers? It discovers the arc: "Started with RL algorithms, discovered systems bottlenecks, shifted to building RL infrastructure." That's a story.

### It tells you what makes you different

Not just "you're an ML engineer" — but why you're more memorable than a typical ML engineer. The distinctiveness thesis explains what combination of strengths gives you an edge.

### You control the emphasis

Mark projects as **highlight** or **supporting** to shape which work gets the most narrative weight. The skill respects your judgment about what represents you best.

### It gets smarter over time

Run it again with new projects — existing analyses are preserved. Changed a repo since last time? It detects staleness via git hashes and file timestamps and re-analyzes only what's changed. URL sources are flagged after 7 days.

## How It Works

A six-step pipeline:

```
Init → Analyze → Position → Synthesize → Write Copy → Review
```

1. **Init** — Creates `~/.career-spotlight/` on first run. Reuses it after that.
2. **Analyze** — Reads each project through a lens matched to its type (code repo, paper, document, URL). Extracts problem, methods, scale, hidden capabilities, and transferable tags.
3. **Position** — Clusters your evidence, infers career directions, and recommends a lead framing. Loads domain-specific industry terminology to sharpen the language.
4. **Synthesize** — Discovers the strongest thread across projects, builds narrative arcs from origin to peak, and writes the aggregated report.
5. **Write Copy** — Transforms the analytical report into first-person copy with the right voice for each format.
6. **Review** — You can add projects, change direction, adjust emphasis, or regenerate any output.

## Where Output Lives

```
~/.career-spotlight/
├── analyses/    # one file per project
├── report.md    # aggregated career brand report
├── copies/      # resume-bullets, elevator-pitch, linkedin-summary, casual-intro
└── history/     # archived versions of reports and copy
```

Everything stays local. Nothing is synced or uploaded.

## Covered Domains

The skill ships with industry-term references for: ML/AI, AI Infrastructure, Software Engineering, Systems, Data Engineering, Data Management, Networking, Product Management, Product Design, Developer Relations, Security, and Academic Research.

For domains not covered, it falls back to general knowledge. You can also add your own `industry-terms-[domain].md` file to the `references/` directory — it will be auto-detected.

## Requirements

- An AI coding agent that supports skills (Claude Code, Codex, Cursor, etc.)
- **Optional:** [pandoc](https://pandoc.org/) for `.docx` file conversion (falls back to python-docx if unavailable)

## License

[MIT No Attribution (MIT-0)](LICENSE)
