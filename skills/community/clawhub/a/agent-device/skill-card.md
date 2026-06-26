## Description: <br>
Automates interactions for iOS simulators/devices and Android emulators/devices for navigating apps, taking snapshots or screenshots, tapping, typing, scrolling, and extracting UI information on mobile targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okwasniewski](https://clawhub.ai/user/okwasniewski) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to drive mobile apps on iOS simulators/devices and Android emulators/devices during exploration, debugging, replay maintenance, and verification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mobile automation can perform high-impact UI actions such as purchases, account changes, or messages. <br>
Mitigation: Use test devices or test accounts when possible and require confirmation before high-impact UI actions. <br>
Risk: The external agent-device CLI can control mobile apps and devices. <br>
Mitigation: Install or run the CLI only from a trusted, pinned source. <br>
Risk: Logs, screenshots, recordings, traces, replay scripts, and generated artifacts may contain sensitive runtime data. <br>
Mitigation: Keep logging off unless debugging, use scoped debugging windows, and review or delete files under ~/.agent-device and other generated artifact paths when finished. <br>


## Reference(s): <br>
- [Snapshot Refs and Selectors](references/snapshot-refs.md) <br>
- [Logs and Debug](references/logs-and-debug.md) <br>
- [Session Management](references/session-management.md) <br>
- [Permissions and Setup](references/permissions.md) <br>
- [Video Recording](references/video-recording.md) <br>
- [Coordinate System](references/coordinate-system.md) <br>
- [Batching](references/batching.md) <br>
- [ClawHub skill page](https://clawhub.ai/okwasniewski/agent-device) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to create local logs, screenshots, recordings, replay scripts, traces, or batch step files during mobile automation workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
