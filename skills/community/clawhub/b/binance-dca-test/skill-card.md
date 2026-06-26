## Description: <br>
Helps agents plan Binance dollar-cost averaging strategies, check balances and trade history, and prepare manual or scheduled spot buy commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fpsjago](https://clawhub.ai/user/fpsjago) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to plan recurring Binance spot purchases, inspect balances and trading history, and set up testnet or live DCA workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent toward live crypto purchases and recurring trading. <br>
Mitigation: Use Binance testnet first, require manual confirmation before real orders or schedules, and set explicit spending limits. <br>
Risk: The referenced dca.sh implementation is missing from the submitted artifact. <br>
Mitigation: Inspect the actual command implementation before live use and deploy only after confirming order, balance, and error handling behavior. <br>
Risk: Binance credentials could authorize unintended trading if over-permissioned. <br>
Mitigation: Use a restricted spot-trading API key, disable withdrawals, and keep credentials in environment variables only. <br>


## Reference(s): <br>
- [Binance API Endpoint](https://api.binance.com) <br>
- [Binance Spot Testnet](https://testnet.binance.vision) <br>
- [ClawHub Skill Page](https://clawhub.ai/fpsjago/binance-dca-test) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading workflow guidance, Binance command examples, setup notes, projections, and safety checks.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
