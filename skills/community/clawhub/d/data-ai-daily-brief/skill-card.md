## Description:

Turn any industry into a daily intelligence briefing: an AI agent searches, filters, writes, and delivers structured briefs to nine channels with machine-checked formatting and a business review gate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Industry analysts and teams use the skill to create recurring, source-linked daily briefs from current industry information. It structures the report, applies a business review gate, and prepares it for delivery to configured channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags SMTP certificate verification and gives the release a suspicious verdict.

Mitigation: Review the email transport configuration and confirm certificate verification is enabled for the SMTP server before using email delivery.

Risk: Reports deployed through GitHub Pages may be publicly accessible.

Mitigation: Check each report for confidential or sensitive material before enabling or running public Pages deployment.

## Reference(s):

- [Industry Daily Brief on ClawHub](https://clawhub.ai/haiyangchenbj/skills/data-ai-daily-brief)
- [CodeBuddy](https://www.codebuddy.ai/)

## Skill Output:

**Output Type(s):** [Markdown, HTML, Configuration instructions]

**Output Format:** [Structured daily industry briefs with source links, summaries, impact judgments, and channel-ready concise summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A target date and industry profile guide each brief; output can be customized for delivery channels.]

## Skill Version(s):

5.0.7 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
