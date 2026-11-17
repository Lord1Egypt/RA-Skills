## Description:

ClawShorts helps an agent check, manage, and configure YouTube Shorts limiting on Fire TV devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindulasai](https://clawhub.ai/user/cindulasai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and home automation agents use this skill to enforce daily YouTube Shorts limits on Fire TV devices, inspect usage, reset counters, manage the background limiter, and tune per-device configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ADB access on a Fire TV can allow local network control of the device.

Mitigation: Enable ADB only on a trusted, password-protected home network and disable it when the limiter is no longer needed.

Risk: The optional background daemon can close YouTube automatically when the configured daily limit is reached.

Mitigation: Review the configured device list and daily limits before starting the daemon, and use the provided stop or uninstall controls when enforcement should end.

Risk: Misconfigured device targets could cause unwanted ADB connection attempts.

Mitigation: Use only private Fire TV IP addresses from the trusted home network; the release evidence notes public IPs are rejected.

## Reference(s):

- [ClawShorts Skill Page](https://clawhub.ai/cindulasai/skills/clawshorts)
- [README](artifact/README.md)
- [Per-Device Config and Auto-Detection Spec](artifact/SPEC.md)
- [Troubleshooting Guide](artifact/TROUBLESHOOTING.md)
- [Security Audit Report](artifact/SECURITY_AUDIT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses adb and python3 on the user's machine; stores per-device settings and usage locally.]

## Skill Version(s):

1.3.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
