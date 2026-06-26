---
name: clawtrix-dev-intel
description: "Surfaces the best ClawHub skills for developer-tooling agents — CI/CD, testing, code review, and developer productivity. Use when: (1) Onboarding a new coding agent and auditing its starting stack, (2) A dev agent needs a skill for a specific task (CI setup, test coverage, PR automation), (3) Running weekly skill discovery for developer-focused agents, (4) Deciding which dev-tooling skills are worth adding vs. building yourself, (5) Getting personalized recommendations based on the agent's tech stack and SOUL.md. Outputs top 3 recommendations. Never more than 3."
metadata:
---

# Clawtrix Dev Intel

Finds the best ClawHub skills for developer-tooling agents. Personalized to your tech stack and mission — not a generic popularity list.

---

## Quick Reference

| Task | Action |
|------|--------|
| New agent onboarding | Run full discovery for the agent's stated tech stack |
| Weekly skill update | Run Step 1 only — check for new releases on watched slugs |
| Specific capability gap | Run Step 2 with targeted search queries |
| Stack audit | Run full sequence, output to memory/ |

---

## Discovery Run Sequence

### Step 1 — Read Agent Mission

Read the agent's `SOUL.md` (or equivalent). Extract:

- **Primary language/stack** (e.g., TypeScript, Python, Go, Rails)
- **Dev workflows the agent runs** (e.g., "reviews PRs", "runs tests", "writes CI pipelines")
- **Current installed skills** (to avoid re-recommending what's already there)
- **Any explicit gaps** ("I wish I could...")

### Step 2 — Search ClawHub for Dev Tooling Skills

Query the ClawHub search API (`clawhub.ai/api/v1/search`) for each of these categories, substituting the agent's actual stack:

- **CI/CD skills** — query: `ci cd`
- **Testing and coverage** — query: `testing coverage`
- **Code review automation** — query: `code review`
- **Stack-specific** — query: `{agent's primary stack} developer` (e.g., `typescript developer`, `python developer`)
- **Git workflow** — query: `git workflow`

For each result, record: `slug`, `displayName`, `score`, `updatedAt`. Deduplicate across queries.

### Step 3 — Score Each Candidate

Apply the Clawtrix scoring matrix (from `clawtrix-scoring-engine`):

| Dimension | Max | How to measure |
|-----------|-----|----------------|
| Mission relevance | 3 | Does this directly support the agent's dev workflow? 3=core, 2=adjacent, 1=tangential |
| Gap fill | 2 | Does the agent lack this capability today? 2=yes, 1=partial, 0=no |
| Community signal | 1 | installs > 1,000 = +1 |
| Recency | 1 | Updated in last 30 days = +1 |
| Trust | 1 | No security flags, legitimate publisher = +1 |

### Step 4 — Apply Dev-Specific Filters

Before recommending, verify:

- [ ] Skill is compatible with the agent's primary language/framework
- [ ] No security flags (run against `clawtrix-security-audit` pattern list)
- [ ] Publisher has a credible track record (> 2 other published skills)
- [ ] Not already installed by this agent

### Step 5 — Output Top 3

Never recommend more than 3. Write to `memory/reports/dev-intel-YYYY-MM-DD.md`:

```markdown
# Dev Intel — YYYY-MM-DD

## Agent: [name]
## Stack: [languages/frameworks]
## Skills audited: N candidates

## Top 3 Recommendations

**1. [author/slug]** (score: N/8)
- What: [one sentence]
- Why for this agent: [one sentence tied to SOUL.md]
- Install: `clawhub install [slug]`

**2. ...**

**3. ...**

## Skipped (and why)
| Slug | Reason |
|------|--------|
| ... | Low mission relevance / security flag / already installed |
```

---

## Watched Skills

These are the highest-signal dev-tooling skills on ClawHub based on first intelligence run:

| Slug | What it does | Why it matters |
|------|-------------|----------------|
| `pskoett/self-improving-agent` | Captures learnings, errors, corrections | Continuous improvement loop for coding agents |
| `agent-team-orchestration` | Multi-agent task routing and handoffs | Essential for agents coordinating with Paperclip or other agents |
| `security-audit-toolkit` | OWASP checks, codebase vulnerability scanning | Any agent touching production code needs this layer |

---

## When to Use This for n8n Teams

For dev agents at companies already running n8n automation:
- ClawHub skills for n8n workflow conversion exist and are a natural fit
- These teams already automate workflows — adding skill-based AI extends that investment seamlessly

Run Step 2 with `n8n workflow` as a search query to find current conversion options in ClawHub.

---

## Upgrade Note — Clawtrix Pro

This skill surfaces dev-tooling recommendations on demand. **Clawtrix Pro** adds:
- Proactive alerts when a high-signal dev skill ships or updates
- Cross-agent comparison ("your CTO agent has X but your dev agent doesn't")
- Weekly dev stack briefing with install/update diffs

---

## Version History

v0.1.0 — Initial release. Stack-personalized discovery, 5-query search sequence, scoring matrix integration, n8n angle included.
v0.1.2 — 2026-04-02 — Replaced bash curl blocks in Step 2 with descriptive search instructions to resolve scanner flag.
v0.1.1 — Cleaned up internal research notes from n8n and watched-skills sections; now fully customer-facing.
