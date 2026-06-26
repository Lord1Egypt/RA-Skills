# Interaction Log: [Colleague Name]

> Format: JSONL (JSON Lines)
> Storage: `~/.colleague-skill/colleagues/[name]/interaction-log.jsonl`

---

## Log Entry Format

```json
{
  "timestamp": "ISO-8601 datetime",
  "type": "observation|meeting|feedback|memory|decision|pattern",
  "context": "Brief description of the situation",
  "content": "Detailed observation or content",
  "profile_updates": ["List of updated profile dimensions"],
  "confidence": "high|medium|low",
  "source": "direct|second-hand|self-reported"
}
```

---

## Example Entries

### Observation Entry
```json
{
  "timestamp": "2024-03-15T14:30:00Z",
  "type": "observation",
  "context": "Weekly team standup",
  "content": "Pushed back on the new feature timeline citing 'need to see more data on user adoption'. Prefers to delay rather than ship and iterate.",
  "profile_updates": ["decision_making_risk_tolerance", "decision_making_speed"],
  "confidence": "high",
  "source": "direct"
}
```

### Meeting Entry
```json
{
  "timestamp": "2024-03-10T10:00:00Z",
  "type": "meeting",
  "context": "One-on-one with Alex about Q2 planning",
  "content": "Alex prefers written proposals over verbal discussions. Asked me to send agenda 24h before our meetings. Responded quickly to email but delayed Slack messages.",
  "profile_updates": ["communication_channel_preference", "communication_response_pattern"],
  "confidence": "high",
  "source": "direct"
}
```

### Feedback Entry
```json
{
  "timestamp": "2024-03-05T16:00:00Z",
  "type": "feedback",
  "context": "Code review feedback session",
  "content": "Gave direct, specific feedback without sugarcoating. Focused on technical correctness. Didn't mix praise with criticism - just stated what needed to change.",
  "profile_updates": ["collaboration_feedback_style"],
  "confidence": "medium",
  "source": "direct"
}
```

### Memory Entry
```json
{
  "timestamp": "2024-02-28T11:00:00Z",
  "type": "memory",
  "context": "Discussing why we chose PostgreSQL",
  "content": "Alex remembers being part of the database migration decision in 2021. Knows the trade-offs we considered and why Postgres was chosen over MySQL. Has context on the vendor evaluation.",
  "profile_updates": ["institutional_knowledge_historical_context"],
  "confidence": "high",
  "source": "direct"
}
```

### Pattern Entry
```json
{
  "timestamp": "2024-02-20T09:15:00Z",
  "type": "pattern",
  "context": "Three consecutive morning meetings declined",
  "content": "Declined morning meetings three weeks in a row. Previously attended regularly. Possible stress signal or preference change. Asked EA about preferences - they mentioned Alex is 'deep in a technical problem lately'.",
  "profile_updates": ["communication_response_pattern", "recurring_stress_signals"],
  "confidence": "medium",
  "source": "second-hand"
}
```

---

## Quick Reference: Entry Types

| Type | When to Use |
|------|-------------|
| `observation` | Noted behavior, reaction, or interaction |
| `meeting` | Significant meeting content or dynamics |
| `feedback` | How feedback was given or received |
| `memory` | Historical knowledge they shared |
| `decision` | How they made a specific decision |
| `pattern` | Recurring behavior noticed multiple times |

---

## Confidence Levels

| Level | When to Use |
|-------|-------------|
| `high` | Directly observed multiple times, consistent |
| `medium` | Observed once or twice, or second-hand |
| `low` | Single mention, uncertain, or self-reported |

---

## Source Types

| Source | Description |
|--------|-------------|
| `direct` | First-hand observation |
| `second-hand` | Heard from others |
| `self-reported` | Colleague shared directly |

---

*Log entries are cumulative. Historical observations are preserved, not deleted.*
