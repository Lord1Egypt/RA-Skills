## Description:

Helps an agent read and manage Confluence pages, spaces, blog posts, comments, and attachments through a Maton-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Confluence users and developers can ask an agent to find, create, update, or delete workspace content and manage related spaces, comments, and attachments. Optional Maton automations can run approved Confluence actions on a schedule or in response to supported external events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorizing Maton may expose Confluence content accessible to the connected account.

Mitigation: Authorize only the intended account and prefer read-only, least-privilege scopes.

Risk: Writes or deletions may change or permanently remove Confluence content.

Mitigation: Confirm the target and intended change with the user before each write or deletion.

Risk: Hosted functions, triggers, or destinations may continue acting or forwarding data after setup.

Mitigation: Review their scope and recipients and obtain separate approval before enabling persistent automation or forwarding.

## Reference(s):

- [Confluence skill on ClawHub](https://clawhub.ai/byungkyu/skills/confluence-api)
- [Maton](https://maton.ai)
- [Confluence REST API v2 documentation](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/)
- [Confluence REST API v2 page reference](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/)
- [Maton API reference](https://docs.maton.ai/api-reference/overview)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with inline commands and examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Confluence content returned through the authorized connection.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
