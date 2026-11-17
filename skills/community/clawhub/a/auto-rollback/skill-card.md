## Description:

Timed rollback safety net for edits to ~/.openclaw/openclaw.json on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extraterrest](https://clawhub.ai/user/extraterrest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before changing OpenClaw Gateway configuration to create a backup, schedule a timed rollback, inspect rollback state, and cancel protection after a healthy restart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that rollback scheduling can falsely report protection when scheduling fails.

Mitigation: Review scheduling results before relying on the rollback as a safety mechanism, and treat failed or uncertain scheduling as unprotected until corrected.

Risk: The security review reports unsafe generation of executable shell source from environment-controlled values.

Mitigation: Validate rollback state and environment-controlled paths before execution, and fail closed when generated rollback scripts cannot be trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/extraterrest/skills/auto-rollback)
- [Publisher profile](https://clawhub.ai/user/extraterrest)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions for backup, launchd scheduling, rollback status inspection, and cancellation.]

## Skill Version(s):

1.2.0-alpha.2 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
