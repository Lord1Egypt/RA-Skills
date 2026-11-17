## Description:

Controls a user's local Chromium browser through an HTTP relay for browser automation, including screenshots that can be sent to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[esojourn](https://clawhub.ai/user/esojourn)

### License/Terms of Use:


## Use Case:

Developers and automation operators use this skill to let an agent drive a local Chromium session for sites that block data-center IP addresses. It supports navigation, clicking, typing, scrolling, JavaScript evaluation, screenshots, tab management, and optional Telegram screenshot delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The relay gives an agent broad control over a real local Chromium session.

Mitigation: Use a dedicated browser profile with no personal logins and stop the relay when browser automation is complete.

Risk: The bearer token and browser screenshots can expose sensitive session or page information.

Mitigation: Protect the relay token, avoid sending screenshots with sensitive content to Telegram, and use Telegram delivery only when explicitly needed.

Risk: The /evaluate capability can execute JavaScript in the browser context.

Mitigation: Limit evaluation to UI automation tasks and do not use it to extract cookies, credentials, authentication headers, or tokens.

Risk: The skill is designed to route browser activity through a local IP to bypass platform data-center IP restrictions.

Mitigation: Review whether this behavior is acceptable for the target platform and use case before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/esojourn/skills/browser-relay-xiaohongshu)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTTP API examples, shell commands, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser-control commands, local screenshot files, and optional Telegram screenshot delivery when explicitly requested.]

## Skill Version(s):

0.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
