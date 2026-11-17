## Description:

Complete browser automation with agent-browser CLI. Supports navigation, forms, screenshots, data extraction, and parallel sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weaglewang](https://clawhub.ai/user/weaglewang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to operate a local Chrome or Chromium browser through agent-browser for navigation, form interaction, screenshots, data extraction, authentication-state reuse, and parallel browser sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad control over a local browser, including navigation, form submission, screenshots, file upload, cookie handling, and page script execution.

Mitigation: Use it only in trusted browser contexts, review commands before execution, avoid sensitive accounts unless necessary, and restrict use to sites and sessions approved for automation.

Risk: Saved browser state can preserve authenticated sessions and other sensitive data.

Mitigation: Treat state files as secrets, keep them out of repositories and transcripts, delete them after use, and clear cookies or saved state after sensitive workflows.

Risk: The documented global npm install can resolve an unpinned latest agent-browser package.

Mitigation: Prefer a pinned, locally reviewed dependency version or install source before enabling the skill in production workflows.

Risk: Browser automation transcripts and command history can expose bearer tokens, credentials, or private page data.

Mitigation: Use environment variables for secrets, avoid embedding real tokens in commands, and redact sensitive output before sharing logs.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/weaglewang/skills/claw-browser-automation-skill)
- [Publisher profile](https://clawhub.ai/user/weaglewang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser automation command sequences, environment configuration, screenshots, PDFs, JSON extraction patterns, and troubleshooting guidance.]

## Skill Version(s):

2.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
