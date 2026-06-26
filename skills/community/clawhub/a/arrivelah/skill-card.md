## Description: <br>
One-word trigger for next bus arrival to your destination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhayjb](https://clawhub.ai/user/abhayjb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to check the next arrival for a configured Singapore bus stop and service with a short trigger. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured bus stop code is sent to the Arrivelah API and may reveal routine travel patterns. <br>
Mitigation: Use only with a stop code you are comfortable sharing with the API, and keep config.json scoped to non-sensitive defaults. <br>
Risk: The one-word trigger "bus" may run accidentally and disclose configured route details in output. <br>
Mitigation: Use a more explicit trigger or confirm before invoking in contexts where travel habits should remain private. <br>


## Reference(s): <br>
- [Arrivelah2 API](https://arrivelah2.busrouter.sg/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text status lines from a shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; reads config.json; sends the configured bus stop code to the Arrivelah2 API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
