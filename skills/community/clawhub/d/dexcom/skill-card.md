## Description: <br>
Monitor blood glucose via Dexcom G7/G6 CGM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-clem](https://clawhub.ai/user/chris-clem) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers with Dexcom G6 or G7 Share access use this skill to retrieve current glucose readings as either a formatted report or raw JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dexcom credentials and glucose readings are sensitive health data and may be exposed through local config, agent context, logs, or chat history. <br>
Mitigation: Use a secure secret store or tightly permissioned local config, avoid committing credentials, limit where output is shared, and rotate the Dexcom password if exposure is suspected. <br>


## Reference(s): <br>
- [Dexcom](https://www.dexcom.com) <br>
- [Dexcom CGM on ClawHub](https://clawhub.ai/chris-clem/dexcom) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Formatted terminal report or raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, Dexcom Share credentials, and DEXCOM_USER and DEXCOM_PASSWORD environment variables.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
