## Description:

Diagnoses Alibaba Cloud WAF OpenAPI parameter errors against the published specification and suggests a corrected call in the same API channel and version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to identify incorrect parameters in WAF 2.0 or 3.0 OpenAPI requests and prepare corrected CLI, SDK, or raw RPC calls. Credential and permission errors, throttling, and service failures are outside its diagnostic scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included installation guidance offers a remote script executed by a shell.

Mitigation: Prefer credential-free diagnosis; avoid the remote installer unless its source is independently trusted.

Risk: Optional live checks and setup instructions may prompt unnecessary credential configuration or plugin changes.

Mitigation: Do not configure long-lived AccessKeys solely for diagnosis; if live reads are needed, use temporary or read-only credentials and review plugin changes before applying them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-waf-openapi-error-diagnosis)
- [Error code map](references/error-code-map.md)
- [WAF API version differences](references/version-differences.md)
- [Parameter specification lookup](references/parameter-spec-lookup.md)
- [Corrected call templates](references/corrected-call-templates.md)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Code, Guidance]

**Output Format:** [Markdown explanation with a corrected CLI, SDK, or RPC call]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies the offending parameter and its constraint; retains the request's API channel and version.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
