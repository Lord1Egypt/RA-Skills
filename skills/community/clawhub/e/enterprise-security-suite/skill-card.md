## Description:

Enterprise Security Suite helps agents request confirmation for high-risk actions, create file backups, record change logs, roll back from backups, and assess skill installation risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gk752448784](https://clawhub.ai/user/gk752448784)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add operational guardrails around high-risk agent actions, including confirmation prompts, backups, change logging, rollback, and pre-installation skill checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan states that the core safety protections are unreliable as an enforcement-grade security layer.

Mitigation: Review before installing and keep independent human approval controls in place for high-risk actions until confirmation enforcement is verified.

Risk: Activation persistently changes the agent's memory.

Mitigation: Run activation only in a controlled workspace after documenting the intended scope and rollback path.

Risk: The security guidance calls out repository verification and rollback validation as areas that need hardening.

Mitigation: Validate source provenance and backup targets before relying on source trust decisions or rollback behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gk752448784/skills/enterprise-security-suite)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell, JavaScript, and JSON examples; runtime helpers return JavaScript objects or booleans.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for human review before risky operations are executed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
