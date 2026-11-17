## Description:

AIGC Generator helps an agent generate text-to-image artwork from prompts with optional negative prompts, aspect ratios, and batch settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gushenjie](https://clawhub.ai/user/gushenjie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an OpenClaw agent for generated images, including AI drawing requests with negative prompts, aspect ratio selection, and small batches. The skill submits the prompt to a configured AIGC service, saves generated images as local files, and prepares them for upload to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompts and images are sent to configured external AIGC and Feishu services.

Mitigation: Use the skill only for non-sensitive prompts and images unless the deployment owner accepts those service transfers.

Risk: The security summary says remote image URLs are relayed without enough safeguards or user control.

Mitigation: Restrict AIGC_BASE_URL to a trusted endpoint and add URL and size validation before downloading, uploading, or relaying returned images.

Risk: Automatic uploads to Feishu or object storage can publish generated content beyond the local workspace.

Mitigation: Require explicit user confirmation before Feishu or OSS uploads in deployments where generated content may be sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gushenjie/skills/aigc-gen)
- [AIGC Studio registration - English](https://tczlld.com/aistudio/en/)
- [AIGC Studio registration - Chinese](https://tczlld.com/aistudio/zh/)
- [AIGC service API endpoint](https://tczlld.com/aistudio/api)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Images]

**Output Format:** [Markdown guidance with shell commands and JSON result parsing; generated images are saved as local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AIGC_API_KEY and the requests Python module; supports ratio, batch, negative prompt, and timeout settings.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
