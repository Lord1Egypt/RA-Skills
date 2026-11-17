## Description:

Guides agents in generating and editing videos with Seedance through AceDataCloud's API using text, images, audio, or video references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acedatacloud](https://clawhub.ai/user/acedatacloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to guide an agent through Seedance video generation, editing, and extension with text or media references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference media URLs are sent to AceDataCloud's Seedance service.

Mitigation: Review the provider's data-handling terms before sending sensitive content.

Risk: An exposed API key could allow unauthorized use of the service.

Mitigation: Use a scoped key where possible and keep it out of prompts and commits.

Risk: Real-person images, voices, or videos may be used without appropriate rights or consent.

Mitigation: Use real-person reference media only with the necessary rights and consent.

## Reference(s):

- [Seedance Video on ClawHub](https://clawhub.ai/acedatacloud/skills/seedance)
- [AceDataCloud first-run guide](https://github.com/AceDataCloud/Skills#first-run-with-clawhub-and-openclaw)
- [AceDataCloud authentication guide](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/authentication.md)
- [AceDataCloud async task guide](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/async-tasks.md)
- [AceDataCloud MCP server guide](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/mcp-servers.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON API requests, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover asynchronous task polling and model-specific media inputs.]

## Skill Version(s):

1.0.1 (source: server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
