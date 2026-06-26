---
name: community-demand-prospecting
description: Audit a repo or product, run market research and competitor research, choose positioning, find users, and draft safe Reddit or X outreach.
---

# Community Demand Prospecting

## Overview

Turn vague growth ideas into a repeatable workflow: find relevant community conversations, estimate intent, avoid bad-fit threads, and draft replies that help first and promote only when appropriate.

Default to human-in-the-loop. This skill is for demand capture and community prospecting, not mass posting or deceptive automation.

It is especially useful for repo audit, launch readiness, market research, competitor research, positioning, finding users for a product, and planning Reddit or X outreach.

## Quick Start

Collect a compact product brief before doing outreach research. Ask for only what is missing:

- Product name and one-line description
- Target user or buyer
- Main pain points solved
- Best differentiators
- Allowed claims and forbidden claims
- Desired tone
- Destination link, demo, or CTA

If the user has not provided a brief, use the template in `assets/product-brief-template.md`.

If the user only provides a repository, landing page, or README, start with a launch-readiness audit and market scan before doing community prospecting. Use:

- `references/repo-launch-readiness.md`
- `references/market-research.md`
- `references/positioning-heuristics.md`
- `assets/repo-audit-template.md`
- `assets/market-scan-template.md`
- `assets/positioning-brief-template.md`

## Operating Sequence

Run the skill in this order unless the user explicitly asks for a narrower deliverable:

1. Extract or complete the product brief.
2. Audit launch readiness if the input is a repo, README, or rough landing page.
3. Research users, competitors, substitutes, and category shape.
4. Choose one primary positioning angle.
5. Translate the product into user pain-language.
6. Generate search queries and locate candidate threads.
7. Score each thread for intent and risk.
8. Choose the engagement ladder.
9. Draft outreach in platform-native style.
10. Return a decision-oriented report.

## Concrete Example

Example request:

```text
I built a small developer tool. Audit the repo, research similar products, figure out the best positioning, then find Reddit threads where people are asking for alternatives and draft replies I could use.
```

Example output shape:

```markdown
## Launch blockers
- No screenshot in README
- Weak headline

## Market summary
- Crowded category with a few incumbents
- Users switch when setup is too slow

## Positioning
- Primary angle: simplicity
- One-line positioning: A lightweight alternative for developers who only need X

## Opportunities
1. Thread: <url>
   - Intent: 5
   - Risk: 2
   - Mode: Soft mention
   - Draft reply: ...
```

## Workflow

Follow this sequence unless the user asks for only one narrow output.

### 1. Build the Product Brief

If the user gives a repo instead of a polished product brief, derive the brief from:

- README headline and subhead
- install steps
- release assets
- screenshots or demo assets
- stated use cases
- obvious trust blockers such as unsigned binaries or missing docs

Call out launch blockers before recommending outreach. Common blockers:

- no screenshot or demo
- weak headline
- unclear audience
- missing install path
- trust friction
- no clear CTA
- overly narrow positioning

If needed, read `references/repo-launch-readiness.md`.

### 2. Research the Market and User Landscape

Before drafting outreach, understand the category:

- who the likely user is
- what job they are hiring the product for
- what alternatives or substitutes they already mention
- whether the market is crowded, fragmented, or lightly served
- what angle is most differentiated: speed, simplicity, price, trust, control, niche fit, or workflow fit

When researching similar products, capture:

- direct competitors
- indirect substitutes
- incumbent tools
- manual workaround patterns

When researching users, capture:

- where they ask for help
- how they describe the pain
- what triggers them to switch
- what objections or trust concerns appear repeatedly

Do not reduce market research to a feature checklist. Prefer:

- positioning differences
- target user differences
- trust and adoption friction
- discovery channel differences

If needed, read `references/market-research.md` and use `assets/market-scan-template.md`.

### 3. Choose the Positioning Angle

After the market scan, decide what the product should lead with.

Choose the main angle from evidence, not preference:

- problem: the pain is obvious and urgent
- audience: the product is clearly for a narrow group with shared identity
- comparison: users already compare products in this category
- simplicity: incumbents feel bloated, complex, or expensive
- trust: users fear failure, security risk, or setup friction
- workflow fit: the product fits a specific repeated job better than generic tools

Pick one primary angle and at most one secondary angle.

Avoid stacking too many angles into the same message. A weak “everything tool” message usually performs worse than a narrow but clear one.

If needed, read `references/positioning-heuristics.md` and use `assets/positioning-brief-template.md`.

### 4. Build the Demand Map

Translate the product brief into how real people describe the problem:

- Frustrations
- Current workaround
- Desired outcome
- Alternatives they mention
- Trigger phrases they use when they are ready to switch or buy

If needed, read `references/intent-signals.md`.

### 5. Generate Search Queries

Create search queries for each platform using:

- problem-first phrases
- comparison phrases
- recommendation phrases
- migration phrases
- complaint phrases
- workflow phrases

Prefer queries that look like what a founder would actually search manually. Include both broad and narrow variants.

### 6. Find Candidate Threads

Search for conversations where the author is:

- actively asking for a tool
- comparing alternatives
- frustrated with an existing workflow
- requesting recommendations
- describing an expensive manual workaround

Do not treat every mention as an opportunity. Skip vanity mentions, generic news, and unrelated discussions.

### 7. Score Intent and Risk

Score each candidate thread across two dimensions:

- Intent score: `0-5`
- Risk score: `0-5`

Use this rubric:

- Intent `5`: actively asking for a solution, recommendation, alternative, or migration path now
- Intent `4`: strong pain and explicit need, but not directly asking to buy
- Intent `3`: clear pain but vague urgency
- Intent `2`: adjacent discussion, weak buyer signal
- Intent `1`: mostly curiosity or news
- Intent `0`: not relevant

- Risk `5`: clear anti-promo context, likely rule violation, or obviously off-topic
- Risk `4`: probably poor fit, strong chance of backlash
- Risk `3`: mixed fit, needs caution
- Risk `2`: reasonable fit, still keep the reply light
- Risk `1`: low risk
- Risk `0`: very safe context

Do not recommend engagement on threads with intent lower than `3` or risk higher than `3` unless the user explicitly asks for aggressive exploration.

If the platform or community norms matter, read `references/platform-guardrails.md`.

### 8. Choose the Engagement Ladder

Choose one of three modes for each thread:

- `Help only`: answer the question without mentioning the product
- `Soft mention`: answer first, then lightly mention the product if it genuinely fits
- `Direct mention`: recommend the product directly because the ask is explicit and the fit is strong

Default to the least promotional option that still serves the user.

### 9. Draft Replies in Native Style

Write like a participant in that platform, not like an ad.

- Reddit: specific, plain, contextual, low-hype
- X: shorter, sharper, more conversational

Avoid:

- generic praise
- vague hype
- repetitive language across threads
- fake neutrality when self-promoting
- pushing links before establishing relevance

If needed, read `references/reply-patterns.md`.

### 10. Produce a Decision-Oriented Output

Return the results in a format the user can act on immediately:

- launch blockers if present
- market summary
- user summary
- competitor or substitute summary
- positioning recommendation
- primary positioning angle
- channel recommendation
- search queries
- top thread or account targets
- intent and risk scores
- recommended engagement mode
- draft reply
- rationale
- follow-up suggestion

Use the template in `assets/outreach-output-template.md` when the user wants a reusable report format.

## Output Standards

When presenting opportunities, keep each item compact and decision-ready:

- `Why this is relevant`
- `Why this is risky or safe`
- `What to say`
- `Why that wording fits`

When the user asks for many replies, vary the structure and opening sentence. Do not generate near-duplicates.

## Guardrails

Treat these as hard constraints:

- Do not optimize for volume over fit.
- Do not advise deceptive personas or fake customer identities.
- Do not recommend mass posting or mass replying.
- Do not ignore subreddit rules or platform rules.
- Do not present spammy behavior as “growth”.
- Do not force a product mention when a helpful answer alone is better.

When unsure, say the thread should be skipped.

## Deliverables

This skill is strongest at producing:

- repo-to-product-brief audits
- launch-readiness assessments
- lightweight market scans
- user pain summaries
- competitor and substitute maps
- positioning briefs
- community prospecting plans
- buyer-intent search queries
- scored lead/thread lists
- platform-native draft replies
- post idea banks based on repeated pain points
- “engage / wait / skip” decisions
- lightweight launch packs for developer-built products

## Resources

Read only the resource that matches the task:

- `references/intent-signals.md`: use when building queries, judging buyer intent, or clustering pain-language
- `references/market-research.md`: use when researching users, competitors, substitutes, and category positioning
- `references/platform-guardrails.md`: use when deciding whether engagement is safe on Reddit or X
- `references/positioning-heuristics.md`: use when deciding whether to lead with problem, audience, comparison, simplicity, trust, or workflow fit
- `references/reply-patterns.md`: use when drafting replies or post ideas
- `references/repo-launch-readiness.md`: use when the user provides a repo, README, release page, or unfinished product positioning
- `assets/market-scan-template.md`: use when the user wants a structured market or competitor scan
- `assets/positioning-brief-template.md`: use when the user wants a concise positioning recommendation before outreach
- `assets/product-brief-template.md`: use when the product brief is incomplete
- `assets/repo-audit-template.md`: use when turning a repo into a usable product brief and launch checklist
- `assets/thread-scorecard-template.md`: use when the user wants a reusable scoring worksheet
- `assets/outreach-output-template.md`: use when the user wants a structured report or operating cadence

## Example Triggers

Use this skill for requests such as:

- “Find Reddit threads where people need this app.”
- “Research X posts from people frustrated with this workflow.”
- “Score these threads and tell me which ones are worth replying to.”
- “Draft helpful Reddit comments that can mention my product if appropriate.”
- “Turn this product brief into community prospecting queries.”
- “I built this repo. Figure out how to market it.”
- “Audit this GitHub project before we try to promote it.”
- “Research the market for this product before suggesting marketing.”
- “Find similar tools and tell me how users talk about this problem.”
- “Figure out how this product should be positioned before we launch.”
- “Do a repo audit before launch.”
- “Run market research and competitor research for this app.”
- “Help me find users for my product.”
- “Create a launch strategy from this GitHub repo.”
- “Plan Reddit outreach for this product.”
- “Find customers for my app without spamming.”
