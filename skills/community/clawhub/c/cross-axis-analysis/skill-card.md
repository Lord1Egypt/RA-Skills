## Description:

Guides an agent to research an unfamiliar domain, product, company, or technology concept through longitudinal timeline analysis and cross-sectional competitive comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcz-user](https://clawhub.ai/user/zcz-user)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn broad research requests into structured reports that combine historical development, competitive landscape comparison, and forward-looking synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may route general research requests into a Chinese-language cross-axis report when that format is not desired.

Mitigation: Review activation terms before deployment and narrow the trigger language or add routing guidance where non-Chinese output is preferred.

Risk: Research quality can be weak for obscure domains or when the underlying agent has limited retrieval coverage.

Mitigation: Require source checking and human review before using outputs for investment, strategy, academic, or other consequential decisions.

## Reference(s):

- [横纵分析法 AI research prompt template](references/prompt-template.md)
- [ClawHub skill page](https://clawhub.ai/zcz-user/skills/cross-axis-analysis)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown research prompt and structured analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deep and quick prompt variants; no code execution.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
