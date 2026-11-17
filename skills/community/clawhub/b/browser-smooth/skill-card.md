## Description:

Smooth Browser helps AI agents use Smooth CLI to navigate websites, authenticate, scrape data, fill forms, test web apps, and automate browser workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoniocirclemind](https://clawhub.ai/user/antoniocirclemind)

### License/Terms of Use:


## Use Case:

Developers and external agent users use this skill to run browser-based tasks through Smooth CLI, including web navigation, form filling, authentication workflows, data extraction, web testing, file-assisted browser sessions, and structured scraping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give agents broad browser automation authority, including access to web accounts, persistent profiles, file uploads, and live authenticated sessions.

Mitigation: Use anonymous or read-only profiles when possible, restrict sessions with allowed URL patterns, and require explicit confirmation before logins, account changes, purchases, public posting, file uploads, or reusing saved authenticated profiles.

Risk: Persistent profiles can retain cookies and browser state across sessions.

Mitigation: Use descriptive profile IDs, limit profile reuse to deliberate workflows, close sessions when finished, and delete profiles that are no longer needed.

## Reference(s):

- [Smooth app and API key portal](https://app.smooth.sh)
- [ClawHub skill page](https://clawhub.ai/antoniocirclemind/skills/browser-smooth)
- [Publisher profile](https://clawhub.ai/user/antoniocirclemind)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce structured JSON outputs when Smooth CLI commands use response schemas or JSON flags.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
