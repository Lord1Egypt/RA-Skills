## Description:

Use when text embeddings are needed from Alibaba Cloud Model Studio models for semantic search, retrieval-augmented generation, clustering, or offline vectorization pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare Alibaba Cloud Model Studio text embedding request payloads for semantic search, retrieval-augmented generation, clustering, and offline vectorization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes local request payload files, so incorrect paths or unintended text input could create or overwrite local output artifacts.

Mitigation: Review the requested output path and payload text before running the helper script, and keep generated request files in a dedicated output directory.

Risk: The helper prepares request JSON but does not submit embeddings or validate Alibaba Cloud service responses.

Mitigation: Use Alibaba Cloud documentation and a separate reviewed client workflow when sending requests or handling credentials.

## Reference(s):

- [Alibaba Cloud Model Studio embedding documentation](https://help.aliyun.com/zh/model-studio/embedding)
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-qwen-text-embedding)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with shell commands and JSON request files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local embedding request JSON payload and does not call network services or handle credentials in the inspected artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
