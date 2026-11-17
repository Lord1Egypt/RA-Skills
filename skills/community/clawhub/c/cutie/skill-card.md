## Description:

Cutie helps agents access crypto KOL signals, market news, KOL profiles, strategy profiles, forums, chat rooms, live rooms, and account actions through the Cutie API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fansen](https://clawhub.ai/user/fansen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to browse Cutie crypto KOL content, account data, signals, and market updates, and to evaluate, compare, or learn from KOL trading strategies. The skill is useful when an agent needs guided REST API or MCP calls for Cutie workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform account-changing actions such as follow, unfollow, subscription, posting, and risk-preference changes.

Mitigation: Require the agent to show the exact action and receive explicit confirmation before making these changes.

Risk: The skill requires a Cutie API key and can access account data through the Cutie service.

Mitigation: Install only when you trust Cutie with the API key and want an agent to access the account.

Risk: KOL strategy data may be retained by an agent beyond the immediate task.

Mitigation: Do not save strategy data in long-term memory unless the user explicitly consents and has a way to delete it.

Risk: Trading signals and KOL strategy outputs can be mistaken for investment advice.

Mitigation: Treat all signal data as informational only and require independent review before trading decisions.

## Reference(s):

- [Cutie ClawHub skill page](https://clawhub.ai/fansen/skills/cutie)
- [Cutie API homepage](https://server.tokenbeep.com)
- [Cutie REST API base](https://server.tokenbeep.com/v1/app)
- [Cutie MCP endpoint](https://server.tokenbeep.com/mcp/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CUTIE_API_KEY, curl, and jq; REST and MCP calls return JSON payloads.]

## Skill Version(s):

2.0.0 (source: server release evidence and CLAWHUB.md version history, released 2026-04-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
