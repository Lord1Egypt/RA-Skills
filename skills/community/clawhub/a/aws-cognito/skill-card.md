## Description:

This skill helps agents build, configure, debug, and manage AWS Cognito user pools, identity pools, app clients, Lambda triggers, federation, and AWS service integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, implement, troubleshoot, and harden AWS Cognito authentication and authorization workflows across application and AWS service integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated authentication code may include unsafe example patterns for real systems.

Mitigation: Review all generated auth code before production use and apply the security guidance from the server evidence.

Risk: Machine-to-machine token helper examples may be copied without constraining trusted domains.

Mitigation: Hardcode or allowlist trusted Cognito domains before using M2M token helper patterns in production.

Risk: Passwordless OTP examples may rely on weak randomness or insufficient abuse controls.

Mitigation: Use cryptographic randomness and enforce rate limits for OTP generation and verification.

Risk: Pre-token examples may introduce administrative claims from an untrusted source.

Mitigation: Derive roles, groups, and privileged claims only from a trusted authorization source.

## Reference(s):

- [Cognito Setup Guide](references/setup-guide.md)
- [Cognito Infrastructure as Code Patterns](references/iac-patterns.md)
- [Cognito Authentication Flows](references/auth-flows.md)
- [Cognito Lambda Triggers](references/lambda-triggers.md)
- [Cognito Security Best Practices](references/security.md)
- [Cognito Troubleshooting Guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill that guides generated Cognito code, infrastructure, and configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
