[简体中文](README.zh.md) · **[English](README.md)** · [日本語](README.ja.md)

# Agentify

Help web pages and sites be easier for **AI agents**, **crawlers**, and **automation tools** to understand, navigate, and operate: analyze agent-friendliness, rewrite templates, and produce team-ready design specs.

## Features

| Capability | Description |
|------------|-------------|
| **Analyze** | Score (0–100) across 9 areas (semantic HTML, ARIA, structured data, forms, navigation, `data-testid`, selector stability, API discoverability, meta signals) with actionable recommendations. |
| **Rewrite** | Enrich HTML/JSX/Vue/Svelte with semantics, ARIA, `data-testid`, JSON-LD, and accessibility/automation attributes **without changing behavior or visuals**. |
| **Design Spec** | Generate an `agent-friendly-spec.md`-style specification for your stack (priorities, examples, anti-patterns, verification). |

Example triggers: *agent-friendly*, *SEO / structured data*, *add data-testid*, *scraper-friendly*, *a11y audit*, etc.

## Repository layout

```
Agentify/
├── README.md               # English (default)
├── README.zh.md
├── README.ja.md
├── SKILL.md                # Skill entry (Agent Skills–compatible)
└── references/
    ├── checklist.md
    ├── frameworks.md
    ├── knowledge-base.md
    ├── patterns.md
    ├── scoring.md
    ├── spec-example.md
    └── spec-template.md
```

For full behavior, see [`SKILL.md`](SKILL.md).

## Usage

The loadable skill is **`SKILL.md` and `references/` as sibling paths** (same directory). You can use this repository root as that folder, or copy/symlink only those two into a dedicated skill directory.

- **Cursor** — Add that folder to your Cursor user skills directory.
- **OpenClaw** — Place it under `~/.openclaw/skills/` or your workspace `skills/` directory (see [OpenClaw Skills](https://docs.openclaw.ai/skills/) for load order and optional `skills.load.extraDirs` in `~/.openclaw/openclaw.json`).

## License

If no `LICENSE` is present, all rights are reserved; add a `LICENSE` file before open distribution.
