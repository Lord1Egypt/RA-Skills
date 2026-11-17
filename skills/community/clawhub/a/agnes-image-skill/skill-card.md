## Description:

Uses Agnes Image 2.1 Flash to generate or edit images from text prompts or input images, with URL or Base64 output and configurable image size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neil-huang](https://clawhub.ai/user/neil-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate new images from prompts or transform supplied images with Agnes Image 2.1 Flash. It is intended for agent workflows that need image URLs, saved image files, or guidance for configuring and invoking the Agnes API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local image inputs can upload arbitrary readable files to the Agnes API if an unsafe path is supplied.

Mitigation: Use only trusted prompts and explicitly approved image paths; confirm any local file before upload.

Risk: Base64 output can overwrite arbitrary writable files if an unsafe output path is supplied.

Mitigation: Write generated files only to approved output directories and confirm before using caller-provided paths.

Risk: The release security verdict is suspicious because local file path handling can be misused.

Mitigation: Review before installation and prefer hardened execution that restricts inputs and outputs to approved directories.

## Reference(s):

- [Agnes Image 2.1 Flash documentation](https://agnes-ai.com/zh-Hans/docs/agnes-image-21-flash)
- [Agnes image generation API endpoint](https://apihub.agnes-ai.cn/v1/images/generations)
- [ClawHub skill page](https://clawhub.ai/neil-huang/skills/agnes-image-skill)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell command examples, plus URL text or saved image files from the generator script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGNES_API_KEY; Base64 image output can be decoded and saved to a caller-specified path.]

## Skill Version(s):

1.0.0 (source: manifest.yaml and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
