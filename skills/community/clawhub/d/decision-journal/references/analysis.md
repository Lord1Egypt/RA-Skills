# Decision Analysis

Methods for extracting insights from your decision history.

## Decision Quality Metrics

### Process Quality Score

Rate each decision's process (1-5):

| Score | Criteria |
|-------|----------|
| 1 | No deliberation, purely reactive |
| 2 | Considered one alternative |
| 3 | Considered 2-3 options briefly |
| 4 | Thorough analysis of multiple options |
| 5 | Used structured framework, sought input |

### Outcome Accuracy

Compare expected vs. actual outcomes:

```
Accuracy = (Expected outcomes that materialized) / (Total expected outcomes)
Surprise factor = (Unexpected significant outcomes) / (Total outcomes)
```

### Decision-Outcome Matrix

| | Good Process | Poor Process |
|---|-------------|--------------|
| **Good Outcome** | Skill, repeatable | Luck, dangerous pattern |
| **Bad Outcome** | Bad luck, review process | Expected, fix process |

## Pattern Detection

### Temporal Patterns

- **Decision velocity**: Decisions per week/month
- **Decision clustering**: Do decisions bunch around certain events?
- **Review compliance**: % of decisions reviewed on schedule

### Category Analysis

By tag (career, finance, health, etc.):

- Which categories consume most decision energy?
- Where are outcomes most/least predictable?
- Which categories show improvement over time?

### Bias Indicators

Watch for these patterns:

| Pattern | Possible Bias |
|---------|---------------|
| Always choosing middle option | Compromise bias |
| Rarely reversing decisions | Sunk cost fallacy |
| Outcomes consistently worse than expected | Overconfidence |
| Avoiding decisions until forced | Procrastination/avoidance |
| Similar decisions, different outcomes | Inconsistency |

## Review Prompts

### Monthly Review Questions

1. What decisions did I make this month?
2. Which decision am I most/least satisfied with?
3. What patterns do I notice in my decision-making?
4. What would I do differently?
5. What's one thing I'll improve next month?

### Quarterly Review Questions

1. How has my decision quality changed?
2. What types of decisions are getting easier?
3. What recurring decision situations do I face?
4. What principles are emerging from my decisions?
5. How can I systematize better decisions?

### Annual Review Questions

1. What were my 5 most consequential decisions?
2. How well did I anticipate outcomes?
3. What have I learned about how I make decisions?
4. What decision-making habits serve me well?
5. What new frameworks or tools should I adopt?

## Visualization Ideas

### Decision Timeline

```
Timeline of decisions with:
- Color = category
- Size = importance
- Shape = outcome (✓ ✗ ~)
```

### Decision Flow

```
[Options considered] → [Decision made] → [Expected] → [Actual] → [Lesson]
```

### Improvement Curve

Track average process quality and outcome accuracy over time.

## Export Formats

### Markdown Report

```markdown
# Decision Review: [Period]

## Summary
- Total decisions: N
- Reviewed on time: N%
- Average process quality: X/5
- Outcome accuracy: Y%

## By Category
[Table]

## Key Insights
[Bullet points]

## Decisions to Revisit
[List]
```

### JSON Structure

```json
{
  "period": "2025-Q1",
  "summary": {
    "total_decisions": 42,
    "reviewed": 38,
    "avg_process_quality": 3.4,
    "outcome_accuracy": 0.72
  },
  "by_category": {
    "career": { "count": 8, "avg_quality": 4.1 },
    "finance": { "count": 12, "avg_quality": 3.2 }
  },
  "patterns": [...],
  "recommendations": [...]
}
```
