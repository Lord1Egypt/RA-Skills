## Description:

GEO-focused fact-checking and evidence collection assistant for written content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoly-geo](https://clawhub.ai/user/geoly-geo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to extract factual claims from drafts, verify them against reliable sources, classify the evidence status, and propose citation-ready corrections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest rewritten factual claims that still depend on source quality, recency, or ambiguous metrics.

Mitigation: Review citations, dates, scopes, and corrected wording before applying recommendations to legal, medical, financial, or public-facing content.

Risk: The skill can trigger broadly on content-review tasks that contain factual claims, which may add verification overhead.

Mitigation: Use the skill when accuracy, citation readiness, or trust-sensitive claims matter, and scope checks to the highest-impact claims when speed is important.

Risk: Unsupported rankings, superlatives, and competitor claims can be overstated if evidence is sparse or inconsistent.

Mitigation: Require explicit source, metric, geography, and time period for rankings, and use cautious phrasing when evidence is mixed or unavailable.

## Reference(s):

- [Claim Types for GEO Fact Checking](artifact/references/claim-types.md)
- [Fact-Checking Patterns for GEO Content](artifact/references/fact-checking-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/geoly-geo/skills/geo-fact-checker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with claim tables, evidence summaries, source notes, risk notes, and revised wording.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include citations, verification statuses, assumptions, and open questions for date-sensitive or weakly supported claims.]

## Skill Version(s):

0.1.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
