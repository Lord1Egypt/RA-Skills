# Data Contracts — JSON Schemas

Single source of truth for all agent outputs. All agents and capabilities reference these schemas.

---

## EvidenceItem

An individual piece of evidence from a source.

```json
{
  "evidence_id": "evi_<hash_first8>",
  "source_type": "web | twitter | academic | government | other",
  "url": "https://...",
  "publisher": "Publisher Name",
  "published_at": "2026-03-09T12:00:00Z",
  "retrieved_at": "2026-03-09T12:30:00Z",
  "snippet": "Relevant excerpt from source...",
  "hash": "<SHA-256 of snippet>",
  "credibility_tier": "tier1_authoritative | tier2_reputable | tier3_general | tier4_social",
  "freshness_status": "current | stale | timeless",
  "evidence_track": "fact | reasoning",
  "social_credibility_flag": "likely_reliable | needs_verification | likely_unreliable | null",
  "verification_priority": "high | medium | low",
  "corroboration_status": "corroborated | uncorroborated | contradicted | null",
  "discovered_by": "orchestrator | pro | con",
  "discovered_at_round": 0,
  "search_context": "initial_broad | judge_feedback_round_N | pro_supplement | con_supplement"
}
```

### Credibility Tiers
- `tier1_authoritative`: Government agencies, central banks, major wire services (AP, Reuters)
- `tier2_reputable`: Major newspapers, established research institutions, peer-reviewed journals
- `tier3_general`: Blogs, smaller publications, industry reports, company press releases
- `tier4_social`: Twitter/X, Reddit, forums, personal posts

### Freshness Status
- `current`: Source is recent enough to support current-state claims
- `stale`: Source was used for a current-state claim but is now outdated
- `timeless`: Historical/mechanism/trend evidence; NEVER auto-downgraded

### Social Credibility Flag
- Only set for `source_type = "twitter"`. LLM pre-screens for fake news patterns. Non-Twitter -> `null`.
- `verification_priority`: Derived from flag. `likely_unreliable` -> `high`, `needs_verification` -> `medium`, otherwise `low`.
- `corroboration_status`: Set during EvidenceVerify. Tracks whether independent non-social sources confirm. Non-Twitter -> `null`.

### v2 Fields
- `discovered_by`: Who found this evidence
- `discovered_at_round`: 0 = initial ingest, N = found during round N
- `search_context`: What drove this search

---

## ClaimItem

A factual or inferential claim made by a debater.

```json
{
  "claim_id": "clm_<round>_<side>_<seq>",
  "round": 1,
  "speaker": "pro | con",
  "claim_type": "fact | inference | analogy",
  "claim_text": "The claim statement...",
  "evidence_ids": ["evi_abc12345", "evi_def67890"],
  "status": "verified | contested | unverified | stale",
  "last_verified_at": "2026-03-09T12:00:00Z",
  "judge_note": "Judge's assessment...",
  "mandatory_response": false,
  "conflict_details": [
    {
      "source_a": {"evidence_id": "evi_xxx", "position": "Source A claims..."},
      "source_b": {"evidence_id": "evi_yyy", "position": "Source B claims..."},
      "divergence_point": "The specific point of disagreement...",
      "judge_assessment": "Judge's evaluation of the conflict..."
    }
  ]
}
```

### Claim Status State Machine

```
                  +----------+
                  |unverified|
                  +----+-----+
                       |
            +----------+----------+
            v          v          v
       +--------+ +---------+ +-----+
       |verified| |contested| |stale|
       +---+----+ +----+----+ +--+--+
           |           |         |
           +---->contested<------+
           |           |         |
           +---->stale  |        |
           |           +---->verified
           |           +---->stale
           +-----------+
```

Transitions (8 total):
- `unverified -> verified`: Cross-source confirmed
- `unverified -> contested`: Sources conflict
- `unverified -> stale`: Current-state source expired
- `verified -> contested`: New contradicting evidence
- `verified -> stale`: Fact-track source expired
- `contested -> verified`: Resolution with new evidence
- `contested -> stale`: All sources expired
- `stale -> verified`: Fresh confirming source found

**Critical rule**: Reasoning-track claims are NEVER auto-transitioned to `stale`.

---

## DebateTurn (Pro/Con Turn Output)

```json
{
  "round": 1,
  "side": "pro | con",
  "arguments": [
    {
      "claim_text": "Main argument statement...",
      "claim_type": "fact | inference | analogy",
      "evidence_ids": ["evi_abc12345"],
      "reasoning_chain": {
        "observed_facts": "What data/events support this...",
        "mechanism": "Why does this cause that...",
        "scenario_implication": "What follows from this...",
        "trigger_conditions": "What would make this scenario happen...",
        "falsification_conditions": "What would prove this wrong..."
      }
    }
  ],
  "rebuttals": [
    {
      "target_claim_id": "clm_1_con_1",
      "rebuttal_text": "Counter-argument...",
      "evidence_ids": ["evi_def67890"]
    }
  ],
  "mandatory_responses": [
    {
      "point_id": "mrp_1_1",
      "response_text": "Addressing judge's point..."
    }
  ],
  "new_evidence": [],
  "historical_wisdom": {
    "weight": "advisory",
    "references": [
      {
        "historical_event": "Name/description of historical event",
        "era_context": "Historical context and background",
        "parallel_to_current": "How this parallels the current debate topic",
        "key_differences": "Critical structural differences from current situation",
        "lesson_extracted": "The insight or lesson drawn",
        "applicability_caveat": "Limitations of this historical reference"
      }
    ]
  },
  "speculative_scenarios": {
    "weight": "exploratory",
    "scenarios": [
      {
        "scenario_name": "Short descriptive name",
        "premise": "The 'what if' starting condition",
        "chain_of_events": "A -> B -> C sequence of consequences",
        "probability_estimate": "low (<10%) | medium (10-40%) | high (>40%)",
        "impact_if_realized": "Severity and scope of impact",
        "early_warning_signals": ["Observable precursors to watch for"],
        "what_would_falsify": "What would invalidate this scenario"
      }
    ]
  }
}
```

---

## JudgeRuling

```json
{
  "round": 1,
  "verification_results": [
    {
      "claim_id": "clm_1_pro_1",
      "original_status": "unverified",
      "new_status": "verified",
      "reasoning": "Cross-source confirmed by Reuters and Bloomberg..."
    }
  ],
  "causal_validity_flags": [
    {
      "claim_id": "clm_1_con_2",
      "issue": "correlation presented as causation",
      "severity": "critical | moderate | minor"
    }
  ],
  "mandatory_response_points": [
    {
      "point_id": "mrp_1_1",
      "target": "pro | con | both",
      "point": "What must be addressed...",
      "reason": "Why this needs response..."
    }
  ],
  "historical_wisdom_assessment": [
    {
      "side": "pro | con",
      "historical_event": "...",
      "relevance_grade": "strong_parallel | moderate_parallel | weak_parallel",
      "honesty_grade": "honest | partially_honest | misleading",
      "note": "..."
    }
  ],
  "round_summary": "Neutral summary of key developments..."
}
```

---

## FinalReport

```json
{
  "topic": "The debate topic",
  "total_rounds": 3,
  "generated_at": "2026-03-09T18:00:00Z",
  "verdict_summary": "One-sentence overall judgment",
  "report_path": "reports/debate_report.md",
  "verified_facts": ["Cross-source confirmed factual statements..."],
  "probable_conclusions": ["High-confidence conclusions with qualifiers..."],
  "contested_points": [
    {
      "point": "The contested claim or issue",
      "claim_ids": ["clm_1_pro_2", "clm_2_con_1"],
      "pro_position": "Pro's strongest argument with evidence summary",
      "con_position": "Con's strongest argument with evidence summary",
      "key_rebuttals": [
        {
          "from": "pro | con",
          "target": "What they're rebutting",
          "argument": "The rebuttal content",
          "evidence_ids": ["evi_xxx"]
        }
      ],
      "judge_assessment": "Judge's evaluation of which side has stronger support",
      "resolution_status": "unresolved | leaning_pro | leaning_con | partially_resolved"
    }
  ],
  "to_verify": ["Claims needing further verification with suggested methods..."],
  "scenario_outlook": {
    "base_case": "Most likely scenario based on verified facts...",
    "upside_triggers": ["Conditions that would improve outlook..."],
    "downside_triggers": ["Conditions that would worsen outlook..."],
    "falsification_conditions": ["What would invalidate base case..."]
  },
  "watchlist_24h": [
    {
      "item": "What to monitor...",
      "reversal_trigger": "What would change conclusions...",
      "monitoring_source": "Where to watch..."
    }
  ],
  "evidence_diversity_assessment": {
    "source_type_distribution": {"web": 15, "academic": 3, "twitter": 8},
    "credibility_tier_distribution": {"tier1": 2, "tier2": 8, "tier3": 10, "tier4": 8},
    "geographic_diversity": "assessment text...",
    "perspective_balance": "assessment text...",
    "diversity_warning": "warning text or null"
  },
  "speculative_frontier": [
    {
      "scenario_name": "...",
      "proposed_by": "pro | con",
      "premise": "...",
      "chain_of_events": "...",
      "probability": "...",
      "impact": "...",
      "early_warnings": ["..."],
      "judge_quality_note": "..."
    }
  ],
  "historical_insights": {
    "key_parallels": ["Most relevant historical parallels..."],
    "conflicting_lessons": ["Where historical evidence points both ways..."],
    "meta_pattern": "Overarching historical pattern, if any..."
  },
  "executive_summary": {
    "summary_paragraph": "One-paragraph executive summary...",
    "top_verified_facts": ["..."],
    "top_contested_points": ["..."],
    "base_case_outlook": "...",
    "top_watchlist_items": ["..."]
  },
  "decision_matrix": {
    "dimensions": [
      {
        "factor": "Factor name",
        "pro_position": "Pro's strongest point on this factor",
        "con_position": "Con's strongest point on this factor",
        "evidence_strength": "strong | moderate | weak",
        "judge_note": "..."
      }
    ],
    "overall_lean": "Slightly favors pro/con because...",
    "key_uncertainty": "The factor most likely to change the conclusion...",
    "recommendation": "Based on current evidence..."
  },
  "conclusion_profiles": [
    {
      "conclusion_id": "concl_1",
      "conclusion_text": "Conclusion description",
      "source_claims": ["clm_1_pro_1", "clm_2_con_3"],
      "profile": {
        "probability": {
          "value": "high (>70%) | medium (30-70%) | low (<30%)",
          "rationale": "Basis for probability judgment"
        },
        "confidence": {
          "value": "high | medium | low",
          "rationale": "How evidence quality affects certainty"
        },
        "consensus": {
          "value": "high | partial | low",
          "rationale": "Degree of disagreement between sides"
        },
        "evidence_coverage": {
          "value": "complete | partial | sparse",
          "gaps": "Key missing links in the evidence chain"
        },
        "reversibility": {
          "value": "high | medium | low",
          "reversal_trigger": "What could overturn this conclusion"
        },
        "validity_window": {
          "value": "hours | days | weeks | months | indefinite",
          "expiry_condition": "What would invalidate this conclusion"
        },
        "impact_magnitude": {
          "value": "extreme | high | medium | low",
          "scope": "Scope and depth of impact"
        },
        "causal_clarity": {
          "value": "clear_chain | partial_chain | correlation_only",
          "weakest_link": "Weakest link in the causal chain"
        },
        "actionability": {
          "value": "directly_actionable | informational | requires_more_data",
          "suggested_action": "Suggested action if actionable"
        },
        "falsifiability": {
          "value": "easily_testable | testable_with_effort | hard_to_test",
          "test_method": "How to verify this conclusion"
        }
      }
    }
  ]
}
```

---

## DebateConfig

```json
{
  "topic": "The debate topic",
  "round_count": 3,
  "pro_model": "balanced",
  "con_model": "balanced",
  "judge_model": "deep",
  "created_at": "2026-03-09T12:00:00Z",
  "domain": "geopolitics | tech | health | finance | philosophy | culture | general",
  "depth": "quick | standard | deep",
  "evidence_scope": "web_only | academic_included | user_provided | mixed",
  "output_format": "full_report | executive_summary | decision_matrix",
  "speculation_level": "conservative | moderate | exploratory",
  "language": "en | zh | bilingual",
  "focus_areas": ["user-defined dimensions to focus on"],
  "mode": "balanced | red_team",
  "evidence_refresh": "upfront_only | per_round | hybrid",
  "status": "initialized | in_progress | complete"
}
```

---

## Audit Trail Entry (JSONL)

Each line in `logs/audit_trail.jsonl`:

```json
{"timestamp": "2026-03-09T12:00:00Z", "action": "workspace_initialized | round_started | pro_turn_complete | con_turn_complete | judge_ruling_complete | claim_status_changed | evidence_added | report_generated | refresh_triggered | per_round_evidence_ingest | evidence_merged_from_turn", "details": {}}
```
