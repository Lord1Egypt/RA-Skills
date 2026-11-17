## Description:

Audits software and documentation claims by checking verification commands, exit codes, and supporting evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cha0smagick](https://clawhub.ai/user/cha0smagick)

### License/Terms of Use:

MIT-0

## Use Case:

Spanish-speaking developers and auditors use this skill to test project guarantees against executable checks and record verified, unverified, or refuted claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running a selected gate may execute untrusted repository code.

Mitigation: Review the command first, keep the default dry-run until ready, and run third-party gates in a disposable worktree, container, or VM.

Risk: Passing --full-env may expose credentials to executed code.

Mitigation: Keep the default filtered environment; use --full-env only when necessary after reviewing the target command.

## Reference(s):

- [Auditoria Por Ejecucion on ClawHub](https://clawhub.ai/cha0smagick/skills/auditoria-por-ejecucion)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, JSON]

**Output Format:** [Spanish-language audit findings and verification reports in text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records claims, supporting observations, commands, exit codes, and residual risk.]

## Skill Version(s):

1.0.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
