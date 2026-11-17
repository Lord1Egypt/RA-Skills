## Description:

Guides developers through integrating the Basic service with Maven dependencies, gRPC clients, REST APIs, tenant context, authentication, and configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[effort02](https://clawhub.ai/user/effort02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as an integration reference for Basic service APIs, SDKs, and configuration across i18n, project, tenant, dictionary, storage, and authentication capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide includes plaintext gRPC and authenticated service-call examples that could normalize insecure transport in production.

Mitigation: Add TLS or enforced mTLS before production use and validate authentication behavior in the target environment.

Risk: Authorization and tenant headers appear in example requests and could be exposed through logs or overly broad credentials.

Mitigation: Redact Authorization, X-TENANT, and X-UID values from logs and use least-privilege, short-lived credentials.

Risk: The Maven examples use SNAPSHOT dependencies that may change unexpectedly.

Mitigation: Replace SNAPSHOT dependencies with pinned releases from a trusted repository.

Risk: The documented APIs include delete, reset, import, rollback, and batch storage operations that can alter or remove business data.

Mitigation: Require confirmation, backup, and approval gates before destructive or bulk operations.

## Reference(s):

- [Basic Integration Guide on ClawHub](https://clawhub.ai/effort02/skills/basic-integration-guide)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guide with XML, YAML, Java, Protobuf, bash, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; examples require environment-specific validation before production use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
