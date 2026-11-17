## Description:

Run the Model Context Protocol (MCP) Atlassian server in Docker, enabling integration with Jira, Confluence, and other Atlassian products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atakanermis](https://clawhub.ai/user/atakanermis)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to start an Atlassian MCP server that lets an agent query Jira issues, search Confluence, and interact with Atlassian services programmatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives Jira credentials to an unpinned third-party Docker image that can change Jira data.

Mitigation: Use a dedicated least-privilege Atlassian token, avoid administrator or broad service-account credentials, test in a non-production project first, prefer a pinned image digest from a trusted publisher, and explicitly review agent write actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atakanermis/skills/atlassian-mcp)
- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and environment-variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker and JIRA_URL, JIRA_USERNAME, and JIRA_API_TOKEN.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
