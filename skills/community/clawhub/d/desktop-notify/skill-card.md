## Description:

Desktop Notify helps agents send cross-platform desktop completion notifications with sound and native system notification bubbles on Windows, macOS, and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cipher0117](https://clawhub.ai/user/cipher0117)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when a long-running task, report, file generation, or background script should notify them after completion. It provides manual notification commands and optional setup scripts for recurring desktop alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup scripts persistently modify global agent memory so future conversations may run a notification command after each response.

Mitigation: Use the notification scripts manually unless global behavior is explicitly desired; review ~/.workbuddy/MEMORY.md after setup and remove the desktop-notify-auto block to disable it.

Risk: macOS notification text is passed through osascript command text.

Mitigation: Avoid passing untrusted or unsanitized notification titles and messages, and prefer hardened argument handling before deploying broadly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cipher0117/skills/desktop-notify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OS-specific notification commands and setup guidance; notification execution depends on local desktop notification support.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
