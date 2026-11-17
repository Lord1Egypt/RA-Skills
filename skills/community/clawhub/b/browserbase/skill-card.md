## Description:

Create and manage persistent Browserbase cloud browser sessions with authentication persistence for browser automation, logged-in workflows, authenticated page scraping, cloud browser management, captcha solving, session recording, screenshots, and session cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesfincher](https://clawhub.ai/user/jamesfincher)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to create Browserbase cloud browser sessions, preserve login state across runs, automate navigation and JavaScript execution, capture screenshots or recordings, and inspect session logs. It is suited to authenticated research, documentation capture, and browser workflow automation where the agent is allowed to control a cloud browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose active session secrets, cookies, debug URLs, and connection URLs in normal command output.

Mitigation: Treat get-cookies, live-url, create-session, and related outputs as credential material; avoid sharing logs that contain them and restrict use to trusted sessions.

Risk: Authenticated sessions and Browserbase contexts may remain logged in across runs.

Mitigation: Use separate contexts per site, avoid sensitive accounts, terminate sessions when work is complete, and delete contexts after the workflow no longer needs persisted authentication.

Risk: Session recording is enabled by default and may capture private authenticated activity.

Mitigation: Use --no-record for sensitive workflows and review recordings before storing or sharing them.

Risk: Captcha solving is enabled by default and may bypass interactive checks on protected pages.

Mitigation: Use --no-solve-captchas unless automated challenge handling is appropriate for the target site and task.

## Reference(s):

- [Browserbase API Quick Reference](references/api-quick-ref.md)
- [Browserbase website](https://www.browserbase.com/)
- [Browserbase API](https://api.browserbase.com/v1)
- [ClawHub skill page](https://clawhub.ai/jamesfincher/skills/browserbase)
- [ClawHub publisher profile](https://clawhub.ai/user/jamesfincher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with shell commands, JSON CLI responses, screenshots, WebM recordings, and local configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Browserbase credentials and can emit session URLs, cookies, logs, extracted page text, screenshot paths, and recording paths.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
