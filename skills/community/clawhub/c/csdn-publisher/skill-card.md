## Description:

Writes Chinese technical articles and publishes them to CSDN using browser automation, QR-code login, optional Telegram QR delivery, and a bundled writing-style workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c4chuan](https://clawhub.ai/user/c4chuan)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and technical writers use this skill to draft Chinese technical blog posts, de-duplicate news items with Notion when configured, and publish approved articles to CSDN through browser automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a real CSDN account and browser session to publish content.

Mitigation: Use a dedicated low-privilege CSDN account and review the article before any final publish action.

Risk: The login flow stores CSDN cookies and browser session state, and optional Telegram notifications require bot credentials.

Mitigation: Protect the credential directory, avoid running as root, clear credentials when no longer needed, and treat Telegram bot tokens and CSDN cookies as secrets.

Risk: Optional Notion and Telegram integrations can send article metadata or login notifications to external services.

Mitigation: Enable Notion and Telegram only when the data shared with those services is acceptable for the deployment.

## Reference(s):

- [Csdn Publisher on ClawHub](https://clawhub.ai/c4chuan/skills/csdn-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown articles, shell commands, browser-action guidance, configuration notes, and published article links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local draft files and use browser automation to publish after user review.]

## Skill Version(s):

2.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
