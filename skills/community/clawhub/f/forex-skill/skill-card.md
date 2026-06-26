## Description: <br>
Automates Forex market analysis by applying Volume Spread Analysis and Price Volume Analysis to detect smart money activity and volume patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vsharmi74](https://clawhub.ai/user/vsharmi74) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Forex traders and agent developers use this skill to monitor currency pairs and produce VSA/PVA-based market analysis for setup detection and position-management decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The published artifact appears to include a live OpenClaw runtime state with credentials, tokens, browser state, cron jobs, device keys, and paired-device/operator credentials that are not needed for the Forex analysis purpose. <br>
Mitigation: Do not install this version as-is; use a republished minimal package containing only the Forex instructions/code and rotate or revoke any exposed credentials. <br>
Risk: The skill requires sensitive credentials and OAuth/API tokens for OpenClaw, OpenRouter, Telegram, Google, or related integrations. <br>
Mitigation: Provision fresh least-privilege credentials outside the package, keep them in a secrets manager, and review configuration before enabling integrations. <br>


## Reference(s): <br>
- [ClawHub Forex Skill release](https://clawhub.ai/vsharmi74/forex-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Configuration] <br>
**Output Format:** [Markdown or conversational text with configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require external market data, OpenRouter credentials, and OpenClaw configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
