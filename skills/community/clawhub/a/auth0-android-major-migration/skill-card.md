## Description:

Upgrades an Android app's Auth0 SDK (com.auth0.android:auth0) from v3 to the next major version by detecting current usage, checking prerequisites, and applying only relevant breaking changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to migrate Android apps with existing Auth0.Android v3 integrations to v4 while checking build prerequisites, updating affected API call sites, and preserving authentication and credential-storage behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A major Auth0.Android migration can raise platform and toolchain requirements, including dropping support for older Android devices.

Mitigation: Review and confirm minSdk, Java, Gradle, AGP, Kotlin, and dependency-version changes before accepting the migration.

Risk: The target version may resolve to a pre-release or to a version the project owner did not intend.

Mitigation: Validate any supplied target version against published Auth0.Android releases, or explicitly review the auto-resolved v4 release before proceeding.

Risk: Credential and logout behavior can change during migration, including minTtl renewal timing and clearCredentials clearing all storage.

Mitigation: Preserve SecureCredentialsManager usage, review logout and credential-renewal assumptions, and set explicit minTtl or separate storage only when the app requires the old behavior.

Risk: Management API functionality removed from the mobile SDK can tempt insecure on-device token handling.

Mitigation: Move Management API operations to a secure backend using minimum required scopes, and never embed Management API tokens or client secrets in the Android app.

## Reference(s):

- [Auth0 Agent Skills Repository](https://github.com/auth0/agent-skills)
- [Auth0.Android GitHub](https://github.com/auth0/Auth0.Android)
- [Auth0.Android Releases](https://github.com/auth0/Auth0.Android/releases)
- [V4 Migration Guide](https://github.com/auth0/Auth0.Android/blob/v4_development/V4_MIGRATION_GUIDE.md)
- [Auth0 Android SDK Documentation](https://auth0.com/docs/libraries/auth0-android)
- [Migration Process](references/process.md)
- [Security Checklist](references/security.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project code and configuration changes, migration summaries, and follow-up review items; uses gh for release and source checks when available.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
