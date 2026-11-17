## Description:

Generate images with Doubao web chat, extract the final generated image URL, save it locally, and return the saved path for browser-based image generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[likely7](https://clawhub.ai/user/likely7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to drive Doubao web chat image generation, select the best available generated image URL, save the image to local disk, and return the file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-script and page-automation patterns may manipulate page state in ways that deserve review before installation.

Mitigation: Review the skill before installing it and use it only with prompts and browser sessions you trust.

Risk: The workflow downloads remote image URLs and writes files to local disk.

Mitigation: Use a dedicated image output folder, avoid privileged accounts, pass output paths as data, and prevent overwriting existing files.

Risk: The skill depends on a third-party web chat session and user login state.

Mitigation: Confirm the Doubao page is the intended destination and continue only after the user has authenticated in the browser when required.

## Reference(s):

- [Doubao Web Chat](https://www.doubao.com/chat/)
- [ClawHub Skill Page](https://clawhub.ai/likely7/skills/doubaoimages)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Guidance]

**Output Format:** [Markdown guidance with inline JavaScript and PowerShell/Python snippets; final response returns a local file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally include the source image URL.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
