## Description:

Guides agents in generating and editing Flux images and generating FLUX 3 videos through AceDataCloud's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acedatacloud](https://clawhub.ai/user/acedatacloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use this skill to prepare image-generation, image-editing, and video-generation requests for AceDataCloud's hosted Flux service and follow up on asynchronous tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and supplied image or video inputs are sent to AceDataCloud's hosted service.

Mitigation: Use the service only when sharing those inputs with the provider is acceptable.

Risk: An exposed service API key can allow unauthorized requests.

Mitigation: Keep the key out of prompts and commits, and consider restricting its allowed APIs.

Risk: The optional MCP integration requires installing an additional package.

Mitigation: Verify the MCP package before installing it.

## Reference(s):

- [Flux Image on ClawHub](https://clawhub.ai/acedatacloud/skills/flux)
- [AceDataCloud API key setup](https://platform.acedata.cloud/console/applications)
- [AceDataCloud authentication guidance](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/authentication.md)
- [AceDataCloud asynchronous task guidance](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/async-tasks.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API request examples]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes model selection, asynchronous task polling, and optional MCP setup guidance.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
