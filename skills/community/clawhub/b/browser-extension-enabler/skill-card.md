## Description:

Auto-detects a disconnected OpenClaw Browser Relay Chrome extension and enables it by moving and clicking the mouse through a native dependency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinzhj](https://clawhub.ai/user/kevinzhj)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this Windows-focused skill to restore an OpenClaw Browser Relay Chrome connection by checking status, focusing Chrome, and clicking the extension icon at configured coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is flagged for review because its mouse-control implementation is missing and it depends on an unpinned native mouse-control skill.

Mitigation: Require the missing PowerShell script to be included and pin or verify the win-mouse-native dependency before treating the release as low risk.

Risk: The skill can move and click the real mouse, which may interfere with user activity or click unintended targets if coordinates are wrong.

Mitigation: Use test mode first, verify coordinates on the target display, keep Chrome visible, and avoid running it during important interactive work.

## Reference(s):

- [Browser Extension Enabler ClawHub page](https://clawhub.ai/kevinzhj/skills/browser-extension-enabler)
- [kevinzhj publisher profile](https://clawhub.ai/user/kevinzhj)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with PowerShell and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-focused usage guidance with configurable screen coordinates and a native mouse-control dependency.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, _meta.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
