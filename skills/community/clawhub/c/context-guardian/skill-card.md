## Description:

Proactive context monitoring with smart 3-level alerts. Know when to restart before quality degrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucey0017-cloud](https://clawhub.ai/user/brucey0017-cloud)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use Context Guardian to monitor context usage during heartbeat or manual checks, receive threshold-based alerts, and decide when to wrap up, compress context, or restart a session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores recent context usage percentages in a local state file.

Mitigation: Use it only in workspaces where local context-usage history is acceptable, and review or clear memory/context-guardian-state.json according to workspace policy.

Risk: The documented reset flow deletes the local state file with rm.

Mitigation: Run the reset command only when intentionally clearing alert history, and verify the target path before deleting state.

Risk: Alerts depend on OpenClaw context status being available and accurately parsed.

Mitigation: Confirm heartbeat or manual checks can read session status before relying on the alerts for session-management decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucey0017-cloud/skills/context-guardian)
- [README](artifact/README.md)
- [Heartbeat integration example](artifact/examples/heartbeat-integration.md)
- [Manual check example](artifact/examples/manual-check.md)
- [Custom configuration example](artifact/examples/custom-config.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces threshold-based context alerts and updates a local state history when context usage can be read.]

## Skill Version(s):

1.0.1 (source: server release, frontmatter, manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
