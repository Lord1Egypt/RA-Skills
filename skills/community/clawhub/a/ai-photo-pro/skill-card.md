## Description:

Generates image files from Chinese prompts through NVIDIA NIM or SiliconFlow image-generation APIs, supporting Kolors, Qwen-Image, and flux.2-klein-4b.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lianghaoxun](https://clawhub.ai/user/lianghaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill when a user asks for AI image generation. The skill sends prompts to the selected provider and returns saved PNG file paths for the agent to present or pass along.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys are stored in scripts/config.json as plaintext.

Mitigation: Use provider keys with limited quota, do not commit or share config.json, and prefer environment variables or a secure secret store where possible.

Risk: Prompts are sent to NVIDIA or SiliconFlow provider APIs.

Mitigation: Avoid sending sensitive, confidential, or regulated information in prompts unless the deployment has approved provider terms and controls.

Risk: The SiliconFlow path downloads provider-returned image URLs without validation.

Mitigation: Validate HTTPS image hosts, set request timeouts and size limits, and verify downloaded content before saving files.

Risk: Generated files remain on disk after creation.

Mitigation: Apply retention, cleanup, and access controls appropriate for the generated image content.

## Reference(s):

- [AI Photo Pro on ClawHub](https://clawhub.ai/lianghaoxun/skills/ai-photo-pro)
- [NVIDIA NIM](https://nim.nvidia.com/)
- [SiliconFlow API](https://cloud.siliconflow.cn/i/IOo0eaWy)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Configuration instructions]

**Output Format:** [PNG image files with returned local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires provider API keys and saves generated images under the skill's img_data directory.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
