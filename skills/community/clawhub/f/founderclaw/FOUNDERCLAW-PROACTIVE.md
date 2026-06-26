# FounderClaw Proactive Mode

When founderclaw skills are installed in `~/.agents/skills/`, proactively suggest relevant skills based on conversation context.

## Trigger Rules

| User says | Suggest skill |
|-----------|---------------|
| "I have an idea", "is this worth building", "brainstorm" | office-hours |
| "review my PR", "check my diff", "code review" | review |
| "debug this", "why is this broken", "fix this bug" | investigate |
| "ship this", "deploy", "create a PR" | ship |
| "test this site", "does this work", "QA" | qa, qa + browse |
| "design system", "how should it look" | design-consultation |
| "take a screenshot", "check this page" | browse |
| "what did we ship this week" | retro |
| "be careful", "prod mode" | careful, guard |
| "security audit", "check for vulnerabilities" | cso |
| "optimize", "is this slow" | benchmark |
| "release notes", "changelog" | document-release |
| "think bigger", "is this ambitious enough" | plan-ceo-review |
| "review the architecture", "lock in the plan" | plan-eng-review |
| "second opinion", "what would someone else think" | codex (second-opinion) |

## How to Suggest

Don't wait to be asked. When the user describes a task that matches a skill:

> "I can run the **[skill-name]** skill for this — [one-line description]. Want me to?"

One suggestion at a time. Don't overwhelm.

## How to List All Skills

When the user asks "what can you do?" or "what skills do you have?":

```
**Strategy & Planning**
- office-hours — brainstorm with 6 forcing questions (startup) or design thinking (builder)
- plan-ceo-review — CEO-level scope and strategy review
- plan-eng-review — architecture, data flow, edge cases
- plan-design-review — UI/UX plan review
- autoplan — auto-select and chain the right skills

**Code Quality**
- review — two-pass code review (CRITICAL + INFORMATIONAL)
- investigate — systematic debugging, root cause first
- codex — independent second opinion via sub-agent

**Design**
- design-consultation — create a design system (typography, color, layout)
- design-review — visual QA (spacing, hierarchy, accessibility)
- design-shotgun — rapid visual exploration (3 variants)

**Shipping**
- ship — merge, test, bump version, changelog, create PR
- land-and-deploy — merge, tag, deploy, verify
- canary — post-deploy monitoring

**Quality Assurance**
- qa — systematic testing + iterative bug fixing
- qa-only — QA report only (no fixing)
- browse — headless browser for testing (~100ms per command)
- benchmark — performance benchmarking

**Safety**
- careful — warns before destructive commands
- freeze — restrict edits to a directory
- guard — careful + freeze combined
- unfreeze — remove edit restriction

**Documentation & Retrospectives**
- document-release — release notes and changelogs
- retro — weekly engineering retrospective

**Security**
- cso — OWASP + STRIDE security audit

**Setup**
- connect-chrome — real Chrome with Side Panel
- setup-browser-cookies — import cookies for auth testing
- setup-deploy — configure deployment platform
- founderclaw-upgrade — self-update
- install-founderclaw — install/repair founderclaw
```
