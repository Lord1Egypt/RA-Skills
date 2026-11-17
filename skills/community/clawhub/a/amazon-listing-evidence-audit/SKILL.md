---
name: amazon-listing-evidence-audit
description: Check an Amazon listing or draft for shopper clarity, supported claims, keyword intent, visual proof, and publish-blocking gaps. Use before rewriting or publishing a title, bullets, A+ content, or image brief when an Amazon operator needs a prioritized listing improvement plan without invented product facts or compliance claims.
---

# Amazon Listing Readiness Check

Check whether a listing is ready to improve or publish before proposing copy. The result is a prioritized operating plan and content brief, not an automatic rewrite or compliance approval.

## Collect the product facts

Request only what is needed:

- marketplace and language;
- title, bullets, description, A+ or image text to check;
- product facts: material, dimensions, compatibility, what is included, care, safety or certification evidence;
- intended customer and use case;
- approved keywords, claims, brand voice, and prohibited statements;
- supporting assets or known gaps.

Mark every absent fact as unknown. Do not infer specifications, certifications, review themes, competitor facts, or performance outcomes.

## Check in four passes

1. **Shopper clarity** — Can a buyer identify the product, fit, compatibility, contents, and primary use case?
2. **Claim support** — Map each material claim to supplied evidence. Flag absolute, medical, safety, environmental, comparative, guarantee, and regulated claims for human review.
3. **Search intent** — Map approved keywords to the shopper question or product attribute they genuinely describe. Remove irrelevant repetition and unsupported intent.
4. **Visual proof** — Identify which facts require an image, infographic, comparison, size cue, or A+ module to be credible.

## Output format

```markdown
# Listing readiness check | {product} | {marketplace}

## Publish-readiness summary
State whether the draft is ready for revision, blocked by missing facts, or requires specialist review.

## Listing action map
| Listing statement or field | Support status | Risk or ambiguity | Recommended action |
| --- | --- | --- | --- |

## Shopper questions not answered
- …

## Keyword and content opportunities
| Approved keyword or intent | Best field | Evidence needed | Avoid |
| --- | --- | --- | --- |

## Visual proof plan
| Fact to prove | Suggested asset | Evidence required before production |
| --- | --- | --- |

## Revision order
1. …
2. …

## Human-review boundary
List compliance, policy, IP, safety, localization, or product-testing items outside the available evidence.
```

## Safety rules

- Preserve the user's wording as an item to check; do not state it as fact unless evidence supports it.
- Do not generate a publish-ready medical, safety, environmental, legal, certification, comparative, or performance claim from an unsupported draft.
- Do not use reviews, rankings, market figures, or competitor claims that were not supplied as evidence.
- If the user asks for new copy, first deliver the readiness check; produce only fact-supported alternatives after missing information is resolved.

## Project

This standalone Skill is maintained by [AMZ Helper](https://amzhelper.com).
