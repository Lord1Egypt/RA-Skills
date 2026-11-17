## Description:

Query builder reputation data via Talent Protocol API, including Builder Rank, human verification, identity resolution, location search, credentials, and GitHub enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juampihernandez](https://clawhub.ai/user/juampihernandez)

### License/Terms of Use:


## Use Case:

Developers and technical operators use this skill to query Talent Protocol profiles, builder ranks, identity links, credentials, and related GitHub activity for builder discovery and reputation analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query external Talent Protocol and GitHub services using profile, identity, wallet, credential, or activity data.

Mitigation: Use a limited Talent API key, use an unscoped GitHub token for public data when needed, and request sensitive identity or credential lookups only when required for the task.

Risk: Builder rank, credentials, human verification, and GitHub activity can be incomplete, stale, or privacy-sensitive.

Mitigation: Treat returned data as external API results, cite or preserve source context when presenting findings, and avoid overclaiming identity or reputation conclusions.

## Reference(s):

- [Talent Protocol](https://talent.app)
- [Talent API data issuers and credentials documentation](https://docs.talentprotocol.com/docs/talent-api/api-reference/get-data-issuers-and-credentials-available)
- [Endpoints](artifact/references/endpoints.md)
- [Use Cases](artifact/references/use-cases.md)
- [GitHub Enrichment](artifact/references/github-enrichment.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with API request examples and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Talent Protocol and GitHub API query examples; ranks are the default reputation output unless scores are explicitly requested.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
