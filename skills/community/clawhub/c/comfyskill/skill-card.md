## Description:

Sends prompts to a local ComfyUI instance to generate images based on user descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edward-hsiao](https://clawhub.ai/user/edward-hsiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to send a text prompt to a local ComfyUI service and receive a short status message after image generation is queued.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to a configured ComfyUI service.

Mitigation: Install only when sending prompts to ComfyUI is intended, check COMFYUI_ENDPOINT and WORKFLOW_PATH before use, and avoid prompts containing secrets or sensitive personal data.

Risk: The current implementation appears brittle because prompt handling and workflow file shape are inconsistent.

Mitigation: Review the workflow path and prompt substitution behavior before relying on the skill in a production workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edward-hsiao/skills/comfyskill)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [String]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a short status message after posting the prompt to ComfyUI.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
