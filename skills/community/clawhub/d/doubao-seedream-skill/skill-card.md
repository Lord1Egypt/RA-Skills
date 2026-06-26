## Description: <br>
Calls the Volcengine Seedream image-generation API when a user needs to generate images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lamuier](https://clawhub.ai/user/Lamuier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate, edit, or batch-generate images with Doubao Seedream models through the Volcengine API. It supports text prompts, optional reference images, model selection, image sizing, seeds, negative prompts, and local output storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and local reference images may be sent to Volcengine for processing. <br>
Mitigation: Avoid secrets, personal data, and regulated image content in prompts or uploads unless the deployment has approved that data flow. <br>
Risk: Generated files are written to a local output directory. <br>
Mitigation: Choose an output path appropriate for generated media and review stored files before sharing or deploying them. <br>
Risk: The optional web_search tool can cause the model to use external search behavior. <br>
Mitigation: Enable web_search only deliberately and only for prompts where external search is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lamuier/doubao-seedream-skill) <br>
- [Volcengine Seedream image generation API endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline command examples, Python API usage, JSON-like API results, image URLs, and local image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VOLCENGINE_API_KEY and can save generated images to a local output directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
