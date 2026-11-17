## Description:

AutoClaw Browser Automation gives agents browser-control tools for navigation, tab management, bookmarks, screenshots, page content extraction, form interaction, JavaScript execution, cookies, storage, and workflow playback through an MCP server and Chrome extension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to let an agent inspect and operate a Chrome browser for tasks such as bookmarking, searching, navigation, screenshots, form interaction, content extraction, and repeatable browser workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad and persistent browser authority over tabs, bookmarks, cookies, storage, screenshots, JavaScript execution, and page actions.

Mitigation: Install and use it only in an isolated test browser profile without email, banking, work applications, saved sessions, or other sensitive data.

Risk: Unsafe local control paths may allow browser or MCP actions beyond the user's intended scope.

Mitigation: Add authenticated pairing for MCP, remove wildcard CORS, disable automatic attach-all behavior by default, and require per-tab and per-action confirmation for sensitive actions.

Risk: Browser automation outputs or logs may expose cookies, sessions, screenshots, page content, or other secrets.

Mitigation: Redact secrets before display or storage and require explicit confirmation before cookie, session, JavaScript, screenshot, or destructive actions.

Risk: Shell-bridge behavior can expand the impact of browser automation if arbitrary command construction is allowed.

Mitigation: Replace shell bridging with a fixed allowlisted argument-vector implementation before normal use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/addogiavara-tech/skills/autoclaw-browser)
- [README](artifact/README.md)
- [SKILL](artifact/SKILL.md)
- [CHANGELOG](artifact/CHANGELOG.md)
- [Official Website](https://www.wboke.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, text, JSON-like tool results, screenshots, browser actions, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser actions can affect live tabs, bookmarks, cookies, storage, screenshots, and page state.]

## Skill Version(s):

6.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
