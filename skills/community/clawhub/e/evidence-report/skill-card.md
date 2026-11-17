## Description:

RumorChecker 统一报告标准。确保证据链可追溯、多元交叉验证可视化、误解来源可解释，培养用户辨别能力。

This skill is ready for commercial/non-commercial use.

## Publisher:

[evianevans](https://clawhub.ai/user/evianevans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce a structured Chinese-language rumor-checking reference report with traceable evidence, cross-source verification, misunderstanding analysis, and practical verification tips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fixed Chinese-language report structure may be inconvenient or confusing in non-Chinese workflows.

Mitigation: Adapt the language and section labels before use in non-Chinese environments while preserving the traceable evidence and cross-verification requirements.

Risk: A rumor-checking report can become misleading if upstream agents provide vague, stale, or unsourced evidence.

Mitigation: Require complete source URLs, source type, publication date, credibility reason, and cross-reference status for every evidence item.

Risk: Readers may treat the report as an authoritative judgment rather than a reference aid.

Mitigation: Keep the disclaimer, reference-opinion wording, confidence caveat, and user-final-judgment framing in generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evianevans/skills/evidence-report)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Structured Chinese-language Markdown report template with JSON intermediate schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires traceable source URLs, source types, publication dates, credibility ratings, cross-reference matrix, misunderstanding analysis, verification tips, and participant attribution.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
