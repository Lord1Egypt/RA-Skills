## Description:

An OpenClaw skill for tracking keyword trends and generating structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesong-hue](https://clawhub.ai/user/yesong-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Content strategists, market researchers, and developers use this skill to monitor configured keywords, collect search results, and produce structured trend reports for planning or competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured search keywords are sent to Tavily for external search.

Mitigation: Review keyword sensitivity and Tavily terms before use; avoid submitting confidential or regulated terms unless approved.

Risk: Webhook delivery can send generated report contents to the configured endpoint.

Mitigation: Use only trusted HTTPS webhook URLs and verify the destination before enabling WEBHOOK_URL.

Risk: The packaged artifact does not include the referenced node index.js runtime file.

Mitigation: Confirm the executable implementation is available and reviewed before relying on the documented node-based workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yesong-hue/skills/content-keyword-tracker)
- [ClawHub Metadata Homepage](https://clawhub.ai/yesong-Hue/content-keyword-tracker)
- [Tavily API](https://tavily.com)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown reports with keyword sections, result tables, summary statistics, and optional webhook delivery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are generated from keywords configured one per line and require a Tavily API key.]

## Skill Version(s):

1.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
