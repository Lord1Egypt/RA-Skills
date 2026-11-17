## Description:

Crypto Social Intel helps AI agents answer crypto social trend, sentiment, KOL-proxy, mention-surge, and Fear & Greed Index requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackxun520](https://clawhub.ai/user/jackxun520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect and summarize crypto social intelligence, including trending tokens, token sentiment, social-dominance anomaly signals, mention spikes, and market Fear & Greed context. Outputs should be treated as market reference material rather than real-time trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto social and sentiment outputs can be mistaken for trading advice or real-time market certainty.

Mitigation: Present outputs as reference material, preserve the skill's disclaimers, and recommend corroborating signals before making decisions.

Risk: Santiment-backed social data may lag by about 35 days on the free tier.

Mitigation: Call out the Santiment delay whenever those tools are used and avoid framing those results as real-time signals.

Risk: Queries are sent to Antalpha's disclosed MCP service.

Mitigation: Install only when sending crypto sentiment and trend queries to that service is acceptable for the deployment.

Risk: KOL signals in v1.0 use social dominance as a proxy rather than real Twitter KOL data.

Mitigation: Label KOL outputs as proxy signals and avoid representing them as direct influencer activity.

## Reference(s):

- [Crypto Social Intel ClawHub page](https://clawhub.ai/jackxun520/skills/crypto-social-intel)
- [Antalpha MCP endpoint](https://mcp-skills.ai.antalpha.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown or structured text summaries with MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include delayed Santiment-backed social metrics, real-time Fear & Greed data, signal labels, and bilingual explanatory notes.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
