## Description: <br>
CLI tool to test REST API endpoints with various HTTP methods, headers, and payloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to manually test REST API endpoints, inspect response headers and bodies, validate status codes, and debug API integrations from a command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests to production or unintended endpoints, especially with DELETE, PUT, PATCH, or authenticated calls, can change remote systems or expose sensitive data. <br>
Mitigation: Verify the exact URL, HTTP method, request body, and headers before running the skill, and prefer staging endpoints and test credentials for mutating or authenticated requests. <br>
Risk: Authentication tokens placed directly in command-line headers may be retained in shell history or logs. <br>
Mitigation: Avoid using production tokens directly in shell commands; use short-lived test credentials and clear or protect shell history where needed. <br>
Risk: Saved response output may contain sensitive API data. <br>
Mitigation: Use the optional output file only for non-sensitive responses or store the file in a protected location within the skill directory. <br>
Risk: Disabling SSL verification can hide certificate or interception problems. <br>
Mitigation: Keep SSL verification enabled unless testing a controlled development endpoint with known certificate constraints. <br>


## Reference(s): <br>
- [README](artifact/README.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Derick001/api-endpoint-tester) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files] <br>
**Output Format:** [JSON object printed to stdout, with optional JSON file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes request status, status code, response headers, response body, response time, URL, and HTTP method.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
