## Description:

Fetch and summarize Medium Daily Digest emails from Gmail, extract article URLs, generate Freedium links, and provide article summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omnimahui](https://clawhub.ai/user/omnimahui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve the latest Medium Daily Digest from Gmail, extract article links, and prepare readable article summaries with Freedium mirror links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gmail app-password credentials may be exposed or reused if placed in a broad agent environment.

Mitigation: Use a dedicated, easily revocable Gmail app password only in a trusted environment, keep EMAIL_PASSWORD scoped away from unrelated tools, and revoke the credential after use.

Risk: The configurable IMAP server parameter could direct credentials to an unintended mail server.

Mitigation: Remove the parameter or strictly allowlist imap.gmail.com before normal use.

Risk: Freedium mirror links route article access through a third-party mirror service.

Mitigation: Review whether Freedium use is acceptable for the user's policy and compliance requirements before relying on mirrored content.

## Reference(s):

- [Daily Medium on ClawHub](https://clawhub.ai/omnimahui/skills/daily-medium)
- [Publisher profile: omnimahui](https://clawhub.ai/user/omnimahui)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [JSON-like article data and human-readable summaries or Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns digest date, digest title, article titles, authors, original Medium URLs, and Freedium mirror URLs; defaults to a maximum of 15 articles.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
