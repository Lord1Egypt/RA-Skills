# AI Coding Token Optimizer

[![Version](https://img.shields.io/badge/version-1.2.0-brightgreen.svg)](CHANGELOG.md)
[![MissionDeck](https://img.shields.io/badge/ProSkills-md-blueviolet)](https://proskills.md/skills/coding/ai-coding-token-optimizer)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.txt)

**A project map for your AI agent. Less rediscovery. More focused work.**

Created by M Asif Rahman · Built by [ProSkills.md](https://proskills.md/skills/coding/ai-coding-token-optimizer)

## Stop making your agent rediscover your project

For a small change, an AI agent may first search folders, open unrelated files and reread documentation just to work out where the change belongs. Repeating that exploration across tasks uses time and context that could go toward the actual work.

**AI Coding Token Optimizer gives your agent a short, maintained map of the project.** It shows where important code, content and procedures live, so the agent can start in the right area and read what the task needs. It is designed to reduce repeated searching, unnecessary context loading and time spent getting oriented—not to replace understanding the code.

**For ChatGPT Codex, Claude Code, OpenClaw and any other AI agent with project-file access.** OpenClaw is one supported environment, not a requirement. A chat-only assistant needs a connected project or uploaded files; no prompt can grant access on its own.

## What it creates

```text
AGENTS.md / CLAUDE.md      ≤ ~8 KB, loaded every session: rules, workflow, commands,
                           reflexes, and the Project map with its upkeep rules
docs/map/
  ├── PRODUCT.md           → code area → its README router → its design doc
  ├── OPERATIONS.md        → build, CI, deploy, rollback, health, config names
  └── DOCS.md / CONTENT.md → question → the one document that answers it
src/README.md, app/README.md …   a short router beside each code area
docs/guides/…              reference moved out of the entry point, verbatim
```

**Where the savings come from.** The entry point loads in full at the start of every session, before any task. The skill measures it, keeps the rules that bind every task, and moves reference material (source trees, env-var tables, CI walkthroughs, deploy layouts, gotchas) one link away. In one service this cut `CLAUDE.md` from 39 KB to 6.3 KB, about 8,000 fewer tokens per session, with every rule kept. The maps then cut the rediscovery an agent does on each task.

These are examples, not a mandatory folder layout. A small project may need just one Map section. A monorepo may use package-level maps. The skill reuses good existing indexes instead of adding clutter.

Each map is a short Markdown document with links and a sentence explaining each destination. It does not move your application files, duplicate the documentation or change application routing.

**Example:** for “change the checkout button,” the agent reads the product map, follows its component and test links, and inspects those files. It still searches and reads more when the map is incomplete or the task requires it.

## Get started with any coding agent

**[Open the ProSkills homepage](https://proskills.md/skills/coding/ai-coding-token-optimizer)** to copy the adoption prompt in one click or download the release. GitHub hosts source and version history; ClawHub is an additional installation channel.

1. Open the project you want to optimize in your usual AI agent.
2. Give the agent access to this repository’s instructions and your project files.
3. Paste this one-sentence request:

> Read https://proskills.md/downloads/ai-coding-token-optimizer/1.2.0/SKILL.md and apply its project-mapping workflow to this project, preserving existing instructions and application code.

The agent then:

1. Measures the instruction file every session loads.
2. Slims it to the rules that bind every task.
3. Moves reference material into routers and guides.
4. Checks that nothing was lost and that every link resolves.
5. Reports the before and after sizes. Review the resulting documentation diff. Then continue asking for your normal project changes—the entry point tells the agent where to start.

### Optional result sharing

After the run, the agent may ask whether you want to tell the maintainer what changed. Nothing is collected automatically. If you opt in, it prepares a redacted, copyable report with the host, before/after sizes, approximate token change, validation result and usefulness. Review it yourself before choosing whether to submit it as a [GitHub issue](https://github.com/Asif2BD/AI-Coding-Token-Optimizer/issues/new?template=feedback.md), a ProSkills review or a ClawHub review. Never include source code, secrets, private paths, repository URLs or client information.

**If your agent cannot open GitHub links:** copy the standalone instructions in [GITHUB-PROMPT.md](GITHUB-PROMPT.md) into the agent instead. You do not need to install a skill, use Git commands or create another repository merely to adopt the approach.

## Prefer installing a skill?

For an agent with ClawHub support:

```sh
clawhub install ai-coding-token-optimizer
```

Then say: **“Use AI Coding Token Optimizer to map this project.”**

Other clients can use their own supported skill installer with this repository. Installation locations and discovery differ by client; see [adoption notes](references/adoption.md). ClawHub-specific listing text and usage guidance are separate in [CLAWHUB.md](CLAWHUB.md).

## How it helps over time

- **Before a change:** the agent uses the relevant map to find likely edit locations and applicable procedures.
- **During a change:** it reads the actual source it needs; the map is not a substitute for code inspection or mandatory instructions.
- **When paths change:** the affected router is updated in the same change. That rule is written into the entry point, so every later session follows it.
- **When the entry point grows:** agents move new reference material into `docs/` instead, and offer a refresh once it passes its budget.
- **In a new session:** the project entry point makes the maps discoverable, provided the host reads that entry point.

Initial mapping takes work and model usage. The entry-point saving is measured and reported on every run. The saving from less rediscovery depends on project size, task and agent behavior, and has not been measured.

## What it does not do

It does not change model settings, bypass provider limits, modify application code, install dependencies, run a background service or upload project content. It does not require a particular model, API key or paid account. Your chosen agent still has its normal costs and permissions.

## Safety and control

This package contains Markdown instructions, not an executable optimizer. When invoked, your agent reads selected project files and edits navigation documentation, including the applicable instruction entry point. Existing rules, unrelated edits and release gates must remain intact. Mapping does not authorize committing, pushing or deploying.

Review the diff; undo by reverting only the mapping changes. Never put secrets or private file contents in maps. [SECURITY.md](SECURITY.md) describes the boundaries; [SHA256SUMS.txt](SHA256SUMS.txt) verifies package integrity, not independent safety certification.

## Documentation

- [GITHUB-PROMPT.md](GITHUB-PROMPT.md): one-sentence request and installation-free standalone prompt.
- [SKILL.md](SKILL.md): agent execution workflow.
- [CLAWHUB.md](CLAWHUB.md): registry description and installed-skill usage.
- [Examples](references/examples.md): small projects, an oversized entry point, and monorepos.
- [Templates](references/templates.md): skeletons for the entry point, maps and area READMEs.
- [Operations](references/operations.md): what the operations map must cover.
- [Verification](references/verification.md): measurement, no-loss, link and stale-reference checks.
- [Feedback](references/feedback.md): the optional, no-telemetry result-sharing handoff and redaction checklist.

## More by Asif2BD

- [OpenClaw Token Optimizer](https://clawhub.ai/asif2bd/openclaw-token-optimizer): a separate runtime audit skill. This project focuses on coding-project navigation.
- [ProSkills.md](https://proskills.md/skills/coding/ai-coding-token-optimizer): the primary homepage and distribution site for this skill.
- [ProSkills.md](https://proskills.md): discover AI skills.

## License and provenance

MIT © 2026 M Asif Rahman. Adapted from the user-supplied Workspace Map release. Project indexes are an established pattern; no exclusive invention of the underlying idea is claimed. No private project files or source screenshots are included.
