## Description:

Use when generating images with Alibaba Cloud Model Studio Z-Image Turbo (z-image-turbo) via DashScope multimodal-generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate text-to-image outputs with Alibaba Cloud Model Studio Z-Image Turbo, including control over prompt, size, seed, prompt extension, endpoint selection, and response mapping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A caller-chosen endpoint can receive the DashScope API key.

Mitigation: Use a dedicated, low-privilege DashScope API key and only allow the official HTTPS DashScope endpoints for base_url or DASHSCOPE_BASE_URL.

Risk: Previous use with an untrusted endpoint may have exposed the API key.

Mitigation: Rotate the DashScope API key after any run that used an untrusted or unexpected endpoint.

Risk: Image prompts or request JSON may contain secrets or sensitive personal data.

Mitigation: Do not include secrets or sensitive personal data in prompts or request files.

Risk: The helper downloads unchecked remote content returned by the API response.

Mitigation: Review the request source and endpoint before execution, and inspect generated files before using or sharing them.

## Reference(s):

- [Z-Image Turbo API Reference](references/api_reference.md)
- [Official Z-Image API Reference](https://help.aliyun.com/zh/model-studio/z-image-api-reference)
- [Alibaba Cloud Z-Image API Reference](https://www.alibabacloud.com/help/zh/model-studio/z-image-api-reference)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, bash, curl, and Python examples; helper script output may include JSON and image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved under output/ai-image-zimage-turbo/images by default; normalized responses can include image URL, dimensions, prompt fields, reasoning, and request ID.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
