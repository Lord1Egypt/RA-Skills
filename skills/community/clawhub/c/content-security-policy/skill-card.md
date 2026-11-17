## Description:

Content security policy skill for sensitive information redaction, dangerous instruction filtering, action permission judgment, and multi-level permission management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foxyy1126](https://clawhub.ai/user/foxyy1126)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to redact common sensitive strings, classify risky instructions, and apply advisory permission checks before handling sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a dependable security or permission gate.

Mitigation: Use it as advisory screening only; require trusted human review before approving dangerous actions.

Risk: The sanitizer script can read and print local files when explicitly invoked with a file path.

Mitigation: Do not provide paths to sensitive local files unless a trusted user intentionally selected those files.

Risk: Redaction and command classification cover only the documented patterns and can miss secrets or risky requests outside those patterns.

Mitigation: Pair the skill with independent secret scanning and operational access controls for real deployments.

## Reference(s):

- [Action Judgment Reference](references/action-judgment.md)
- [Instruction Filter Reference](references/instruction-filter.md)
- [ClawHub Skill Page](https://clawhub.ai/foxyy1126/skills/content-security-policy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit redacted text, risk classifications, permission decisions, and operational guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
