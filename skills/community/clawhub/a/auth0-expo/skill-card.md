## Description: <br>
Adds Auth0 authentication to Expo (React Native) mobile apps, including login, logout, session handling, protected routes, biometrics, token management, Expo config plugin setup, and native iOS/Android build guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Auth0 authentication to Expo mobile apps, configure Auth0 tenant and application settings, install react-native-auth0, set callback URLs, and verify native builds with a custom Expo development client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token-handling examples could be copied into a real app without adequate review, including examples that log access tokens or pass session transfer tokens in URL query parameters. <br>
Mitigation: Review token-handling examples before reuse, avoid logging access tokens, and use safer server-side protections for session transfer flows. <br>
Risk: Automatic setup can affect an Auth0 tenant and modify Expo project configuration. <br>
Mitigation: Confirm the active Auth0 tenant, review the script change plan before applying changes, and keep the project under version control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/auth0/auth0-expo) <br>
- [Auth0 agent skills repository](https://github.com/auth0/agent-skills) <br>
- [Setup Guide](references/setup.md) <br>
- [Integration Patterns](references/integration.md) <br>
- [API Reference and Testing](references/api.md) <br>
- [Auth0 Expo Quickstart](https://auth0.com/docs/quickstart/native/react-native-expo/interactive) <br>
- [react-native-auth0 repository](https://github.com/auth0/react-native-auth0) <br>
- [react-native-auth0 API documentation](https://auth0.github.io/react-native-auth0/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide project file updates and Auth0 setup steps; review proposed changes before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
