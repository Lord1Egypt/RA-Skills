## Description:

Guides agents through setting up and using Capawesome Cloud for Capacitor apps, including native builds, live updates, app store publishing, and CI/CD integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robingenz](https://clawhub.ai/user/robingenz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and mobile release engineers use this skill to configure Capawesome Cloud for Capacitor apps, automate iOS and Android builds, ship live updates, and publish builds to app stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable command-line installs can execute newer CLI behavior than the reviewed skill examples assume.

Mitigation: Review commands before execution and prefer pinned, lockfile-managed CLI versions.

Risk: Release credentials, signing keys, app store credentials, and Capawesome tokens can authorize sensitive build and publishing operations.

Mitigation: Use CI secret stores or interactive prompts, keep signing keys outside the repository with restrictive permissions, and grant only the minimum required permissions.

## Reference(s):

- [Capawesome Cloud](https://console.cloud.capawesome.io)
- [Trapeze](https://trapeze.dev/)
- [App Store Connect CLI](https://github.com/rudrankriyam/App-Store-Connect-CLI)
- [Native Builds](references/native-builds.md)
- [Live Updates](references/live-updates.md)
- [App Store Publishing](references/app-store-publishing.md)
- [CLI Commands Reference](references/cli-commands.md)
- [App Configuration](references/build-configuration.md)
- [Build Types](references/build-types.md)
- [Build Stacks](references/build-stacks.md)
- [Build Troubleshooting](references/build-troubleshooting.md)
- [Environments](references/environments.md)
- [Android Signing Certificates](references/certificates-android.md)
- [iOS Signing Certificates](references/certificates-ios.md)
- [Apple App Store Credentials](references/apple-app-store-credentials.md)
- [Google Play Store Credentials](references/google-play-store-credentials.md)
- [Live Update Plugin API Reference](references/live-update-plugin-api.md)
- [Plugin Configuration](references/live-update-configuration.md)
- [Live Update CI/CD Integrations](references/live-update-ci-cd-integrations.md)
- [Live Update Advanced Topics](references/live-update-advanced-topics.md)
- [Update Strategies](references/update-strategies.md)
- [Live Update FAQ](references/live-update-faq.md)
- [Advanced Guides](references/build-guides.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that authenticate services, configure CI/CD, manage signing credentials, and publish mobile app releases.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
