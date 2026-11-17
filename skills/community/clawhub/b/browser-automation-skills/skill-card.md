## Description:

Browser Automation Skills lets agents navigate, screenshot, interact with, scrape, debug, test, and record local Google Chrome sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaerye23](https://clawhub.ai/user/huaerye23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill pack to let coding assistants inspect and operate web pages in local Chrome for navigation, visual capture, form interaction, scraping, debugging, QA reports, and session recording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad control over a user's existing logged-in Chrome session.

Mitigation: Use a separate Chrome profile or disposable browser instance, avoid sensitive logged-in tabs, and require explicit confirmation before login, form submission, scraping, recording, or input locking.

Risk: Chrome remote debugging could expose browser control beyond the intended local workflow if misconfigured.

Mitigation: Keep remote debugging bound to localhost and connect only to the intended local Chrome session.

Risk: Input locking can temporarily block normal browser interaction during automation.

Mitigation: Require explicit confirmation before input locking and unlock the browser promptly after interactive sequences.

## Reference(s):

- [Browser Automation Skills README](README.md)
- [Browser Automation API Reference](docs/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/huaerye23/skills/browser-automation-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown reports, structured text or JSON data, shell command snippets, and screenshot or recording file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, responsive captures, debug summaries, scraped data, QA PASS/FAIL reports, and session recording paths.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
