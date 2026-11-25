## Description:

Before installing any npm or PyPI package, GitHub repository, agent skill or MCP server, check it with alalanet install_check and never install on block.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alalaalex](https://clawhub.ai/user/alalaalex)

### License/Terms of Use:

MIT-0

## Use Case:

Agent developers use this skill to check a requested package, repository, agent skill, or MCP server before installing it. It explains how to respond to block, hold, and allow decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned package could change upstream before installation.

Mitigation: Pin the version being installed, including after an allow decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alalaalex/skills/alalanet-install-guard)
- [alalanet install-guard MCP server](https://alalanet.com/mcp/guard)
- [alalanet install-check API](https://alalanet.com/v1/install-check?target=<url-encoded-target>)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands]

**Output Format:** [Markdown instructions with example MCP and HTTP requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Explains how to check an exact installation target and act on the returned decision.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
