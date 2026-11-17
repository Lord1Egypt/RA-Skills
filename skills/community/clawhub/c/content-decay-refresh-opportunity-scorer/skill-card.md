## Description:

Analyze content decay patterns and prioritize refresh opportunities by scoring search ranking loss, engagement drop-off, competitor movement, and outdated data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, SEO, and content operations teams use this skill to audit content performance decay, prioritize refresh candidates, and produce specific refresh recommendations for ranking recovery and audience re-engagement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may connect to sensitive marketing analytics, content management, and Slack systems.

Mitigation: Use read-only or least-privilege accounts, restrict WordPress application passwords, and send Slack reports only to controlled channels.

Risk: SERP credential naming may be ambiguous between SERP_API_KEY and SERPAPI_KEY.

Mitigation: Confirm the intended variable name before execution and avoid storing unused credentials in the agent environment.

Risk: Refresh recommendations could affect published content and SEO strategy.

Mitigation: Review recommendations against current analytics, search data, and editorial requirements before applying content changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/content-decay-refresh-opportunity-scorer)
- [ncreighton publisher profile](https://clawhub.ai/user/ncreighton)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with optional CSV exports and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prioritized content decay scores, refresh briefs, batch audit summaries, and integration setup guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
