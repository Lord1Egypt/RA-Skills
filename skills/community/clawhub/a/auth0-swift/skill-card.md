## Description: <br>
Adds Auth0.swift authentication to native Apple platform apps, including Web Auth, CredentialsManager, and optional biometric protection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add Auth0 authentication to iOS, macOS, tvOS, watchOS, or visionOS apps, configure callback URLs and tenant settings, and integrate login and logout flows with SwiftUI or UIKit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify a local Xcode project and live Auth0 tenant configuration. <br>
Mitigation: Confirm the active tenant and target application, review callback and logout URL changes, and preserve any existing allowed URLs that are still required. <br>
Risk: The skill handles sensitive Auth0 credentials and includes examples that can print access tokens. <br>
Mitigation: Do not expose tokens in logs or copied examples, store credentials with CredentialsManager, and redact sensitive values before sharing output. <br>


## Reference(s): <br>
- [Setup Guide](./references/setup.md) <br>
- [Integration Patterns](./references/integration.md) <br>
- [API Reference & Testing](./references/api.md) <br>
- [Auth0 Agent Skills](https://github.com/auth0/agent-skills) <br>
- [Auth0.swift GitHub](https://github.com/auth0/Auth0.swift) <br>
- [Auth0 iOS/macOS Quickstart](https://auth0.com/docs/quickstart/native/ios-swift) <br>
- [Auth0.swift API Documentation](https://auth0.github.io/Auth0.swift/documentation/auth0/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Swift, shell, JSON, and plist snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local Xcode project changes and Auth0 tenant configuration steps; review proposed changes before applying them.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
