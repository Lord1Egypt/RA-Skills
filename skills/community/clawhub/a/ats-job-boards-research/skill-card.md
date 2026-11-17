## Description:

Retrieves public job listings, posting details, and hiring snapshots from company ATS boards through Crawlora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, job seekers, and market researchers use this skill to review a company's public ATS openings, inspect individual roles, and compare hiring activity over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company and ATS slugs and job-board query parameters are sent to Crawlora.

Mitigation: Use only public board queries and avoid private candidate, employee, or internal recruiting data.

Risk: Exposing the Crawlora API key could allow unauthorized use.

Mitigation: Keep CRAWLORA_API_KEY in environment or secret storage; do not hardcode or commit it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/ats-job-boards-research)
- [ATS endpoint reference](artifact/reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell examples and JSON job-board responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Board results may be paginated; a Crawlora API key is required.]

## Skill Version(s):

1.0.17 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
