## Description:

Enforce real progress for long-running tasks by separating execution from reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardsun700](https://clawhub.ai/user/richardsun700)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to require concrete progress evidence for long-running agent work, including file changes, commits, test output, and blocker reports. It can also run a closed-loop verify-execute-verify cycle when the operator intentionally configures an executor command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Closed-loop mode can automatically run powerful commands.

Mitigation: Use closed-loop mode only when automatic execution is intentional, and restrict the executor to a fixed, low-privilege command.

Risk: Untrusted text in verifier or executor command arguments can lead to unsafe execution.

Mitigation: Do not pass untrusted text into --verify-cmd or --execute-cmd, and avoid --force unless it has been explicitly reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richardsun700/skills/execution-verifier)
- [Publisher profile](https://clawhub.ai/user/richardsun700)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, JSON]

**Output Format:** [Markdown guidance with shell commands and verifier JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Strict three-line progress reports; closed-loop mode emits before, triggered_execute, execute_result, and after fields.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
