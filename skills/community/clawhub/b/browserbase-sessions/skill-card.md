## Description:

Create and manage persistent Browserbase cloud browser sessions with authentication persistence. Use when you need to automate browsers, maintain logged-in sessions across interactions, scrape authenticated pages, or manage cloud browser instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesfincher](https://clawhub.ai/user/jamesfincher)

### License/Terms of Use:

MIT

## Use Case:

Developers and external automation agents use this skill to create, resume, and manage Browserbase cloud browser sessions for authenticated browsing, browser automation, research, scraping, screenshots, logs, recordings, downloads, and human handoff workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browserbase cloud sessions may hold authenticated browser state, recordings, logs, cookies, downloads, screenshots, and live control URLs.

Mitigation: Treat live control URLs and cookie output as secrets, isolate workspaces per site or account, and disable recording, logging, captcha solving, or persistence when not needed.

Risk: The artifact includes an undocumented ChatGPT and Suno automation script that can act under logged-in user accounts.

Mitigation: Avoid the dedication npm script unless that account-level automation is intentional and has been reviewed before use.

Risk: The built-in installer can install dependencies into broad Python environments.

Mitigation: Install dependencies in a dedicated virtual environment with pinned versions instead of relying on system-level installation behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jamesfincher/skills/browserbase-sessions)
- [Browserbase Documentation](https://docs.browserbase.com)
- [Browserbase API Quick Reference](references/api-quick-ref.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, JSON command responses, and file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create screenshots, rrweb recording JSON, session logs, downloaded file archives, cookies, and Browserbase context/session state.]

## Skill Version(s):

2.5.0 (source: frontmatter metadata and changelog, released 2026-02-14; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
