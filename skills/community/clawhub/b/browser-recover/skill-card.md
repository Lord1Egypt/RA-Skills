## Description:

Recover the local Chromium/Chrome environment when browser tool calls fail by diagnosing stale processes, CDP connection errors, port conflicts, lock files, and page freezes, then retrying the original browser task once.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wind0ws](https://clawhub.ai/user/wind0ws)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to recover OpenClaw-managed Chromium or Chrome browser sessions after startup, CDP connection, port, lock-file, or page-freeze failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recovery can close browser processes, terminate services using selected local ports, and delete OpenClaw browser lock or cache state without proving they belong to the intended OpenClaw instance.

Mitigation: Run check_state.sh first, avoid default full recovery on shared machines, do not run as root or in a privileged container, and verify the target browser profile and port belong to the current OpenClaw instance before running recover.sh.

## Reference(s):

- [Browser Recovery Configuration](references/configuration.md)
- [Safety Guidelines for Browser Recovery](references/safety.md)
- [Browser Recovery Troubleshooting Guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and diagnostic text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single recovery flow with a bounded retry policy.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
