## Description: <br>
Helps agents plan Binance spot dollar-cost averaging strategies, check balances and prices, place market or limit buy orders, and review trade history using environment-provided Binance API credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fpsjago](https://clawhub.ai/user/fpsjago) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and crypto operators use this skill to plan recurring Binance spot purchases, run manual or scheduled buy commands, and inspect balances or trade history while keeping credentials in environment variables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Binance spot buy orders when valid API credentials are configured. <br>
Mitigation: Use Binance testnet first, keep order sizes small, and confirm each command before allowing live execution. <br>
Risk: API credentials could enable unintended account actions if over-permissioned or exposed. <br>
Mitigation: Use a dedicated Binance API key with withdrawals disabled, restrict by IP where possible, and avoid storing secrets in shared shell startup files. <br>
Risk: Scheduled DCA jobs may continue buying after a user's budget, strategy, or market assumptions change. <br>
Mitigation: Regularly review or disable cron and OpenClaw jobs, and keep execution alerts enabled for each scheduled run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fpsjago/binance-dca) <br>
- [Binance](https://www.binance.com) <br>
- [Binance Spot Testnet](https://testnet.binance.vision) <br>
- [Binance announcements](https://www.binance.com/en/support/announcement) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON snippets, plus shell command output from scripts/dca.sh.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead to Binance API calls when generated shell commands are executed with configured credentials.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact changelog, released 2026-02-05) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
