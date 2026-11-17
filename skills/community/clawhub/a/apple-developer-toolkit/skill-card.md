## Description:

Apple Developer Toolkit helps agents search Apple developer documentation and WWDC content, manage App Store Connect workflows, and generate Swift/SwiftUI Apple-platform apps through the appledev command-line tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdullah4ai](https://clawhub.ai/user/abdullah4ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to add Apple platform guidance to agents, look up Apple APIs and WWDC material, automate App Store Connect tasks, and scaffold Swift/SwiftUI apps. App Store Connect and app-builder workflows require appropriate credentials and local Apple tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned external binary from a mutable Homebrew tap.

Mitigation: Install only when the publisher is trusted, and prefer a pinned, checksum-verified release before using it in sensitive workflows.

Risk: App Store Connect commands can affect production builds, TestFlight, submissions, signing, subscriptions, analytics, and release workflows.

Mitigation: Use least-privilege App Store Connect API keys, confirm destructive or publishing actions, and review automation configuration before execution.

Risk: The skill can use App Store Connect private keys and LLM API keys.

Mitigation: Avoid raw private keys in environment variables where possible, keep credential scope narrow, rotate keys regularly, and review third-party integrations and LLM data handling.

Risk: Generated Swift/SwiftUI app code and automated fixes may be incorrect or incomplete.

Mitigation: Review generated code, run local builds and tests, and inspect App Review, privacy, entitlement, and accessibility requirements before release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abdullah4ai/skills/apple-developer-toolkit)
- [Publisher Profile](https://clawhub.ai/user/abdullah4ai)
- [App Store Connect API Keys](https://appstoreconnect.apple.com/access/integrations/api)
- [Apple Developer Documentation](https://developer.apple.com)
- [Agent Skills Format](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated source or configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke appledev, Node.js, Xcode, App Store Connect credentials, and an LLM API key depending on the selected workflow.]

## Skill Version(s):

3.5.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
