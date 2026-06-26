## Description: <br>
Generates high-quality images from text prompts or reference images and supports image editing, style transfer, and batch variants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, illustrators, content creators, ecommerce and marketing teams, and game or anime creators use this skill to generate, edit, restyle, and batch-produce images from prompts or reference images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts or reference images may be sent to the configured image-generation provider. <br>
Mitigation: Avoid uploading sensitive or regulated images, and install only when the configured provider is appropriate for the data being processed. <br>
Risk: API keys and provider billing limits can be exposed or misused if handled carelessly. <br>
Mitigation: Store API keys in environment variables or a secret manager and monitor provider billing limits. <br>
Risk: The example command references generate.py, but this release is instruction-only. <br>
Mitigation: Use only trusted local scripts and do not run an unrelated generate.py solely because the example names one. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/ai-image-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of image prompts, edited images, style-transfer outputs, and batch variants through the configured image-generation provider.] <br>

## Skill Version(s): <br>
1.0.52 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
