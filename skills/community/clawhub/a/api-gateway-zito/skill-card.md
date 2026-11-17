## Description:

Api Gateway connects an agent to REST or GraphQL APIs with simple configuration for authentication, rate limiting, caching, retries, and API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miguelguerra200022-sudo](https://clawhub.ai/user/miguelguerra200022-sudo)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to configure named external APIs and let an agent call REST or GraphQL endpoints through centralized authentication, caching, rate limiting, retry, logging, and testing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad arbitrary outbound API calls, including credentialed requests to third-party services.

Mitigation: Restrict configured APIs to approved services, use least-privilege tokens, and avoid sending secrets or sensitive user content in direct requests.

Risk: API credentials and sensitive payloads may appear in gateway configuration, request parameters, or logs.

Mitigation: Prefer header-based authentication where supported, store secrets outside prompts and checked-in files, and require log redaction for credentials and sensitive payloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miguelguerra200022-sudo/skills/api-gateway-zito)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe configured outbound API calls, authentication settings, cache behavior, rate limits, retries, logs, stats, and connection tests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
