## Description:

Sends a liveness heartbeat so registry-dashboard-53592 can show the tool as online.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silakge](https://clawhub.ai/user/silakge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to report a tool's online status to a local dashboard daemon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The heartbeat connects to a local daemon socket under the profile-sync directory.

Mitigation: Install only if you expect communication with that local daemon; verify the socket belongs to the intended service.

Risk: The skill declares filesystem write and network egress permissions.

Mitigation: Review these permissions and run --init only when you want the per-user configuration created.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/silakge/skills/beacon-000)

## Skill Output:

**Output Type(s):** [Text, Configuration guidance]

**Output Format:** [JSON status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports initialization or heartbeat status once per run.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
