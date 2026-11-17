## Description:

Generates a premarket A-share briefing before trading days by collecting market news and macro events and structuring investment-reference analysis with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchaoqun](https://clawhub.ai/user/chenchaoqun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill before A-share market open to assemble a concise premarket briefing with key news, market-bias framing, likely leading sectors, watchlist ideas, and source links. The output is informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated market-bias and watchlist content may be incomplete, stale, or mistaken.

Mitigation: Treat the briefing as informational only, verify material claims against primary market sources, and avoid using it as the sole basis for investment decisions.

Risk: The workflow depends on networked market-news searches and a locally installed summarize executable.

Mitigation: Use trusted installation sources, pin or verify dependency versions where possible, and run the skill in an environment appropriate for outbound web access.

Risk: The artifact's trading-day check only excludes weekends and may not account for market holidays.

Mitigation: Confirm the relevant exchange calendar before relying on a generated premarket briefing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenchaoqun/skills/a-stock-premarket-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text and Markdown-style briefing with optional JSON framework]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes search queries, market-bias framing, sector and watchlist guidance, source-link requirements, and an investment-risk disclaimer.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
