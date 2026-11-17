## Description:

Helps developers add Auth0 authentication to native Android applications using the Auth0 Android SDK, including Web Auth, secure credential storage, biometric protection, and MFA patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate Auth0 login, logout, credential storage, biometric protection, MFA handling, and Android project configuration into Kotlin or Java native Android apps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can run an online Auth0 CLI installer and make Auth0 tenant changes beyond local app integration.

Mitigation: Prefer manual Auth0 configuration, or require the agent to show each proposed tenant change and local file diff before execution; verify the installer source before allowing persistent CLI installation.

Risk: Authentication credentials and tokens can be mishandled during Android integration.

Mitigation: Store client ID and domain in Android resources, never include a client secret in the native app, use SecureCredentialsManager for tokens, and avoid logging tokens.

Risk: Incorrect callback, logout URL, or scheme configuration can break redirects or weaken deep-link handling.

Mitigation: Use exact Auth0 callback and logout URLs, prefer HTTPS App Links for production where feasible, and ensure custom schemes are lowercase.

## Reference(s):

- [Setup Guide](references/setup.md)
- [Integration Patterns](references/integration.md)
- [Testing & Reference](references/api.md)
- [Auth0 Agent Skills Repository](https://github.com/auth0/agent-skills)
- [Auth0 Android SDK Documentation](https://auth0.com/docs/libraries/auth0-android)
- [Auth0 Android GitHub Repository](https://github.com/auth0/auth0-android)
- [Android SDK Javadoc](https://auth0.com/docs/references/android)
- [Auth0 Android Quickstart](https://auth0.com/docs/quickstart/native/android)
- [Auth0 Android Sample App](https://github.com/auth0-samples/auth0-android-sample)
- [Android Security Best Practices](https://developer.android.com/privacy-and-security)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Kotlin, Java, Gradle, XML, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file edits, Auth0 tenant configuration changes, and build verification commands.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
