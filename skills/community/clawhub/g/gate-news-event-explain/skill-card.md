## Description: <br>
Explains crypto price moves by tracing recent events, market snapshots, news, and on-chain context into an event attribution report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to ask why a cryptocurrency pumped, dumped, crashed, or surged, and receive a source-attributed explanation of likely event drivers. It is intended for explanatory market context, not trading recommendations or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Event attribution can sound more certain than the available market, news, and on-chain evidence supports. <br>
Mitigation: State causal links as likely or uncertain, cite available sources, and disclose when no single clear triggering event is identified. <br>
Risk: Forward-looking impact-duration language may be mistaken for price prediction or investment advice. <br>
Mitigation: Frame forward outlook sections as watchpoints and uncertainty notes, and keep buy, sell, and hold recommendations out of the response. <br>
Risk: The workflow depends on Gate-News and Gate-Info MCP availability for read-only market, event, and on-chain data. <br>
Mitigation: Degrade gracefully when a required data source is unavailable, reduce confidence, and tell the user which evidence could not be checked. <br>


## Reference(s): <br>
- [Gate News EventExplain MCP Specification](references/mcp.md) <br>
- [gate-news-eventexplain Scenarios & Prompt Examples](references/scenarios.md) <br>
- [ClawHub skill page](https://clawhub.ai/gate-exchange/gate-news-event-explain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown attribution report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes volatility summary, triggering-event assessment, impact chain, on-chain verification when available, ripple effects, forward outlook, and uncertainty notes.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
