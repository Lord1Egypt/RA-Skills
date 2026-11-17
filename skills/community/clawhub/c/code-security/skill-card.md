## Description:

Reviews application code in the current workspace for concrete security issues and provides proportionate fixes for risks such as injection, authorization flaws, sensitive data leaks, unsafe file handling, and command execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sf0799](https://clawhub.ai/user/sf0799)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review code for realistic security risks and receive prioritized findings, impact explanations, and actionable remediation guidance. It is especially suited to focused reviews of input handling, secrets, authentication, authorization, file access, logging, and command execution paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review output can miss issues or overstate low-confidence findings.

Mitigation: Treat findings as review assistance and validate important conclusions against the affected code, tests, and threat model before deployment.

Risk: Patch suggestions may change behavior or introduce regressions if applied without project-specific review.

Mitigation: Review proposed changes, run the relevant test suite, and apply patches only after confirming they fit the application architecture.

Risk: The skill may answer or present prompts in Chinese by default.

Mitigation: Set the desired response language explicitly when a different review language is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sf0799/skills/code-security)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown security review with risk levels, impact notes, remediation steps, and patch or code suggestions when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May answer in Chinese by default based on the skill text and interface prompts.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
