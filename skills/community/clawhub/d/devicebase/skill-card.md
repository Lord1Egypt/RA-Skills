## Description:

Devicebase CLI - cross-platform Go CLI for remote Android, HarmonyOS, and iOS device control via HTTP API, including tap, swipe, text input, app launching, screenshots, UI hierarchy inspection, and device information retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richieone](https://clawhub.ai/user/richieone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to automate and inspect remote Android, HarmonyOS, and iOS devices through the Devicebase CLI. It supports mobile testing, AI-agent device workflows, device-farm integrations, and CI/CD automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to run remote installer scripts.

Mitigation: Obtain Devicebase CLI from a signed or checksum-verified release, or review the installer before execution.

Risk: Remote device automation can expose sensitive screen content, UI hierarchy data, and entered text.

Mitigation: Use the skill only with devices you own or are authorized to control, and avoid sensitive login, messaging, payment, or personal-data screens unless explicitly required and handled carefully.

Risk: The CLI requires credential configuration for API access.

Mitigation: Configure credentials only after installation and handle DEVICEBASE_API_KEY as a secret.

## Reference(s):

- [Devicebase website](https://www.devicebase.cn/)
- [ClawHub skill page](https://clawhub.ai/richieone/skills/devicebase)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell command examples and JSON-producing CLI workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands that can create screenshot image files and JSON hierarchy or device-information dumps.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
