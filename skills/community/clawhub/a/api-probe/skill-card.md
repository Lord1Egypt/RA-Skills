## Description:

API 探针 is an API testing and validation skill for REST, GraphQL, WebSocket, contract validation, mock service generation, performance testing, security testing, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shylamb-token](https://clawhub.ai/user/shylamb-token)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to plan and generate API test suites from API documentation, endpoint details, cURL commands, Postman collections, or OpenAPI artifacts. It is intended for APIs they own or are explicitly authorized to test, including contract checks, mock services, performance checks, security checks, and test reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated tests may include destructive API operations, security payloads, or load-testing behavior against live services.

Mitigation: Run only against owned or explicitly authorized staging or disposable environments; remove destructive payloads by default; set timeouts and rate limits; avoid real credentials; require separate confirmation for security or load testing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks and structured test or report examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Python pytest, requests, websockets, Flask mock server, JSON report, and command examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
