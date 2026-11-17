## Description:

Automates Android apps from an agent through Termux, MCP, and uiautomator2 for clicking, swiping, typing, screenshots, UI text extraction, app control, price monitoring, scheduled tasks, and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to connect an agent to an Android device, inspect app screens, operate mobile apps, compare shopping prices, schedule checks, and send alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad control over a real Android device, including app control, screenshots, UI dumps, text input, file transfer, shell access, logs, clipboard access, and app data clearing.

Mitigation: Use a dedicated test phone and test accounts, keep debugging disabled when not actively needed, and require explicit review before posting, clearing app data, installing apps, running shell commands, or operating sensitive screens.

Risk: Screenshots, UI dumps, logs, clipboard contents, and notification tokens can expose sensitive personal data or credentials.

Mitigation: Treat screenshots, UI dumps, logs, Telegram bot tokens, chat IDs, and price-history files as sensitive; avoid banking, payment, and private-message screens.

## Reference(s):

- [Setup Guide](references/setup-guide.md)
- [uiautomator2-mcp](https://pypi.org/project/uiautomator2-mcp/)
- [uiautomator2](https://github.com/openatx/uiautomator2)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON, Python, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to produce MCP tool calls, Android UI actions, screenshots, UI dumps, price reports, and notification messages.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
