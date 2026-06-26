## Description: <br>
Monitors premium RSS feeds for breaking news, matches stories to Polymarket markets, and generates trade signals when estimated price impact exceeds the configured threshold. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richducat](https://clawhub.ai/user/richducat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run an automated news-monitoring workflow that identifies potentially market-moving events and evaluates related Polymarket trading opportunities. It defaults to dry-run and requires explicit live mode before placing trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real trades using the Simmer API key. <br>
Mitigation: Keep dry-run enabled until the code, trade size, venue, thresholds, and external account limits have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richducat/dolph-news-events) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Command-line logs and trade API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode is the default; live trading requires the --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata lists 2.0.1/2.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
