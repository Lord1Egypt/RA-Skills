## Description:

Guides agents through general Capacitor app development, including core concepts, CLI usage, app configuration, platform management, security, CI/CD, testing, and Android/iOS troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robingenz](https://clawhub.ai/user/robingenz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when working on existing Capacitor 6, 7, or 8 apps and need actionable guidance for project detection, configuration, platform workflows, security, CI/CD, testing, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable CI/CD and configuration examples can expose deployment credentials or release settings if copied without review.

Mitigation: Use pinned lockfile-controlled CLI execution in CI, avoid passing deployment tokens as command-line arguments when safer authentication is available, and scope and rotate CI tokens.

Risk: Development-only WebView debugging, cleartext traffic, signing passwords, or live-reload settings could be carried into production configuration.

Mitigation: Review app configuration before release, keep signing secrets outside source-controlled config, and remove debug WebView or live-reload settings from production builds.

## Reference(s):

- [App Configuration](references/app-configuration.md)
- [CI/CD for Capacitor Apps](references/ci-cd.md)
- [Capacitor CLI](references/cli.md)
- [Core Concepts](references/core-concepts.md)
- [Cross-Platform Best Practices](references/cross-platform-best-practices.md)
- [Deep Links and Universal Links](references/deep-links.md)
- [Android Edge-to-Edge Support](references/edge-to-edge.md)
- [File Handling Best Practices](references/file-handling.md)
- [iOS Package Managers](references/ios-package-managers.md)
- [Live Reload](references/live-reload.md)
- [Capacitor Platforms](references/platforms.md)
- [Android Safe Area Handling](references/safe-area.md)
- [Security Best Practices](references/security.md)
- [Splash Screens and App Icons](references/splash-screens-and-icons.md)
- [Storage Solutions](references/storage.md)
- [Testing Capacitor Apps](references/testing.md)
- [Android Troubleshooting](references/troubleshooting-android.md)
- [iOS Troubleshooting](references/troubleshooting-ios.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline commands, file paths, and diff blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific guidance may depend on detected Capacitor version, native platform directories, framework configuration, and iOS dependency manager.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
