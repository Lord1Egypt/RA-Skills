## Description:

Perform structured HTTP/HTTPS requests (GET, POST, PUT, DELETE) with custom headers and JSON body support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to make structured HTTP and HTTPS requests for API testing, health checks, and REST service interactions without relying on curl.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests may include tokens or sensitive payloads.

Mitigation: Use trusted endpoints, prefer test tokens over production credentials, and avoid sending unnecessary sensitive data.

Risk: HTTP URLs can transmit headers and payloads without transport encryption.

Mitigation: Prefer HTTPS endpoints when sending credentials, headers, or private payloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanng-ide/skills/api-tester)
- [Publisher profile](https://clawhub.ai/user/wanng-ide)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured JavaScript object with status, headers, parsed data, raw response body, and error message when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js built-in http and https modules, supports JSON request bodies and responses, and defaults to a 10000 ms timeout.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
