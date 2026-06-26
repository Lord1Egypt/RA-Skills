## Description: <br>
Analyzes Polymarket CLOB order books to score liquidity gaps, order book imbalance, whale activity, and fake breakouts, then generates trading signals and can fade fake breakouts through Simmer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mibayy](https://clawhub.ai/user/Mibayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan active Polymarket markets for order book microstructure signals and automate dry-run or live mean-reversion trading decisions through a configured Simmer account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real orders through the configured Simmer account. <br>
Mitigation: Keep the skill in dry-run mode until the strategy, limits, and account permissions have been reviewed; use --live only when real trading authority is intended. <br>
Risk: The skill requires a Simmer API key for account access. <br>
Mitigation: Provide SIMMER_API_KEY only through the runtime environment and limit the credential to the minimum permissions needed for the intended deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mibayy/clob-microstructure) <br>
- [Polymarket CLOB book API](https://clob.polymarket.com/book) <br>
- [Polymarket trades API](https://data-api.polymarket.com/trades) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console logs and status text with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to dry-run and only places real orders when run with --live.] <br>

## Skill Version(s): <br>
2.0.6 (source: server evidence release and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
