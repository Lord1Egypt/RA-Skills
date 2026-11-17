## Description:

This skill helps internal control reviewers evaluate confirmed Taobao/Tmall merchant, Cainiao station, and logistics supplier violations and draft penalty recommendations with cited rules and corrective actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Internal control and compliance staff use this skill as decision support when they have confirmed violation facts and need a structured penalty recommendation, rule basis, severity grading, and remediation plan. It covers merchant, Cainiao station, and logistics supplier violations described in the skill evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Penalty guidance may be wrong or outdated if platform rules, legal requirements, or the referenced docs are missing or stale.

Mitigation: Confirm current platform rules, legal basis, and referenced policy docs before relying on any recommendation.

Risk: The skill may recommend high-impact actions such as refunds, takedowns, supplier pauses, blacklisting, or legal escalation.

Mitigation: Use the output as decision support only and require review by an authorized internal owner before action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/06-penalty-calculator)
- [docs/GLOSSARY.md](docs/GLOSSARY.md)
- [docs/INSUFFICIENCY-HANDLING.md](docs/INSUFFICIENCY-HANDLING.md)
- [docs/RULE-UPDATE-SOP.md](docs/RULE-UPDATE-SOP.md)
- [docs/LINKING-SOP.md](docs/LINKING-SOP.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown-style penalty recommendation with sections for facts, severity grading, penalty rationale, remediation, and caveats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language advisory output; decision-support only and subject to internal approval.]

## Skill Version(s):

1.7.0 (source: SKILL.md frontmatter); ClawHub release version 1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
