## Description:

Edit images with Alibaba Cloud Model Studio Qwen Image Edit models (qwen-image-edit, qwen-image-edit-plus, qwen-image-edit-max and snapshots).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and image-workflow operators use this skill to prepare and document instruction-based edits against Alibaba Cloud Model Studio Qwen Image Edit models, including inpainting, replacement, style transfer, local edits, and subject-consistency workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alibaba Cloud credentials can be exposed if API keys or credential files are stored or shared carelessly.

Mitigation: Use a narrowly scoped and revocable DASHSCOPE_API_KEY or credentials entry, keep it out of committed files, and rotate it after suspected exposure.

Risk: Saved request payloads, prompts, result URLs, and image references may contain sensitive user content.

Mitigation: Write artifacts only to controlled output locations, retain only what is needed for reproducibility, and clean the output directory after use.

Risk: Unpinned SDK installation can reduce reproducibility across environments.

Mitigation: Install the dashscope dependency in an isolated virtual environment and pin or lock the dependency when reproducible runs matter.

## Reference(s):

- [Artifact sources](references/sources.md)
- [Alibaba Cloud Model Studio Qwen Image Edit guide](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with bash examples and JSON request or response artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save request payloads, result URLs, model parameters, and output image references under the configured output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
