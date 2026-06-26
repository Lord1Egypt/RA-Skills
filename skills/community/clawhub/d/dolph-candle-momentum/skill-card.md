## Description: <br>
Trade Polymarket 5-minute crypto fast markets using 1-minute Binance candle body analysis and volume surge detection across BTC, ETH, SOL, XRP, and BNB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richducat](https://clawhub.ai/user/richducat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and traders use this skill to run or adapt a dry-run-first Polymarket fast-market trading workflow based on Binance candle strength and volume signals. It can place live trades when explicitly run with the live trading flag and a Simmer API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live financial trades can be placed quietly when the skill is run with live trading enabled, especially from cron or quiet mode. <br>
Mitigation: Test in dry-run first, keep max_position small, use a dedicated low-privilege Simmer API key where available, and avoid quiet mode until separate monitoring is in place. <br>
Risk: Asset scope, source tags, and monitoring mismatches can make real exposure harder to understand. <br>
Mitigation: Verify configured assets, thresholds, source tags, venue, and open positions before enabling scheduled or live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richducat/dolph-candle-momentum) <br>
- [Binance klines API endpoint](https://api.binance.com/api/v3/klines) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with Python and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; dry-run by default, with live trading only when explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
