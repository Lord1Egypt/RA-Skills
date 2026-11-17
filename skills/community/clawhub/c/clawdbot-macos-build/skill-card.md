## Description:

Build the Clawdbot macOS menu bar app from source. Use when you need to install the Clawdbot.app companion (for menu bar status, permissions, and Mac hardware access like camera/screen recording). Handles dependency installation, UI build, Swift compilation, code signing, and app packaging automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manish-basargekar](https://clawhub.ai/user/manish-basargekar)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build, sign, install, and launch the Clawdbot macOS companion app from source for menu bar status, permissions, notifications, and Mac hardware access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill builds and launches a sensitive macOS app from unpinned remote code.

Mitigation: Pin or verify the upstream commit or signed release, use a frozen lockfile where possible, and inspect the packaging script before running the build.

Risk: The built app may request sensitive macOS permissions such as Accessibility, Screen Recording, Microphone, or Camera.

Mitigation: Build in an isolated account or VM first, and grant sensitive permissions only after reviewing the app and confirming the intended use.

Risk: Repository-provided commands or packaging steps could perform privileged actions if run with elevated permissions.

Mitigation: Avoid running repository-provided commands with sudo except for separately understood system requirements, and review each privileged command before execution.

## Reference(s):

- [Clawhub skill page](https://clawhub.ai/manish-basargekar/skills/clawdbot-macos-build)
- [Clawdbot macOS documentation](https://docs.clawd.bot/platforms/macos)
- [Clawdbot macOS release documentation](https://docs.clawd.bot/platforms/mac/release)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes prerequisite, signing, packaging, installation, launch, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
