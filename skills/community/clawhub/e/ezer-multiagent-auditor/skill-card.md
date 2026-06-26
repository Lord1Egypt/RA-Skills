## Description: <br>
Runs Ezer financial audit tasks by security code, reporting period, year, and language, then returns the final structured audit result from the configured Ezer API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mx-222](https://clawhub.ai/user/mx-222) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and audit operators use this skill to create an Ezer audit task, poll for completion, and retrieve structured financial audit output for a specified code, period, year, and language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network calls to the configured Ezer API and may include an optional bearer token in requests. <br>
Mitigation: Install only when the configured API endpoint is trusted, restrict EZER_API_BASE_URL to an allowed host, and provide EZER_BEARER_TOKEN only through the runtime environment. <br>
Risk: The manifest documents the required base URL but the script also supports optional bearer-token authentication. <br>
Mitigation: Review deployment configuration so operators understand both required and optional environment variables before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mx-222/ezer-multiagent-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/mx-222) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON] <br>
**Output Format:** [JSON payload printed to stdout, with JSON error payloads on stderr for failures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EZER_API_BASE_URL and python3; supports optional EZER_BEARER_TOKEN for API authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
