## Description:

Comfy Skill sends prompts to a local ComfyUI endpoint using the bundled workflow to generate images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edward-hsiao](https://clawhub.ai/user/edward-hsiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and AI artists use this skill to ask an agent to generate images through a local ComfyUI service with the included workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts may contain secrets or sensitive personal data that the local ComfyUI service could save in outputs or logs.

Mitigation: Avoid putting secrets or sensitive personal data in prompts, and review local ComfyUI logging and output retention before use.

Risk: The skill depends on a local ComfyUI instance at 127.0.0.1:8188.

Mitigation: Install only when you intend to use that local ComfyUI service and have reviewed the bundled workflow.

Risk: The skill documentation is Chinese-only.

Mitigation: Non-Chinese readers should translate and review the documentation before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edward-hsiao/skills/comfy-skill)
- [Publisher Profile](https://clawhub.ai/user/edward-hsiao)

## Skill Output:

**Output Type(s):** [API Calls, Generated image files, Configuration]

**Output Format:** [Local ComfyUI image output using a JSON workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local ComfyUI endpoint at http://127.0.0.1:8188 with workflow.json.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
