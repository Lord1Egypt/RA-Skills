---
name: "factual-claim-verifier"
description: "Check factual claims in drafts before publication, delivery, or decisions."
license: "MIT-0"
---

# Factual Claim Verifier

Use this skill when reviewing text, posts, captions, emails, scripts, articles, reports, summaries, technical documents, product copy, launch copy, educational content, or AI-generated answers that contain factual claims and may be published, sent, used for decisions, or shown to others.

Trigger examples:

- "Verify this text"
- "Fact-check this"
- "Check whether this is true"
- "Review this for factual errors"
- "Check this before I publish it"
- "Tell me if this is exaggerated"

Do not require exact trigger words. If a draft contains factual assertions that matter, use this skill.

## Purpose

Separate style from truth. Identify factual claims, verify them against reliable sources when needed, flag uncertainty or exaggeration, and propose safer wording before content leaves the workspace.

## Mandatory Workflow

1. Read the full text before judging it.
2. Extract factual claims that can be checked, including:
   - Numbers, dates, prices, percentages, rankings, timelines.
   - Names, titles, organizations, places, events.
   - Product capabilities, availability, integrations, model names, or platform rules.
   - Legal, medical, financial, investment, safety, copyright, or compliance claims.
   - Technical claims, benchmarks, comparisons, and cause-effect statements.
3. Separate facts from opinions. Opinions do not need verification unless they are presented as objective facts.
4. Verify important or risky claims using, in priority order:
   - User-provided source material.
   - The original document, transcript, thread, or linked material.
   - Primary sources: official docs, policy pages, papers, laws, product pages, filings, or direct source material.
   - Web search for current or changing facts.
   - Careful reasoning only when no source access exists, clearly labeled as such.
5. Classify each important claim.
6. Flag errors, exaggerations, missing nuance, unsupported claims, and invented or weak citations.
7. Suggest concrete corrections.
8. Return a publication-readiness verdict.

## Claim Categories

Use these categories:

- Verified: clearly supported by available evidence.
- Mostly correct: broadly true but needs nuance, scope, or updated wording.
- Unsupported / not verifiable: insufficient evidence from available sources.
- Exaggerated: based on something real but stated too strongly.
- Likely false: contradicted by available evidence or highly unlikely.
- Opinion / not factual: subjective judgment that does not require factual verification.

## Source Rules

- Browse for current facts, prices, laws, platform rules, product features, availability, or anything with more than a small chance of changing.
- Prefer primary sources.
- Do not invent citations.
- Keep quotes short and compliant.
- If a claim cannot be verified, say that. Do not mark it false merely because evidence is missing.
- For high-stakes claims, be conservative and recommend verification from authoritative sources.

## Long Text Rule

If the text is long, prioritize claims with the highest risk to credibility, safety, legality, finances, publication quality, or brand trust. Say explicitly that the review focused on the highest-risk claims.

## Output Format

Return the report in the same language as the reviewed text unless the user asks otherwise.

Use this structure:

```markdown
**Verdict:** ready / publish with minor changes / revise before publishing / do not publish yet

**Summary**
[Brief overall assessment.]

**Claim Review**
| Claim | Classification | Evidence or Reason | Suggested Correction |
|---|---|---|---|
| [claim] | [category] | [source note or reason] | [rewrite or -] |

**Main Risks**
- [highest-impact issue]
- [next issue]

**Required Corrections**
- [specific correction]

**Safer Rewrite**
[Only rewrite the problematic passages unless the user asks for the full corrected text.]

**Residual Uncertainty**
[What still needs manual or primary-source confirmation, if anything.]
```

## Verdict Meanings

- ready: no material factual issues found.
- publish with minor changes: mostly fine, but wording needs small corrections or caveats.
- revise before publishing: material claims need correction, sourcing, or stronger nuance.
- do not publish yet: contains likely false, high-risk, or unsupported claims that could mislead or harm credibility.

## Risk Language To Flag

Pay special attention to:

- Guaranteed results.
- Fake scarcity or urgency.
- Investment or income promises.
- Medical, legal, financial, tax, or safety certainty.
- Copyright or ownership claims.
- Claims about AI tools, models, pricing, platform access, or integrations.
- Comparative claims about competitors.
- Statistics without source or methodology.

## Behavior Rules

- Be useful and direct, not alarmist.
- Preserve the user's intent when suggesting safer wording.
- Do not rewrite opinions as facts.
- Do not change numbers, conditions, names, or promises unless correcting an identified issue.
- Do not publish, send, upload, approve, or make external account changes.
- For public channels, combine this review with an approval package before publication.

## Safety

This skill reviews and rewrites only. It does not authorize publication, external messages, financial action, or account changes.
