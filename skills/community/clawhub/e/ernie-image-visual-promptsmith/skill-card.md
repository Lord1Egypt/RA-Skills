## Description:

Generate ERNIE-Image-Turbo images through Baidu AI Studio and craft ERNIE-Image prompts for posters, comics, infographics, ecommerce images, UI-style visuals, bilingual text rendering, structured layouts, negative prompts, generation settings, and use_pe decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoimiya66](https://clawhub.ai/user/yoimiya66)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to refine ERNIE-Image prompts, choose image-generation presets and settings, and optionally generate images through Baidu AI Studio with their own API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generation parameters are sent to Baidu AI Studio.

Mitigation: Avoid secrets, private designs, personal data, and regulated content in prompts or generation settings.

Risk: Returned image URLs are downloaded and saved locally without validation or response-size limits.

Mitigation: Review use before deployment; restrict downloads to trusted HTTPS hosts, validate image content, and enforce response-size limits before auto-attaching files.

Risk: The skill requires a user-provided AI Studio API key.

Mitigation: Provide the key through BAIDU_AISTUDIO_API_KEY and do not paste credentials into prompts or shared output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yoimiya66/skills/ernie-image-visual-promptsmith)
- [Baidu AI Studio API Key Page](https://aistudio.baidu.com/account/accessToken)
- [AI Studio ERNIE-Image API Endpoint](https://aistudio.baidu.com/llm/lmapi/v3/images/generations)
- [AI Studio ERNIE-Image API](artifact/references/api.md)
- [Prompt Architecture](artifact/references/prompt-architecture.md)
- [Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, API calls, Files]

**Output Format:** [Markdown guidance with inline shell commands and MEDIA path output for generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send prompts and generation parameters to Baidu AI Studio and save returned images locally.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
