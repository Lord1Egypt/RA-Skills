## Description:

Publish Markdown or HTML to a clean, shareable dochost.io link and hand the URL back to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyli5313](https://clawhub.ai/user/zyli5313)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish generated Markdown or HTML documents, reports, README content, or pages to a shareable dochost.io URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected Markdown or HTML is published to a public or unlisted dochost.io URL and may expose secrets, confidential drafts, private keys, or sensitive customer data.

Mitigation: Review the exact content before publishing and only use the skill for material that is acceptable to share at the resulting URL.

Risk: The skill requires a dochost.io API key for authenticated publishing.

Mitigation: Use a dedicated API key when possible and avoid embedding credentials in published content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zyli5313/skills/dochost-publish)
- [dochost.io](https://dochost.io)
- [dochost MCP API endpoint](https://dochost.io/api/mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a public or unlisted dochost.io URL and may return an expiration time or edit token.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
