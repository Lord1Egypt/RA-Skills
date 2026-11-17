## Description:

Rust-based browser automation using local Chrome for fast DOM extraction, session management, screenshots, scraping, and site structure analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujinlong001](https://clawhub.ai/user/yujinlong001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate local Chrome sessions for navigation, page interaction, DOM extraction, screenshots, Markdown conversion, and sitemap or page-structure analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a local browser and handle session cookies, which may expose sensitive authenticated activity if used with real accounts.

Mitigation: Use an isolated browser profile or test accounts, avoid financial or administrative sessions, and treat saved session files as secrets equivalent to login tokens.

Risk: The security evidence flags weak scoping, unsafe defaults, and browser actions that may affect sites beyond the user's intended target.

Mitigation: Review commands before execution, narrow triggers and permissions, keep Chrome sandboxing enabled by default, and require explicit confirmation for sensitive browser actions.

Risk: The artifact includes documentation for bypassing bot detection and reusing login sessions, which can enable misuse or violations of site protections.

Mitigation: Do not use the skill to bypass site protections, scrape protected services, or reuse sessions without authorization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yujinlong001/skills/fast-browser-use-local)
- [Publisher profile](https://clawhub.ai/user/yujinlong001)
- [Homepage from ClawHub metadata](https://github.com/rknoche6/fast-browser-use)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and structured browser automation outputs such as JSON, Markdown, and PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Chrome or Chromium and runs browser actions through a local Rust CLI or MCP server.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
