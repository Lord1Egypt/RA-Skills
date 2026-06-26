## Description: <br>
Generate images with Model Studio DashScope SDK using Qwen Image generation models (qwen-image, qwen-image-plus, qwen-image-max and snapshots). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to standardize Alibaba Cloud DashScope Qwen image generation requests, map normalized image.generate fields, and capture generated image outputs and metadata for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local path supplied as reference_image can be read and uploaded to DashScope without validation or confirmation. <br>
Mitigation: Only pass inspected reference images, keep sensitive files outside the agent workspace, and require explicit user control over generation requests. <br>
Risk: Image generation requests are external Alibaba Cloud uploads that may incur cost and expose prompts or image inputs to the service. <br>
Mitigation: Use a scoped DASHSCOPE_API_KEY, limit request scope, and treat each generation as a potentially billable external operation. <br>


## Reference(s): <br>
- [DashScope SDK Reference (Qwen Image)](references/api_reference.md) <br>
- [Prompt Guide (Qwen Image)](references/prompt-guide.md) <br>
- [Source list](references/sources.md) <br>
- [ClawHub release page](https://clawhub.ai/cinience/alicloud-ai-image-qwen-image) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON examples, Python code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes normalized image.generate request and response fields; the helper can download generated image files and print normalized JSON metadata.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
