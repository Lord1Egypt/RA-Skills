## Description: <br>
Selects A-share stocks with a public-source approximation of a net-profit growth strategy using Eastmoney public market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luyao-inc](https://clawhub.ai/user/luyao-inc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents or analysts use this skill to run a Python-based A-share selector for a profit-growth approximation and receive ranked stock data for review. Outputs are informational and not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The stock-selection results are approximate and may be incorrect or unsuitable for a specific investment decision. <br>
Mitigation: Treat results as informational, review the returned data independently, and do not use the output as investment advice. <br>
Risk: The skill runs a repo-local Python script and fetches public market data over the network. <br>
Mitigation: Review the script before execution and run it only in an environment where Python network access to the public data source is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luyao-inc/china-stock-profitgrowth) <br>
- [Publisher profile](https://clawhub.ai/user/luyao-inc) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [a_share_public_selector.py](artifact/scripts/a_share_public_selector.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON from the selector script, with concise textual guidance from the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The selector returns ok, strategy_type, stocks, and message fields; results are an approximation and not investment advice.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
