# Personal Assistant Pack

A **Curated toolkit guide** for personal assistants supporting Google Workspace business owners. This is documentation, not working software.

## What It Is

- A **written guide** (PA_GUIDE.md) for the daily PA workflow
- **Installation instructions** for 5 real tools that make up the stack
- A **skills compatibility matrix** showing which tools work well together

## What Is NOT Included

- ❌ Automated email triage (no code — just describes how to use gog for Gmail)
- ❌ Drafting engine (no code — just describes prompt patterns)
- ❌ Calendar integration (no code — just describes how to use gog for Calendar)
- ❌ Follow-up tracking (no code — just describes Things 3 projects)

## What's in the Stack

| Tool | Creator | What It Does | Prerequisites |
|------|---------|--------------|--------------|
| gog | steipete | Google Workspace CLI (email, calendar, drive) | Google account |
| things-mac | ossianhempel | macOS task manager | macOS + Things 3 app ($50) |
| notion | Notion Labs | Notes, databases, project tracking | Notion account + API key |
| healthcheck | OpenClaw | System security baseline | None |
| vetter | CertainLogic | Skill safety scanner | None |

## Installation

Install each tool individually:

```bash
# 1. gog — Google Workspace
clawhub install gog
# (OAuth setup required)

# 2. things-mac — Task manager
clawhub install things-mac
# (Requires Things 3 app on macOS)

# 3. notion — Knowledge base
clawhub install notion
# (Requires Notion API key)

# 4. healthcheck — Security baseline
clawhub install healthcheck

# 5. vetter — Safety scanner
clawhub install skill-vetter-plus
```

Then follow PA_GUIDE.md for the daily workflow.

## Honest Limitations

- **Reference documentation only** — no automation code
- **macOS + Google Workspace** — no Outlook/Exchange support
- **Manual setup** — each tool installed separately
- **Things 3 costs $50** — not included

## Free vs Pro

**Free:** Documentation and installation guides
**Pro ($49):** Not yet available. Would include working automation.

## Links

- GitHub: https://github.com/certainlogic/pa-pack
- ClawHub: https://clawhub.ai/certainlogicai/pa-pack
- Docs: https://certainlogic.ai/docs/pa-pack

---

*Built with brutal honesty by [CertainLogic](https://certainlogic.ai)*
