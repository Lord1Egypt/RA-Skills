## Description: <br>
Complete setup guide for running Freqtrade, a cryptocurrency trading bot, legally in the United States with Kraken, Docker configuration, secure API key handling, and dry-run testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and crypto traders use this skill to set up Freqtrade for US-compliant exchange access, secure Kraken API key configuration, and cautious dry-run validation before live trading. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Automated crypto trading can lose money if the bot, strategy, exchange, or account settings are configured incorrectly. <br>
Mitigation: Start in dry-run mode, backtest strategies, use small stake amounts before scaling, and monitor live trading closely. <br>
Risk: Leaked exchange API keys can expose a financial account to unauthorized trading or fund loss. <br>
Mitigation: Disable withdrawal permission, store keys in a local .env file, add .env to .gitignore, never commit API keys, and rotate keys immediately if exposure is suspected. <br>
Risk: Running setup commands from an unexpected repository could install or execute unintended code. <br>
Mitigation: Verify the Freqtrade repository before running Docker commands or cloning source code. <br>
Risk: Using exchanges that block US users or bypassing geo-restrictions can violate terms of service and may freeze funds. <br>
Mitigation: Use a US-compatible exchange such as Kraken and do not use VPNs to bypass exchange restrictions. <br>


## Reference(s): <br>
- [Exchange Comparison for US Traders](references/exchange-comparison.md) <br>
- [Security Checklist for Freqtrade + Kraken](references/security-checklist.md) <br>
- [Freqtrade Documentation](https://www.freqtrade.io) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, JSON, YAML, and text code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Docker setup steps, exchange selection guidance, API key storage guidance, and operational safety checklists.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
