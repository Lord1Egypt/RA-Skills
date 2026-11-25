## Description:

Generates sourced daily industry briefings and prepares them for delivery through configured channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Business intelligence teams and practitioners use the skill to create recurring, source-backed industry briefs, review them, and deliver them to configured channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports an email certificate-verification weakness.

Mitigation: Use a mail server with certificate verification enabled, or avoid sending sensitive reports by email.

Risk: Publishing reports through GitHub Pages makes them publicly accessible.

Mitigation: Review report contents for confidential or unpublished information before deployment and keep the business review gate in place.

Risk: The skill requests file and network access, and the security scan was partial.

Mitigation: Grant only the file and network access needed for the selected workflow, and review the skill before use.

## Reference(s):

- [Industry Daily Brief on ClawHub](https://clawhub.ai/haiyangchenbj/skills/data-ai-daily-brief)

## Skill Output:

**Output Type(s):** [Markdown, HTML, Text, Files]

**Output Format:** [Structured daily brief with source links, summaries, impact judgments, and channel-ready summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Industry focus, language, and delivery channels are configurable.]

## Skill Version(s):

5.0.8 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
