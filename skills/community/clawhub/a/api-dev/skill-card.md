## Description: <br>
Scaffold, test, document, and debug REST and GraphQL APIs, including API endpoints, integration tests, OpenAPI specs, curl testing, mock APIs, and HTTP troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build, test, document, mock, and debug REST or GraphQL APIs from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples can send state-changing HTTP requests, upload files, run local servers, or save API responses to disk. <br>
Mitigation: Use local or test APIs by default, review POST, PUT, PATCH, DELETE, and upload commands before running them, and avoid saving sensitive responses unless needed. <br>
Risk: API tokens and secrets can appear in Authorization headers, verbose curl output, logs, or shell history. <br>
Mitigation: Use scoped test tokens, redact secrets from logs, and avoid pasting production credentials into shell commands. <br>


## Reference(s): <br>
- [API Development on ClawHub](https://clawhub.ai/gitgoodordietrying/api-dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides examples for curl requests, API test scripts, OpenAPI specifications, mock servers, Express scaffolding, and HTTP debugging.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
