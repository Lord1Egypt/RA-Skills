## Description:

Adds Auth0 authentication to Apple-platform Swift apps using Auth0.swift Web Auth, CredentialsManager, Keychain-backed credential storage, callback configuration, and optional biometric protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to add native Auth0 login, logout, token renewal, and credential storage to Apple-platform Swift apps. It also supports Xcode project configuration and Auth0 tenant callback setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flagged unsafe installation guidance.

Mitigation: Avoid curl-to-shell installation paths; use a reviewed package manager or verify installer contents before running them.

Risk: The security review flagged examples that can leak tokens into logs.

Mitigation: Remove logging of access tokens, refresh tokens, ID tokens, passwords, MFA tokens, and authorization headers before use.

Risk: The bootstrap flow can change an Auth0 tenant and local Xcode project files.

Mitigation: Run the bootstrap only against the intended Auth0 tenant and Xcode project, and review the change plan before applying it.

Risk: The security guidance recommends dependency review.

Mitigation: Prefer pinned dependencies or a reviewed lockfile before running the Node bootstrap tooling.

## Reference(s):

- [Setup Guide](references/setup.md)
- [Integration Patterns](references/integration.md)
- [API Reference and Testing](references/api.md)
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills)
- [Auth0.swift GitHub](https://github.com/auth0/Auth0.swift)
- [Auth0 iOS/macOS Quickstart](https://auth0.com/docs/quickstart/native/ios-swift)
- [Auth0.swift API Documentation](https://auth0.github.io/Auth0.swift/documentation/auth0/)
- [Auth0.swift Examples](https://github.com/auth0/Auth0.swift/blob/master/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Swift, XML, Ruby, JavaScript, and shell command snippets; may also create Auth0.plist and entitlements files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update an Xcode project, package manager files, Auth0.plist, entitlements, and Auth0 tenant settings when used with tools.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
