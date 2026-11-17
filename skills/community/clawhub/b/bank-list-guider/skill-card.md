## Description:

Helps agents answer Chinese-language questions about which banks are supported by a treasury management system, including full bank lists and single-bank support checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songsongjiang](https://clawhub.ai/user/songsongjiang)

### License/Terms of Use:

MIT-0

## Use Case:

Customer support and treasury operations agents use this skill to answer whether specific banks are supported and to present the current supported-bank directory by category.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is written for Chinese-language treasury-system bank support scenarios.

Mitigation: Install it only for users who need Chinese-language support, or add translation and locale handling before broader use.

Risk: Unmet bank requests could contain personal or sensitive business details if recorded.

Mitigation: Avoid recording such details unless the user explicitly agrees and a defined storage process is in place.

Risk: Bank availability answers can become stale when supported banks change.

Mitigation: Review and update artifact/references/banks.md before relying on the skill for customer-facing answers.

## Reference(s):

- [Supported Bank List](artifact/references/banks.md)
- [ClawHub Skill Page](https://clawhub.ai/songsongjiang/skills/bank-list-guider)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text answers with categorized bank lists and single-bank support status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language reference answers based on the bundled supported-bank list]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
