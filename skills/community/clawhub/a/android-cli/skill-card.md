## Description:

Orchestrates Android development tasks including project creation, deployment, SDK management, and environment diagnostics using the `android` command-line tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide Android CLI workflows for SDK management, project creation, APK deployment, emulator control, device interaction, documentation lookup, UI inspection, and journey-style app testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SDK installs, updates, removals, CLI updates, emulator deletion, APK deployment, adb input, and skill add/remove commands can change the local Android environment or a connected device.

Mitigation: Review proposed commands before execution and apply them only to the intended SDK path, emulator, project, or device.

Risk: Screenshots and layout dumps can capture secrets, private data, or sensitive on-screen content.

Mitigation: Avoid saving or sharing screen captures and layout output from sensitive screens, and redact artifacts before retaining or transmitting them.

## Reference(s):

- [Android interaction reference](references/interact.md)
- [Android journey testing reference](references/journeys.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Android CLI commands, adb input commands, UI layout JSON interpretation, journey result JSON, and concise troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
