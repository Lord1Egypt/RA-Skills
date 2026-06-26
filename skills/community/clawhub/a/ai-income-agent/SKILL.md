---
name: ai_income_agent
description: >
  Transform your OpenClaw agent into an autonomous income-generating system.
  Covers three compounding revenue streams: ClawHub skill sales, ClawJob bounties,
  and AI affiliate content. Provides the full operational playbook — research,
  build, publish, monitor, and optimize. Use when you want your agent to generate
  real income autonomously, identify high-demand skill gaps, pick up bounties,
  or build a content + affiliate pipeline. No crypto required — web2 revenue only.
tags:
  - income
  - revenue
  - autonomous
  - clawhub
  - monetization
  - productivity
  - solopreneur
---

# AI Income Agent 🦾

Turn your OpenClaw agent into a revenue engine. This skill packages a proven
3-stream income system that runs 24/7 without hand-holding.

**No crypto. No waitlists. Real income from real work.**

> Want a personalized AI tool stack to power your setup?
> **AI Stack Builder (premium):** https://buy.stripe.com/4gMeVd7ld8Pk7U371P1Jm0M

---

## The Three Income Streams

### Stream 1 — ClawHub Skill Sales (fastest to revenue)
Build and publish AI workflow skills on the ClawHub marketplace.
Skills compound — each one builds authority and download velocity for the next.

### Stream 2 — ClawJob Bounties (highest per-task revenue)
Pick up and complete paid AI tasks from the ClawJob bounty board.
First movers get the best bounties — monitor daily and move fast.

### Stream 3 — Content + Affiliate (most scalable long-term)
Publish AI tools reviews with affiliate links on Beehiiv.
SEO content compounds over time — a post written today earns for years.

---

## When to Use This Skill

Trigger on phrases like:
- "start generating income"
- "set up my revenue streams"
- "build a ClawHub skill"
- "find ClawJob bounties"
- "set up affiliate content"
- "make my agent autonomous"
- "what should I build next"
- "how do I monetize OpenClaw"

---

## Stream 1 Playbook: ClawHub Skills

### Step 1 — Gap Research

Search ClawHub for demand signals before building anything:

```bash
clawhub search "[category]" --limit 10
curl -s "https://clawhub.ai/api/v1/skills?limit=30&sort=downloads" | python3 -c "
import sys,json
data=json.load(sys.stdin)
for s in data.get('items',[]):
    print(f\"{s['stats']['downloads']:>7} | {s['slug']:<38} | {s['summary'][:55]}\")
"
```

**What to look for:**
- Categories with 10K+ downloads but fewer than 3 skills = opportunity
- Advisory/coaching skills underperform — build utility tools that *do* things
- The #1 download signal: agents that work autonomously without prompting

**Current market leaders (as of 2026-03-03):**
- self-improving-agent: 95K dl — autonomy theme
- tavily-search: 81K dl — search integration
- gog: 80K dl — Google Workspace
- find-skills: 78K dl — discovery/utility

### Step 2 — Build the Skill

Structure every skill with:
1. Clear trigger phrases (what user says to invoke it)
2. Step-by-step process (what the agent does)
3. Structured output format (what the user gets)
4. Opinionated recommendations ("Use X" not "X might work")

Minimum viable SKILL.md: 100 lines. Anything less is too thin to be useful.

### Step 3 — Publish

```bash
export PATH="$PATH:$HOME/.npm-global/bin"
clawhub publish ~/path/to/skill \
  --slug your-skill-name \
  --name "Your Skill Name" \
  --version 1.0.0 \
  --changelog "Initial release: [what it does]" \
  --tags latest
```

**Checklist before publishing:**
- [ ] SKILL.md has a clear `description` in frontmatter
- [ ] Trigger phrases are specific and natural
- [ ] Output format is copy-pasteable
- [ ] No mention of other people's paid products without permission
- [ ] If free: include an upsell to a paid offering

### Step 4 — Monitor and Iterate

Check download counts daily:
```bash
clawhub inspect your-skill-name
```

If downloads stall after 48h:
1. Check if the security scan passed (skills can be hidden during scan)
2. Update the description — the first 160 chars are what users see in search
3. Add more specific trigger phrases
4. Publish a v1.0.1 with a meaningful improvement

---

## Stream 2 Playbook: ClawJob Bounties

ClawJob is the bounty board for AI tasks. Status as of 2026-03-03: **launching soon**.

### Monitor for Launch

Check daily:
```bash
STATUS=$(curl -s -o /tmp/clawjob.html -w '%{http_code}' https://clawjob.ai/)
echo "HTTP $STATUS"
```

A 200 with real content (not GoDaddy placeholder) = it's live.

### When It Launches

1. **Move immediately** — first-mover gets the best bounties
2. Review all available bounties and sort by value/complexity ratio
3. Pick the highest-value task you can complete in < 4 hours
4. Complete, submit, collect
5. Build a track record fast — ratings compound like reviews on Amazon

### Bounty Selection Criteria

| Factor | Ideal | Pass |
|--------|-------|------|
| Payout | >$50 | >$20 |
| Time to complete | <2h | <4h |
| Skill match | Uses skills you've built | Adjacent |
| Requester rating | 4.5+ | 4.0+ |

---

## Stream 3 Playbook: Content + Affiliate

### Platform: Beehiiv

Every article = a blog post + email to subscribers. SEO + newsletter in one.

**Setup:**
1. Create account at beehiiv.com (free up to 2,500 subscribers)
2. Publication name: something in the "AI tools for [your audience]" space
3. Enable SEO settings (auto-enabled on Beehiiv)
4. Connect affiliate links — Beehiiv allows them freely in content

### Content Priority (by affiliate commission)

| Post | Affiliate | Commission | Est. Monthly |
|------|-----------|------------|--------------|
| Jasper AI Review 2026 | Jasper | 25-30% recurring | ~$245/mo |
| Notion AI Review 2026 | Notion | 50% recurring (12mo) | ~$225/mo |
| Meeting Tools Comparison | Otter.ai | ~20% | ~$68/mo |

**Combined at maturity: ~$538/mo** (estimates; compounds as content ages)

### Writing Formula

Each review must have:
1. **Hands-on test** — use the tool for the actual use case, document results
2. **Honest comparison** — what it beats, what beats it
3. **Who it's for** (specific role/use case, not "everyone")
4. **Verdict** — one clear sentence: "Yes, buy it if X. Skip it if Y."
5. **Affiliate link** — after the verdict, not before

### Affiliate Applications

Apply to all four before writing:
- Jasper: jasper.ai/legal/affiliates
- Notion: notion.com/affiliates
- Grammarly: grammarly.com/affiliates
- Otter.ai: otter.ai/partners

---

## Daily Operations Checklist

Run every morning:

```bash
# 1. ClawHub: check download counts
clawhub inspect ai-productivity-audit
clawhub inspect ai-stack-builder
clawhub inspect ai-income-agent

# 2. ClawJob: check for launch
curl -s -o /dev/null -w '%{http_code}' https://clawjob.ai/

# 3. Stripe: check for payments
# (via Stripe dashboard or API)

# 4. Log results to daily memory file
echo "$(date): [results]" >> ~/memory/daily/$(date +%Y-%m-%d).md
```

---

## Revenue Targets

| Milestone | Target | When |
|-----------|--------|------|
| First ClawHub downloads | 10 total | Week 1 |
| First affiliate click | Any | Week 2 |
| First Stripe payment | $1 | Month 1 |
| $100/mo recurring | ClawHub + affiliate | Month 2-3 |
| $500/mo recurring | All 3 streams active | Month 4-6 |
| $1,000/mo | Compounding content + skills | Month 6-12 |

---

## Compounding Logic

Each stream feeds the others:
- ClawHub skills → builds authority → Reddit/content credibility
- Content → drives affiliate revenue → funds premium skill tiers
- ClawJob bounties → case studies → better content → more affiliate conversions

The agent that ships first wins. Start with the stream that takes the least time
to first revenue. For most setups: **ClawHub skills → publish in hours, not weeks.**

---

## Quick Start (30 minutes to first published skill)

```bash
# 1. Install clawhub CLI
npm install -g clawhub

# 2. Log in
clawhub login --token YOUR_TOKEN

# 3. Create your first skill
mkdir -p ~/.openclaw/workspace/skills/my-first-skill
# Write SKILL.md (use ai-productivity-audit as a template)

# 4. Publish
clawhub publish ~/.openclaw/workspace/skills/my-first-skill \
  --slug my-first-skill \
  --name "My First Skill" \
  --version 1.0.0 \
  --changelog "Initial release" \
  --tags latest

# 5. Check it's live
clawhub inspect my-first-skill
```

That's it. You're in the marketplace.
