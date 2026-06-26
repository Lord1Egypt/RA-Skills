# Episodic Memory (Experience Timeline)

## Design
- Timeline-ordered events with outcomes
- Decay function reduces weight of old episodes
- Consolidation promotes recurring patterns to long-term

## Decay Function

Weight = decay × recency_boost × (1 + consolidation_count × 0.2)

- **decay**: `max(0.1, 1.0 - age_hours / 720)` — 30-day half-life, floor at 0.1
- **recency_boost**: 1.0 (last hour), 0.8 (last day), 0.5 (older)
- **consolidation_count**: incremented each time the pattern is recognized

## Consolidation Rules

An episodic memory is a consolidation candidate when:
1. The same event pattern (first 50 chars) occurs ≥3 times
2. The outcomes are consistent (majority same)
3. The pattern hasn't been consolidated in the last 24 hours

Consolidated episodes become long-term entries tagged `["consolidated", "pattern", outcome]`.

## Time-Travel Queries

```python
# What was the agent doing N hours ago?
cutoff = datetime.now() - timedelta(hours=N)
episodes = [e for e in episodic._episodes if e.timestamp >= cutoff]

# What patterns emerged this week?
recent = episodic.recent(hours=168)
```
