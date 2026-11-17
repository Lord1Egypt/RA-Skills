## Description:

CreBee | 热点与内容选题研究 helps agents query CreBee trend feeds, daily collection records, and account-personalized creator-center insights across supported Chinese content platforms for topic planning and case research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n8spxd](https://clawhub.ai/user/n8spxd)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketing teams, and agents assisting them use this skill to research current hot topics, daily captured trend records, benchmark content, creator-center insights, and actionable topic ideas through the local CreBee desktop client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query account-personalized creator insights through the local CreBee client, which may expose account-specific business context in agent outputs.

Mitigation: Use only the CreBee desktop login flow, avoid manually providing tokens, and keep outputs clear about which selected account the insight data belongs to.

Risk: Trend and creator-center results can be mistaken for universal market conclusions when they are source-specific or account-personalized.

Mitigation: Treat results as evidence from the queried source or account, label account-scoped insights, and review suggested topics before making publishing or business decisions.

Risk: A workflow could move beyond read-only insight gathering if an agent follows adjacent operational suggestions without user review.

Mitigation: Review any proposed action that goes beyond trend research, and use the appropriate CreBee skill for publishing, analytics, or downloads.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/n8spxd/skills/crebee-insights)
- [CreBee Website](https://www.crebee.cn)
- [CreBee Download Page](https://www.crebee.cn/#/download)
- [Creative Insights Reference](references/creative-insights.md)
- [Troubleshooting Reference](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Concise text or Markdown with optional inline shell commands and structured-result interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may summarize trend data, account-scoped creator insights, troubleshooting guidance, and suggested content topics.]

## Skill Version(s):

1.9.13 (source: server release evidence and skill compatibility marker)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
