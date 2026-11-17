## Description:

AI Browser lets an agent control a real Chromium browser over WebSocket for navigation, clicking, typing, screenshots, DOM snapshots, and page status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbo405](https://clawhub.ai/user/linbo405)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to run browser automation workflows such as web testing, data collection, screenshot capture, form filling, and site monitoring through a local WebSocket-controlled Chromium session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes powerful browser access with weak boundaries.

Mitigation: Install only in a trusted, isolated local environment and restrict WebSocket and debugging ports before use.

Risk: Browser automation may expose sensitive accounts, passwords, tokens, private intranet sites, or confidential form data.

Mitigation: Avoid sensitive sites and accounts unless authentication is added, snapshots are redacted, and script evaluation is removed or tightly gated.

Risk: Chromium is launched with reduced sandboxing in the artifact behavior.

Mitigation: Run Chromium with stronger sandboxing before using the skill beyond controlled local testing.

## Reference(s):

- [AI Browser ClawHub Skill Page](https://clawhub.ai/linbo405/skills/ai-browser)
- [Project homepage](https://github.com/openclaw/ai-browser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe WebSocket actions and browser-control responses, including screenshot data and DOM snapshots.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
