## Description:

Detects OpenClaw browser processes orphaned after Gateway restarts and reports or optionally cleans them up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqunabc](https://clawhub.ai/user/guoqunabc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining OpenClaw environments use this skill to find browser processes left after Gateway restarts, review memory impact, and optionally terminate stale current-user processes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kill mode can terminate more processes than the documentation promises.

Mitigation: Use detect-only mode first, inspect the listed PIDs, and enable --kill only after confirming the targets are stale OpenClaw browser processes.

Risk: A broad or empty browser pattern can expand the set of matching processes.

Mitigation: Keep the default .openclaw/browser/ pattern unless there is a reviewed operational reason to override it.

Risk: Running --kill from a privileged health-check account can increase cleanup blast radius.

Mitigation: Run as the intended non-privileged user and harden process-group targeting and the log path before automating kill mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoqunabc/skills/browser-zombie-cleaner-removed)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with bash commands; script output is plain text or JSON when --json is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default operation is detect-only; --kill enables process termination.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
