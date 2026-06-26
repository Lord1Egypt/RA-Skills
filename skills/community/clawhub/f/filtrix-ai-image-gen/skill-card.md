## Description: <br>
Generate and edit images using OpenAI, Google Gemini, and fal.ai providers with user-supplied API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lumenclaw-cloud](https://clawhub.ai/user/lumenclaw-cloud) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to generate new images or edit existing images through supported AI image providers from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected images, masks, and related metadata may be sent to external AI providers. <br>
Mitigation: Use only providers whose terms are acceptable for the data, and avoid sensitive or regulated images unless those terms permit the intended use. <br>
Risk: Provider API calls may incur cost through user-supplied keys. <br>
Mitigation: Set only the provider keys intended for use and monitor account usage and spending. <br>
Risk: Image edit and output paths affect local files selected by the user or agent. <br>
Mitigation: Verify input, mask, and output paths before running generation or edit commands. <br>


## Reference(s): <br>
- [Filtrix Prompt Library](https://www.filtrix.ai/prompts) <br>
- [OpenAI Image Generation Reference](references/openai.md) <br>
- [Gemini Image Generation Reference](references/gemini.md) <br>
- [fal.ai Image Generation Reference](references/fal.md) <br>
- [Prompt Writing Guide](references/prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and generated image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image bytes are written to local image files by the provider scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
