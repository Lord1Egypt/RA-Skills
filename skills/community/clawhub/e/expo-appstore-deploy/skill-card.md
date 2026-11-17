## Description:

Deploy Expo/React Native apps to Apple App Store and Google Play Store using EAS Build + Submit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jini92](https://clawhub.ai/user/jini92)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to build Expo and React Native production binaries with EAS Build, submit iOS and Android builds to app stores, manage signing prerequisites, and troubleshoot common release failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents production build and app-store submission commands, including auto-submit, that can affect live release channels.

Mitigation: Require human release approval before submission, avoid auto-submit unless explicitly approved, and run submissions with only the required credentials available.

Risk: The documented commands invoke eas-cli through npx without pinning the CLI version.

Mitigation: Pin eas-cli through the project lockfile or release tooling before using the deployment commands.

## Reference(s):

- [Expo App Store Deploy on ClawHub](https://clawhub.ai/jini92/skills/expo-appstore-deploy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes EAS build and submit commands, prerequisite checks, common failure fixes, and app-store review guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
