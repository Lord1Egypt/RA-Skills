## Description:

An A-share stock trading assistant for China mainland markets that helps with real-time quotes, individual stock analysis, market sentiment, hot sectors, trading strategy suggestions, and price alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent for China A-share market quotes, technical and fundamental analysis, market sentiment summaries, sector highlights, trading strategy suggestions, and price-alert tracking. It is scoped to Shanghai and Shenzhen A-share stocks and excludes Hong Kong, U.S., and other overseas markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can provide trading suggestions that may be mistaken for definitive financial advice.

Mitigation: Treat suggestions as informational, verify market data independently, and require risk warnings with all price or trading recommendations.

Risk: Ambiguous stock requests may be outside the intended market scope.

Mitigation: Confirm that requests concern Shanghai or Shenzhen A-share stocks and ignore Hong Kong, U.S., and other overseas securities.

Risk: Price alerts may be stored locally in a watchlist file when monitoring targets is requested.

Mitigation: Tell users when watchlist entries are created and avoid storing unnecessary personal or sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alvis2-a-stock-trading-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with tables, structured analysis, risk notes, and occasional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should include data source and retrieval time when presenting market data, and price suggestions should include risk warnings.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
