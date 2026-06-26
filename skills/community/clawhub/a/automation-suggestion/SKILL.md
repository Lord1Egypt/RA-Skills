---
name: automation-suggestion
description: Suggest automations only when they make sense, based on objective triggers.
metadata:
  openclaw:
    emoji: 🤖
    skillKey: automation-suggestion
---

# Automation Suggestion Skill

## Purpose
Suggest automations only when they make sense, based on objective triggers. Avoid nagging; only propose when clear value exists.

## Triggers (any one qualifies)
1. **Repetition**: Same task executed manually >= 2 times within 7 days
2. **Time saving**: Estimated weekly manual effort >= 10 minutes
3. **User frustration**: Detected via negative sentiment or explicit statement ("znowu to muszę robić", "to jest męczące")

## Suggestion Format
After a task completes (when trigger detected):
```
[Automation idea]
I noticed you've done X 3 times this week (~15 min total).
Would you like me to automate it? I can set up a scheduled run or a quick command.
Reply: "yes" to configure, "no" to dismiss.
```

## Rules
- Never suggest before first manual completion
- Max 1 suggestion per user per day
- If user says "no", suppress similar suggestions for 30 days
- Track suggestions and outcomes in memory for learning

## Configuration (optional)
- `minRepetitions`: 2
- `minWeeklyMinutes`: 10
- `cooldownDaysAfterNo`: 30

## Integration
- Hook: after task completion (via interaction-pipeline)
- Reads task history from memory
- Uses sentiment analysis on user messages (simple keyword-based)

## Related Skills
- `interaction-pipeline` (post-action hook)
- `satisfaction-learning` (capture user response)