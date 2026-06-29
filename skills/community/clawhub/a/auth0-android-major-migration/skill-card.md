## Description: <br>
Use when upgrading an Android app's Auth0 SDK (com.auth0.android:auth0) to the next major version. Detects the current version, checks prerequisites, and applies only the breaking changes that affect the project's real call sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to migrate existing Android apps from Auth0.Android v3 to v4 while gating each code change on actual SDK usage in the project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real Android project changes during an Auth0 SDK migration. <br>
Mitigation: Run it from a clean git tree, keep the safety backup branch, review the resulting diff, and build the project before accepting the migration. <br>
Risk: Raising minSdk to 26 can drop support for Android 7.1 and older devices. <br>
Mitigation: Confirm the platform-floor change with product owners before applying it, or stay on Auth0.Android v3 if those devices must remain supported. <br>
Risk: Auth storage, logout, DPoP, MFA, and Management API call sites can affect authentication behavior if migrated incorrectly. <br>
Mitigation: Gate changes on actual source usage, preserve SecureCredentialsManager for token storage, run the bundled security checklist, and retest affected authentication flows end to end. <br>


## Reference(s): <br>
- [Auth0 agent skills repository](https://github.com/auth0/agent-skills) <br>
- [Auth0.Android GitHub](https://github.com/auth0/Auth0.Android) <br>
- [Auth0.Android releases](https://github.com/auth0/Auth0.Android/releases) <br>
- [Auth0.Android v4 migration guide](https://github.com/auth0/Auth0.Android/blob/v4_development/V4_MIGRATION_GUIDE.md) <br>
- [Auth0 Android SDK documentation](https://auth0.com/docs/libraries/auth0-android) <br>
- [Migration process reference](references/process.md) <br>
- [Security checklist reference](references/security.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, code edits, and migration summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-specific migration steps and may modify Android source, Gradle configuration, and related Auth0 integration code after gated checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
