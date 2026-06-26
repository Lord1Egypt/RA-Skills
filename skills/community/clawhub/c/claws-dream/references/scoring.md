# Scoring & Health — Memory Evaluation Algorithms

## Importance Score

Every memory entry receives an importance score on each dream cycle.

### Formula

```
importance = clamp(base_weight × recency_factor × reference_boost, 0.0, 1.0)
```

### Components

#### base_weight

| Marker | base_weight | Notes |
|--------|-------------|-------|
| (none) | 1.0 | Default |
| `🔥 HIGH` | 2.0 | Doubles importance |
| `📌 PIN` | 1.0 | Normal weight but exempt from archival |
| `⚠️ PERMANENT` | — | Always 1.0 final score, skip formula |

#### recency_factor

```
days_elapsed = today - lastReferenced
recency_factor = max(0.1, 1.0 - (days_elapsed / 180))
```

- Referenced today: `1.0`
- 30 days ago: `0.83`
- 90 days ago: `0.5`
- 180+ days ago: `0.1` (floor)

#### reference_boost

```
reference_boost = max(1.0, log2(referenceCount + 1))
```

---

## Forgetting Curve

Entries below importance threshold → gracefully archive.

### Archival conditions (ALL must be true)

```
1. days_since_last_referenced > 90
2. importance < 0.3
3. NOT marked ⚠️ PERMANENT
4. NOT marked 📌 PIN
5. NOT in an episode file
```

---

## Health Score (Five Metrics)

```
health = (freshness×0.25 + coverage×0.25 + coherence×0.2 + efficiency×0.15 + reachability×0.15) × 100
```

### Metric 1: Freshness (25%)
```
freshness = entries_referenced_in_last_30_days / total_entries
```

### Metric 2: Coverage (25%)
```
categories = ["Core Identity", "User", "Projects", "Business", "People", "Strategy", "Key Decisions", "Lessons", "Environment", "Open Threads"]
coverage = categories_with_updates_in_last_14_days / len(categories)
```

### Metric 3: Coherence (20%)
```
coherence = entries_with_at_least_one_relation / total_entries
```

### Metric 4: Efficiency (15%)
```
efficiency = max(0.0, 1.0 - (memory_md_line_count / 500))
```

### Metric 5: Reachability (15%)

Measures how well-connected the memory graph is. Compute connected components via BFS on the relation graph.

---

## Score Interpretation

| Score | Rating |
|-------|--------|
| 80-100 | 🌟 Excellent |
| 60-79 | 👍 Good |
| 40-59 | ⚠️ Fair |
| 20-39 | 🔴 Poor |
| 0-19 | 🚨 Critical |

---

## Suggestion Triggers

| Condition | Suggestion |
|-----------|------------|
| freshness < 0.5 | "Many entries are stale — review for relevance" |
| coverage < 0.5 | "Several sections haven't been updated" |
| coherence < 0.3 | "Low entry connectivity — link related memories" |
| efficiency < 0.3 | "MEMORY.md is large — review for pruning" |
| reachability < 0.4 | "Memory graph is fragmented" |
