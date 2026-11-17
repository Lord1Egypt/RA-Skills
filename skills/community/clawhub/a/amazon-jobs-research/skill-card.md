## Description:

Searches public Amazon.jobs postings by keyword or category and retrieves individual job descriptions and qualifications through Crawlora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers, recruiters, and researchers use this skill to find public Amazon job openings, browse categories, and inspect individual postings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search parameters and the API key are sent to Crawlora.

Mitigation: Do not put secrets or personal data in searches; keep the API key in the environment and never commit it to files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/amazon-jobs-research)
- [Amazon Jobs endpoint reference](artifact/reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON job listings and posting details; text summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are paginated; individual postings include descriptions and qualifications.]

## Skill Version(s):

1.0.18 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
