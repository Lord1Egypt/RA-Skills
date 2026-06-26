## Description: <br>
Provides token-level on-chain analysis through Gate-Info for holder distribution, on-chain activity, and large or unusual transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to answer token-level on-chain questions with structured markdown reports covering holders, activity, and large transfers. It is intended for informational analysis only, not trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: On-chain and market outputs may be mistaken for investment advice. <br>
Mitigation: Present results as informational analysis only and avoid buy, sell, or price-prediction guidance. <br>
Risk: Gate-Info MCP tools or individual data scopes may be unavailable or return incomplete data. <br>
Mitigation: Label missing dimensions clearly, degrade gracefully with available data, and avoid fabricating values. <br>
Risk: Single-address tracking, Smart Money analysis, and broader risk checks are outside this skill's supported scope. <br>
Mitigation: Route those requests to the appropriate reviewed skill or state the limitation before continuing with supported holder, activity, and transfer scopes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gate-exchange/gate-info-tokenonchain) <br>
- [Gate runtime rules](references/gate-runtime-rules.md) <br>
- [Info and news common runtime rules](references/info-news-runtime-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Structured markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only Gate-Info MCP results when available and degrades gracefully when a data dimension is unavailable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
