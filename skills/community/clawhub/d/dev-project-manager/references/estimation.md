# Estimation & Effort Communication Guide

## Purpose

This reference covers how to translate engineering effort estimates into client-friendly language, how to calculate AI vs. human cost comparisons, and how to assess AI agent success probability for tasks.

## Translating Engineer Estimates for Clients

Engineers think in story points, components, and technical complexity. Clients think in time, money, and impact. Your job is to translate without losing accuracy.

### Effort-to-Timeline Translation

Never give the client a single number. Always give a range, because estimates are inherently uncertain.

| Engineer Says | You Tell the Client |
|--------------|-------------------|
| "Trivial, maybe 1 story point" | "This is a quick change — we're looking at a few hours of work, likely completed within a day." |
| "Small, 2-3 story points" | "A straightforward change that should take 1-3 days to implement and verify." |
| "Medium, 5-8 story points" | "This is a moderate piece of work — roughly 1-2 weeks including development and testing." |
| "Large, 13+ story points" | "This is a significant effort — we're looking at 2-4 weeks of dedicated development, possibly more depending on what we find during implementation." |
| "Epic, needs to be broken down" | "This is a major initiative that we'd recommend breaking into phases. Each phase would have its own timeline once we've mapped out the approach." |

### Language Rules for Client Communication

**Do say:**
- "Roughly," "approximately," "in the range of"
- "Based on our assessment, we estimate..."
- "This could take longer if [specific condition]"

**Do not say:**
- Story points, sprints, velocity (these are internal terms)
- Exact hours with false precision ("37.5 hours")
- "Easy" or "simple" (reduces perceived value and creates accountability risk)
- "Guaranteed by [date]" (estimates are estimates, not commitments)

### Surfacing Risk in Estimates

When an estimate has high uncertainty, communicate it clearly:

"We estimate this at roughly 2 weeks of development work. However, the [specific area] involves [specific risk — e.g., integration with a third-party API we haven't tested], which could add up to an additional week if we encounter complications. We'll have a clearer picture after the first few days of implementation."

## AI vs. Human Cost Model

Every SRS includes a cost comparison section. Here's how to build it.

### Standard Human Bill Rates

Use these default rates unless the client has established different rates. Rates should reflect typical market rates for qualified professionals. Adjust per region/context as needed.

| Role | Default Hourly Rate |
|------|-------------------|
| Senior Full-Stack Developer | $150/hr |
| Frontend Developer | $125/hr |
| Backend Developer | $135/hr |
| QA Engineer | $100/hr |
| DevOps / Infrastructure | $140/hr |
| Database Administrator | $130/hr |
| UI/UX Designer | $120/hr |
| Project Manager (human) | $130/hr |

### Human Effort Estimation by Complexity

These are baseline estimates for a single requirement or task. Actual hours come from the engineer's assessment — these are sanity-check ranges.

| Complexity | Typical Human Hours (per requirement) | Roles Typically Involved |
|-----------|---------------------------------------|------------------------|
| Trivial | 1-4 hours | 1 developer |
| Low | 4-16 hours | 1-2 developers |
| Medium | 16-40 hours | 2-3 developers + QA |
| High | 40-120 hours | 3-4 developers + QA + DevOps |
| Very High | 120-320 hours | Full team, multi-sprint |

### AI Agent Effort Estimation

AI agents work faster but their reliability varies by complexity. Use this model:

| Complexity | AI Estimated Time | Time Reduction vs Human | Notes |
|-----------|------------------|----------------------|-------|
| Trivial | 5-15 minutes | ~95-98% faster | Automated changes, config updates |
| Low | 15 min - 2 hours | ~90-95% faster | Straightforward component work |
| Medium | 2-8 hours | ~80-90% faster | Multi-component, moderate logic |
| High | 8-40 hours | ~60-80% faster | Complex logic, needs iteration |
| Very High | 40-100+ hours | ~40-70% faster | May need human oversight/intervention |

### AI Cost Calculation Formula

AI costs are estimated based on token consumption, which correlates with task complexity.

**Base assumptions:**
- Input token cost: $5.00 per million tokens
- Output token cost: $15.00 per million tokens
- Average input-to-output ratio: 3:1 (AI reads more than it writes)

**Token consumption estimates by complexity:**

| Complexity | Estimated Input Tokens | Estimated Output Tokens | Estimated Iterations | Total Cost |
|-----------|----------------------|----------------------|--------------------|-----------| 
| Trivial | 10,000 | 3,000 | 1-2 | $0.10 - $0.20 |
| Low | 50,000 | 15,000 | 2-3 | $0.50 - $1.00 |
| Medium | 200,000 | 60,000 | 3-5 | $2.00 - $5.00 |
| High | 800,000 | 250,000 | 5-10 | $8.00 - $25.00 |
| Very High | 3,000,000 | 1,000,000 | 10-20 | $30.00 - $100.00 |

**Formula per task:**
```
AI Cost = (input_tokens × $5.00 / 1,000,000) + (output_tokens × $15.00 / 1,000,000)
Total AI Cost = AI Cost × estimated_iterations
```

**Note:** These are estimates. Actual token consumption varies based on codebase size, context needed, and number of revision cycles. When presenting to clients, use the range and note that actual costs may vary.

### Savings Calculation

```
Human Cost = sum of (hours_per_role × hourly_rate) for each role involved
AI Cost = calculated per formula above
Savings = Human Cost - AI Cost
Savings Percentage = (Savings / Human Cost) × 100
```

### Risk-Adjusted Cost

For tasks where AI success probability is below 85%, calculate a risk-adjusted cost that accounts for potential fallback to human work:

```
Risk-Adjusted AI Cost = (AI Cost × Success%) + (Human Cost × (1 - Success%))
Risk-Adjusted Savings = Human Cost - Risk-Adjusted AI Cost
```

Present both the optimistic (straight AI) and risk-adjusted numbers in the SRS.

## AI Success Probability Framework

Every task in the SRS gets an AI success probability rating. This represents the PM's and engineer's joint assessment of how likely the AI agents are to successfully implement the task without significant human intervention.

### Probability Guidelines

| Probability | Criteria | Examples |
|------------|---------|---------|
| 95-99% | Trivial or highly repetitive tasks with clear patterns. Never say 100%. | Copy changes, config updates, simple CRUD, CSS adjustments, adding a standard form field |
| 85-94% | Straightforward tasks with clear requirements and established patterns | New component following existing patterns, standard API endpoint, basic validation logic |
| 70-84% | Moderate complexity with some ambiguity or multi-step coordination | Complex form with conditional logic, multi-table query changes, integration with familiar APIs |
| 50-69% | High complexity, novel patterns, or significant uncertainty | New architectural patterns, complex business rules, unfamiliar third-party integrations |
| Below 50% | Very high complexity, cutting-edge requirements, or high ambiguity | Novel algorithms, complex migrations with data transformation, real-time system changes, tasks requiring extensive domain knowledge not in codebase |

### Factors That Lower Probability

- Ambiguous requirements (even after elicitation)
- Complex state management across multiple components
- Integration with poorly documented third-party services
- Database migration with data transformation
- Requirements that cross multiple system boundaries
- Novel UI interactions without existing patterns to follow
- Performance optimization without clear benchmarks

### Factors That Raise Probability

- Clear, testable acceptance criteria
- Existing patterns in the codebase to follow
- Well-documented APIs and services
- Isolated changes that don't affect other components
- Standard CRUD operations
- Changes matching common software patterns

### Presenting Probability to Clients

Frame it positively and practically:

"For this feature, we rate our AI development confidence at 85%. That means we expect the automated development process to handle this smoothly, with a small chance we'll need some additional iteration. The cost estimate already accounts for this — we've included a buffer."

For lower-confidence items:

"This feature has some complexity that makes AI-only delivery less certain — we rate it at 65%. We've included a risk-adjusted cost estimate that accounts for the possibility that some portions may need additional work cycles. Even at this confidence level, the cost savings compared to traditional development are significant."

**Never present probability as a quality indicator.** A 65% success probability doesn't mean the end result will be 65% as good — it means there's a 35% chance the agents need more iterations or human guidance to get it right. The delivered quality standard is the same regardless.

## Presenting Estimates in Context

When you assemble the full cost/effort section of the SRS or Client Assessment Summary, organize the information in layers:

1. **Summary first** — Total project cost comparison, total savings, overall timeline comparison
2. **Feature-by-feature** — Individual breakdowns so the client can see where the value is
3. **Risk-adjusted view** — Show what happens if the lower-confidence items need extra work
4. **Methodology note** — Brief explanation of how estimates were derived (human rates based on market standards, AI costs based on computational resources consumed)

This lets the client see the forest before the trees, and gives them the detail they need to make informed decisions.
