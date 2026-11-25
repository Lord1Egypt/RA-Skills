## Description:

Guides developers in integrating Didit verification, transaction monitoring, and end-user authentication in web and mobile apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build Didit SDK integrations for web and mobile applications, including backend session creation, device transaction submission, event monitoring, and supported authentication flows. It provides code examples and setup guidance while keeping the API key on the backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial, with 50% coverage and medium confidence, so it may not account for all behavior.

Mitigation: Review the skill's code and its requested host permissions before enabling it.

Risk: Integration examples handle an API key and send user-related data to Didit.

Mitigation: Keep the API key on the backend and review which data each integration sends to Didit.

Risk: The security guidance flags unpinned Expo references, which may change over time.

Mitigation: Check current Expo guidance and package versions when applying the examples.

## Reference(s):

- [Didit SDK integration overview](https://docs.didit.me/integration/sdks)
- [Didit Web SDK documentation](https://docs.didit.me/integration/web-sdks/javascript-sdk)
- [Didit native SDK overview](https://docs.didit.me/integration/native-sdks/overview)
- [Didit transaction SDK submission](https://docs.didit.me/transaction-monitoring/sdk-transaction-submission)
- [Didit event SDK submission](https://docs.didit.me/transaction-monitoring/sdk-event-submission)
- [ClawHub skill release](https://clawhub.ai/rosasalberto/skills/didit-sdk-integration)

## Skill Output:

**Output Type(s):** [Code, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with code examples and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Platform-specific integration examples for web, iOS, Android, React Native, Flutter, and backend services.]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
