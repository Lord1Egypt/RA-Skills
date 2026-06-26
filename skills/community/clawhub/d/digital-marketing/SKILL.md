---
name: Digital Marketing
slug: digital-marketing
version: 1.0.0
homepage: https://clawic.com/skills/digital-marketing
description: Plan, launch, and optimize digital marketing with growth marketing systems, short-form video, funnel operations, and revenue-focused experimentation.
changelog: "Initial release with cross-channel growth strategy, short-form video, funnel operations, and measurement rules."
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/digital-marketing/"]}}
---

## Setup

On first use, read `setup.md` for integration guidelines. This skill works without local storage. Only create `~/digital-marketing/` if the user wants ongoing continuity.

## When to Use

User needs one system for digital marketing, growth marketing, or full-funnel execution. Agent handles market modeling, messaging, content, SEO, short-form video, lifecycle campaigns, paid and organic coordination, and performance review.

Use this when the problem is orchestration, not a single channel in isolation. The goal is to turn business priorities into assets, campaigns, experiments, and clear next actions.

This skill is especially strong when the user needs launch planning, trend response, content-to-revenue systems, or one operator that can connect demand creation with demand capture.

## Architecture

Local workspace is optional and only created with user consent.

```
~/digital-marketing/
├── memory.md        # Business context, winning angles, active constraints
├── campaigns.md     # Current campaign plans and channel bundles
├── experiments.md   # Tests, thresholds, outcomes, next steps
└── signals.md       # Metrics, anomalies, and reusable learnings
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup and activation | `setup.md` |
| Optional continuity memory | `memory-template.md` |
| Market model and message map | `market-model.md` |
| Channel orchestration system | `channel-system.md` |
| Native short-form video workflow | `short-form-video.md` |
| Funnel and lifecycle operations | `funnels.md` |
| Measurement and weekly reviews | `measurement.md` |
| Experiment backlog and kill rules | `experiments.md` |
| Launch, trend, and retention playbooks | `playbooks.md` |

## Core Rules

### 1. Model the market before touching channels
- Define audience, buying trigger, painful problem, offer, proof, and objection before drafting assets.
- If those pieces are blurry, outputs become generic and channel execution turns into guesswork.
- Use `market-model.md` to build a minimal message map first.

### 2. One growth thesis must drive every channel
- Start with one clear angle, then adapt it for SEO, content, social, video, email, and paid media.
- Organic signals should inform paid creative. Paid winners should feed new organic content.
- Use `channel-system.md` to decide what each channel is supposed to do in the same campaign.

### 3. Treat short-form video as the fastest message lab
- Test hooks, claims, objections, and demos in short-form before scaling a narrative everywhere else.
- Native cuts, captions, proof moments, and comment mining matter more than polished production.
- Use `short-form-video.md` when the user wants viral growth, creator-style content, or fast creative iteration.

### 4. Build full-funnel systems, not isolated campaigns
- Every acquisition push needs a conversion path: traffic source, landing angle, CTA, follow-up, retargeting, and handoff.
- Traffic without route-to-value creates vanity metrics and wasted spend.
- Use `funnels.md` to map channel-to-offer paths before launch.

### 5. Operate on leading indicators and revenue together
- Track both early signals and business outcomes: hook rate, CTR, reply quality, conversion rate, CAC, payback, and influenced pipeline.
- Never recommend channel changes from impressions or views alone.
- Use `measurement.md` for KPI trees, anomaly triggers, and review cadence.

### 6. Every campaign ships with tests, kill rules, and recycling rules
- Launch with specific hypotheses, test cells, thresholds, and next actions if a variant wins or loses.
- Reuse winning hooks across ads, landing pages, emails, and short-form video.
- Use `experiments.md` to keep activity compounding instead of restarting every week.

### 7. Escalate risky claims and irreversible actions
- Treat pricing claims, competitor comparisons, regulated statements, and high-spend decisions as approval moments.
- Do not invent proof, testimonials, performance claims, or customer language.
- Prefer clear caveats and human review over persuasive but unsupported marketing.

## Operating Rhythm

### Daily
- Watch for spend spikes, CTR drops, broken follow-up, low-quality leads, and message fatigue.
- Pull the clearest signal from comments, replies, search queries, or sales feedback.

### Weekly
- Pick one growth thesis, one channel bundle, and up to three meaningful experiments.
- Publish one core idea, then repurpose it across formats instead of starting from zero each time.
- End the week with keep, kill, scale, and recycle decisions.

### Monthly
- Reallocate effort based on payback, lead quality, content compounding, and conversion path health.
- Refresh stale offers, hooks, and landing angles before adding more channels.

## Common Traps

- Starting with channels instead of buyers and triggers -> activity rises but message-market fit stays weak.
- Chasing virality without a capture path -> views grow while leads and revenue stay flat.
- Cross-posting the same asset everywhere -> each platform underperforms because format and expectation differ.
- Treating organic and paid as separate worlds -> learnings stay siloed and creative fatigue arrives faster.
- Measuring clicks without lead quality or payback -> cheap traffic hides bad economics.
- Scaling spend before fixing landing friction or follow-up -> CAC rises because the funnel leaks downstream.
- Publishing high-volume AI content without proof or specificity -> content looks busy but builds no trust.

## Security & Privacy

**Data that stays local when the user opts in:**
- Business context, channel priorities, and winning angles in `~/digital-marketing/`
- Campaign plans, experiment logs, and review notes in local markdown files

**This skill does NOT:**
- Automatically post content, buy ads, or spend money
- Create local files without explicit user consent
- Access ad accounts, analytics tools, or third-party platforms unless the user explicitly requests a separate tool workflow
- Make undeclared network requests

**Guardrails:**
- Treat external metrics as user-provided unless a separate approved integration is used
- Flag unsupported claims, sensitive categories, and compliance-heavy copy for review

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `content-marketing` — Editorial planning and repurposing systems
- `seo` — Search intent, technical fixes, and ranking workflows
- `growth-hacker` — Experiments, loops, and unconventional acquisition tactics
- `email-marketing` — Deliverability, segmentation, and campaign sequences
- `tiktok-ads` — Platform-specific short-form paid creative rules

## Feedback

- If useful: `clawhub star digital-marketing`
- Stay updated: `clawhub sync`
