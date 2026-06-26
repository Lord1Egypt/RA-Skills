## Description: <br>
Trades a market when your estimated probability diverges from the live market price, with dry-run by default, context checks, reasoning tags, and optional live execution through AION. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssj124](https://clawhub.ai/user/ssj124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill as an execution wrapper for a market where they already have a probability estimate. It compares that estimate with live AION market context, holds on warnings or low edge, and defaults to dry-run unless live execution is explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can connect an agent to AION trading credentials and financial-account actions. <br>
Mitigation: Keep the skill in dry-run unless deliberately placing live trades, and require explicit confirmation before credential registration, spending approvals, live orders, bulk order cancellation, or redemption. <br>
Risk: The scheduled run can repeatedly evaluate and act on a configured market if live mode and credentials are enabled. <br>
Mitigation: Review or disable the scheduled run and apply scoped risk limits before enabling live automated execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ssj124/aionmarket-sdk-divergence-trader) <br>
- [Polymarket CLOB endpoint](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text operator summaries with optional JSON API responses and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to dry-run; live trades require --live and AION credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
