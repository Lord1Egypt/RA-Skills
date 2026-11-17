## Description:

Create, schedule, and manage social posts via Aidelly's public MCP server, including post creation, scheduling, approval workflows, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wilzer](https://clawhub.ai/user/wilzer)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and social media operators use this skill to guide agents through Aidelly MCP workflows for creating, scheduling, approving, and analyzing posts across connected social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent actions can publish, schedule, approve, or upload media against connected social accounts.

Mitigation: Preview generated content, media, platforms, and account selections before execution; use approval-required scheduling when possible.

Risk: Some published social posts may be difficult to undo because platform deletion support is limited.

Mitigation: Confirm platform constraints before publishing, especially for channels where deletion is unsupported or manual.

## Reference(s):

- [Aidelly Public API Docs](https://docs.aidelly.ai/api/v1)
- [Aidelly MCP Public API Endpoint](https://app.aidelly.ai/api/mcp/public-api)
- [Aidelly Plugin Repository](https://github.com/Aidelly/claude-plugin)
- [Aidelly Dashboard](https://app.aidelly.ai)
- [ClawHub Skill Page](https://clawhub.ai/wilzer/skills/aidelly-social)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with shell setup commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Aidelly API credentials and workspace or account identifiers for live actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
