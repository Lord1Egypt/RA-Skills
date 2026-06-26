## Description: <br>
Finds markets where Simmer's AI consensus diverges from market prices, checks fees and safeguards, and can trade the mispriced side using Kelly sizing on qualifying zero-fee markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richducat](https://clawhub.ai/user/richducat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to scan Simmer and prediction-market divergence, review candidate opportunities, and optionally execute constrained trades when live mode is explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can spend real money without per-trade confirmation. <br>
Mitigation: Start in dry-run mode, review --live use carefully, and set small max bet and daily budget limits before enabling live execution. <br>
Risk: The skill requires a Simmer API key for market data and trading actions. <br>
Mitigation: Use a revocable API key and rotate or revoke it if the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/richducat/dolph-ai-divergence) <br>
- [Simmer API endpoint](https://api.simmer.markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [Plain text scanner output, JSON reports, and CLI configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run scanning is the default; live trading requires the --live flag or a simulated venue.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
