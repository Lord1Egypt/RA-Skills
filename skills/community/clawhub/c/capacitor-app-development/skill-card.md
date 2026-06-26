## Description: <br>
Guides agents through Capacitor app development topics including core concepts, CLI usage, app configuration, platform management, security, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robingenz](https://clawhub.ai/user/robingenz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to get focused, project-aware guidance for existing Capacitor 6, 7, or 8 apps, including configuration, native platform management, live reload, storage, security, testing, CI/CD, and Android or iOS troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proposed commands or diffs can change project files, native project settings, or build outputs. <br>
Mitigation: Review proposed commands and diffs before applying them, especially changes under Android, iOS, and Capacitor configuration files. <br>
Risk: Live reload and cleartext HTTP settings can expose development traffic or accidentally remain in release builds. <br>
Mitigation: Use live reload and cleartext HTTP only on trusted development networks, and remove development server settings before release. <br>
Risk: Authentication tokens, signing secrets, and sensitive client data can be mishandled during app configuration or CI/CD work. <br>
Mitigation: Store secrets in secure storage, environment variables, or CI secret stores rather than embedding them in app code. <br>
Risk: Cache deletion or cleanup commands can remove useful local state when run in the wrong path. <br>
Mitigation: Double-check cleanup command paths and scope before running them. <br>


## Reference(s): <br>
- [App Configuration](references/app-configuration.md) <br>
- [CI/CD for Capacitor Apps](references/ci-cd.md) <br>
- [Capacitor CLI](references/cli.md) <br>
- [Core Concepts](references/core-concepts.md) <br>
- [Cross-Platform Best Practices](references/cross-platform-best-practices.md) <br>
- [Deep Links and Universal Links](references/deep-links.md) <br>
- [Android Edge-to-Edge Support](references/edge-to-edge.md) <br>
- [File Handling Best Practices](references/file-handling.md) <br>
- [iOS Package Managers](references/ios-package-managers.md) <br>
- [Live Reload](references/live-reload.md) <br>
- [Capacitor Platforms](references/platforms.md) <br>
- [Android Safe Area Handling](references/safe-area.md) <br>
- [Security Best Practices](references/security.md) <br>
- [Splash Screens and App Icons](references/splash-screens-and-icons.md) <br>
- [Storage Solutions](references/storage.md) <br>
- [Testing Capacitor Apps](references/testing.md) <br>
- [Android Troubleshooting](references/troubleshooting-android.md) <br>
- [iOS Troubleshooting](references/troubleshooting-ios.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and diff blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses project auto-detection and topic-specific reference files before giving instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
