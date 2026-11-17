## Description:

Connects an agent to a configured ComfyUI server to generate images from prompts, inspect server state, and interact with ComfyUI REST and WebSocket endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqliaoxin](https://clawhub.ai/user/qqliaoxin)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to connect to a trusted ComfyUI server, submit image-generation prompts, retrieve generated image URLs, and check queue, model, history, and server status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and workflow data are sent to the configured ComfyUI server.

Mitigation: Install and use the skill only with a ComfyUI server that the operator trusts for the prompts and generated content being handled.

Risk: The upload command can send arbitrary local file paths to the configured server.

Mitigation: Do not use upload for sensitive paths, keys, configuration files, documents, or workspace files; restrict uploads to intended image assets.

Risk: The skill can inspect or change remote ComfyUI execution state beyond simple image generation.

Mitigation: Limit use of queue, history, cancel, interrupt, and status commands to operators authorized to manage the target ComfyUI server.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qqliaoxin/skills/comfyui-api)
- [Publisher profile](https://clawhub.ai/user/qqliaoxin)

## Skill Output:

**Output Type(s):** [Text, JSON, Image URLs, Configuration guidance]

**Output Format:** [Structured JSON-style responses with status fields, messages, and generated image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ComfyUI prompt IDs, queue or history data, server status, model listings, and error messages.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
