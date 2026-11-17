## Description:

Searches public Apple job postings and retrieves posting details through the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and recruiters use this skill to search Apple's public careers listings by role or location and retrieve descriptions and qualifications for individual postings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries are sent to Crawlora, a third-party API provider.

Mitigation: Review Crawlora's terms and avoid including sensitive personal information in search parameters.

Risk: Using the API requires a Crawlora API key.

Mitigation: Keep the key in the environment; do not include it in queries or commit it to source control.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/apple-jobs-research)
- [Apple Jobs endpoint reference](artifact/reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Concise text and structured job-posting JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include job metadata; individual posting lookups include descriptions and qualifications.]

## Skill Version(s):

1.0.18 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
