---
name: belief-assessor
description: LLM-driven epistemic reasoning engine. Evaluates claims against evidence, outputs calibrated confidence and structured belief state (VERIFIED/CONTESTED/UNCERTAIN). v2 adds 4-way constraint system, parameterized configuration, and formula-based confidence intervals. Use when the agent needs to assess whether information is trustworthy, detect contradictions in evidence, or quantify uncertainty.
---

# belief-assessor v2

Evaluates the trustworthiness of a claim based on evidence. **v2** adds a projection layer with 4 constraints + formula-based confidence intervals + parameterized policy presets.

## v2 vs v1

| Feature | v1 | v2 |
|---------|-----|-----|
| Thresholds | Hardcoded 0.65/0.25 | Configurable via `ProjectionConfig` |
| Constraints | None | 4-way: contradiction, provenance, temporal, density |
| Confidence interval | ±0.15 fixed | Formula: (1-Q)×base + min/√n_eff |
| Strategies | 1 | 3 presets: standard, conservative, permissive |
| Output reasons | None | `veto_reasons` explains WHY |
| LLM calls | 1 | 1 (unchanged) |
| Dependencies | 0 | 0 (unchanged) |

## When to use

- User asks "is this true?" or "can I trust this?"
- Agent collects information from multiple sources and needs to assess reliability
- Detecting contradictions between evidence pieces
- Quantifying confidence in a conclusion
- High-stakes decisions needing conservative assessment

## ⚡ AUTO WORKFLOW (Default - Always Run This First)

**IMPORTANT: When this skill is triggered, you MUST follow this workflow automatically:**

```python
from assess import get_assessment_prompt, assess_claim_with_response, ProjectionConfig

# Step 1: SEARCH FOR EVIDENCE (MANDATORY)
# Use your search tool (online-search, multi-search-engine, etc.) to find
# real, verifiable evidence about the claim. Search for:
#   - Official data and statistics
#   - Academic research and studies
#   - Credible news reports
#   - Expert opinions

# Step 2: Get the assessment prompt and choose strategy
prompt = get_assessment_prompt(claim="The claim", evidence="Search results + user's evidence")

# If high-stakes (financial, medical, legal), use conservative:
# config = ProjectionConfig.conservative()

# Step 3: YOU (the AI) answer the prompt with 6 boolean judgments
# Based on your search results and analysis:
#   - direct_support: Does the evidence directly support the claim?
#   - new_info: Does it provide new information?
#   - logical_consistent: Is it logically consistent?
#   - direct_refute: Does it explicitly refute the claim?
#   - limitation: Are there limitations or exceptions?
#   - error_outdated: Is the claim outdated or wrong?
#
# Your answer format:
#   {"direct_support": true/false, "new_info": true/false, "logical_consistent": true/false, "direct_refute": true/false, "limitation": true/false, "error_outdated": true/false}

# Step 4: Get final result
result = assess_claim_with_response(
    claim="The claim",
    evidence="Search results + user's evidence",
    llm_response='{"direct_support": true, ...}',  # YOUR judgment
    # config=ProjectionConfig.conservative()  # uncomment for high-stakes
)

# Step 5: Present the result to the user
# Include: state, confidence, veto_reasons (if any), and your interpretation
# If veto_reasons is non-empty, explain WHY the confidence was capped
```

### Workflow Summary (Quick Reference)

| Step | Action | Tool/Function |
|------|--------|---------------|
| 1 | **Search for evidence** | online-search / multi-search-engine |
| 2 | **Choose strategy + get prompt** | `ProjectionConfig.conservative()` / `get_assessment_prompt()` |
| 3 | **Make 6 judgments** | YOU (the AI) |
| 4 | **Get result** | `assess_claim_with_response(claim, evidence, llm_response, config?)` |
| 5 | **Interpret & present** | Check `veto_reasons`, explain if confidence was capped |

## How it works

1. **Search for evidence** (MANDATORY): Use search tools to find real, verifiable evidence about the claim.

2. **Rule layer** (Python): Extracts 4 continuous signals:
   - `source_reliability` — URL domain scoring + keyword detection
   - `evidence_density` — segment count and richness
   - `temporal_freshness` — 1/(1+age) from year extraction
   - `provenance_quality` — TLD diversity across sources

3. **LLM layer** (YOU): The AI agent answers 6 boolean questions about the evidence.

4. **Projection layer** (Python — v2):
   - Applies 4 constraints (contradiction, provenance, temporal, density)
   - Caps confidence when constraints trigger
   - Computes formula-based confidence interval
   - Determines state with configurable thresholds

5. **Aggregation** (Python): Returns calibrated confidence + state + reasons.

## Output

```json
{
  "state": "VERIFIED",
  "confidence": 0.83,
  "confidence_range": [0.68, 0.95],
  "features": {"direct_support": true, "new_info": true, ...},
  "veto_reasons": [],          // v2: empty = no constraints triggered
  "cap_applied": 1.0,          // v2: 1.0 = no cap
  "summary": "Evidence strongly supports the claim"
}
```

States:
- **VERIFIED**: Agent can cite this information with confidence
- **CONTESTED**: Agent should note "there is disagreement" or constraints
- **UNCERTAIN**: Agent should say "need more information"

### v2: Interpreting veto_reasons

When `veto_reasons` is non-empty, the confidence was deliberately capped:

| Reason | Meaning |
|--------|---------|
| `contradiction_capped` | Evidence contradicts — confidence capped |
| `contradiction_dominates` | Refutation dominates support — forced CONTESTED |
| `provenance_gated` | Source quality too low — cannot be VERIFIED |
| `temporal_decayed` | Evidence is stale — confidence capped (historical claims exempt) |
| `density_floor` | Evidence too sparse — cannot be VERIFIED |

## Strategy Presets

```python
# Standard (default) — general-purpose
config = ProjectionConfig.standard()
config = None  # equivalent

# Conservative — high-stakes (finance, medical, legal)
config = ProjectionConfig.conservative()

# Permissive — low-stakes, brainstorming
config = ProjectionConfig.permissive()

# Custom
config = ProjectionConfig(
    verify_threshold=0.80,
    contradiction_cap=0.45,
    min_provenance_quality=0.60,
)
```

## Incremental updates

When evidence arrives in stages, the engine updates beliefs incrementally:

```python
results = assess_incremental(
    claim="The claim",
    evidence_stages=["Stage 1 evidence", "Stage 2 evidence", "Stage 3 evidence"],
    llm_func=my_llm,
    config=ProjectionConfig.conservative(),  # optional
)
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| claim | string | Yes | The claim to evaluate |
| evidence | string | No | Evidence text |
| llm_response | string | Yes* | AI agent's JSON with 6 boolean judgments |
| previous_confidence | float | No | Previous confidence for incremental update |
| config | ProjectionConfig | No | Strategy preset or custom configuration |

*Required for `assess_claim_with_response`. For `assess_claim()`, use `llm_func` instead.

## Legacy API (v1 compatible)

For backward compatibility, `assess_claim()` with `llm_func` callback still works and now automatically uses v2 projection with standard config:

```python
from assess import assess_claim, ProjectionConfig
result = assess_claim(claim="...", evidence="...", llm_func=my_llm)
# v1 result format still returned, plus new v2 fields (veto_reasons, cap_applied)
```

## API Reference

### assess_claim(claim, evidence?, previous_confidence?, llm_func, config?) → dict

Full assessment with LLM call. Uses `llm_func` callback.

### assess_incremental(claim, evidence_stages, llm_func, config?) → list[dict]

Process evidence stage by stage, tracking confidence evolution.

### get_assessment_prompt(claim, evidence?) → str

Returns the prompt text for the AI agent to answer.

### assess_claim_with_response(claim, evidence?, llm_response, previous_confidence?, config?) → dict

Uses AI agent's 6-boolean response. No LLM call inside.

### ProjectionConfig

Dataclass with 3 presets and full customizability. See `scripts/assess.py` for all parameters.

### get_skill_definition() → dict

Returns structured skill definition for agent framework registration.
