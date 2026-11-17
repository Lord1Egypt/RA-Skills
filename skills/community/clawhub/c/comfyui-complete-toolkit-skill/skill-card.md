## Description:

Comfy UI Complete Toolkit provides portable ComfyUI workflow and API guidance for building, validating, submitting, and troubleshooting image and video workflows across local, remote, and cloud installs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zambav](https://clawhub.ai/user/zambav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, artists, and workflow operators use this skill to have an agent discover a ComfyUI install, build or repair workflow JSON, submit jobs through the ComfyUI API, monitor results, and troubleshoot model, LoRA, node, or output issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote or cloud ComfyUI submissions may consume paid compute or affect shared infrastructure.

Mitigation: Confirm the target server is controlled by, or authorized for, the user before queueing jobs, especially on hosted deployments.

Risk: Incorrect node, model, encoder, VAE, LoRA, or scheduler assumptions can produce failed jobs or wasted GPU time.

Mitigation: Discover node classes and dropdown values with /object_info and validate family compatibility before submitting workflows.

Risk: Install-specific paths, secrets, or private environment details could leak if embedded in reusable workflow guidance.

Mitigation: Keep setup values in user-owned configuration, avoid absolute filesystem paths, and never store API tokens or credentials in skill docs or workflow JSON.

## Reference(s):

- [ComfyUI API guidance](references/api.md)
- [Setup and onboarding](references/setup.md)
- [Workflow patterns](references/workflow-patterns.md)
- [Model-family guidance](references/models.md)
- [Compatibility checks](references/compatibility.md)
- [LoRA guidance](references/lora.md)
- [Graph conventions](references/graph-conventions.md)
- [Config template](references/config-template.md)
- [Prompting guidance](references/prompting.md)
- [ClawHub skill page](https://clawhub.ai/zambav/skills/comfyui-complete-toolkit-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, and ComfyUI workflow JSON when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent output should be based on live ComfyUI discovery and user-provided install details rather than hardcoded local paths or model names.]

## Skill Version(s):

1.0.0 (source: server release metadata and references/changelog.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
