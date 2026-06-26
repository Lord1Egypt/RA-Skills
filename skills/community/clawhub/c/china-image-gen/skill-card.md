## Description: <br>
A China-accessible text-to-image skill that uses the SiliconFlow API to generate images with FLUX.1-schnell, FLUX.1-dev, Kolors, and Stable Diffusion 3 models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate images from text prompts through SiliconFlow, especially in China-accessible workflows that do not require a VPN. It helps select a model, prepare prompts and parameters, run the API call, and return the generated image URL with reproducibility details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are submitted to SiliconFlow for image generation and may expose sensitive or confidential content. <br>
Mitigation: Avoid including secrets, personal data, or confidential business details in prompts. <br>
Risk: Image generation can consume SiliconFlow credits or incur billing charges. <br>
Mitigation: Monitor SiliconFlow credits or billing before and during use. <br>
Risk: Generated image URLs are short-lived and may expire before the user saves them. <br>
Mitigation: Download generated images promptly after receiving the URL. <br>


## Reference(s): <br>
- [SiliconFlow image generation API endpoint](https://api.siliconflow.cn/v1/images/generations) <br>
- [SiliconFlow text-to-image model list](references/models.md) <br>
- [ClawHub skill page](https://clawhub.ai/ToBeWin/china-image-gen) <br>
- [Publisher profile](https://clawhub.ai/user/ToBeWin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, API request examples, generated image URL, and generation parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a short-lived generated image URL, selected model, image size, prompt, inference steps, and seed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
