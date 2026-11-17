## Description:

Read-only Fomo App API for public market-research data through ReplyNodes prepaid credits with one long-lived Bearer fetcher key; per-operation credit cost follows the authoritative catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[replynodes-ai](https://clawhub.ai/user/replynodes-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query public Fomo App market-research data, including leaderboards, token lists, user activity, trades, theses, search results, alerts, and notifications through the ReplyNodes gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a long-lived ReplyNodes fetcher key and requests may consume prepaid credits.

Mitigation: Store the key only in the agent secret store, avoid prompts, logs, URLs, and returned data, and use billing caps if a paid plan is selected.

Risk: The API is limited to public read-only Fomo data and may return unavailable upstream data.

Mitigation: Do not claim private, unauthenticated, write, guaranteed-availability, or unsupported pricing capabilities; preserve unavailable responses without fabricating fields.

## Reference(s):

- [Operations catalog](artifact/references/operations.json)
- [Skill page](https://clawhub.ai/replynodes-ai/skills/fomo-app-data-api)
- [ReplyNodes authentication](https://app.replynodes.com/auth)
- [ReplyNodes developer keys](https://app.replynodes.com/developers)
- [ReplyNodes API gateway](https://api.replynodes.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration, Markdown, JSON, Guidance]

**Output Format:** [Markdown guidance with HTTP examples and JSON API responses from the gateway]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only HTTP GET requests; requires a ReplyNodes Bearer fetcher key stored as REPLYNODES_API_KEY.]

## Skill Version(s):

2.0.1 (source: frontmatter, manifest, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
