# clear-view


> An agent skill that turns any conversation, article, paper, tutorial, product brief, or messy discussion into a clear picture of **what is going on right now**: a structured text version plus a lightweight, self-contained HTML infographic.

## What it does

Every run produces two deliverables (unless you ask for only one):

1. **Text version**: topic, current status in one line, structure/flow, what each party said, topic threads, common ground, points of contention, open questions, and a short summary. Sections that do not apply are skipped.
2. **Visual version**: a single-file HTML infographic that opens offline, with speaker markers and a legend, topic branches, and step or relationship diagrams. Mermaid or trees are added only when they help, never instead of the HTML.

It stays faithful to the source: views are attributed to their speakers, unclear points are marked as unclear (dashed lines or question marks on the diagram), and the agent does not take sides or invent facts.

## When to use it

- A group chat or meeting where it is hard to tell who argued what
- A long article or paper you want mapped by argument and evidence
- A tutorial whose outline is unclear
- A product brief with scattered features
- Any "explain this clearly / sort this out" request

Not meant for one-line summaries, pure translation, or code changes.

## Install

Copy this folder into your agent's skills directory. A Chinese (Simplified) version of the skill is available in the GitHub repository under `zh-CN/`. The skill is a single portable `SKILL.md` that works with Codex, Claude Code, Hermes, OpenClaw, and other Agent Skills compatible clients.

```bash
git clone https://github.com/0xcjl/clear-view.git
cp -r clear-view ~/.agents/skills/clear-view   # adjust to your client's skills path
```

From ClawHub:

```bash
clawhub install clear-view
```

## Usage

Give the agent the material and ask, for example:

> Use clear-view to sort out this discussion.

You get the structured text in chat and a `clear-view-{short-slug}.html` file to open.

## Files

```text
clear-view/
├── SKILL.md          # English skill (entry point)
├── README.md
└── LICENSE           # MIT
```

## Attribution

The "shortest visualization that works" idea is inspired by the `show-me` skill from [humanlayer/skills](https://github.com/humanlayer/skills). clear-view is an independent rewrite focused on clarifying text rather than code; no files are copied from that project.

## License

MIT
