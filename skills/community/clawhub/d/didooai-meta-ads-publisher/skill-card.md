## Description:

Executes Meta Ads campaign management tasks such as creating, modifying, pausing or activating, changing budgets, and duplicating campaigns; requires Meta ad account credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elias-didoo](https://clawhub.ai/user/elias-didoo)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, campaign operators, and developers can use this skill to guide Meta Marketing API campaign creation and management tasks, including paused campaign setup, budget changes, activation workflows, duplication, and performance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide spend-affecting Meta ad account changes, including activation and budget updates.

Mitigation: Require explicit user confirmation before activation, budget changes, or any other live account operation that can affect spend.

Risk: Meta access tokens and ad account identifiers grant sensitive advertising account authority.

Mitigation: Use least-privilege, short-lived tokens stored in secret management and do not paste or log tokens in conversation, command output, or URL query strings.

Risk: Campaigns created or duplicated with unsuitable targeting, creative, or budget settings can waste spend or underperform.

Mitigation: Keep new campaigns paused until targeting, creative, pixel or CAPI setup, bid strategy, and budget are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elias-didoo/skills/didooai-meta-ads-publisher)
- [Publisher profile](https://clawhub.ai/user/elias-didoo)
- [Meta Graph API v21.0 endpoint](https://graph.facebook.com/v21.0/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API request examples, tables, and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Meta Marketing API request guidance and campaign-management summaries; spend-affecting actions require explicit review.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
