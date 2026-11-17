## Description:

Control Browser's kernel for web automation. Supports web navigation, element interaction, page scrolling, file/video downloading, and content extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handongpu16](https://clawhub.ai/user/handongpu16)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser navigation, inspect page state, interact with page elements, scroll, download files or videos, and extract current page content as Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can make high-impact system package and system Python changes.

Mitigation: Review the installer and QQ Browser/x5use distribution source before running it, and prefer an isolated environment with only the permissions required for browser automation.

Risk: Typed browser input can be exposed in logs.

Mitigation: Do not enter secrets through input_text.py unless logging is fixed or disabled, and review or clean generated logs after use.

Risk: The X5 background service runs locally and writes logs under /usr/local/qb_logs.

Mitigation: Know how to stop the service after each session and clean /usr/local/qb_logs when the session is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handongpu16/skills/automation-browser)
- [QQ Browser and x5use distribution source](https://dldir1v6.qq.com/invc/tt/QB/Public/ubuntu_qb)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text command output with page state, action results, and interactive element indexes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may return current page metadata, extracted Markdown, and viewport interactive elements for follow-on automation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
