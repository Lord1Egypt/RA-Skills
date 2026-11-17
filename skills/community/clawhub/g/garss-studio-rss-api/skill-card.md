## Description:

Use when an AI agent needs to read, refresh, summarize, or inspect RSS news from GARSS Studio through its backend API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoolee](https://clawhub.ai/user/zhaoolee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to authenticate with GARSS Studio, read subscribed RSS items, inspect subscriptions, and summarize news while preserving source names and article links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to clone and run an unpinned Docker stack locally.

Mitigation: Review any clone and build step before execution, run only trusted source code, and keep the service bound to loopback.

Risk: The documented local setup uses a default access code and may receive passwords through URLs.

Mitigation: Change the default access code, avoid putting passwords in URLs, and never expose Bearer tokens in final responses.

Risk: Forced refreshes can contact upstream RSS sources and unfamiliar hosts.

Mitigation: Prefer cached reads unless a refresh is explicitly requested, and do not send tokens to non-HTTPS or unfamiliar hosts.

## Reference(s):

- [GARSS Studio Backend API Reference](references/api.md)
- [GARSS project repository](https://github.com/zhaoolee/garss)
- [ClawHub skill page](https://clawhub.ai/zhaoolee/skills/garss-studio-rss-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl commands, Bearer-token handling guidance, endpoint paths, and RSS summary guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
