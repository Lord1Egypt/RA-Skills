## Description: <br>
ApiTest fetches tool information from a local localhost:8080/gettool endpoint using an API_TEST_KEY bearer token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yehan5555](https://clawhub.ai/user/yehan5555) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to retrieve JSON tool data from a trusted local server after configuring API_TEST_KEY. It is appropriate only when the user controls localhost:8080 or explicitly intends to send the token to that local service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically send API_TEST_KEY to localhost:8080 when broad localhost or tool-data triggers match. <br>
Mitigation: Install only when you control the localhost:8080 service, and prefer disabling auto invocation or narrowing triggers so the request runs only when explicitly requested. <br>
Risk: The local endpoint response comes from a service outside the skill package. <br>
Mitigation: Verify the local service and review returned tool data before relying on it in downstream agent actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yehan5555/apitest) <br>
- [Publisher profile](https://clawhub.ai/user/yehan5555) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, text] <br>
**Output Format:** [JSON response data from the local endpoint, returned as agent text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API_TEST_KEY and a reachable localhost:8080 service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter name) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
