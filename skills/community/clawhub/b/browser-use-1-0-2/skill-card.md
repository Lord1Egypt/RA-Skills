## Description:

Automates browser interactions for web testing, form filling, screenshots, and data extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlshiny](https://clawhub.ai/user/zlshiny)

### License/Terms of Use:


## Use Case:

Developers, QA engineers, and automation users use this skill to navigate websites, inspect page state, interact with elements, take screenshots, and extract page data through the browser-use CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use real browser login sessions and browser profiles.

Mitigation: Prefer isolated Chromium for routine browsing, and confirm the exact account, domain, browser mode, and profile before using authenticated sessions.

Risk: Cookie sync and cookie export can expose sensitive session data.

Mitigation: Use domain-specific sync only when needed, avoid full-profile cookie sync, and avoid plaintext cookie files such as /tmp/cookies.json.

Risk: Tunnels and public session sharing can expose local services or browser sessions.

Mitigation: Confirm the local port, session, and sharing scope before creating tunnels or public session links, and stop tunnels or sessions after use.

## Reference(s):

- [browser-use CLI README](https://github.com/browser-use/browser-use/blob/main/browser_use/skill_cli/README.md)
- [ClawHub skill page](https://clawhub.ai/zlshiny/skills/browser-use-1-0-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and browser automation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, page state summaries, extracted web content, JSON command output, and browser session management guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
