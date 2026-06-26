## Description: <br>
Generate high-quality images from text prompts using BytePlus Seedream models with support for multiple artistic styles and aspect ratios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RaeZhLiu](https://clawhub.ai/user/RaeZhLiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to generate images from prompts, transform reference images, and run batch image generation through BytePlus Seedream models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images are sent to BytePlus for image generation. <br>
Mitigation: Avoid sensitive or confidential prompts and images unless BytePlus processing is acceptable for the use case. <br>
Risk: The ARK_DOLA_API_BASE environment variable can route requests to a different API endpoint. <br>
Mitigation: Verify ARK_DOLA_API_BASE is unset or points to a trusted endpoint before running the skill. <br>
Risk: The skill requires an API key for BytePlus Seedream access. <br>
Mitigation: Use a limited API key and keep ARK_DOLA_API_KEY out of logs, prompts, and committed files. <br>


## Reference(s): <br>
- [BytePlus ModelArk Seedream documentation](https://docs.byteplus.com/en/docs/ModelArk/1399008) <br>
- [ClawHub skill page](https://clawhub.ai/RaeZhLiu/dola-seedream) <br>
- [RaeZhLiu publisher profile](https://clawhub.ai/user/RaeZhLiu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, image URLs, base64 image data] <br>
**Output Format:** [Markdown guidance, Python code examples, shell commands, and JSON API responses containing generated image URLs or base64 image data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARK_DOLA_API_KEY and may use ARK_DOLA_API_BASE to select the BytePlus-compatible API endpoint.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
