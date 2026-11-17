## Description:

Generic macOS desktop control using AppleScript for app and window semantics plus screenshot, OCR, mouse, and keyboard workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kd-oauth](https://clawhub.ai/user/kd-oauth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to control a macOS desktop session through app/window inspection, screenshot capture, OCR or image matching, and mouse or keyboard actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control the screen, mouse, keyboard, clipboard, and AppleScript in the active macOS session.

Mitigation: Use it only in a dedicated, low-sensitivity macOS session with explicit Screen Recording and Accessibility permissions.

Risk: Pasted text or generated screenshots may expose sensitive information.

Mitigation: Avoid pasting secrets, clear or protect generated screenshots, and verify target fields before sending externally visible input.

Risk: Untrusted app names can trigger AppleScript interpolation risk until the issue is fixed.

Mitigation: Use only trusted app names or bundle paths and review the AppleScript command path before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kd-oauth/skills/desktop-control-for-macos)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; scripts may emit JSON coordinates, file paths, and image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS Screen Recording and Accessibility permissions; OCR uses Apple Vision through PyObjC.]

## Skill Version(s):

1.1.2 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
