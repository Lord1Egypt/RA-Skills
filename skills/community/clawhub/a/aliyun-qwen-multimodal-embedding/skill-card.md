## Description:

Prepares Alibaba Cloud Model Studio multimodal embedding request payloads for text, image, and video retrieval, cross-modal search, clustering, and offline vectorization workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare normalized Alibaba Cloud Model Studio multimodal embedding requests and supporting guidance for retrieval, similarity search, clustering, and vectorization pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real embedding workflows require Alibaba Cloud credentials.

Mitigation: Use DASHSCOPE_API_KEY or Alibaba Cloud credentials only in trusted environments, and avoid exposing credentials in logs, generated files, or shared output locations.

Risk: Generated request files may contain sample text or media references.

Mitigation: Keep output directories access-controlled and avoid placing sensitive inputs in shared directories.

## Reference(s):

- [Skill reference sources](references/sources.md)
- [Alibaba Cloud Model Studio embedding documentation](https://help.aliyun.com/zh/model-studio/embedding)
- [Alibaba Cloud Model Studio model list](https://help.aliyun.com/zh/model-studio/models)
- [Alibaba Cloud Model Studio model updates](https://help.aliyun.com/zh/model-studio/newly-released-models)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and JSON request payload files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write request JSON under output/aliyun-qwen-multimodal-embedding/ with model, modality mix, selected dimension, and sample input references.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
