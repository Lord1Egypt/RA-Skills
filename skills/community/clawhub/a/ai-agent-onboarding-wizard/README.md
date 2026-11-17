# CertainLogic Onboarding Wizard

**5 minutes to a productive agent. Not 5 days of trial and error.** ⚡

Most new OpenClaw users install a dozen random skills, discover half don't work, uninstall them, and repeat. A week later they're frustrated and their agent still can't do useful work.

This wizard fixes that. One scan, one report, exact install commands. Your agent is productive on day 1.

v2.1.0

## What It Does

1. **Auto-scans your environment** — OS, OpenClaw version, installed skills
2. **Detects your goal** — developer, business, research, productivity, beginner
3. **Recommends a starter stack** — CertainLogic skills + verified community skills
4. **Generates install checklist** — exact `clawhub install` commands, you run when ready

**Nothing auto-installs. Nothing auto-configures. You control every step.**

## Quick Start

```bash
clawhub install certainlogic-onboarding-wizard
```

Then say:
- "Run onboarding wizard"
- "I'm a developer"
- "Set up my business stack"

## What You Get

A markdown report like:

```markdown
## Environment Detected
- OS: Linux (Ubuntu 22.04)
- OpenClaw: 2026.4.12
- Existing skills: 12 installed

## CertainLogic Skills Recommended
- ⬜ Skill Vetter Plus — `clawhub install skill-vetter-plus`
- ⬜ Smart Router — `clawhub install certainlogic-smart-router`
- ✅ Token Reduction Engine (already installed)

## Community Skills Recommended
- ⬜ GitHub Integration — `clawhub install github`
- ⬜ Skill Creator — `clawhub install skill-creator`
- ⏭️ Things 3 (skipped — macOS only, you're on Linux)
```

## Automated Detection

| What It Checks | How |
|----------------|-----|
| Operating system | `platform.system()` — Linux/macOS |
| OpenClaw version | `openclaw --version` |
| Installed skills | Scans `~/.openclaw/skills/` |
| Platform compatibility | Skips macOS-only skills on Linux |

## Honest Limitations

- Recommendations are opinions (our testing, not universal)
- Auto-detection is heuristic (misses custom setups)
- Doesn't configure API keys or credentials
- Verification checks file structure, not runtime behavior

## Free Is the Product

CertainLogic free products are built to the same standard as paid products.
Upgrade when you want deeper support, not when you need basic features.

**Everything here is free:**
- Full environment scan
- All goal profiles
- One-command setup scripts (`--setup-script`)
- Post-install verification (`--verify`)
- Weekly checkups (`--weekly-checkup`)
- Team onboarding export (`--team-export`)

**Pro ($29) is a relationship, not an unlock:**
- Priority support (24 hour response guarantee)
- Early access to new features
- Custom industry templates (healthcare, legal, finance)
- One-on-one onboarding call (15 min)

## Why Not Fork This?

Clones ship code. We ship code + documentation + edge-case handling + active maintenance.

Every failure path in this wizard has a helpful error message.
Knockoffs ship `print("error")` and call it a day.

## Links

- [GitHub](https://github.com/CertainLogicAI/certainlogic-onboarding-wizard)
- [ClawHub](https://clawhub.ai/certainlogicai/certainlogic-onboarding-wizard)

---

*Built by CertainLogicAI. We want every new OpenClaw user to start strong.*
