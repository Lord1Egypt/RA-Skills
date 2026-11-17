## Description:

Interact with Apollo.io REST API (people/org enrichment, search, lists).

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhumanj](https://clawhub.ai/user/jhumanj)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure and call Apollo.io REST API endpoints for people search, organization enrichment, and organization list retrieval from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential configuration is unsafe enough to warrant review before installation.

Mitigation: Review the shell scripts before use, keep the Apollo configuration file private and non-writable by others, and use a least-privileged Apollo API key where possible.

Risk: The scripts may read a hardcoded developer path instead of the documented config/apollo.env file.

Mitigation: Confirm and update the configuration path before running the scripts in a local or shared environment.

Risk: APOLLO_BASE_URL controls the destination for authenticated API requests.

Mitigation: Set APOLLO_BASE_URL only to the intended Apollo HTTPS API origin.

## Reference(s):

- [Apollo API origin](https://api.apollo.io)
- [ClawHub skill page](https://clawhub.ai/jhumanj/skills/apollo)
- [Publisher profile](https://clawhub.ai/user/jhumanj)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on Apollo API availability, account plan permissions, rate limits, and the configured API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
