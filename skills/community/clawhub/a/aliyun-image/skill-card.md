## Description:

aliyun-image helps agents use Alibaba Cloud DashScope Qwen image models for text-to-image generation, image editing, multi-image fusion, style transfer, and image text translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanleychanh](https://clawhub.ai/user/stanleychanh)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to generate images from prompts, edit or combine input images, and translate text embedded in images through Alibaba Cloud DashScope APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and images may be sent to Alibaba Cloud DashScope, including local files if the helper script receives a readable local image path.

Mitigation: Use only non-sensitive prompts and images that the user is authorized to send to the external service, and avoid passing arbitrary local paths to the helper script.

Risk: The download command can overwrite writable files at a caller-provided path.

Mitigation: Review the destination path before running downloads and use a dedicated output directory for generated assets.

Risk: Running the helper script from untrusted instructions could cause unintended uploads, API calls, or file writes.

Mitigation: Review commands before execution and run the skill only in a constrained workspace with the required DashScope API key.

## Reference(s):

- [Text-to-image API reference](references/text-to-image.md)
- [Image editing API reference](references/image-edit.md)
- [Image translation API reference](references/image-translate.md)
- [Client helper script](scripts/client.py)
- [ClawHub skill page](https://clawhub.ai/stanleychanh/skills/aliyun-image)
- [Skill metadata repository link](https://github.com/StanleyChanH/aliyun-image-skill)
- [Skill metadata ClawHub link](https://clawhub.com/skill/aliyun-image)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with API examples, JSON payloads, Python code, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return temporary generated or translated image URLs from DashScope; artifact notes that generated image URLs expire after 24 hours.]

## Skill Version(s):

1.1.0 (source: server release metadata, artifact metadata, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
