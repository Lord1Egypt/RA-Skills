## Description: <br>
Bytedance Ai Image Gen helps an agent generate and edit images with ByteDance Doubao Seedream models through Volcengine Ark, supporting text-to-image, image-to-image, image sequences, multi-image fusion, and image edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etmnb](https://clawhub.ai/user/etmnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents with Volcengine Ark credentials use this skill to generate, edit, and combine images from text prompts or reference images. It is suited for creative image production workflows where the user accepts external API processing, quota use, and local output storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected images are sent to Volcengine/ByteDance for image generation. <br>
Mitigation: Use only prompts and images appropriate for that external service, and avoid sensitive personal or business images unless that processing is acceptable. <br>
Risk: The skill can consume API quota without an extra confirmation step once invoked. <br>
Mitigation: Use a dedicated low-privilege API key and deploy the skill only where automatic quota-consuming image calls are acceptable. <br>
Risk: Prompts, reference image values, output URLs, temp copies, and generated files may be stored locally. <br>
Mitigation: Run the skill in a workspace with appropriate access controls and clean local history or outputs when retention is not desired. <br>
Risk: Optional IAM keys expand credential exposure beyond the image-generation API key. <br>
Mitigation: Avoid configuring optional IAM credentials unless usage synchronization is necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/etmnb/bytedance-ai-image-gen) <br>
- [Volcengine Ark Seedream image generation documentation](https://www.volcengine.com/docs/82379/1541523) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated-image status text, and local file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved as local files; prompts, reference image values, output URLs, temp copies, and generation history may also be stored locally.] <br>

## Skill Version(s): <br>
2.4.2 (source: server release metadata; artifact frontmatter is 2.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
