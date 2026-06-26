## Description: <br>
Use when adding authentication to Android applications (Kotlin/Java) with Web Auth, biometric-protected credentials, and MFA - integrates com.auth0.android:auth0 SDK for native Android apps <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Auth0 authentication to native Android applications, including Web Auth login and logout, secure credential storage, biometric-protected credentials, MFA handling, and project configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic setup can install the Auth0 CLI and make persistent Auth0 tenant changes. <br>
Mitigation: Install the Auth0 CLI from a trusted source and verify the tenant, native application, callback URLs, logout URLs, and database connection before allowing automated setup. <br>
Risk: The skill handles Auth0 client identifiers, domains, OAuth tokens, and other authentication-sensitive configuration. <br>
Mitigation: Prefer manual Client ID and Domain entry when possible, keep secrets out of source code and logs, and review all project diffs before accepting changes. <br>
Risk: Incorrect callback URLs, schemes, manifest placeholders, or SDK configuration can break login or weaken the native app authentication flow. <br>
Mitigation: Confirm callback and logout URL settings against the Auth0 application, use SecureCredentialsManager for token storage, and run Android build and device or emulator verification. <br>


## Reference(s): <br>
- [Auth0 Android Skill Page](https://clawhub.ai/auth0/auth0-android) <br>
- [Publisher Profile](https://clawhub.ai/user/auth0) <br>
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills) <br>
- [Auth0 Android SDK Documentation](https://auth0.com/docs/libraries/auth0-android) <br>
- [Auth0 Android GitHub Repository](https://github.com/auth0/auth0-android) <br>
- [Auth0 Android Quickstart](https://auth0.com/docs/quickstart/native/android) <br>
- [Android SDK Javadoc](https://auth0.com/docs/references/android) <br>
- [Sample App](https://github.com/auth0-samples/auth0-android-sample) <br>
- [Setup Guide](references/setup.md) <br>
- [Integration Patterns](references/integration.md) <br>
- [Testing and Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Kotlin, Java, Gradle, XML, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify Android project files, add Gradle dependencies, update Android resources and manifest placeholders, and run build verification.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
