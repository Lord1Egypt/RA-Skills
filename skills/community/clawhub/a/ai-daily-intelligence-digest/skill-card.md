## Description:

AI Daily Intelligence Digest aggregates RSS news sources, summarizes key insights with AI, and publishes a formatted daily digest to a Feishu Wiki knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, product, management, and research teams use this skill to turn daily technology and AI news feeds into a shared Feishu Wiki digest for market monitoring, competitor tracking, and team briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically write AI-generated RSS digests to a Feishu Wiki.

Mitigation: Use tightly scoped Feishu credentials, verify the target Wiki space and permissions, and test a manual run before enabling cron.

Risk: The publishing path relies on dependent skills that are not pinned in the release evidence.

Mitigation: Review or pin rss-aggregator, summarize-pro, and feishu-wiki before operational use.

Risk: AI summaries of news content can be incomplete or inappropriate for publication.

Mitigation: Review digest content and source links before relying on it for team decisions or broad distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/ai-daily-intelligence-digest)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration]

**Output Format:** [Markdown digest with text status output and a Feishu Wiki page URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishes generated summaries to the configured Feishu Wiki destination when credentials and destination settings are provided.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
