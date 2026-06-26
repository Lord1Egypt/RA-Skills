## Description: <br>
Generate and edit images and produce text or image analysis with Google Gemini models through the Corespeed AI Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zypher-agent](https://clawhub.ai/user/zypher-agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Gemini models through the configured Corespeed AI Gateway for text-to-image generation, image editing, multi-image input, image analysis, and text generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, input images, and generated content are processed through the configured external Corespeed Gemini gateway. <br>
Mitigation: Use only trusted gateway configuration and token accounts, and avoid sending confidential prompts or private images unless that processing is acceptable. <br>
Risk: The skill creates local output files from model responses. <br>
Mitigation: Review generated files and paths before relying on or sharing them. <br>
Risk: Runtime dependencies are installed through uv from inline script metadata. <br>
Mitigation: Pin or review dependencies in stricter environments before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zypher-agent/corespeed-nanobanana) <br>
- [Corespeed](https://corespeed.io) <br>
- [uv](https://github.com/astral-sh/uv) <br>
- [PEP 723 inline script metadata](https://peps.python.org/pep-0723/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated files may be images, text, Markdown, or structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv plus CS_AI_GATEWAY_BASE_URL and CS_AI_GATEWAY_API_TOKEN; image prompts and input images are sent to the configured external Gemini gateway.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
