## Description: <br>
Monitors the FC Online website for new activities and produces notifications about relevant game events, seasonal cards, gift packs, and version updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FlaxenHair](https://clawhub.ai/user/FlaxenHair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and game community operators use this skill to monitor FC Online activity pages, detect newly published promotions or updates, and receive concise notifications or status reports. Developers can also use it to configure scheduled checks and keyword filters for agent-driven monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can make privileged system changes, including package-manager operations, writes under /root and OpenClaw directories, and creation of a systemd service file. <br>
Mitigation: Review install.sh before installing; prefer manual execution or a user-level scheduler, and run as root only when those system changes are intentional. <br>
Risk: The release creates monitoring persistence without a clear opt-in flow. <br>
Mitigation: Confirm scheduler or service creation before enabling it, and verify how to disable and remove service, configuration, state, and log files. <br>
Risk: Notifications or webhook destinations can send monitoring results outside the local machine. <br>
Mitigation: Use only trusted notification endpoints and avoid placing sensitive information in webhook configuration or monitored output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/FlaxenHair/fco-monitor) <br>
- [FC Online official site](https://fco.qq.com/main.shtml) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Quick start guide](artifact/QUICK_START.md) <br>
- [Examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain-text notifications with shell command snippets and JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May stay quiet when no new activity is detected; scheduled runs can create local logs, state files, and configuration files.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
