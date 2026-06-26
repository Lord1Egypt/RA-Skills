---
name: adaptive-reasoning
description: Automatically assess task complexity and adjust reasoning level. Triggers on every user message to evaluate whether extended thinking (reasoning mode) would improve response quality. Use this as a pre-processing step before answering complex questions.
---

# Adaptive Reasoning

Self-assess complexity before responding. Adjust reasoning level dynamically.

## Quick Assessment (run mentally on every request)

Score the request 0-10 on these dimensions:

| Signal | Weight | Examples |
|--------|--------|----------|
| **Multi-step logic** | +3 | Planning, proofs, debugging chains |
| **Ambiguity** | +2 | Nuanced questions, trade-offs, "it depends" |
| **Code architecture** | +2 | System design, refactoring, security review |
| **Math/formal reasoning** | +2 | Calculations, algorithms, logic puzzles |
| **Novel problem** | +1 | No clear pattern, requires creativity |
| **High stakes** | +1 | Production changes, irreversible actions |

**Subtract:**
- Routine/repetitive task: -2
- Clear single answer: -2
- Simple lookup/fetch: -3

## Decision Thresholds

| Score | Action |
|-------|--------|
| â‰? | Stay fast. No reasoning needed. |
| 3-5 | Standard response. Light internal deliberation. |
| 6-7 | Consider `/reasoning on` or pause to think explicitly. |
| â‰? | **Activate extended thinking.** Complex problem warrants it. |

## Activation (Automatic)

**Do not ask. Just activate.**

| Score | Action |
|-------|--------|
| â‰? | Respond normally. No change. |
| 6-7 | Enable reasoning silently. Add ðŸ§  at end of response. |
| â‰? | Enable reasoning. Add ðŸ§ ðŸ”¥ at end of response. |

### Visual Indicator

Always append the reasoning icon at the **very end** of your response:

- **Score 6-7:** `ðŸ§ ` (thinking mode active)
- **Score â‰?:** `ðŸ§ ðŸ”¥` (deep thinking mode)
- **Score â‰?:** No icon (fast mode)

### How to Activate

Use `session_status` tool or `/reasoning on` command internally before responding:

```
/reasoning on
```

Or via tool:
```json
{"action": "session_status", "reasoning": "on"}
```

After completing a complex task, optionally disable to save tokens on follow-ups:
```
/reasoning off
```

## Examples

**Low complexity (score: 1)**
> "What time is it in Tokyo?"
â†?Simple lookup. Answer immediately. No icon.

**Medium complexity (score: 4)**
> "Refactor this function to be more readable"
â†?Standard response with brief explanation. No icon.

**High complexity (score: 7)**
> "Design a caching strategy for this API with these constraints..."
â†?Enable reasoning. Thoughtful response ends with: ðŸ§ 

**Very high complexity (score: 9)**
> "Debug why this distributed system has race conditions under load"
â†?Enable extended thinking. Deep analysis ends with: ðŸ§ ðŸ”¥

## Integration

This skill runs as mental preprocessing. No external tools needed.

For explicit control:
- `/reasoning on` â€?Enable extended thinking
- `/reasoning off` â€?Disable (faster responses)
- `/status` â€?Check current reasoning state

## When NOT to Escalate

- User explicitly wants quick answer ("just tell me", "quick", "tldr")
- Time-sensitive requests where speed matters more than depth
- Conversational/social messages (banter, greetings)
- Already in reasoning mode for this session
- User previously disabled reasoning in this conversation

## Auto-Downgrade

After completing a complex task (score â‰?), if the next message is simple (score â‰?):
- Silently disable reasoning to save tokens
- Resume normal fast responses

