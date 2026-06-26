## Description: <br>
API debugging skill for quickly testing APIs, generating request code, and analyzing responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, frontend and backend engineers, and QA testers use this skill to test REST and GraphQL APIs, generate curl, Python, Node.js, and browser fetch request examples, and analyze JSON responses during debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Template API commands may modify or delete data when adapted to real PUT, PATCH, DELETE, upload, or authenticated endpoints. <br>
Mitigation: Confirm target URLs and methods before execution, prefer test environments, and review generated commands before running them. <br>
Risk: Authentication tokens, API keys, credentials, or response payloads may be exposed through shell history, query strings, logs, or screenshots. <br>
Mitigation: Use least-privilege credentials, avoid putting secrets in URLs or shell history, and redact sensitive request and response data before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/api-debugger-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for command examples; jq is referenced for optional JSON formatting examples.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
