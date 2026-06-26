# Maturity Scoring Rubric

Every scoring cycle evaluates the artifact across four axes. Each axis is scored 0-25 by the expert council. The total maturity score is the sum of all axes (0-100). Convergence requires a total of 100.

## Axes

### Breadth (0-25): Does the knowledge base cover the full scope of the domain?

| Score | Meaning |
|-------|---------|
| 0-6 | Only one narrow sub-domain covered; major areas missing |
| 7-12 | Core sub-domains present but significant gaps in peripheral areas |
| 13-18 | Good coverage of most sub-domains; minor gaps in edge cases |
| 19-22 | Comprehensive coverage; nearly all sub-domains addressed |
| 23-25 | Exhaustive coverage including emerging and niche areas |

Evidence sources:
- Number of distinct `routing_keywords` across all expert profiles
- `coverage_axes` matrix completeness in the domain definition
- Number of active experts vs domain breadth
- Council consensus on sub-domain coverage

### Depth (0-25): Does each expert profile contain rich, actionable knowledge?

| Score | Meaning |
|-------|---------|
| 0-6 | Profiles are skeletons; `reasoning_kernel` empty, no `canonical_works` |
| 7-12 | Basic profiles filled; some `reasoning_kernel` fields populated |
| 13-18 | Rich profiles with full reasoning kernels, question playbooks, quote banks |
| 19-22 | Deep profiles with verified source alignment, detailed critique styles |
| 23-25 | Authoritative profiles that could serve as standalone reference works |

Evidence sources:
- Profile field completeness (all 20+ REQUIRED_PROFILE_FIELDS populated)
- `source_confidence` levels across the council
- `reasoning_kernel` depth (core_questions, decision_rules, failure_taxonomy, preferred_abstractions)
- Quote bank size and source attribution quality

### Thickness (0-25): Is the knowledge practically implementable?

| Score | Meaning |
|-------|---------|
| 0-6 | Theoretical only; no actionable implementation guidance |
| 7-12 | Some practical advice but lacks specifics (no code, no commands, no tools) |
| 13-18 | Includes concrete implementation patterns, tool recommendations, code examples |
| 19-22 | Full implementation guides with tested code, configuration, deployment steps |
| 23-25 | Production-ready implementation with error handling, edge cases, monitoring |

Evidence sources:
- Presence of executable code and configuration files
- Build success rate across iterations
- Test coverage percentage
- Deployment artifact completeness
- Error handling and edge case coverage

### Effectiveness (0-25): Does the built project solve the original problem?

| Score | Meaning |
|-------|---------|
| 0-6 | Does not address the stated problem |
| 7-12 | Partially addresses the problem; major use cases broken or missing |
| 13-18 | Addresses core use cases; some edge cases or quality issues remain |
| 19-22 | Fully functional solution with good reliability |
| 23-25 | Polished, production-quality solution that exceeds expectations |

Evidence sources:
- Functional test pass rate
- User-flow verification results
- Performance benchmark alignment with domain expectations
- Council consensus on problem-solution fit

## Expert Voting Protocol

Each expert in the council votes on each axis independently.

### Weight Calculation

```
expert_weight = base_weight × source_confidence × role_multiplier

Where:
- base_weight: 1.0 (default), adjusted for council balance (max 0.3 per expert)
- source_confidence: from profile's source_confidence.weighted_score (0.0-1.0)
- role_multiplier: chair=1.5, reviewer=1.2, advocate=1.0, skeptic=1.0
```

### Vote Aggregation

The final axis score is the **weighted median** of all expert votes, clamped to 0-25.

Steps:
1. Collect all expert votes for the axis
2. Sort votes by value
3. Compute cumulative weight from lowest to highest
4. Find the vote where cumulative weight crosses 50% of total weight
5. That vote value is the axis score

### Anti-Inflation Mechanism

The skeptic role is specifically tasked with challenging the highest-scoring axes. Before final aggregation:
- The skeptic reviews each axis score that exceeds 20
- If the skeptic provides evidence that the score should be lower, their challenge vote is added with 1.5x weight for that axis only
- This prevents rubber-stamp high scores

### Anti-Deflation Mechanism

The advocate role is tasked with highlighting what is working well. Before final aggregation:
- The advocate reviews each axis score that is below 15
- If the advocate provides evidence that the score should be higher, their boost vote is added with 1.2x weight for that axis only
- This prevents overly harsh first-round scores from stalling the loop

### Tie-Breaking

If the weighted median falls between two integer values, round down. The pipeline must earn every point.

## Scoring Report Format

Each scoring cycle produces a report at `scoring_reports/<domain_id>_<timestamp>.json`:

```json
{
  "domain": "domain-id",
  "artifact_path": "path/to/artifact",
  "iteration": 1,
  "council_id": "council-id",
  "axes": [
    {
      "axis": "breadth",
      "score": 20,
      "evidence": ["5 experts covering 8 sub-domains", "..."],
      "gaps": ["Missing coverage of X sub-domain"],
      "expert_votes": {
        "expert-1": 22,
        "expert-2": 18,
        "expert-3": 20
      }
    }
  ],
  "total": 75,
  "verdict": "needs_work",
  "generated_at": "2026-01-01T00:00:00Z",
  "recommendations": ["Add expert for X sub-domain", "Deepen Y expert profile"]
}
```

Verdict values:
- `converged`: total = 100, all verification passes
- `needs_work`: total < 100, specific gaps identified
- `blocked`: fundamental issue preventing progress (requires human intervention)
