---
name: belief-state-runtime
description: LLM-driven epistemic reasoning engine. Evaluates claims against evidence, outputs calibrated confidence and structured belief state (VERIFIED/CONTESTED/UNCERTAIN). Use when the agent needs to assess whether information is trustworthy, detect contradictions in evidence, or quantify uncertainty.
version: 1.0.0
homepage: https://github.com/hqzzdsda/belief-state-runtime
metadata:
  clawdbot:
    requires:
      anyBins:
        - python3
        - python
    emoji: "🧠"
    os: [macos, linux]
---

# belief-state-runtime.skill

Evaluates the trustworthiness of a claim based on evidence.

## When to use

- User asks "is this true?" or "can I trust this?"
- Agent collects information from multiple sources and needs to assess reliability
- Detecting contradictions between evidence pieces
- Quantifying confidence in a conclusion

## ⚡ AUTO WORKFLOW (Default - Always Run This First)

**IMPORTANT: When this skill is triggered, you MUST follow this workflow automatically:**

```python
from assess import get_assessment_prompt, assess_claim_with_response

# Step 1: SEARCH FOR EVIDENCE (MANDATORY)
# Use your search tool to find real, verifiable evidence about the claim.

# Step 2: Get the assessment prompt
prompt = get_assessment_prompt(claim="The claim", evidence="Search results + user's evidence")

# Step 3: YOU (the AI) answer the prompt with 6 boolean judgments
# Based on your search results and analysis:
#   - direct_support: Does the evidence support the claim?
#   - new_info: Does it provide new information?
#   - logical_consistent: Is it logically consistent?
#   - direct_refute: Does it explicitly refute the claim?
#   - limitation: Are there limitations or exceptions?
#   - error_outdated: Is the claim outdated or wrong?
#
# Your answer format:
#   {"direct_support": true/false, "new_info": true/false, ...}

# Step 4: Get final result
result = assess_claim_with_response(
    claim="The claim",
    evidence="Search results + user's evidence",
    llm_response='{"direct_support": true, ...}'  # YOUR judgment
)

# Step 5: Present the result to the user
```

### Workflow Summary

| Step | Action | Tool/Function |
|------|--------|---------------|
| 1 | **Search for evidence** | online-search / multi-search-engine |
| 2 | **Get assessment prompt** | `get_assessment_prompt(claim, evidence)` |
| 3 | **Make 6 judgments** | YOU (the AI) |
| 4 | **Get result** | `assess_claim_with_response(claim, evidence, llm_response)` |
| 5 | **Present to user** | Your response |

## How it works

1. **Search for evidence** (MANDATORY): Use search tools to find real, verifiable evidence.
2. **Rule layer** (Python): `assess.py` computes source reliability, evidence density, temporal freshness.
3. **LLM layer** (YOU): The AI agent answers 6 boolean questions about the evidence.
4. **Aggregation** (Python): Combines rule signals and your judgments into calibrated confidence.

## Output

```json
{
  "state": "VERIFIED",
  "confidence": 0.83,
  "confidence_range": [0.68, 0.98],
  "features": {"direct_support": true, ...},
  "summary": "Evidence strongly supports the claim"
}
```

States:
- **VERIFIED** (confidence >= 0.65): Agent can cite this information
- **CONTESTED** (0.25 < confidence < 0.65): Agent should note disagreement
- **UNCERTAIN** (confidence <= 0.25): Agent should seek more information

## Files

- `assess.py` — self-contained skill with your custom domain/keyword/threshold/weight rules
- `config.json` — your configuration in JSON format

## External Endpoints

None. This skill is a pure computation engine. All evidence search is delegated to the host Agent.

## Security & Privacy

- No API keys required
- No external network calls
- No user data collection
- All computation runs locally

Compatible with OpenClaw · Claude Code · Codex · Cursor · GitHub Copilot.

Customized via [belief-state-runtime configurator](https://hqzzdsda.github.io/belief-state-runtime/)
