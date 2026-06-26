## Description: <br>
Generates ERNIE-Image-Turbo images through Baidu AI Studio and crafts ERNIE-Image prompts for posters, comics, infographics, ecommerce images, UI-style visuals, bilingual text rendering, structured layouts, negative prompts, generation settings, and use_pe decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoimiya66](https://clawhub.ai/user/yoimiya66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to turn image-generation requests into ERNIE-Image-ready prompts and, when configured with a Baidu AI Studio API key, generate and save resulting images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and generation settings are sent to Baidu AI Studio. <br>
Mitigation: Avoid sensitive or confidential prompt content and use a revocable Baidu AI Studio API key. <br>
Risk: Generated images are saved locally in the configured output directory. <br>
Mitigation: Review generated files before sharing them and choose an output directory appropriate for the content. <br>
Risk: The skill requires a user-provided BAIDU_AISTUDIO_API_KEY credential. <br>
Mitigation: Provide the key through the environment variable and rotate or revoke it if it is exposed. <br>


## Reference(s): <br>
- [AI Studio ERNIE-Image API](references/api.md) <br>
- [Prompt Architecture](references/prompt-architecture.md) <br>
- [Examples](references/examples.md) <br>
- [Baidu AI Studio Access Token](https://aistudio.baidu.com/account/accessToken) <br>
- [ClawHub skill listing](https://clawhub.ai/yoimiya66/ernie-image-visual-promptsmith) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and generated media paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print IMAGE_URL and MEDIA lines when generation succeeds; generated images are saved locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
