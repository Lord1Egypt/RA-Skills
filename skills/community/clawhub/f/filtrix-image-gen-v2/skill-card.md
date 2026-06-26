## Description: <br>
Generate images using AI providers (OpenAI gpt-image-1, Google Gemini, fal.ai). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lumenclaw-cloud](https://clawhub.ai/user/lumenclaw-cloud) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and creative teams use this skill to generate new images from prompts or edit existing images through OpenAI, Google Gemini, or fal.ai using their own provider API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected images or masks are sent to external AI providers. <br>
Mitigation: Use only provider keys and inputs approved for those services, and avoid sensitive or regulated images unless the provider terms and internal policy allow them. <br>
Risk: The fal.ai edit path disables a provider safety checker by default. <br>
Mitigation: Review or patch that path before relying on fal.ai edits, especially for production or user-supplied inputs. <br>
Risk: The scripts can write output to caller-selected paths. <br>
Mitigation: Choose output paths deliberately and review generated files before using or publishing them. <br>


## Reference(s): <br>
- [Filtrix prompt library](https://www.filtrix.ai/prompts) <br>
- [OpenAI image generation reference](references/openai.md) <br>
- [Gemini image generation reference](references/gemini.md) <br>
- [fal.ai image generation reference](references/fal.md) <br>
- [Prompt writing guide](references/prompts.md) <br>
- [ClawHub skill page](https://clawhub.ai/lumenclaw-cloud/filtrix-image-gen-v2) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lumenclaw-cloud) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated PNG image files from provider scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-supplied provider API keys and writes generated or edited images to a requested path or a default /tmp path.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
