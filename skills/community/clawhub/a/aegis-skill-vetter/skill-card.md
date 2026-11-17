## Description:

Enterprise-grade security vetting protocol for AI agent skills. Automated threat detection, quantified risk scoring, and zero-trust code analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[r00tfe1](https://clawhub.ai/user/r00tfe1)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to vet third-party agent skills before installation by applying source, code, permission, dependency, and behavior checks. It produces a security-oriented recommendation and audit trail for installation decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the skill's recommendation as an independent sandbox or final authority.

Mitigation: Use it as a review framework and verify generated recommendations before permitting installation or execution actions.

Risk: Example commands may inspect local skill files or query public repository metadata.

Mitigation: Run commands only against skill folders intended for review and confirm network-facing examples before use.

Risk: The artifact contains scanner-triggering examples that describe threats rather than implemented behavior.

Mitigation: Interpret scanner hits in context and rely on the server security verdict and summary for release risk.

## Reference(s):

- [Aegis skill source](artifact/skill.md)
- [ClawHub skill page](https://clawhub.ai/r00tfe1/skills/aegis-skill-vetter)
- [ClawHub publisher profile](https://clawhub.ai/user/r00tfe1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown security review reports with command snippets and decision guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk scores, critical and warning classifications, audit details, and recommended installation decisions.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
