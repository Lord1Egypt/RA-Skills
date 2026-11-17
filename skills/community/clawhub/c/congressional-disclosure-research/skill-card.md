## Description:

Research public House and Senate financial-disclosure filings through Crawlora and summarize supported Senate reports with source-linked transaction evidence and coverage limitations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and analysts use this skill to inventory public congressional disclosures and prepare source-linked transaction evidence briefs, preserving filing coverage, ownership, dates, amount ranges, and unresolved duplicates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key is a secret, and disclosure-search parameters and filing URLs are sent to Crawlora.

Mitigation: Use Crawlora only with authorization, keep CRAWLORA_API_KEY secret, and avoid sending unnecessary sensitive query details.

Risk: Search and report requests may consume credits or exceed the intended research scope.

Mitigation: Bound pages, calls, and the credit budget to the requested scope.

Risk: Unsupported documents and overlapping filings can make transaction coverage incomplete or duplicated.

Mitigation: Mark unavailable report bodies, retain source links, and label probable duplicates without collapsing uncertain matches.

## Reference(s):

- [Congressional disclosure endpoint reference](artifact/reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/congressional-disclosure-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown filing inventory or transaction evidence brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source links and dates, document availability, owner and amount ranges, probable duplicates, and explicit coverage limitations.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
