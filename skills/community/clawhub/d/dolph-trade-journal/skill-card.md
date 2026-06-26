## Description: <br>
Auto-log trades with context, track outcomes, generate calibration reports to improve trading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richducat](https://clawhub.ai/user/richducat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to sync Simmer prediction-market trade history, inspect recent trades, update market outcomes, export records, and generate win-rate, P&L, and calibration reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive trading records and ships with prefilled data/trades.json trade records. <br>
Mitigation: Review or clear bundled trade data before relying on reports for a personal account, and treat exported CSVs and reasoning/context notes as sensitive records. <br>
Risk: The skill uses SIMMER_API_KEY and can send authenticated requests to SIMMER_API_URL. <br>
Mitigation: Use only a Simmer API key intended for this skill and keep SIMMER_API_URL unset unless the endpoint is deliberately trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/richducat/dolph-trade-journal) <br>
- [Simmer API Base URL](https://api.simmer.markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [CLI text reports, local JSON trade records, and optional CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY for API sync; stores trade data locally under data/trades.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter metadata.version is 1.1.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
