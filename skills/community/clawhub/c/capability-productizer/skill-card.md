## Description:

识别可变现能力、校验证据，并生成低风险的首个付费产品化实验方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cglt2026opc](https://clawhub.ai/user/cglt2026opc)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese-language users, creators, and solo operators use this skill to evaluate 1-5 personal capabilities for paid-offer potential. It helps separate facts, assumptions, and validation gaps, then designs a small 7-14 day paid experiment for the strongest candidate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pricing or regulated-service recommendations may be mistaken for professional advice.

Mitigation: Frame prices as experiment hypotheses and require professional and compliance review for medical, legal, financial, or other regulated services.

Risk: Weak or self-reported demand signals may lead to premature productization.

Mitigation: Separate facts, assumptions, and validation items; require evidence of real transactions or customer payment commitment before prioritizing.

Risk: Optional evaluator results depend on the user's JSON fields and may be over-trusted.

Mitigation: Review the input JSON before running the evaluator and treat statuses as screening guidance, not final business decisions.

## Reference(s):

- [产品化判定规则](references/rubric.md)
- [ClawHub skill page](https://clawhub.ai/cglt2026opc/skills/capability-productizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell command and JSON classifier output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference an optional Excel self-check template and evaluate JSON lists with scripts/evaluate.py.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
