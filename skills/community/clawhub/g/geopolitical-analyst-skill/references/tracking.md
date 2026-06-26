# Longitudinal Tracking Reference

## Purpose

Track situations over time. Compare current assessment to prior assessments. Flag when conditions change or when prior assessments were wrong.

---

## tracking_log.jsonl Schema

One JSON object per line. Append — never overwrite.

```json
{
  "assessment_id": "uuid-v4",
  "topic": "string (normalized: lowercase, no special chars, max 60 chars)",
  "country_codes": ["ISO-3166-1 alpha-2"],
  "assessment_date": "ISO8601",
  "depth_level": "FLASH | BRIEF | FULL",
  "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
  "trend": "ESCALATING | STABLE | DE-ESCALATING",
  "confidence": "HIGH | MEDIUM | LOW | UNVERIFIABLE",
  "gdelt_tone_at_assessment": 0.0,
  "gdelt_tone_trend_at_assessment": "deteriorating | stable | improving",
  "key_actors": ["string"],
  "main_conclusion": "string (1–2 sentences)",
  "watch_item": "string (the single most important thing flagged to monitor)",
  "scenarios": {
    "base_case": "string",
    "alternative": "string",
    "tail_risk": "string"
  },
  "red_team_gaps": ["string (key intelligence gaps identified)"],
  "sources_used": ["string"],
  "outcome_verified": null,
  "outcome_notes": null,
  "superseded_by": null
}
```

---

## Update Rules

### When to create a NEW entry (not update):
- Each new analysis cycle, regardless of topic
- When depth level changes (BRIEF → FULL)
- When a scenario from a previous assessment activates

### When to mark an entry as superseded:
- When a more recent assessment of the same topic exists
- Set `superseded_by` to the new `assessment_id`
- Never delete old entries — historical record has analytical value

### Outcome verification:
- When a situation resolves (ceasefire, election result, coup succeeds/fails):
  - Set `outcome_verified: true`
  - Write `outcome_notes`: what actually happened vs what was assessed
  - This creates a feedback loop for analytical improvement

---

## Delta Analysis Protocol

When loading a prior assessment, generate a delta report:

```
CHANGED:
  - Risk level: [old] → [new] | Reason: [driver of change]
  - Trend: [old] → [new]
  - GDELT tone: [old score] → [new score] (delta: X)
  - Key actors: [added/removed]

HELD FROM PRIOR ASSESSMENT:
  - [What was predicted that proved accurate]

MISSED FROM PRIOR ASSESSMENT:
  - [What changed that the prior assessment did not anticipate]
  - [Identify which intelligence gap (from red_team_gaps) was responsible]

WATCH ITEM STATUS:
  - Prior watch item: [text]
  - Did it materialize? YES / NO / PARTIALLY
  - If YES: note the impact on current assessment
```

Being explicit about misses is as important as tracking accuracy. Analytical credibility requires intellectual honesty about errors.

---

## Topic Normalization

Use consistent topic keys to enable longitudinal tracking across sessions:

| Format | Example |
|--------|---------|
| `[country]-[conflict-type]` | `ukraine-war` |
| `[country]-[political-event]` | `iran-elections-2024` |
| `[actor]-[issue]` | `hamas-ceasefire` |
| `[region]-[dynamic]` | `sahel-coup-wave` |

Always normalize before writing to log. Search by normalized topic key to retrieve prior assessments.

---

## Retrieval Query

When checking for prior assessments:

```python
# Pseudocode — implement in tracking script
entries = load_jsonl("tracking_log.jsonl")
prior = [e for e in entries 
         if e["topic"] == normalized_topic 
         and e["superseded_by"] is None]
prior.sort(key=lambda x: x["assessment_date"], reverse=True)
most_recent = prior[0] if prior else None
```

---

## Self-Correction Protocol

After 10+ entries in tracking_log.jsonl, run periodic calibration:

```
Accuracy metrics to track:
- Risk level predictions: how often did HIGH → escalate vs resolve?
- Trend predictions: how often did ESCALATING → continue vs reverse?
- Watch item activation rate: how often did flagged items materialize?
- Scenario activation: which scenario type activates most often?

If any metric shows systematic bias (e.g., consistently overestimating escalation):
→ Note as calibration flag
→ Adjust confidence thresholds accordingly
→ Document in tracking_log as a meta-entry
```
