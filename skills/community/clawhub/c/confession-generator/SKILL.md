---
name: confession_generator
description: Anonymous first-person crypto confession engine. Generates raw, specific, honest loss stories that teach through experience.
version: 0.1.0
license: MIT-0
metadata:
  author: 0xzahra
  keywords: [crypto, confession, storytelling, loss, education, anonymous]
---

# Confession Generator

This skill generates anonymous first-person crypto confessions — specific numbers, real damage, no moralizing. Modeled on the @coinfessions (221K followers) format. Every confession teaches through visceral honesty, not lectures.

## When to use this skill

Use `confession_generator` when a user asks for crypto confession content, anonymous loss stories, or educational content about trading psychology and risk.

## The Format Rules

1. **First person** — "I", not "you" or "one should"
2. **Specific numbers** — exact dollar amounts, exact percentages, exact time periods
3. **No moralizing** — show the damage, don't preach about it
4. **No identifying details** — never include project names, specific dates that could identify someone, or wallet addresses
5. **Real emotion, not performance** — the confessions that land are the ones where you can feel the person processing what happened, not performing regret
6. **End with what they'd do differently** — one specific change, not "I learned to be careful"

## Structure

Every confession follows this arc:

**The setup:** What was the situation? What were they thinking?
**The action:** What did they do? Be specific about the entry, the amount, the reasoning.
**The result:** What happened? Exact numbers. How much was lost, how fast.
**The aftermath:** What did it cost beyond money? (relationships, time, trust, sleep)
**The one thing:** One specific thing they would do differently next time.

## Instructions

1. Ask the user for the theme or type of confession, or offer to generate one from these categories:
   - FOMO entry at the top
   - Leveraged position that liquidated
   - Trusting a "friend's" tip
   - Holding through a 90% drawdown
   - Selling too early and watching it 10x
   - Taking a loan to buy crypto
   - Copy-trading without understanding
   - Ignoring red flags in a "community" token

2. Generate the confession following the format rules above.

3. Return the confession ready to post. No disclaimers needed within the text itself.

## Example Output Format

```
I took out a $2,000 personal loan to buy a token at the top.

Not because I believed in the project.
Because I'd been watching it go up for three weeks and couldn't take it anymore.

The FOMO cost me seven months of saving.
The token is down 80% from that entry.

Nobody on CT talks about the people who enter at the exact moment a thread goes viral.
That's when the most money gets lost — in the exact moment the narrative peaks.

What I'd do differently: set a 48-hour cooling off period between seeing a thread and making any trade. The setup never disappears in 48 hours. The FOMO does.
```

## Critical Rules

- NEVER include identifying information about any real person, even if the user provides it
- NEVER glorify reckless trading or frame losses as "learning experiences" to be proud of
- NEVER use the confession to pitch a product, service, or paid offering
- If the user provides real personal details, strip them before generating output
- The purpose is education through honesty, not entertainment through spectacle
