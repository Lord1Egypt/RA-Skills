## Description: <br>
Conversational interface for AIDA to query building status, control devices, optimize smart-building objectives, and run diagnostics through authenticated REST APIs. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[AK-Khalis](https://clawhub.ai/user/AK-Khalis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Building operators, facilities teams, and developers can use this skill to demonstrate conversational access to AIDA building status, device control, optimization, and preventive diagnostics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated control and optimization intents may affect real smart-building operations. <br>
Mitigation: Use a trusted AIDA endpoint, provide only a least-privilege bearer token, and require human confirmation before control or optimization actions. <br>
Risk: The skill can return fallback success-style messages when an API request fails. <br>
Mitigation: Verify API responses and operational state before treating status, control, optimization, or diagnostics replies as successful. <br>
Risk: The artifact does not document safety boundaries for building control workflows. <br>
Mitigation: Review the deployment environment and define approval, monitoring, and rollback procedures before connecting to live building systems. <br>


## Reference(s): <br>
- [AIDA ClawHub skill page](https://clawhub.ai/AK-Khalis/aida) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, guidance, configuration] <br>
**Output Format:** [Text replies from an agent, with authenticated REST API requests to the configured AIDA endpoint.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIDA_API_URL and AIDA_API_KEY environment variables; API responses should be verified before acting on control or optimization results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
