## Description:

Searches arXiv papers, retrieves PDF links, and parses paper content for academic research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and developer agents use this skill to search for arXiv papers, retrieve PDF links, and summarize or extract paper content through a configured external service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends paper queries and arXiv identifiers to an external Xiaobenyang service.

Mitigation: Use it only when the user accepts sharing those queries and identifiers with the service.

Risk: The skill may persist the API key in a local .env file.

Mitigation: Use a limited-scope key where possible, avoid broad or sensitive credentials, and remove or rotate the key after use.

Risk: The release evidence reports mismatched gaokao-related code and documentation.

Mitigation: Review behavior before deployment and verify that the configured tools match the intended arXiv workflow.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cainingnk/skills/arxiv-paper-search)
- [Xiaobenyang service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown summaries with structured data from API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API key; results depend on the external Xiaobenyang service and arXiv identifiers or queries supplied by the user.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
