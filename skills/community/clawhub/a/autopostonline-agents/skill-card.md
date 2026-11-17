## Description:

Enable autonomous AI agents to draft, schedule, publish, and analyze social media content securely via AutoPostOnline's unified publishing API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autopostonline](https://clawhub.ai/user/autopostonline)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, founders, agencies, and agent builders use this skill to let an agent draft, schedule, publish, upload media, and retrieve analytics through AutoPostOnline while staying inside owner-approved campaign rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can publish live social content through AutoPostOnline after receiving an API key.

Mitigation: Start in safe mode with drafts and require explicit owner authorization before autonomous scheduling or publishing.

Risk: Publishing to the wrong connected account or channel could affect a brand or campaign.

Mitigation: List connected integrations before drafting, scheduling, or publishing, and restrict allowed channels and campaign rules.

Risk: Exposure of the AutoPostOnline API key could allow unauthorized publishing actions.

Mitigation: Provide the key only through environment variables or a secret manager, never log it, and revoke or rotate it when publishing access is no longer needed.

Risk: Autonomous social posts could include private, misleading, illegal, hateful, or spam content.

Mitigation: Use owner-approved campaign scope, restricted topics, approval boundaries, and draft fallback when the agent is uncertain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autopostonline/skills/autopostonline-agents)
- [AutoPostOnline agent docs](https://autopostonline.com/docs/agents/)
- [AutoPostOnline agent landing page](https://autopostonline.com/agents/)
- [AutoPostOnline app](https://app.autopostonline.com)
- [AutoPostOnline API base URL](https://app.autopostonline.com/api)
- [AutoPostOnline MCP endpoint](https://app.autopostonline.com/api/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline text, HTTP examples, bash commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Docs-only guidance for using an external publishing API; requires an AutoPostOnline API key.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
