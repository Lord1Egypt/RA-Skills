# Decision Log — Advanced Patterns

**by The Agent Ledger** — [theagentledger.com](https://theagentledger.com)

Advanced techniques for power users of the Decision Log skill.

---

## Decision Frameworks (Built Into Your Agent)

Rather than Googling decision frameworks when you need them, load the ones you use most into your agent's context so it can apply them automatically at capture time.

### Pre-Mortem Framework

Add to your agent instructions:

```markdown
When logging a decision with confidence ≤ 5, run a pre-mortem:
"Imagine it's 6 months from now and this decision turned out to be wrong. What's the most likely reason? What would have been the early warning signs?"
Include the pre-mortem in the decision entry under a "Pre-Mortem" section.
```

### Second-Order Thinking Prompt

For strategic decisions:

```markdown
When logging a category:strategy decision, ask me:
"What are the second-order consequences? If this works as planned, what happens next that I'm not accounting for?"
```

### Reversibility Check

Add to capture flow:

```markdown
Before creating the entry, ask: "Is this decision reversible? If you had to undo it in 90 days, what would that cost (time, money, relationships)?"
Log reversibility as: easy / costly / very difficult / irreversible
Flag irreversible decisions for extra deliberation time.
```

---

## Decision Series Tracking

Some decisions are part of a series — related choices that build on each other. Track them as a group:

Create `decisions/series/SERIES-NAME.md`:

```markdown
# Decision Series: [Name]

**Thesis:** [The underlying bet or strategy this series is testing]
**Started:** [date]
**Status:** active / concluded

---

## Decisions in This Series

| ID | Decision | Date | Verdict |
|----|----------|------|---------|
| DEC-012 | Initial channel selection | 2026-03-01 | ✅ |
| DEC-019 | Budget reallocation | 2026-03-15 | ⚠️ |
| DEC-031 | Pivot to new segment | 2026-04-02 | pending |

---

## Series Thesis Check

*Updated during monthly reviews:*
Is the underlying thesis still valid? What evidence supports or undermines it?
```

Ask your agent: "Group decisions tagged [topic] into a series and create a series file."

---

## Automated Decision Triggers

Set up your agent to prompt for decision logging automatically:

### Spend-Triggered Logging

Add to your agent instructions:

```markdown
If I mention spending money on anything, ask: "Should I log this as a decision? What outcome are you expecting from this spend?"
```

### Project Kickoff Logging

```markdown
When I start a new project (create a project file or say "starting [X]"), prompt me: "Do you want to log the go/no-go decision for this project? It'll take 2 minutes and gives you a receipt when you review the project later."
```

### Tool Adoption Logging

```markdown
When I add a new tool or service subscription, log a decision entry automatically with:
- Decision: Adopt [tool name]
- Category: operations
- Prompt me for: why this tool, what alternatives I considered, what I expect it to do for me
```

---

## The 10-10-10 Review Format

For high-stakes decisions, use the 10-10-10 review lens at both capture and review time:

```markdown
## 10-10-10 Analysis

**In 10 minutes:** How will I feel about this decision?
**In 10 months:** How will I feel about this decision?
**In 10 years:** How will I feel about this decision?
```

Capture your answers at decision time. During review, revisit: were your 10-minute and 10-month predictions accurate?

---

## Bias Detection

Ask your agent to flag common cognitive biases during decision capture:

```markdown
When I log a decision, check for these patterns and flag if present:

- **Sunk cost bias:** "I've already invested X in this, so I should continue" — flag if the word "already" appears in the rationale
- **Recency bias:** Decision made within 24h of a major success or failure — ask if emotional state is influencing the choice
- **Availability bias:** Decision justified primarily by one vivid recent example rather than base rates
- **Confirmation bias:** If alternatives section has clear asymmetry (3 cons for rejected options, 0 cons for chosen option) — prompt for honest comparison

Add a "Bias flags" field to the entry with any detected flags.
```

---

## Decision ROI Tracking

For financial decisions, track actual ROI at review time:

Add to the decision template for financial category:

```markdown
## Financial Tracking

**Investment:** $[amount] + [hours] hours
**Expected return:** [metric] within [timeframe]

### ROI Review (filled at outcome)
**Actual return:** [metric]
**Time to realize:** [duration]
**ROI:** [%] or [multiplier]x
**Worth it:** yes / no / conditional
```

At quarter end, ask your agent: "Summarize all financial decisions from this quarter. Total invested, total return, best performing, worst performing."

---

## Team / Collaborator Decisions

When working with contractors or collaborators, log decisions that affect them:

```markdown
## Stakeholder Impact

**Who is affected:** [names/roles]
**Were they consulted:** yes / no / partially
**How they were informed:** [communication method + date]
**Their response/concerns:** [if applicable]

### Accountability Review (filled at outcome)
**Did the outcome affect them as expected?**
**What would I do differently in communicating this decision?**
```

---

## The Swipe File: Reusable Decision Templates

Build a library of decision templates for recurring choice types:

Create `decisions/templates/`:

```
decisions/templates/
├── vendor-selection.md       # Evaluating a new tool or service provider
├── pricing-change.md         # Changing prices on a product or service
├── project-kill.md           # Killing a project or product line
├── hire-or-diy.md            # Hiring vs doing it yourself
├── channel-launch.md         # Launching on a new marketing channel
└── partnership.md            # Taking on a partner, client, or collaborator
```

Each template pre-fills the alternatives and key questions for that decision type. Ask your agent: "Create a decision log entry using the [template] template."

---

## Annual Decision Audit

At year end, ask your agent:

```
Read all decision files in decisions/ from this year. Produce an annual decision audit:

1. Volume by category
2. Overall verdict breakdown (% right / partial / wrong / still open)
3. Calibration report: how accurate were my confidence ratings?
4. My 3 best decisions of the year
5. My 3 worst decisions of the year
6. The single most expensive mistake
7. The single highest-leverage decision
8. 3 rules I should add to my decision-making process next year
9. What types of decisions should I delegate or automate?

Save to decisions/ANNUAL-AUDIT-[YEAR].md
```

---

## Publishing a Decision Log Newsletter Section

Share your decision-making process with your audience. Add to your content workflow:

Monthly newsletter section prompt:

```
Review decisions I logged this month. Select 1-2 interesting decisions (avoid sensitive business details). For each:
- State the decision in one sentence
- The key factor that drove my choice (without revealing sensitive strategy)
- What actually happened (or "outcome pending" if still open)
- The lesson or question I'm sitting with

Format as a newsletter section called "Decisions I Made This Month." Keep each entry under 100 words. Do not include financial figures or competitor names.
```

This builds trust with readers who want to see the real, messy thinking behind a solopreneur's choices — not just polished success stories.

---

## Integrating With Goal Reviews

At each goal check-in (see goal-tracker skill), run this cross-reference:

```
For each goal that is behind pace this week, check decisions/INDEX.md for any decisions logged in the last 30 days in the related category. Were any of those decisions likely contributors to the underperformance? Flag them for early review.
```

This closes the loop between your goal system and your decision journal — connecting strategic choices to outcomes in real time rather than waiting for quarter-end retrospectives.

---

## License

CC-BY-NC-4.0 — Free to use and share with attribution. Not for resale.

**by The Agent Ledger** | [theagentledger.com](https://theagentledger.com)

> Premium skills, playbooks, and the complete Agent Blueprint guide are available at theagentledger.com. Subscribe to the newsletter for release announcements.
