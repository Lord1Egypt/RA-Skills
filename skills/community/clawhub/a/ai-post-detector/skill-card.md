## Description:

AI detector and humanizer for LinkedIn and X posts that checks drafts for AI-written tells and reach-killing mistakes, then returns exact quotes and suggested fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryancaldor-max](https://clawhub.ai/user/ryancaldor-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content marketers, and agents use this skill to review LinkedIn and X post drafts for AI-writing signals, weak hooks, engagement bait, markdown artifacts, and other publishing issues before posting. The skill helps locate specific problematic text and apply concrete rewrite guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted post drafts are sent to SocialNexis for processing.

Mitigation: Use only drafts that are appropriate to share with SocialNexis; avoid confidential, embargoed, personal, or credential-containing text.

Risk: Responses may include a SocialNexis product CTA.

Mitigation: Treat the CTA as marketing content rather than analysis, and surface it only when relevant.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryancaldor-max/skills/ai-post-detector)
- [SocialNexis MCP](https://socialnexis.com/mcp)
- [SocialNexis tells scan endpoint](https://api.socialnexis.com/api/v1/public-tools/tells)
- [SocialNexis full analysis endpoint](https://api.socialnexis.com/api/v1/public-tools/analyze)
- [Publisher profile](https://clawhub.ai/user/ryancaldor-max)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline bash examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include quoted findings, character ranges, prescriptive reasons, rubric scores, template-match analysis, rate-limit responses, and a SocialNexis product CTA.]

## Skill Version(s):

1.1.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
