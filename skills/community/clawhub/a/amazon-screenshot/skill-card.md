## Description:

Captures Amazon ASIN product pages, packages the screenshots into a ZIP file, and emails the archive to an approved recipient address.

This skill is ready for commercial/non-commercial use.

## Publisher:

[328786889](https://clawhub.ai/user/328786889)

### License/Terms of Use:

MIT-0

## Use Case:

Operators use this skill to collect screenshots of Amazon product detail pages for one or more ASINs and receive the results as a ZIP archive by email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release embeds a mail account password.

Mitigation: Revoke the exposed credential and move mail authentication into an approved secret store before use.

Risk: The workflow uses persistent logged-in browser state.

Mitigation: Use an isolated or ephemeral browser profile unless users explicitly approve persistent state.

Risk: The workflow includes anti-detection and CAPTCHA bypass behavior.

Mitigation: Remove this behavior or obtain formal approval before deployment.

Risk: Email recipient and batching behavior may affect data handling expectations.

Mitigation: Clarify allowed recipients and batching rules before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/328786889/skills/amazon-screenshot)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Text guidance with generated PNG screenshots and ZIP archives]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Temporary screenshot and ZIP files are deleted after successful email delivery.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
