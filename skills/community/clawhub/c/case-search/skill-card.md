## Description:

Searches legal case summaries for scenarios described by the user and returns the most relevant case details in a structured format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuwano1](https://clawhub.ai/user/zhuwano1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and legal-research agents can use this skill to match a described legal scenario against bundled Chinese case categories, retrieve up to three similar cases, and format case details for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide confidential, identifying, or privileged legal facts, and unmatched scenarios may be sent to an external search tool.

Mitigation: Use anonymized scenarios and require a consent or minimization step before any external search fallback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuwano1/skills/case-search)
- [Case category index](artifact/case_info/case_index.md)
- [Traffic accident cases](artifact/case_info/traffice_accident.md)
- [Personal injury cases](artifact/case_info/human_hurt.md)
- [Divorce property division cases](artifact/case_info/finance_divorce.md)
- [Property misappropriation cases](artifact/case_info/finance_eat.md)
- [Property theft cases](artifact/case_info/finance_steal.md)
- [Corruption and bribery cases](artifact/case_info/corruption_bribery.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown-like text with repeated case-detail fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to three relevant cases, or explicit empty fields when no match is found.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
