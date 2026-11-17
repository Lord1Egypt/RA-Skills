## Description:

Controls a user-selected existing Chrome tab through OpenClaw Session Attach, including extension setup, connection configuration, attach and detach, screenshots, navigation, form entry, and tab management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meowlegemy-sudo](https://clawhub.ai/user/meowlegemy-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent work with a Chrome tab they have explicitly attached, without logging in through an OpenClaw-managed browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The attached browser session and gateway token are sensitive, and the agent can view or act on the attached page.

Mitigation: Attach only intended tabs, avoid banking, admin, email, or other highly sensitive sessions unless the user accepts that access, and keep the gateway token out of chats, logs, screenshots, and shared terminals.

Risk: Connecting the gateway incorrectly can expose the attach workflow beyond the intended local session.

Mitigation: Verify the gateway is running locally on 127.0.0.1, use the expected port and token, and detach the tab when agent control is no longer needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides extension setup, gateway token configuration, browser-tab attachment, browser actions, detachment, and troubleshooting.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
