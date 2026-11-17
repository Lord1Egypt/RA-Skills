## Description:

Use when visual reasoning is needed with Alibaba Cloud Model Studio QVQ models, including step-by-step image reasoning, chart analysis, and visually grounded problem solving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to prepare Alibaba Cloud Model Studio QVQ visual-reasoning requests for tasks such as screenshot math, diagram analysis, chart interpretation, and visually grounded multi-step problem solving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The validation instructions contain a mismatched output path, which may cause automated validation to check the wrong file.

Mitigation: Review or correct the validation path before relying on automated validation results.

Risk: The helper script can write generated request payloads to a caller-selected path.

Mitigation: Keep generated output paths constrained to the intended output directory before execution.

## Reference(s):

- [Alibaba Cloud Model Studio QVQ Documentation](https://help.aliyun.com/document_detail/2850932.html)
- [Alibaba Cloud Model Studio Newly Released Models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [sources.md](references/sources.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script writes a minimal request payload using qvq-plus by default and supports caller-selected output paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
