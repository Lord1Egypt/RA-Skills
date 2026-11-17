## Description:

订阅摘要(专业版) helps agents manage RSS/feed subscriptions with AI summaries, multi-source aggregation, scheduled delivery, team sharing, personalized recommendations, semantic search, and reading analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and team knowledge-management staff use this skill to collect RSS/feed items, summarize and aggregate them, deliver scheduled digests, share selected items with teams, and generate recommendations from reading history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad exec-enabled instructions can run scheduled feed and delivery commands outside the intended RSS digest workflow.

Mitigation: Review commands before execution, restrict use to RSS/feed-digest tasks, and run only in a controlled agent environment.

Risk: Webhook-based delivery can send digests or feed content to unintended external destinations.

Mitigation: Store webhook URLs in a secret manager or protected environment variables and confirm every destination before enabling scheduled push.

Risk: Personalized recommendations and reading-history profiling may retain or expose user activity patterns.

Mitigation: Avoid private/internal feeds unless approved and disable personalization unless users understand what history will be shared or retained.

## Reference(s):

- [Detailed reference](artifact/references/detail.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/feed-digest-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, configuration, and JSON-style response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include status, result data, execution logs, digest content, recommendations, and configuration snippets.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
