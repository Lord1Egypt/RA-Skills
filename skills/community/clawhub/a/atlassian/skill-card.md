## Description:

Operate Atlassian Cloud APIs and CLIs across Jira, Confluence, Bitbucket, Trello, Admin, Forge, Compass, Opsgenie, and Statuspage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Atlassian administrators use this skill to choose the correct Atlassian Cloud API or CLI path for Jira, Confluence, Bitbucket, Trello, Cloud Admin, Forge, Compass, Opsgenie, Statuspage, and GraphQL automation. It supports read, write, search, setup, and administrative workflows while emphasizing product-specific authentication, pagination, rate limits, and target review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential examples can expose tokens in shell history, logs, or URLs.

Mitigation: Use least-privilege credentials, prefer OAuth or first-party CLI login where possible, and avoid pasting real tokens directly into shell commands or URLs.

Risk: Cloud Admin, Statuspage, Opsgenie, Jira, Bitbucket, Trello, and Confluence writes can have high operational impact.

Mitigation: Require explicit target review before mutation, especially for bulk, administrative, or destructive actions.

Risk: CLI downloads or npm installs can introduce unreviewed third-party code.

Mitigation: Verify CLI downloads and npm installs before use instead of relying blindly on latest.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/atlassian)
- [Atlassian CLI Commands](https://developer.atlassian.com/cloud/acli/reference/commands/)
- [Atlassian CLI Getting Started](https://developer.atlassian.com/cloud/acli/guides/how-to-get-started/)
- [Forge CLI Reference](https://developer.atlassian.com/platform/forge/cli-reference/)
- [Jira Platform REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [Jira Software REST API](https://developer.atlassian.com/cloud/jira/software/rest/intro/)
- [Jira Service Management REST API](https://developer.atlassian.com/cloud/jira/service-desk/rest/intro/)
- [Confluence Cloud REST API](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/)
- [Bitbucket Cloud REST API](https://developer.atlassian.com/cloud/bitbucket/rest/intro/)
- [Trello REST API](https://developer.atlassian.com/cloud/trello/rest/)
- [Atlassian Cloud Admin REST APIs](https://developer.atlassian.com/cloud/admin/rest-apis/)
- [Atlassian GraphQL API](https://developer.atlassian.com/platform/atlassian-graphql-api/graphql/)
- [Compass REST API](https://developer.atlassian.com/cloud/compass/rest/v2/intro/)
- [Compass GraphQL API](https://developer.atlassian.com/cloud/compass/graphql/)
- [Statuspage API](https://developer.statuspage.io/)
- [Opsgenie API Overview](https://docs.opsgenie.com/docs/api-overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, API requests, JSON examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires product-specific Atlassian credentials; ClawHub metadata lists Linux, macOS, and Windows support with curl or jq available.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
