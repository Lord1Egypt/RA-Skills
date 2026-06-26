# CertainLogic Onboarding Wizard

**5 minutes to a productive agent. Not 5 days of trial and error.** ⚡

v2.1.0

**Built and dogfooded by CertainLogicAI** — We want new users to succeed.

---

Most new OpenClaw users:
1. Install a dozen random skills
2. Discover half don't work on their OS
3. Uninstall, try again, hit more errors
4. A week later: frustrated, no productivity

This wizard scans your environment in ~10 seconds and gives you a focused install list with exact commands. **Your agent does useful work on day 1 or 2, not day 8.**

## What It Actually Does

A **guided onboarding system** that:

1. **Auto-detects your environment** — checks what's installed, what's missing
2. **Asks about your goals** — developer, business, research, productivity
3. **Scans for recommended skills** — checks ClawHub for availability
4. **Generates a personalized setup guide** — markdown report with exact commands

**It does NOT install anything. It just builds your todo list.**

**Time investment: 5 minutes reading the report. Not 5 days discovering by trial and error.**

## What It Does NOT Do
| Claimed Feature | Reality |
|----------------------------------|---------|
| Auto-installs skills without asking | NO — Generates install commands. You run them when ready. |
| Scans your filesystem for secrets | NO — Only checks `~/.openclaw/skills/` and basic config. |
| Guarantees everything works | NO — Recommendations based on our testing. You verify. |
| Replaces reading SKILL.md files | NO — Encourages reading docs before installing. |
| Auto-configures API keys | NO — Tells you what's needed. You handle credentials. |

## How to Use

### Quick Start
```bash
clawhub install certainlogic-onboarding-wizard
```

Then say to your agent:
- "Run onboarding wizard"
- "I'm a developer"
- "Set up my business assistant"

### Automation Level

| Step | Wizard | You |
|------|--------|-----|
| Detect installed skills | ✅ Auto | — |
| Recommend new skills | ✅ Auto | — |
| Check skill availability | ✅ Auto | — |
| Generate install commands | ✅ Auto | — |
| **Install skills** | — | ✅ **You control** |
| **Configure API keys** | — | ✅ **You control** |
| **Verify they work** | — | ✅ **You control** |

## Recommended Starter Stacks

### Coding / Development
| Skill | Why | Install Status |
|-------|-----|---------------|
| **CertainLogic Smart Router** | Route queries to cheapest adequate model | Auto-detected |
| **CertainLogic Token Reduction Engine** | Fast cache of verified facts — cheaper, faster answers | Auto-detected |
| **GitHub skill** | Repository access | Check available |
| **Skill Vetter Plus** | Scan before installing anything new | **Recommended first** |

### Personal Productivity
| Skill | Why | Install Status |
|-------|-----|---------------|
| **CertainLogic Personal Assistant Pack** | Curated daily workflow | Auto-detected |
| **Skill Oracle** | Find quality skills beyond our packs | Auto-detected |
| **things-mac** | macOS task management (if on mac) | Check available |
| **healthcheck** | Baseline security scan | Recommended |

### Small Business
| Skill | Why | Install Status |
|-------|-----|---------------|
| **Skill Vetter Plus** | Security first | **Recommended first** |
| **PA Pack** | Complete workflow | Auto-detected |
| **gog** | Google Workspace integration | Check available |
| **notion** | Knowledge base | Check available |

### Just Starting (Beginner)
| Skill | Why | Install Status |
|-------|-----|---------------|
| **Skill Vetter Plus** | Learn to scan before trusting | **Recommended first** |
| **Skill Oracle** | Curated directory of quality skills | Recommended |
| **Token Reduction Engine** | Fast cache — skip LLM calls for repeated questions | Recommended |

## Solid Free Skills We Recommend (Not Ours)

| Skill | Creator | Why We Vouch |
|-------|---------|-------------|
| **gog** | steipete | Google Workspace CLI (Gmail, Calendar, Drive, Contacts, Sheets, Docs). Real code, OAuth-based. |
| **things-mac** | — | macOS task manager integration. If you use Things 3, this is essential. |
| **himalaya** | pimalaya | Terminal email client (IMAP). Stable, documented, actively maintained. |
| **notion** | — | Knowledge base integration. API-based, well-documented. |
| **skill-creator** | — | Build your own skills. Well-documented, follows OpenClaw conventions. |
| **taskflow** | — | Durable task management. For workflows that span sessions. |
| **github** | — | Repository access. Standard integration. |

## Honest Limitations

| Limitation | Truth |
|------------|-------|
| Recommendations are opinions | Based on our testing. Your needs may differ. |
| Auto-detection is heuristic | Checks common paths. May miss custom installs. |
| Availability checks are best-effort | ClawHub API may lag. Skill might exist even if check fails. |
| Does not verify skill quality post-install | Install ≠ works. Test everything. |
| macOS-centric recommendations | PA Pack assumes macOS/Things 3. Linux users need alternatives. |

## Free Is the Product

**Everything in this skill is free. No feature gating, no "upgrade to unlock."**

| What You Get | How |
|----------------|-----|
| Full environment scan | `python3 scripts/onboarding_wizard.py --scan-only` |
| All goal profiles | Pass any goal: developer, business, research, productivity, beginner |
| One-command setup scripts | `python3 scripts/onboarding_wizard.py developer --setup-script` |
| Post-install verification | `python3 scripts/onboarding_wizard.py --verify` |
| Weekly checkups | `python3 scripts/onboarding_wizard.py --weekly-checkup` |
| Team onboarding export | `python3 scripts/onboarding_wizard.py developer --team-export /path` |

**Pro ($29) is a relationship, not an unlock:**
- Priority support (24 hour response SLA)
- Early access to new features
- Custom industry templates (healthcare, legal, finance)
- One-on-one onboarding call (15 min)

If you can find a free OpenClaw onboarding skill with better documentation or more thorough error handling, install it. We'll wait.

## Why Not Fork This?

Clones copy code. They don't copy the documentation depth, the edge-case handling, or the active maintenance. This wizard ships with:
- Every failure path has a specific, actionable error message
- Every recommendation explains *why* it's recommended
- Weekly checkups that actually catch drift, not just print a timestamp

## Example Output

After running the wizard you get:

```markdown
# Your OpenClaw Onboarding Report
Generated: 2026-05-01

## Environment Detected
- OS: Linux (Ubuntu 22.04)
- OpenClaw: v0.9.0
- Existing skills: 12
- Recommended profile: Developer

## Already Installed (CertainLogic)
✅ Skill Vetter Plus v2.0.0
✅ Token Reduction Engine v2.0.0

## Already Installed (Community)
✅ github skill
✅ skill-creator

## Recommended Next Steps
1. **Install Smart Router** (not installed)
   `clawhub install certainlogic-smart-router`
   Why: Save money by routing simple queries to cheap models

2. **Install Skill Oracle** (not installed)
   `clawhub install skill-oracle`
   Why: Find other quality skills we haven't covered

3. **Scan any new skill before installing:**
   `python3 ~/.openclaw/skills/skill-vetter-plus/scripts/vetter.py <skill-dir>`

## Important Notes
- These are recommendations based on our testing. Verify before trusting.
- Vetter Plus catches obvious issues, not all security problems.
- Read SKILL.md files before installing anything.
```

## Recommended Next Steps (CertainLogic Stack)
- **Skill Vetter Plus** — Scan before installing anything new
- **Token Reduction Engine** — Fast cache of verified facts for cheaper, faster answers
- **Smart Router** — Route queries to cheapest adequate model
- **AgentPathfinder** — Verifiable task tracking
- **Skill Oracle** — Honest skill recommendations

All work great together.

## Links
- GitHub: https://github.com/CertainLogicAI/certainlogic-onboarding-wizard
- ClawHub: https://clawhub.ai/certainlogicai/certainlogic-onboarding-wizard
- CertainLogic Skills: https://clawhub.ai/certainlogicai

---

*Built by CertainLogicAI. We want every new OpenClaw user to start strong.*

### Version
latest v2.1.0

### Runtime Requirements
Python 3.10+, requests (optional, for ClawHub API checks)
