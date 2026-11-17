## Description:

CDP browser control at localhost:9222. Use when you need to inspect tabs, take screenshots, navigate, scroll, post to X, or run JS in a persistent browser session (e.g. logged into X, Gmail).

This skill is ready for commercial/non-commercial use.

## Publisher:

[gostlightai](https://clawhub.ai/user/gostlightai)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to control a local Chrome or Chromium browser over CDP for tab inspection, navigation, screenshots, page queries, scrolling, and user-approved X posting from a persistent browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a Chrome profile that may already be logged into sensitive websites.

Mitigation: Keep remote debugging bound to localhost, avoid sensitive browser profiles, and review actions before using the skill on authenticated sessions.

Risk: Screenshots and page queries may expose sensitive page content.

Mitigation: Store generated screenshots and copied page content privately and avoid capturing confidential pages unless necessary.

Risk: The optional Telegram confirm-button flow can post to X from weak shared pending state.

Mitigation: Avoid the Telegram confirm-button posting flow until approvals are tied to a specific draft or session and expire after one use.

Risk: Automated X posting can publish unintended content if approval is ambiguous.

Mitigation: Use tweet-draft as the default flow and require explicit --confirm only after user approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gostlightai/skills/cdp-browser)
- [Security Considerations](SECURITY.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON command output, text or HTML query results, and PNG screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser actions run against a local Chrome or Chromium session on localhost:9222 and may interact with logged-in sites.]

## Skill Version(s):

2.0.1 (source: release evidence, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
