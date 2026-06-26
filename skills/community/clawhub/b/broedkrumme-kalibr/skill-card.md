## Description: <br>
Captures agent outcomes and LLM telemetry for continuous self-improvement and optional intelligent model routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Broedkrummen](https://clawhub.ai/user/Broedkrummen) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and agent operators use this skill to send run outcomes and LLM usage telemetry to Kalibr, inspect status, and optionally let Kalibr choose model routing for agent runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telemetry and outcome capture are enabled by default and may send operational agent metadata to the configured Kalibr service. <br>
Mitigation: Install only when the publisher and service are trusted, configure the endpoint deliberately, and disable telemetry or outcome capture when the deployment should not send this data. <br>
Risk: When routing is enabled, the remote service can influence model selection and tool-call parameters. <br>
Mitigation: Keep enableRouting off unless remote routing is explicitly desired, and avoid using it around high-impact tools until injected parameters are constrained, visible, and approved. <br>
Risk: The security review asks the publisher to document data handling and declare or pin the Kalibr SDK dependency. <br>
Mitigation: Review data-handling documentation and dependency declarations before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Broedkrummen/broedkrumme-kalibr) <br>
- [Publisher profile](https://clawhub.ai/user/Broedkrummen) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, API calls, guidance] <br>
**Output Format:** [Plain text status output and plugin configuration for telemetry, outcome reporting, and optional routing calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Kalibr API key; telemetry and outcome capture are enabled by default, while routing is disabled by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
