## Description:

Boot Resume detects interrupted OpenClaw sessions after gateway restart or system wake and schedules a continuation event so the agent can resume from session history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[belugary](https://clawhub.ai/user/belugary)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to recover OpenClaw agent sessions that were interrupted by gateway restarts, crashes, OOM kills, SIGKILL, or system wake events. It is intended for environments where automatic continuation of in-progress agent work is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent hooks can automatically resume agent sessions after restarts or wake events without fresh user confirmation.

Mitigation: Enable the systemd integration only in environments where automatic continuation is intended; otherwise use manual invocation and inspect the installed service and drop-in files before enabling them.

Risk: The recovery script reads recent OpenClaw session history to decide whether work was interrupted.

Mitigation: Limit installation to trusted user environments and review local session retention and access controls before deployment.

Risk: Incomplete uninstall or failed install could leave copied scripts, service files, or drop-ins active.

Mitigation: After uninstall, verify the user service, gateway drop-in, copied script, skill directory, and any partial files have been removed.

## Reference(s):

- [Boot Resume ClawHub Skill Page](https://clawhub.ai/belugary/skills/boot-resume)
- [Belugary ClawHub Publisher Profile](https://clawhub.ai/user/belugary)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install user-level systemd hooks and write operational logs under /tmp/openclaw.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
