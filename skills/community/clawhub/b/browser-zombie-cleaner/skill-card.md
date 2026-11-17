## Description:

Detects orphaned OpenClaw browser processes and can optionally terminate them after user, origin, orphan status, and age checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqunabc](https://clawhub.ai/user/guoqunabc)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect and clean up browser processes left behind after OpenClaw Gateway restarts, especially when memory use is high or browser processes are accumulating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kill mode can be widened enough to close unrelated browser processes.

Mitigation: Run the default detect mode first, avoid overriding --pattern, and use --kill only after reviewing the listed processes as OpenClaw browser leftovers.

Risk: The local shell script can terminate browser process groups with SIGTERM and SIGKILL.

Mitigation: Run it as the regular user, keep a conservative --min-age value, and review the audit log at the configured log path before using it unattended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guoqunabc/skills/browser-zombie-cleaner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script reports detected browser process counts, zombie counts, memory estimates, action mode, and zombie details; it can also emit JSON with --json.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
