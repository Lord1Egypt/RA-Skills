## Description:

Convert curl commands to Postman Collection v2.1 importable JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuliwanzi](https://clawhub.ai/user/liuliwanzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn pasted curl commands into formatted Postman Collection v2.1 JSON for direct import into Postman.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied curl commands may contain live Authorization headers, Basic Auth credentials, cookies, API keys, or sensitive body fields that are preserved in the generated Postman collection.

Mitigation: Redact secrets and sensitive request body values before using, storing, or sharing generated collections.

## Reference(s):

- [Postman Collection v2.1 schema](https://schema.getpostman.com/json/collection/v2.1.0/collection.json)
- [ClawHub skill page](https://clawhub.ai/liuliwanzi/skills/curl-to-postman)
- [ClawHub publisher profile](https://clawhub.ai/user/liuliwanzi)

## Skill Output:

**Output Type(s):** [JSON, Code, Guidance]

**Output Format:** [Postman Collection v2.1 JSON with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves headers, request method, URL query parameters, request body, redirect and SSL options, and supported authentication fields from the pasted curl command.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
