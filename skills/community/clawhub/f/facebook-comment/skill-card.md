## Description:

Analyzes Facebook post comments, summarizes positive, negative, demand, and competitor sentiment, and generates interactive HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Brand teams, creators, product teams, and market researchers use this skill to review Facebook post comments, identify audience feedback and competitor mentions, and share comment analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted comments may escape the documented shell command or inject content into generated HTML.

Mitigation: Pass comment data without shell interpolation, escape or sanitize HTML fields, and review generated reports before opening or sharing.

Risk: The complete submitted post URL is sent to RedFox, and comment data is saved locally before report approval.

Mitigation: Avoid URLs containing private tokens and review the local report and its output location before sharing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/redfox-data/skills/facebook-comment)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML reports]

**Output Format:** [Markdown comment tables and sentiment summaries, plus interactive HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can cover one page or combine multiple pages; AI-generated sentiment analysis is for reference.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
