## Description:

Adds authentication to React Native and Expo mobile apps with biometric support by integrating the react-native-auth0 SDK and native deep linking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Auth0 authentication to React Native or Expo mobile applications, including SDK installation, native callback configuration, provider setup, login/logout flows, API token access, biometric patterns, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing npm or npx packages can introduce dependency supply-chain risk.

Mitigation: Review package sources, pin package versions where practical, commit lockfiles, and install in a normal project environment without unnecessary secrets exposed.

Risk: Auth0 domain, client ID, callback URLs, and token scopes are sensitive application authentication configuration.

Mitigation: Keep environment files out of public repositories, review callback and logout URLs before release, and limit requested scopes to the app's needs.

Risk: Incorrect mobile deep-link configuration can break login/logout return flows or cause callback mismatches.

Mitigation: Validate iOS URL schemes, Android intent filters, Expo schemes, and Auth0 dashboard callback URLs on both target platforms.

Risk: Client-side token handling can lead to over-trusting mobile app state.

Mitigation: Use secure platform storage, rely on PKCE-based flows, refresh credentials deliberately, and validate access tokens on backend APIs.

## Reference(s):

- [Setup Guide](references/setup.md)
- [Patterns Guide](references/patterns.md)
- [API Reference](references/api.md)
- [Auth0 React Native SDK Documentation](https://auth0.com/docs/libraries/react-native-auth0)
- [Auth0 React Native Quickstart](https://auth0.com/docs/quickstart/native/react-native)
- [React Native Auth0 SDK GitHub](https://github.com/auth0/react-native-auth0)
- [Auth0 Agent Skills Repository](https://github.com/auth0/agent-skills)
- [React Native Deep Linking](https://reactnative.dev/docs/linking)
- [Expo Deep Linking](https://docs.expo.dev/guides/deep-linking/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, TypeScript examples, XML snippets, JSON configuration, and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project-specific setup guidance for React Native CLI and Expo mobile authentication flows.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
