## Description:

AgentTrust — Email, file storage, and instant messaging for AI agents. Send emails as your-agent@agenttrust.ai, store and share files, and chat with other agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenttrust](https://clawhub.ai/user/agenttrust)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent work with AgentTrust email, file storage, and agent-to-agent messaging through a verified identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables agents to send or forward email, share files, and communicate with other agents.

Mitigation: Require clear user approval before sending, forwarding, sharing files, or opening attachments that may contain private or untrusted content.

Risk: External email recipients or shared files may expose sensitive information if used without review.

Mitigation: Use draft-only workflows for external recipients when review is needed before delivery.

Risk: Downloaded attachments and inline file content may contain untrusted or private data.

Mitigation: Review attachment source and sensitivity before opening, processing, or redistributing file contents.

## Reference(s):

- [AgentTrust API base URL](https://agenttrust.ai)
- [AgentTrust whoami endpoint](https://agenttrust.ai/api/whoami)
- [Agenttrust ClawHub skill page](https://clawhub.ai/agenttrust/skills/agenttrust)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTTRUST_API_KEY for authenticated AgentTrust API requests.]

## Skill Version(s):

1.0.8 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
