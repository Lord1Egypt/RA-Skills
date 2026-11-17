## Description:

Scaffold, test, document, and debug REST and GraphQL APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to scaffold REST or GraphQL endpoints, test APIs with curl or scripts, generate OpenAPI specs, create mocks, and debug HTTP behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destructive API examples could mutate or delete production data when copied without review.

Mitigation: Use the examples against local or test APIs by default, and verify base URLs, methods, payloads, and resource IDs before running POST, PUT, PATCH, or DELETE requests.

Risk: Credential-bearing request examples could expose tokens through shell history, logs, or shared terminals.

Mitigation: Use disposable or scoped test tokens, avoid pasting production secrets, and clear or disable command history when handling sensitive values.

Risk: Unpinned npm-based CLI execution could run unexpected package versions.

Mitigation: Pin or lock npm CLI package versions before use, especially in CI or shared development environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitgoodordietrying/skills/api-dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command examples, code snippets, API specifications, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples may include curl commands, OpenAPI YAML, Bash or Python test scripts, mock servers, and Node.js Express scaffolding.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
