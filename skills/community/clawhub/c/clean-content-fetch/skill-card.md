## Description:

Clean Content Fetch extracts readable main content from modern web pages, blogs, news, announcements, WeChat articles, and other noisy pages, returning cleaned Markdown or JSON for downstream use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jllyzzd](https://clawhub.ai/user/jllyzzd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch public web-page article bodies, reduce page noise, and convert the result into Markdown or JSON for summarization, archiving, analysis, or batch collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs unpinned third-party packages and may execute web-fetching dependencies with broad behavior.

Mitigation: Install it in an isolated project environment, pin and review dependencies before use, and avoid system-wide package installation.

Risk: The artifact references implementation scripts that are not included in the bundle.

Mitigation: Verify any separately obtained script before running it and confirm it matches the documented public-page fetching behavior.

Risk: Using the skill on logged-in, private, credentialed, or restricted pages could expose non-public content.

Mitigation: Use it only for public pages and do not run it with logged-in sessions, credentials, private pages, or restricted content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jllyzzd/skills/clean-content-fetch)
- [Usage](references/usage.md)
- [Selector Strategy](references/selectors.md)
- [Release Notes 1.0.1](references/release-1.0.1.md)
- [Site Overrides Example](references/site-overrides.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown by default, with optional JSON output for structured or batch use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is truncated by the requested max_chars value; selector overrides can customize extraction per site.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
