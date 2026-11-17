## Description:

Blocks YouTube Shorts on Fire TV by monitoring watch time and closing YouTube after a daily limit is reached.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindulasai](https://clawhub.ai/user/cindulasai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install, configure, monitor, and troubleshoot a local Fire TV YouTube Shorts limiter on trusted home networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables a persistent local service with ADB control over Fire TV devices.

Mitigation: Use it only on trusted home networks, keep ADB limited to intended devices, and uninstall the limiter when it is no longer needed.

Risk: Security evidence reports a command-injection flaw in the deprecated bash daemon fallback.

Mitigation: Fix or remove the deprecated bash daemon argument handling before broad use.

Risk: The service can inspect Fire TV UI state and force-stop YouTube.

Mitigation: Review the stored ~/.clawshorts history and log files and confirm the behavior is acceptable for the household or deployment.

Risk: Security guidance flags fixed /tmp UI files.

Mitigation: Replace fixed /tmp UI files with private temporary files before wider deployment.

## Reference(s):

- [Clawshorts Pkg on ClawHub](https://clawhub.ai/cindulasai/skills/clawshorts-pkg)
- [Android Debug Bridge documentation](https://developer.android.com/tools/adb)
- [README](README.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command-oriented guidance for local Fire TV device setup, quota checks, daemon control, usage history, logs, and troubleshooting.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
