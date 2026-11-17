## Description:

Generates images with Alibaba Cloud Model Studio DashScope SDK using Qwen Image generation models and helps agents map normalized image.generate requests to SDK calls and responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to integrate Alibaba Cloud Qwen Image generation into workflows, normalize prompt, size, seed, and reference_image inputs, and produce image URLs, downloaded files, and metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted request JSON can cause local reference_image paths to be read and sent to the image generation service.

Mitigation: Use only trusted request JSON and restrict reference images to explicit files from a dedicated input folder.

Risk: The helper can download returned image URLs without independent URL validation.

Mitigation: Constrain outbound downloads before production use and review returned URLs before saving generated files.

Risk: The DashScope API key is required for operation and could be exposed through unsafe local configuration.

Mitigation: Protect DASHSCOPE_API_KEY and credentials files, and avoid printing or committing secrets.

Risk: The dashscope dependency is installed at runtime unless constrained by the deployment environment.

Mitigation: Pin the dashscope dependency and review dependency updates before production deployment.

## Reference(s):

- [DashScope SDK Reference (Qwen Image)](references/api_reference.md)
- [Prompt Guide (Qwen Image)](references/prompt-guide.md)
- [Source List](references/sources.md)
- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/alicloud-ai-image-qwen-image)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON request and response examples, Python code, shell commands, and generated image file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DASHSCOPE_API_KEY for authenticated image generation and may write generated images and response metadata under output directories.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
