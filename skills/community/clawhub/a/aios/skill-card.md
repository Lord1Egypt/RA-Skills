## Description:

AIOS (Aiden Investment Operating System) helps users perform pre-trade checks, position sizing, trade logging, monthly review, and investment risk-management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jchcvfsf4n-cmd](https://clawhub.ai/user/jchcvfsf4n-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to structure investment trade decisions with pre-trade questionnaires, risk-reward checks, position-sizing calculations, trade logs, and periodic reviews. It is not a substitute for financial advice or independent review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or update local logs containing sensitive financial information such as account size, holdings, trade rationale, prices, and emotional state.

Mitigation: Use the skill only in a private workspace and review generated log files before sharing or committing them.

Risk: The skill requests broad Bash and write access and documents shell command patterns that can be unsafe with untrusted values.

Mitigation: Review commands before execution, avoid pasting untrusted input into shell examples, and prefer structured argument passing with private file permissions.

Risk: Investment workflow outputs can be mistaken for personalized financial advice.

Mitigation: Treat the output as decision-support guidance and independently verify financial decisions before acting.

## Reference(s):

- [AIOS Manual](artifact/references/AIOS-Manual.md)
- [Trade Journal Template](artifact/references/trade-journal-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with optional shell commands and JSON log/configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local logs in the user's current working directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; skill frontmatter reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
