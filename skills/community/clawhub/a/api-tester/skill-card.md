## Description: <br>
Perform structured HTTP/HTTPS requests (GET, POST, PUT, DELETE) with custom headers and JSON body support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to test REST services, run health checks, and interact with HTTP APIs programmatically without relying on curl. It supports custom headers, JSON request bodies, timeout handling, and structured response data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send arbitrary outbound HTTP or HTTPS requests with headers and payloads supplied by the agent. <br>
Mitigation: Use it only with trusted endpoints and avoid sending real tokens or sensitive data unless the endpoint and authorization context are approved. <br>
Risk: Direct execution includes hardcoded network smoke checks against google.com and example.com. <br>
Mitigation: Review or disable the direct-execution smoke test path in environments where unapproved outbound network calls are restricted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanng-ide/api-tester) <br>


## Skill Output: <br>
**Output Type(s):** [API responses, JSON, Text] <br>
**Output Format:** [JSON-compatible object with status, headers, parsed data, raw body, and error message fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Parses JSON responses when the response Content-Type is application/json; otherwise returns raw response text.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
