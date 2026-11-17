## Description:

Cross-Platform Social Poster helps agents prepare and send platform-specific posts for X (Twitter), Telegram, and Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and operators use this skill to draft and execute cross-platform social updates, announcements, and media posts while adapting formatting for X, Telegram, and Discord.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External posting with real social accounts can publish unintended, private, or incorrect content.

Mitigation: Use test accounts or limited webhooks first, and review every destination and message before posting.

Risk: Credentials and webhook URLs can be exposed through `.env` files, shell history, or copied examples.

Mitigation: Protect `.env` files, use secret storage when available, and avoid posting secrets, internal screenshots, or private media.

Risk: Unpinned CLI dependencies can change behavior or introduce supply-chain risk.

Mitigation: Pin and verify CLI dependencies before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/cross-platform-social-poster)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
