## Description:

Generates quality-scored technology news digests from RSS, Twitter/X, GitHub, Reddit, and web-search sources with Markdown, Discord, email, and PDF-oriented outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users can use this skill to configure, run, and deliver recurring technology news digests across chat, email, Markdown, and PDF workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use API credentials while fetching broad external sources.

Mitigation: Use least-privilege tokens, restrict configured sources, and review enabled credential fallbacks before installation or scheduling.

Risk: Custom feeds and web sources may cause the agent environment to contact unintended hosts.

Mitigation: Run network-fetching steps in an environment that cannot reach localhost, private networks, or cloud metadata services when untrusted sources are configured.

Risk: Scheduled workflows can send generated reports to email or chat destinations.

Mitigation: Confirm all delivery destinations and cron jobs before enabling recurring delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asterisk622/skills/dinstein-tech-news-digest)
- [digest-prompt.md](references/digest-prompt.md)
- [discord.md](references/templates/discord.md)
- [email.md](references/templates/email.md)
- [pdf.md](references/templates/pdf.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration JSON, generated digest text, HTML email, and PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can archive digest outputs and produce temporary JSON, HTML, and PDF pipeline artifacts.]

## Skill Version(s):

3.15.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
