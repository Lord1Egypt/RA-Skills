## Description:

Qwen Image helps agents call Alibaba Cloud DashScope/Model Studio Qwen Image and Wanxiang 2.6 models for text-to-image generation, image editing, and interleaved text-image output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awsl1110](https://clawhub.ai/user/awsl1110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate or edit images through Alibaba Cloud DashScope/Model Studio models and to prepare the required shell commands, parameters, and environment setup. It is most useful for workflows involving qwen-image, wan2.6-image, or wan2.6-t2i model access.

### Deployment Geography for Use:

Global, subject to DashScope/Model Studio regional endpoint and model availability.

## Known Risks and Mitigations:

Risk: Setup guidance can expose the DashScope API key if users print the environment variable value.

Mitigation: Use a presence-only environment check and never display, log, or paste the API key into shared output.

Risk: Fallback installation guidance can alter system Python packages.

Mitigation: Run the skill through uv or an isolated virtual environment and avoid --break-system-packages.

Risk: Prompts and source images are sent to Alibaba Cloud DashScope endpoints.

Mitigation: Submit only prompts and images that are approved for processing by that external service.

Risk: Unpinned or loosely pinned Python dependencies can change behavior over time.

Mitigation: Pin dependency versions where operational reproducibility or review requirements apply.

## Reference(s):

- [Alibaba Cloud Model Studio text-to-image documentation](https://help.aliyun.com/zh/model-studio/text-to-image)
- [PEP 723 inline script metadata](https://peps.python.org/pep-0723/)
- [ClawHub Qwen Image skill page](https://clawhub.ai/awsl1110/skills/aliyun-qwen-image)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash commands; script execution saves generated image files and, for interleaved Wanxiang output, optional text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and uv or pip; supports cn, intl, and us region flags with model-specific availability limits.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
