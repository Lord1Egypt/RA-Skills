# Council Protocol

Expert councils are deliberative bodies that collectively evaluate, score, and guide the autonomous pipeline. This document defines their formation, operation, and decision-making rules.

## Council Formation

### Size

- Minimum: 3 experts
- Recommended: 4-6 experts
- Maximum: 10 experts (beyond this, split into sub-councils)

### Role Assignment

Each council member receives one of four roles:

| Role | Responsibility | Selection Criteria |
|------|---------------|-------------------|
| **chair** | Presents artifact, synthesizes votes, makes final recommendations | Highest `source_confidence` + broadest `routing_keywords` |
| **reviewer** | Focuses on quality, completeness, and correctness | Most detailed `critique_style` profile field |
| **advocate** | Identifies strengths, prevents under-scoring | Most `canonical_works` entries |
| **skeptic** | Challenges high scores, finds flaws, prevents inflation | Most self-identified `blind_spots` (their self-awareness makes them good at finding issues) |

Role assignment algorithm:
1. Score each expert against all four role criteria
2. Assign each expert their highest-scoring role
3. If multiple experts tie for a role, prefer higher `source_confidence`
4. Every council must have at least one chair and one skeptic
5. If insufficient experts for all roles, one expert may hold multiple roles (chair + advocate, reviewer + skeptic)
6. Councils with more than 4 experts will have multiple members in the "reviewer" role — this is expected and ensures all voices participate in scoring

### Weight Balancing

No single expert should dominate voting:

```
expert_vote_weight = min(base_weight, 0.3)

Where:
- base_weight = source_confidence.weighted_score × role_multiplier
- role_multiplier: chair=1.5, reviewer=1.2, advocate=1.0, skeptic=1.0
- All weights are normalized so they sum to 1.0 across the council
```

## Council Debate Sequence

Each scoring cycle follows this debate protocol:

### Round 1: Chair Presentation

1. Chair receives the artifact and scoring rubric
2. Chair presents initial assessment of each axis
3. Chair identifies key areas of uncertainty

### Round 2: Independent Expert Review

Each expert reviews the artifact independently through their reasoning kernel lens:

1. Load the expert's `reasoning_kernel.core_questions` — what would this expert ask first?
2. Load `preferred_abstractions` — what concepts frame their evaluation?
3. Load `critique_style` — how do they pressure-test claims?
4. Load `advantage_knowledge_base.anti_patterns` — what would they immediately distrust?
5. Score each axis (0-25) with supporting evidence

### Round 3: Skeptic Challenge

The skeptic explicitly challenges any axis score above 20:
1. For each high score, the skeptic must provide:
   - At least one specific gap or weakness
   - A counter-evidence reference
   - An alternative lower score with justification
2. The challenged score enters a "disputed" state until resolved

### Round 4: Advocate Affirmation

The advocate explicitly supports any axis score below 15:
1. For each low score, the advocate must provide:
   - At least one specific strength being overlooked
   - Supporting evidence from the artifact
   - An alternative higher score with justification
2. The supported score enters a "boosted" state for aggregation

### Round 5: Chair Synthesis

1. Chair collects all votes, challenges, and affirmations
2. Resolves disputes: if skeptic challenge has merit, reduce the challenged expert's vote by up to 5 points for that axis
3. Resolves boosts: if advocate affirmation has merit, increase the boosted expert's vote by up to 3 points for that axis
4. Computes weighted median for each axis
5. Produces the final scoring report with recommendations

## Dynamic Member Addition

When the gap analyst identifies a coverage gap that requires a new expert:

### Fast-Track Protocol

1. Discover candidate via web search (single candidate, targeted)
2. Collect minimum viable sources (1 Tier A + 1 Tier B)
3. Run abbreviated audit (skip full source quality review)
4. Create skeleton profile with key fields pre-filled
5. Add to active council with role assignment
6. Flag profile as `fast-tracked` for later full review

### Integration Rules

- Fast-tracked experts start with a weight cap of 0.2 (vs normal 0.3)
- Their votes are labeled `fast-tracked` in the scoring report
- After 2 full scoring cycles, the fast-track flag is removed
- If a fast-tracked expert consistently votes against consensus (>10 point deviation from median), flag for manual review

### Council Expansion Limits

- Maximum 2 new experts per iteration
- Total council size must not exceed 10
- New experts must cover a gap identified by the gap analyst (no speculative additions)

## Consensus Rules

### Weighted Median

For each axis, the final score is the weighted median of all expert votes:
1. Sort votes by value (ascending)
2. Compute cumulative weight from lowest to highest
3. The vote where cumulative weight crosses 50% of total weight is the axis score

### Disagreement Handling

If any two experts' votes for the same axis differ by more than 10 points:
1. Flag the disagreement in the scoring report
2. The chair must document both positions
3. The wider range indicates uncertainty — the final score leans conservative (toward the lower value)
4. If the same axis has high disagreement across 3+ iterations, recommend adding a domain-specific expert

### Unanimous Convergence

For a total score of 100, all four axes must individually score 25. This means:
- Every expert must agree the artifact is exhaustive in breadth
- Every expert must agree the profiles are authoritative in depth
- Every expert must agree the implementation is production-ready in thickness
- Every expert must agree the solution fully solves the problem in effectiveness

This is intentionally hard. A score of 100 means the expert council cannot find meaningful improvements.

## Council Metadata

Each council is stored at `councils/<council_id>.json`:

```json
{
  "id": "domain-id-main",
  "name": "Main Council for Domain",
  "domain": "domain-id",
  "members": [
    {
      "expert_id": "expert-1",
      "role": "chair",
      "weight": 0.25,
      "joined_at": "2026-01-01T00:00:00Z",
      "fast_tracked": false
    }
  ],
  "routing_rules": [
    { "keyword": "testing", "expert_ids": ["expert-1", "expert-3"] },
    { "keyword": "architecture", "expert_ids": ["expert-2"] }
  ],
  "created_at": "2026-01-01T00:00:00Z",
  "updated_at": "2026-01-01T00:00:00Z",
  "scoring_history_refs": ["scoring_reports/domain-id_20260101.json"]
}
```
