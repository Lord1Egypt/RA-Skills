## Description:

A macOS desktop automation skill that helps an agent inspect the screen, operate browser and desktop interfaces, manage files, and verify each step of multi-step computer tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinxulin8899-dotcom](https://clawhub.ai/user/jinxulin8899-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to guide an agent through supervised macOS desktop workflows such as browser tasks, form entry, file organization, downloads, and app interactions that require screenshots, clicks, keyboard input, shell commands, and step verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can observe the screen and control clicks and keystrokes across the desktop.

Mitigation: Run it only in a supervised macOS session and confirm each sensitive desktop action before allowing it to proceed.

Risk: The skill can overwrite the clipboard and paste into the active application.

Mitigation: Review clipboard content and active window focus before text entry, especially for credentials, messages, and forms.

Risk: The skill can run arbitrary shell commands and move, copy, or download local files as the current user.

Mitigation: Restrict use to trusted tasks and review shell commands and file paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinxulin8899-dotcom/skills/chuntai-desktop-agent)
- [Publisher profile](https://clawhub.ai/user/jinxulin8899-dotcom)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser actions, desktop automation commands, file operation commands, status checkpoints, and verification notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
