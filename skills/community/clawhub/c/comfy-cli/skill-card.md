## Description:

Install, manage, and run ComfyUI instances. Use when setting up ComfyUI, launching servers, installing/updating/debugging custom nodes, downloading models from CivitAI/HuggingFace, managing workspaces, running API workflows, or troubleshooting node conflicts with bisect.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johntheyoung](https://clawhub.ai/user/johntheyoung)

### License/Terms of Use:


## Use Case:

Developers and ComfyUI users use this skill to install and manage ComfyUI instances, launch servers, manage custom nodes and models, run API workflows, and troubleshoot workspace issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to install or update executable ComfyUI components and custom nodes.

Mitigation: Prefer pinned versions and review custom nodes and workflow dependencies before installing or updating them.

Risk: The skill includes workflows for storing or passing CivitAI and Hugging Face tokens.

Mitigation: Avoid placing tokens in shared logs or command history, and keep provider credentials in appropriate local configuration or secret storage.

Risk: The skill can guide users to expose a ComfyUI server on the network.

Mitigation: Do not bind ComfyUI to 0.0.0.0 unless explicit network controls are in place.

Risk: The skill can guide model downloads from third-party sources.

Mitigation: Review model sources and download URLs before use, especially for gated or externally hosted content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johntheyoung/skills/comfy-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/johntheyoung)
- [CivitAI model download endpoint example](https://civitai.com/api/download/models/12345)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance can include commands that install or update executable ComfyUI components, alter local workspaces, store model-provider tokens, or expose a ComfyUI server.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
