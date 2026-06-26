## Description: <br>
Token on-chain analysis via Gate-Info MCP for holder distribution, on-chain activity, and large or unusual transfers, with Smart Money analysis explicitly unavailable in this version. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request token-level on-chain summaries for holders, activity, and transfers. The skill produces informational crypto analysis and routes unsupported requests, such as single-address tracking or Smart Money analysis, to other capabilities or graceful fallback guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat informational on-chain analysis as financial advice or a trading signal. <br>
Mitigation: Keep reports neutral and explicitly state that the output is not investment advice or a prediction of future prices. <br>
Risk: The skill depends on the Gate-Info MCP server and its returned data. <br>
Mitigation: Install only when the Gate-Info MCP server is trusted; if tools are unavailable or fail, degrade gracefully and label missing data. <br>
Risk: Large-transfer or holder data may include wallet addresses and labels that can be misread or over-attributed. <br>
Mitigation: Shorten addresses, avoid doxxing, and describe exchange or entity labels as best-effort. <br>
Risk: Smart Money analysis is not supported in this version. <br>
Mitigation: State the limitation directly and offer holder distribution, activity, and transfer analysis instead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gate-info-tokenonchain-staging) <br>
- [Gate Info Token Onchain Runtime Rules](references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Informational crypto analysis only; sections may be omitted or marked unavailable when tool data is unavailable.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
