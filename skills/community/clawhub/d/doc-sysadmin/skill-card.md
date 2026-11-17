## Description:

Doc Sysadmin helps maintain Ubuntu 24.04 hosts by checking disk, memory, load, logs, and cleanup tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zelzaclaw](https://clawhub.ai/user/zelzaclaw)

### License/Terms of Use:


## Use Case:

Developers, operators, and system administrators use this skill to inspect Ubuntu 24.04 host health, diagnose slowdowns, report disk and memory status, and propose cleanup actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change the host system through elevated maintenance commands, including package removal, temporary-directory deletion, log vacuuming, and cache changes.

Mitigation: Review proposed commands before use, separate read-only diagnostics from remediation, and require explicit confirmation before privileged or destructive actions.

Risk: Broad cleanup behavior can delete shared temporary data or remove packages without clear confirmation.

Mitigation: Narrow cleanup targets, add dry-run output, and confirm the exact files or packages affected before execution.

## Reference(s):

- [Ubuntu 24.04 Essential Commands](references/ubuntu24-commands.md)
- [Doc Sysadmin ClawHub Skill Page](https://clawhub.ai/zelzaclaw/skills/doc-sysadmin)
- [zelzaclaw ClawHub Publisher Profile](https://clawhub.ai/user/zelzaclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose privileged Ubuntu maintenance commands and before/after status summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
