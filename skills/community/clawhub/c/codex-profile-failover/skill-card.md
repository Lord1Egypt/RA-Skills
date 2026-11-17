## Description:

Codex Profile Failover helps OpenClaw operators rotate Codex OAuth profiles automatically or manually when usage is low, usage checks fail, or local token state indicates a problem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugurinanc12](https://clawhub.ai/user/ugurinanc12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install, configure, dry-run, and operate profile failover for Codex sessions that have multiple available OpenAI Codex OAuth profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying failover can persistently change Codex session profile state.

Mitigation: Run the threshold guard or watchdog in dry-run mode first, review the selected current and candidate profiles, and keep generated backups available before applying changes.

Risk: A long-running watchdog can continue applying profile switches after initial setup.

Mitigation: Start the watchdog only after defining an explicit stop procedure and reviewing the workspace-local log and event-log paths.

Risk: The manual trigger's session-key output filter may imply narrower scope than the apply operation enforces.

Mitigation: Do not rely on trigger_profile_failover.py --session-key as the only scope control unless the implementation is fixed to enforce that selection before changes are applied.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ugurinanc12/skills/codex-profile-failover)
- [Setup](references/setup.md)
- [Watchdog configuration example](references/watchdog-config.example.json)
- [Threshold configuration example](references/threshold-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python scripts, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run and apply modes; applying failover can update workspace session state and write event logs and backups.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
