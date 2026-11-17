## Description:

Capture and prepare App Store / Google Play screenshots for any React Native / Expo app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenshowinnovation](https://clawhub.ai/user/tenshowinnovation)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to capture, resize, document, and optionally upload localized iOS App Store and Google Play screenshots for React Native and Expo apps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented eval-based setup step can be unsafe when run against untrusted Expo configuration.

Mitigation: Run configuration detection only in trusted app repositories, review emitted environment values before use, and avoid the eval setup pattern for untrusted projects.

Risk: Store-upload helpers can replace public App Store Connect or Google Play screenshots when supplied with valid credentials.

Mitigation: Use least-privilege store credentials, keep them out of shared shells and logs, and require explicit human review before upload commands are executed.

Risk: The skill controls simulators, emulators, or attached devices and may alter status-bar/demo-mode state during capture.

Mitigation: Run against dedicated test devices or simulators, confirm the target device serial or UDID, and reset demo/status-bar state after capture.

## Reference(s):

- [App Store Connect API appStoreVersionLocalization](https://developer.apple.com/documentation/appstoreconnectapi/appstoreversionlocalization)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces screenshot file paths, per-device summary markdown, and optional store-upload command guidance.]

## Skill Version(s):

0.2.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
