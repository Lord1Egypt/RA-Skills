## Description:

Comprehensive ComfyUI operations reference for the Genor-Comfy-Gate gateway, covering multimodal audio, image, and planned video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[genortg](https://clawhub.ai/user/genortg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate a local ComfyUI gateway, manage reusable workflows, submit generation jobs, and retrieve generated audio or image outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes high-impact server, file, media, and workflow controls.

Mitigation: Run it only on a trusted local machine or isolated account, bind the server to 127.0.0.1 unless intentionally publishing it, and avoid exposing /mcp to untrusted users.

Risk: Authentication and media-link behavior may be unsafe for sensitive files or private generated media.

Mitigation: Set a strong API key and fix authentication and media-link expiry controls before using the skill with sensitive content.

Risk: Path validation and PM2/admin controls require review before sensitive deployment.

Mitigation: Review and fix path handling and administrative controls before connecting private files, workflows, or production-like ComfyUI backends.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/genortg/skills/genor-comfy-gate)
- [Publisher profile](https://clawhub.ai/user/genortg)
- [GSD Core attribution](https://github.com/open-gsd/gsd-core)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, API descriptions, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to submit ComfyUI workflow jobs and handle generated media references.]

## Skill Version(s):

2.2.0 (source: server-resolved release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
