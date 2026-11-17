## Description:

Generates PNG images from text prompts using Baidu's ERNIE-Image API through a Python command-line script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[livingbody](https://clawhub.ai/user/livingbody)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn user image prompts into PNG files via Baidu AI Studio, choose a supported resolution, and save the result in the current workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts are sent to Baidu's API.

Mitigation: Avoid sending sensitive, confidential, or regulated prompt content unless Baidu AI Studio use is approved for that data.

Risk: API keys can be exposed if pasted into chat or passed on the command line.

Mitigation: Use a narrowly scoped Baidu key from an environment variable and avoid sharing secrets in prompts or chat history.

Risk: User-selected output paths can overwrite files or place generated images outside the intended workspace.

Mitigation: Choose explicit filenames inside the active workspace and review paths before running the script.

Risk: Documentation mentions image editing, but the shipped script supports text-to-image generation only.

Mitigation: Use the skill for text-to-image requests and do not rely on it for editing existing images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/livingbody/skills/ernie-image)
- [Baidu AI Studio access token page](https://aistudio.baidu.com/account/accessToken)
- [ERNIE-Image product page](https://aistudio.baidu.com/ernieimage)
- [ERNIE-Image model details](https://aistudio.baidu.com/modelsdetail/46030/intro)
- [Baidu AI Studio ERNIE-Image blog post](https://aistudio.baidu.com/blog/detail/794723628346373)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and generated PNG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script saves one PNG file per run and prints the saved path.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
