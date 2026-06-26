## Description: <br>
Generates local PNG images with Baidu AI Studio's ERNIE-Image and ERNIE-Image-Turbo models from text prompts, with support for batch generation, size selection, seeds, inference steps, guidance scale, and prompt enhancement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiwork4me](https://clawhub.ai/user/aiwork4me) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate image assets through Baidu AI Studio when they need ERNIE image generation, Chinese-language prompts, Chinese-style imagery, or local PNG outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation parameters are sent to Baidu AI Studio. <br>
Mitigation: Avoid private personal data, secrets, and confidential business data in prompts, and follow Baidu AI Studio terms and applicable platform rules. <br>
Risk: The skill requires a sensitive API key. <br>
Mitigation: Keep AI_STUDIO_API_KEY in the environment and out of chat or generated logs. <br>
Risk: Generated files are written to local storage. <br>
Mitigation: Choose or confirm the output directory before generation and review generated PNG files before use. <br>


## Reference(s): <br>
- [ERNIE-Image API Reference](references/api-guide.md) <br>
- [Baidu AI Studio Access Token](https://aistudio.baidu.com/account/accessToken) <br>
- [Baidu AI Studio OpenAI-Compatible API Endpoint](https://aistudio.baidu.com/llm/lmapi/v3) <br>
- [ClawHub Skill Page](https://clawhub.ai/aiwork4me/ernie-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, JSON, Guidance] <br>
**Output Format:** [PNG image files with MEDIA lines, optional JSON status output, and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AI_STUDIO_API_KEY in the environment; accepts prompt, model, size, count, seed, steps, guidance, prompt enhancement, output directory, and filename prefix options; avoids overwriting existing files by adding numeric suffixes.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
