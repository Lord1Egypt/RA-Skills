## Description:

Use when adding authentication to Expo (React Native) mobile apps, including login, logout, user sessions, protected routes, biometrics, token management, app.json plugin configuration, custom scheme setup, and credential management with the react-native-auth0 SDK and Expo Config Plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Auth0 authentication to Expo React Native applications, configure native callback schemes, set up login and logout flows, manage credentials, and verify development or EAS builds. It is intended for Expo projects that can use a custom development client or native build, not Expo Go or non-Expo React Native projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe token-handling examples could expose access tokens, API tokens, or session-transfer tokens if copied directly.

Mitigation: Redact token values, avoid logging credentials, and review any session-transfer URL handling before using the generated code.

Risk: Mutable install commands and unpinned package or tool versions can change behavior between runs.

Mitigation: Prefer pinned package versions, a reviewed lockfile, and verified installer contents before running bootstrap or dependency installation commands.

Risk: Bootstrap automation can create or update Auth0 tenant resources and modify app.json for the active tenant.

Mitigation: Confirm the active Auth0 tenant, review the displayed change plan, and use manual setup when changes should not be applied automatically.

## Reference(s):

- [Auth0 Expo ClawHub Page](https://clawhub.ai/auth0/skills/auth0-expo)
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills)
- [Setup Guide](references/setup.md)
- [Integration Patterns](references/integration.md)
- [API Reference & Testing](references/api.md)
- [Auth0 Expo Quickstart](https://auth0.com/docs/quickstart/native/react-native-expo/interactive)
- [react-native-auth0 Repository](https://github.com/auth0/react-native-auth0)
- [react-native-auth0 API Documentation](https://auth0.github.io/react-native-auth0/)
- [Auth0 Expo Sample App](https://github.com/auth0-samples/auth0-react-native-sample/tree/master/00-Login-Expo)
- [react-native-auth0 Examples](https://github.com/auth0/react-native-auth0/blob/master/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, JSON, and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run Node.js and Auth0 CLI bootstrap automation, install Expo dependencies, update app.json, and provide manual setup guidance based on project state.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
