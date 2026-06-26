## Description: <br>
API documentation helper that also includes a Python utility for user-supplied GET and POST API requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2367961075](https://clawhub.ai/user/2367961075) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers can use this skill to draft REST API documentation and interface specifications. The included Python utility can also fetch external API data through GET or POST requests when the operator intentionally supplies a target URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is described as an API documentation helper, but its code can make arbitrary external GET and POST requests with user-supplied data. <br>
Mitigation: Review the skill purpose before installation and use it only when a generic API-calling tool is intended. <br>
Risk: User-supplied headers, request bodies, and URLs could expose secrets or send data to unintended destinations. <br>
Mitigation: Do not provide authorization headers, secrets, internal URLs, or sensitive request bodies unless destination limits and explicit operator confirmation are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2367961075/api-test) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, JSON] <br>
**Output Format:** [Markdown documentation guidance and JSON API response objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [API calls return status, URL, method, and response data; text responses are truncated to 1000 characters.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
