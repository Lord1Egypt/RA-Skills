---
name: visibility-content-check
description: >
  Use when the user wants to quality-check a draft before publishing it to improve AI visibility. Covers citation friendliness, Q&A structure, factual density, entity clarity, authority signals, and release readiness for developer-tool or open-source content.
---

# visibility-content-check

Use this skill to decide whether a draft is ready to influence LLM answers.

## Trigger

Use this skill before publishing a tutorial, comparison article, FAQ page, changelog summary, or product page update.

## Outputs

| Output | Description |
|---|---|
| Visibility readiness verdict | go, revise, or block |
| Issue list | missing signals, weak structure, entity ambiguity, thin evidence |
| Revision priorities | top fixes before publish |

## Next Best Skill

If the draft is blocked because of negative framing or wrong facts, use `visibility-repair`.
