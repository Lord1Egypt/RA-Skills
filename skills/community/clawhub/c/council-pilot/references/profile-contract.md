# Expert Profile Contract

Every promoted expert profile should follow this contract. Keep it compact enough for routing, but rich enough to act as a durable reasoning lens.

```json
{
  "id": "expert-id",
  "name": "Expert Name",
  "domains": ["domain-id"],
  "roles": ["methodology_reviewer", "systems_builder", "venue_strategist"],
  "routing_keywords": ["keyword", "subfield"],
  "bio_arc": "Public career arc relevant to this forum.",
  "canonical_works": [
    {
      "title": "Work title",
      "year": "2024",
      "why_it_matters": "What this work contributes to the expert lens."
    }
  ],
  "signature_ideas": ["Idea distilled from public sources."],
  "reasoning_kernel": {
    "core_questions": ["What would this expert ask first?"],
    "decision_rules": ["How they choose between competing explanations."],
    "failure_taxonomy": ["Common failure mode they detect quickly."],
    "preferred_abstractions": ["Concepts or models they repeatedly use."]
  },
  "preferred_evidence": ["Evidence type they trust."],
  "critique_style": ["How they pressure-test claims."],
  "blind_spots": ["Where this lens can overreach."],
  "advantage_knowledge_base": {
    "canonical_concepts": ["Reusable concept"],
    "favorite_benchmarks": ["Benchmark or standard"],
    "known_debates": ["Debate they sharpen"],
    "anti_patterns": ["Claim pattern they would distrust"]
  },
  "question_playbook": [
    {
      "situation": "When to ask this question.",
      "question": "Specific probe.",
      "expected_evidence": ["What would answer it."]
    }
  ],
  "domain_relevance": {
    "summary": "Why this expert matters for this forum.",
    "best_used_for": ["Task type"],
    "avoid_using_for": ["Task type"]
  },
  "quote_bank": [
    {
      "quote": "Short verified quote or clearly marked paraphrase.",
      "source_ref": "source id",
      "quote_type": "verbatim_or_paraphrase"
    }
  ],
  "source_refs": ["source-id"],
  "source_confidence": {
    "level": "high|medium|low",
    "weighted_score": 0.0,
    "rationale": "Why this confidence level is justified."
  },
  "freshness": {
    "status": "fresh|mixed|stale",
    "last_checked": "YYYY-MM-DD",
    "notes": "What may need refresh."
  },
  "usage_boundaries": [
    "Expert memory is an analysis lens, not primary evidence."
  ]
}
```

## Distillate Markdown

Write `distillate.md` as a human-readable version with these sections:

- Public evidence base
- Career and idea arc
- Signature reasoning kernel
- What this expert will catch
- What this expert may miss
- Best routing situations
- Source notes and freshness

