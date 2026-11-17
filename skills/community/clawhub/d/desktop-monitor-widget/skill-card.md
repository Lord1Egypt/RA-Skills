## Description:

Desktop Monitor Widget helps an agent launch a local floating system monitor that displays CPU, memory, disk, temperature, uptime, and process count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1173910773](https://clawhub.ai/user/1173910773)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and desktop users use this skill to start a browser-based or Tkinter-based local monitor for quickly checking host resource usage during active work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher may install the psutil Python package automatically.

Mitigation: Prefer installing psutil manually in a virtual environment before running the skill, and do not run the launcher with sudo.

Risk: The browser mode starts a localhost web server that exposes live host resource data.

Mitigation: Start it only from a directory without sensitive files and stop the process when monitoring is no longer needed.

Risk: The README includes optional systemd autostart guidance that can make the monitor persistent.

Mitigation: Enable autostart only when persistent startup is intended and the operator knows how to disable or remove the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1173910773/skills/desktop-monitor-widget)
- [Local web monitor endpoint](http://127.0.0.1:8765)

## Skill Output:

**Output Type(s):** [shell commands, code, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local runtime instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a local web server or Tkinter desktop window and refreshes host metrics about every two seconds.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
