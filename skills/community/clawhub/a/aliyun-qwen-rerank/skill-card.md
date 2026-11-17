## Description:

Use when reranking search candidates is needed with Alibaba Cloud Model Studio rerank models, including hybrid retrieval, top-k refinement, and multilingual relevance sorting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare Alibaba Cloud Model Studio rerank request payloads after embedding or vector retrieval. It supports candidate reordering, top-k refinement, and multilingual relevance sorting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can write local output files to any path allowed by the running agent when --output is supplied.

Mitigation: Review the output path before execution and restrict it to the intended workspace or artifact directory.

Risk: The generated payload is only a request template; actual Alibaba Cloud API calls and credential handling happen outside this skill.

Mitigation: Use approved credential storage and request review processes when adapting the payload for live API calls.

## Reference(s):

- [Sources](references/sources.md)
- [Alibaba Cloud Model Studio Embedding Documentation](https://help.aliyun.com/zh/model-studio/embedding)
- [Alibaba Cloud Model Studio Newly Released Models](https://help.aliyun.com/zh/model-studio/newly-released-models)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, JSON]

**Output Format:** [Markdown guidance with bash examples and generated JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper writes a local request JSON file to the configured output path.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
