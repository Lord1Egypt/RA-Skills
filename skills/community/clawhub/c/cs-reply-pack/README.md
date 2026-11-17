# Customer Service Reply Pack

> Customer-service reply library and auto-reply rule pack — intent classification, emotion de-escalation (LEAP method), objection-handling matrix, escalation red lines. Outputs a JSON rule table you can import into any helpdesk or chatbot.

**Category:** customer-support  |  **License:** CC-BY-4.0  |  **Version:** 1.0.0
**Price:** Free on GitHub & skills.sh (CC BY 4.0). Curated bundle on Gumroad: $9 (Pro $29).

## What it does

The three deadly sins of support replies: slow, defensive, blame-shifting. Agents freeze on angry messages; bots answer off-template.

Hardens 'how to answer every message type' into a three-layer structure — intent -> strategy -> script — that human agents copy-paste and bots use as their rule set.

## What you get

- Intent classification: 8 message types mapped to priority + template set.
- Objection matrix using the LEAP method (Listen / Empathize / Ask-Act / Promise) with every promise carrying a deadline.
- Escalation red lines: safety, legal threats, journalists, key accounts, over-limit refunds -> immediate human handoff.
- Deliverables: 30 paste-ready scenario scripts, a 4-step anger cooldown flow, review-recovery scripts, and a JSON auto-reply rule table (intent -> template -> escalate?) importable into any helpdesk or chatbot.

## How to use

- **As an agent skill:** drop `SKILL.md` into your agent's skills folder, or install from the GitHub repo below.
- **As a prompt pack:** open `SKILL.md` and follow the workflow section step by step.
- Works with any agent that reads `SKILL.md` (Claude Code, OpenCode, Cursor, Gemini CLI, Cline, and more).

## Install

```bash
# skills.sh / ClawHub
npx skills add https://github.com/chinabizskills/cs-reply-pack
# ClawHub (after publish)
openclaw skills install @chinabizskills/cs-reply-pack
```

Or clone: `git clone https://github.com/chinabizskills/cs-reply-pack.git`

## Pricing & license

Licensed under **CC BY 4.0** — free to use, share, and adapt (attribution required). A curated, expanded bundle (with the Pro templates) is sold on Gumroad for $9 (Pro $29). The free GitHub/skills.sh version is the complete, working skill.

## Tags

customer-support, chatbot, helpdesk, scripts, automation

## Contents

- `SKILL.md` — the skill definition / prompt library (this is the product).
- `README.md` — this file.
- `skill-card.md` — ClawHub metadata card.
- `RELEASE_NOTES.md` — version history.

---

Part of the **China-Biz Skills** collection by RAY — practical AI agent skills for business, e-commerce, support, legal triage, and content.
