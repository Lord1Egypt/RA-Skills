---
name: evidence-first
description: >
  Part of the Overpowered skill suite.
  Require evidence proportional to material claims and clearly separate evidence, inference, and uncertainty. Use for research, analysis, recommendations, reports, audits, or decisions where unsupported confidence would be harmful; do not use for purely creative or stylistic tasks.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "0-primitive"
  version: "0.1.0"
---

# Overpowered / Evidence First

## Core rule

**Do not turn a plausible statement into a factual claim without evidence appropriate to its importance.**

## Procedure

1. Identify the claims that could change a decision, commitment, risk assessment, or conclusion.
2. For each material claim, classify its support as:
   - **direct evidence** — the source directly establishes it;
   - **derived** — computed or logically inferred from evidence;
   - **assumption** — intentionally accepted without proof;
   - **unknown** — evidence is missing or insufficient.
3. Prefer authoritative and primary sources when the task provides or exposes them.
4. Preserve provenance closely enough that another agent can inspect the support.
5. Calibrate language to evidence strength. Never hide uncertainty behind confident prose.

## Output contract

For material conclusions, make the chain visible:

```text
Claim
Evidence
Inference, if any
Confidence / limitation
```

Use compact inline provenance when a full evidence table would be excessive.

## Gotchas

- More sources do not compensate for the wrong source authority.
- A precedent proves that something happened before; it does not prove that it is currently permitted.
- An agent-generated summary is not the authoritative source when the underlying artifact is available.
- Do not manufacture citations, file locations, query results, or verification evidence.

## Stop condition

Stop gathering evidence when every material claim has support adequate for the decision or is explicitly marked uncertain.
