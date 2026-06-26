## Description: <br>
All-in-one Apple developer skill for searching Apple documentation and WWDC sessions, managing App Store Connect workflows, and generating multi-platform Swift/SwiftUI apps through the `appledev` toolkit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abdullah4AI](https://clawhub.ai/user/Abdullah4AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding agents use this skill to retrieve Apple platform guidance, prepare App Store Connect operations, and produce Swift/SwiftUI app code, commands, and project configuration for Apple platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and relies on a third-party Homebrew package for the `appledev` binary. <br>
Mitigation: Install it only when the publisher and package source are trusted and the Apple automation features are needed. <br>
Risk: App Store Connect and LLM credentials may be exposed if raw private keys or debug logs are handled carelessly. <br>
Mitigation: Prefer a private-key file or keychain-backed authentication, avoid debug mode around secrets, and keep credential environment variables scoped to trusted sessions. <br>
Risk: Automation hooks can perform release-sensitive actions such as publishing builds, pushing git tags, or sending notifications. <br>
Mitigation: Review hook configuration before enabling automation and use dry runs or least-privilege credentials where possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Abdullah4AI/apple-developer-toolkit) <br>
- [Publisher Profile](https://clawhub.ai/user/Abdullah4AI) <br>
- [App Store Connect API Keys](https://appstoreconnect.apple.com/access/integrations/api) <br>
- [Apple Developer Documentation](https://developer.apple.com) <br>
- [Swift](https://swift.org) <br>
- [Node.js](https://nodejs.org) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [iOS Development Rules](skills/ios-rules/SKILL.md) <br>
- [SwiftUI Guides](skills/swiftui-guides/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may depend on local Apple tooling, the third-party `appledev` binary, App Store Connect credentials, an LLM API key, and Xcode for app-building workflows.] <br>

## Skill Version(s): <br>
3.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
