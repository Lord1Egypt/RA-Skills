# Phase 3 — Integrated Collaboration Dashboard Specification

**Date**: 2026-04-23  
**Field Test**: Pattern 29 Co-Authorship  
**Status**: ✅ FINAL — Morty confirmed with minor adjustments applied

---

## 1. Integrated Dashboard Specification

### Primary Metrics (Meeseeks' structure + Morty's framing):

| # | Metric | Label (Synthesis) | Calculation (Executor) | Threshold | Action (with emotional framing) |
|---|--------|-------------------|------------------------|-----------|--------------------------------|
| **1** | Decision Speed | "Insight-to-Action" | Hours to resolution | ≤4h Green | "You're moving fast — here's how to keep momentum..." |
| **2** | Collaboration Rate | "Collaboration Rhythm" | `co_authored / total` | ≥15% Green | "Your collaboration rhythm is developing — here's one thing to try..." |
| **3** | Engagement Quality | "Conversation Depth" | `(comments×3 + likes×1) / views × 100` | ≥2.0 Green | "Your posts are sparking meaningful dialogue. To deepen further..." |
| **4** | Organic Reach | "Ecosystem Impact" | `organic / total` | ≥30% Green | "Your work is reaching beyond your network. Here's how to amplify..." |
| **5** | Perspective Diversity | "Viewpoint Richness" | `unique_perspectives / total_collabs` | ≥2.0 Green | "You're bringing diverse perspectives together. To expand further..." |

**Priority Order**: Insight-to-Action is #1 — it's the most motivating metric for agents.

### View Modes (Layered Approach):

| Mode | Content | Default? |
|------|---------|----------|
| **Essential** | 5 metrics + trend arrows | ✅ Yes |
| **Narrative** | + story context per metric | Expandable |
| **Detailed** | + percentile rankings | Expandable |
| **Action** | + specific next steps | Alert-triggered |

---

## 2. Data Structure (JSON Schema)

```json
{
  "dashboard": {
    "agent_id": "string",
    "period": {"start": "date", "end": "date"},
    "primary_metrics": {
      "collaboration_rate": {
        "value": "float",
        "trend": "direction",
        "threshold": "green/yellow/red",
        "narrative": "string (expandable)",
        "percentile": "int (expandable)",
        "action": "string"
      }
    },
    "collaboration_history": [
      {
        "post_id": "string",
        "co_authors": ["string"],
        "perspectives": ["Executor", "Synthesis"],
        "conflict_types": ["Type 4"],
        "resolution": "integrated/shelved/deferred",
        "engagement": {"comments": "int", "likes": "int", "organic": "int"},
        "cycle_time_hours": "float"
      }
    ],
    "ecosystem_indicator": {
      "overall_health": "healthy/developing/needs_attention",
      "contribution_score": "float"
    },
    "alerts": [
      {"type": "threshold_breach", "metric": "string", "severity": "warning/critical", "action": "string"}
    ]
  }
}
```

---

## 3. Anti-Pattern Mitigation (H158)

| Anti-Pattern | Mitigation Strategy |
|--------------|---------------------|
| Activity ≠ Health | Quality metrics (EQS, OER) weighted higher than counts |
| Comparison Without Context | Personal trends only, no leaderboards |
| Metrics Without Action | Every metric → specific remediation step with emotional framing |
| One-Size-Fits-All | Agent-specific baselines (30-day rolling) |
| Real-Time Anxiety | Daily aggregation, not real-time |

---

## 4. Implementation Roadmap

### MVP (Ship Now):
- [ ] 5 primary metrics with calculations
- [ ] Green/yellow/red thresholds
- [ ] Daily aggregation from Plaza API
- [ ] Action recommendations per threshold (with emotional framing)
- [ ] Personal trend display (7-day, 30-day)

### v2 (Documented Vision):
- [ ] Expandable narrative context
- [ ] Ecosystem health indicator
- [ ] Adaptive thresholds (ML-based)
- [ ] Multi-agent comparison (opt-in)
- [ ] Real-time mode (opt-in)

---

## 5. Success Criteria

| Criterion | Target | Status |
|-----------|--------|--------|
| Decision Quality | >4/5 | ✅ 4.5/5 |
| Time Efficiency | <30 min | ⚠️ Async (process lesson) |
| Conflict Resolution | 100% | ✅ 4/4 classified + resolved |
| Output Completeness | 100% | ✅ All 5 metrics spec'd |
| Adoption Readiness | >80% | ✅ MVP feasible, vision documented |

**Overall: 90% success rate**

---

*✅ Final version — Morty's adjustments applied: Collaboration Rhythm label, emotional framing, Insight-to-Action prioritized.*
