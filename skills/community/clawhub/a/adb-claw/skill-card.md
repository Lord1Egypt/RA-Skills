## Description:

ADB Claw lets agents observe and control connected Android devices with screenshots, indexed UI trees, taps, swipes, deep links, app lifecycle commands, file transfer, audio capture, and structured JSON command output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dionren](https://clawhub.ai/user/dionren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, testers, and automation agents use this skill to inspect and operate connected Android devices over ADB for mobile app testing, debugging, live UI monitoring, audio capture, file transfer, and app management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install an unpinned adb-claw executable from GitHub releases.

Mitigation: Install only when the release binary is trusted, or verify checksums, audit the source, or build the binary yourself before use.

Risk: The skill exposes broad Android device-control capabilities, including screenshots, audio capture, file transfer, app deletion or data clearing, and raw shell commands.

Mitigation: Use it only with devices you control and require explicit approval before audio capture, file transfer, app deletion, data clearing, or raw shell commands.

Risk: USB debugging keeps a connected Android device open to host-side control.

Mitigation: Disable USB debugging when adb-claw work is finished and reconnect only when active control is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dionren/skills/adb-claw)
- [adb-claw GitHub repository](https://github.com/llm-net/adb-claw)
- [adb-claw GitHub releases](https://github.com/llm-net/adb-claw/releases)
- [macOS Apple Silicon binary](https://github.com/llm-net/adb-claw/releases/latest/download/adb-claw-darwin-arm64)
- [macOS Intel binary](https://github.com/llm-net/adb-claw/releases/latest/download/adb-claw-darwin-amd64)
- [Linux x86_64 binary](https://github.com/llm-net/adb-claw/releases/latest/download/adb-claw-linux-amd64)
- [Linux ARM64 binary](https://github.com/llm-net/adb-claw/releases/latest/download/adb-claw-linux-arm64)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command-output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses adb-claw commands that return structured JSON envelopes when executed.]

## Skill Version(s):

1.6.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
