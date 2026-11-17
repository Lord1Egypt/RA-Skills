# AI Coding Token Optimizer — ClawHub description

Version: 1.2.0
Slug: ai-coding-token-optimizer

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

## Install and use

`clawhub install ai-coding-token-optimizer`

Then ask: “Use AI Coding Token Optimizer to map this project.”

ClawHub is a distribution option, not an OpenClaw-only dependency. For agents without ClawHub, use the GitHub adoption prompt or their supported skill installer.

## Agent guidelines

Follow SKILL.md:

1. Measure the always-loaded entry point.
2. Keep its binding rules, and move reference material verbatim into routers and guides.
3. Write the task-table maps and a README router for each area.
4. Repoint references to moved sections.
5. Verify that nothing was lost and every link resolves.
6. Report the before and after sizes.

Preserve mandatory instructions and source code, and update the routers whenever paths change. No project scripts, external publishing or secret reading is authorized by mapping.

## Expectations

The first mapping pass uses normal agent context. The always-loaded entry-point saving is measured and reported. Later tasks may also benefit from less repeated exploration, which is not measured. Host discovery of project instructions varies.

## Optional feedback loop

After a run, the skill may ask whether you want to tell the maintainer what changed. This is opt-in and manual: no project data, telemetry or automatic upload is involved. If you agree, the agent prepares a redacted report with host, before/after sizes, approximate token change, validation and usefulness. Review it before submitting through GitHub, ProSkills or ClawHub. Never share code, secrets, private paths, repository URLs or client information.

## Related projects

OpenClaw Token Optimizer audits runtime settings; this skill maps coding projects. ProSkills.md hosts this skill and its adoption prompt. Find more skills at ProSkills.md. None is required to use this package.
