## Description:

Generate and edit images with Agnes Image 2.0 Flash using text-to-image, image-to-image, and multi-image composition workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lutongsuo](https://clawhub.ai/user/lutongsuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users can use this skill to call the Agnes Image API for generating new images, editing existing public images, composing multiple source images, and saving image URLs, files, or base64 output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and image URLs are sent to a third-party API.

Mitigation: Avoid confidential prompts, private images, proprietary image URLs, and other sensitive content.

Risk: The script can download output from an API-supplied URL without validating the target or file type.

Mitigation: Run in a constrained environment, choose explicit output paths, and inspect or scan downloaded files before further use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lutongsuo/skills/agnes-image)
- [API documentation](artifact/references/API.md)
- [Prompt guide](artifact/references/PROMPT_GUIDE.md)
- [Examples](artifact/references/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated image URLs, downloaded image files, or base64 text output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Agnes API key and sends prompts and public image URLs to a third-party API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
