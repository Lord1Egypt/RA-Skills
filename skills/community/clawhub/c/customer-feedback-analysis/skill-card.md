## Description:

Analyze public customer reviews and discussions through Crawlora to identify complaint themes, feature requests, praise, and competitive gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Product teams and analysts use bounded samples of public reviews and discussions to create cited voice-of-customer briefs, compare feedback across products, and identify themes for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Crawlora API key and query terms are sent to Crawlora when collecting reviews.

Mitigation: Use a key you are comfortable sharing with Crawlora and avoid sensitive query terms.

Risk: Filtered public review samples may misrepresent overall customer sentiment or expose unnecessary reviewer details.

Mitigation: Bound the sample, specify market and language, disclose filters and sample counts, and omit unnecessary author details.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/customer-feedback-analysis)
- [Crawlora](https://crawlora.net)
- [Supported feedback sources and endpoints](artifact/reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown theme table and cited narrative]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links, example excerpts, sample counts and denominators, collection filters, exclusions, and follow-up hypotheses.]

## Skill Version(s):

1.0.12 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
