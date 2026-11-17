## Description:

Use when integrating with the energy-app-middle BFF service - covers REST API endpoints, gRPC client setup, authentication headers, multi-tenancy, and downstream service dependencies for the changyuanfeilun energy platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[effort02](https://clawhub.ai/user/effort02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate agents or implementation work with the energy-app-middle BFF service, including REST endpoints, gRPC client setup, authentication headers, tenant scoping, downstream dependencies, DTOs, and environment configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plaintext gRPC configuration example may be inappropriate for environments where traffic can carry tokens, tenant context, or user identifiers.

Mitigation: Confirm the cluster trust boundary before reuse and prefer TLS or mTLS for sensitive service-to-service traffic.

Risk: The guide targets an internal energy-platform integration and may not apply outside environments that intentionally use energy-app-middle and its downstream services.

Mitigation: Install and apply the skill only when this internal energy-platform reference matches the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/effort02/skills/energy-app-middle-integration)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code, Shell commands]

**Output Format:** [Markdown with tables and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only integration guidance; no hidden execution or persistence behavior reported by security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
