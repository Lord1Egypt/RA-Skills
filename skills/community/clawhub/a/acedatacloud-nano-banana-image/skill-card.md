## Description:

Generate or edit images with Nano Banana through AceDataCloud, including the 2.1 model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acedatacloud](https://clawhub.ai/user/acedatacloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other ClawHub users use this skill to generate or edit images through AceDataCloud's Nano Banana API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and source image URLs are sent to AceDataCloud.

Mitigation: Avoid sensitive content and never include secrets in prompts.

Risk: Image requests may incur charges, including duplicate submissions while a task is pending.

Mitigation: Check service pricing and poll the existing task ID instead of resubmitting.

Risk: The optional mcp-nano-banana package adds a separate dependency.

Mitigation: Pin or review the package separately before enabling it.

## Reference(s):

- [AceDataCloud first-run guide](https://github.com/AceDataCloud/Skills#first-run-with-clawhub-and-openclaw)
- [AceDataCloud authentication guide](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/authentication.md)
- [AceDataCloud async task guide](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/async-tasks.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API requests]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation and editing requests can return an asynchronous task ID requiring polling.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
