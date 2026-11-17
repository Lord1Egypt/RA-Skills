## Description:

Generate images, video, audio, and 3D with Comfy Cloud - search hundreds of models and workflow templates, run custom ComfyUI workflows, and manage generation jobs through the hosted Comfy Cloud MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[comfy-org](https://clawhub.ai/user/comfy-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect OpenClaw to Comfy Cloud for hosted media generation, ComfyUI workflow execution, template discovery, job management, and output retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated media requests and referenced files may be uploaded to Comfy Cloud.

Mitigation: Use this skill only with files and prompts appropriate for processing by Comfy Cloud.

Risk: Generation jobs may spend Comfy Cloud credits.

Mitigation: Confirm account billing, subscription, or credit balance before running generation workflows.

Risk: API-key setup can expose long-lived credentials if stored in shell profiles.

Mitigation: Use OAuth when possible; for headless use, store API keys in a protected secret store.

## Reference(s):

- [Comfy Cloud skill page](https://clawhub.ai/comfy-org/skills/comfy)
- [Comfy Cloud MCP documentation](https://docs.comfy.org/cloud/mcp)
- [Comfy Cloud MCP endpoint](https://cloud.comfy.org/mcp)
- [Comfy Cloud](https://cloud.comfy.org)
- [ComfyUI](https://www.comfy.org)
- [Comfy CLI local ComfyUI documentation](https://docs.comfy.org/comfy-cli/getting-started)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and MCP tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated media outputs as signed URLs returned by Comfy Cloud.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
