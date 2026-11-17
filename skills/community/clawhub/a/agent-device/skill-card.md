## Description:

Automates interactions for iOS simulators/devices and Android emulators/devices. Use when navigating apps, taking snapshots/screenshots, tapping, typing, scrolling, or extracting UI info on mobile targets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okwasniewski](https://clawhub.ai/user/okwasniewski)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to automate authorized iOS and Android app interaction flows, collect UI state, maintain deterministic replays, and troubleshoot logs or crashes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: On-demand package execution can install an unexpected or unverified agent-device version.

Mitigation: Prefer a trusted preinstalled binary; if installation is required, pin and verify the exact package version before use.

Risk: Device logs and generated artifacts may contain sensitive app or runtime data.

Mitigation: Keep logging off except during scoped debugging, review or delete files under ~/.agent-device, and use redaction patterns when needed.

Risk: Physical iOS device setup can involve sensitive signing or provisioning configuration.

Mitigation: Use Xcode Automatic Signing where possible, keep signing environment variables unset by default, and avoid sharing or committing secret values.

Risk: Mobile automation could affect devices, simulators, or apps outside the intended scope.

Mitigation: Run the skill only against authorized targets and prefer least-privilege, isolated environments for autonomous workflows.

## Reference(s):

- [Snapshot Refs and Selectors](references/snapshot-refs.md)
- [Logs and Debug](references/logs-and-debug.md)
- [Session Management](references/session-management.md)
- [Permissions and Setup](references/permissions.md)
- [Video Recording](references/video-recording.md)
- [Coordinate System](references/coordinate-system.md)
- [Batching](references/batching.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to create local screenshots, recordings, logs, traces, and replay scripts during authorized mobile automation workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
