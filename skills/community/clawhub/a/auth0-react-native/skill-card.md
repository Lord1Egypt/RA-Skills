## Description: <br>
Use when adding authentication to React Native or Expo mobile apps (iOS/Android) with biometric support - integrates react-native-auth0 SDK with native deep linking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add Auth0 login, logout, deep linking, token access, and mobile authentication patterns to React Native or Expo applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security adjudication is incomplete even though the supplied scanner context is clean. <br>
Mitigation: Inspect the skill artifacts before installation and review generated setup steps before applying them to a mobile app. <br>
Risk: The skill handles OAuth configuration and sensitive Auth0 client settings. <br>
Mitigation: Keep Auth0 domain and client ID values in environment-specific configuration, verify callback and logout URLs, and avoid committing local credential files. <br>


## Reference(s): <br>
- [Setup Guide](references/setup.md) <br>
- [Patterns Guide](references/patterns.md) <br>
- [API Reference](references/api.md) <br>
- [Auth0 Agent Skills](https://github.com/auth0/agent-skills) <br>
- [Auth0 React Native SDK Documentation](https://auth0.com/docs/libraries/react-native-auth0) <br>
- [Auth0 React Native Quickstart](https://auth0.com/docs/quickstart/native/react-native) <br>
- [Auth0 React Native SDK Repository](https://github.com/auth0/react-native-auth0) <br>
- [React Native Deep Linking](https://reactnative.dev/docs/linking) <br>
- [Expo Deep Linking](https://docs.expo.dev/guides/deep-linking/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, XML, JSON, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes mobile app configuration steps, Auth0 SDK usage examples, setup commands, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
