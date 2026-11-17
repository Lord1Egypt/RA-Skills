## Description:

Generates, edits, and blends images through APIYI's gpt-image-2-all image service using Node.js or Python helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate new images, edit existing images, or blend multiple reference images from natural-language prompts. It provides command guidance for APIYI-backed image generation with API key configuration and output file handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and input images are sent to APIYI for processing.

Mitigation: Avoid confidential prompts and sensitive images unless the user accepts the data-sharing implications.

Risk: Raw user text in command templates can be unsafe if interpolated into a shell command.

Mitigation: Invoke helper scripts with argument arrays or otherwise shell-safe quoting, and prefer the APIYI_API_KEY environment variable over command-line API keys.

Risk: The helper scripts download generated image URLs returned by the service.

Mitigation: Review generated URLs and run the skill in an environment where outbound network access and downloaded files are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuchubuzai2018/skills/apiyi-gpt-image-2-all-gen)
- [APIYI platform](https://api.apiyi.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command examples; helper scripts produce PNG image files or image URLs/base64 data from the API response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation may take about 60 to 300 seconds; default URL responses are described as temporary and should be saved if long-term retention is needed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
