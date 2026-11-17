## Description:

Checks whether a named product's required hardware resource assessment elements are complete against a local Chinese-language knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellohushuai](https://clawhub.ai/user/hellohushuai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to compare provided hardware resource assessment elements with standard requirements for supported Chinese clinical product lines. It returns whether the assessment is complete or identifies missing elements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Completeness results can be unreliable for blank or loosely matched provided elements.

Mitigation: Treat ok results cautiously and manually review supplied elements until the input-validation issue identified by the security scan is fixed.

Risk: The skill depends on a local Chinese-language knowledge base for standard product requirement files.

Mitigation: Install only when that local knowledge base is trusted and kept current for the supported product lines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hellohushuai/skills/get-resource-element)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON examples and optional JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script output reports ok or lists missing assessment elements.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
