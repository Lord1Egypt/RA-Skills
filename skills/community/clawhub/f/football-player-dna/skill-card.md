## Description:

Football player DNA similarity search that finds style-matched alternatives at lower market values using AI vector search across 56,000+ players.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeleon](https://clawhub.ai/user/leeleon)

### License/Terms of Use:

MIT-0

## Use Case:

External users, scouts, analysts, and developers use this skill to ask an agent for football players who are statistically similar to a named player, including cheaper or style-matched alternatives. The skill returns ranked similarity results with club, position, market value, savings, and playing-style details when available from the Rising Transfers API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Player names entered in searches are sent to the Rising Transfers API.

Mitigation: Install and use the skill only if you trust Rising Transfers with those football player queries.

Risk: API calls use RT_API_KEY and may consume billed or credit-limited Rising Transfers usage.

Mitigation: Monitor account credits and keep RT_API_KEY scoped and stored in the agent environment rather than in prompts or files.

Risk: Autonomous invocation for football similarity requests may trigger API calls without an explicit manual step.

Mitigation: Disable auto-discovery when manual approval is required before credit-consuming searches.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leeleon/skills/football-player-dna)
- [Rising Transfers API](https://api.risingtransfers.com)
- [DNA Search Endpoint](https://api.risingtransfers.com/api/v1/intelligence/dna-search)
- [Player Lookup Endpoint](https://api.risingtransfers.com/api/v1/intelligence/player)
- [Rising Transfers Privacy Policy](https://risingtransfers.com/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown response with a ranked table and concise follow-up guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RT_API_KEY and network access to api.risingtransfers.com; API calls may consume Rising Transfers credits.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
