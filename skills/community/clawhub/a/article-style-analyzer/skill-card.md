## Description:

Generates Chinese-language article style analysis and imitation guidance from one or more writing samples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengxiaotian](https://clawhub.ai/user/pengxiaotian)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writing-focused agent workflows use this skill to analyze author style, extract stable stylistic traits across samples, and produce structured imitation guidance for new writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is tailored for Chinese-language article style analysis, which may not fit English or locale-neutral workflows.

Mitigation: Use it for Chinese-language style analysis or adapt the schema and guidance before applying it to other locales.

Risk: Style imitation outputs can overfit superficial wording and miss deeper authorial reasoning patterns.

Mitigation: Require multi-sample analysis when possible and review outputs against the skill's stable-trait and imitation-priority checks.

## Reference(s):

- [Analysis Dimensions](references/analysis-dimensions.md)
- [Output Schema](references/output-schema.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON]

**Output Format:** [Markdown and JSON-structured analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese-language analysis and schema guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
