## Description:

Personal App Store Publishing Assistant helps an agent publish built application packages to a personal app store and provide automatic-update integration guidance for APK, EXE, DMG, and similar package formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justsosog](https://clawhub.ai/user/justsosog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill after building an application package to register or update an app listing, upload a new version, and return download and update-check URLs. They can also use it to generate client-side automatic-update integration guidance for Android, Windows, macOS, and Linux applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create external account state and initiate payment activation without a clear consent checkpoint.

Mitigation: Require explicit user approval before registration, payment-order creation, or payment-status polling.

Risk: The skill uploads build artifacts to appstore.qinghuan.fun and may publish them publicly by default.

Mitigation: Confirm package path, app identifier, version, release notes, and public or private visibility before each upload.

Risk: APPSTORE_TOKEN can authorize uploads and private-app update checks if exposed.

Mitigation: Keep APPSTORE_TOKEN out of logs, command transcripts, client binaries, and generated public documentation; use a backend proxy for private app update checks.

Risk: Copied auto-update client code may download and install packages without independent integrity verification.

Mitigation: Add signature, checksum, or platform-native verification before installing downloaded updates.

Risk: Application or version deletion actions are irreversible according to the artifact behavior.

Mitigation: Require explicit confirmation before app deletion or version deletion and verify the target identifier from a fresh app-details response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justsosog/skills/appstore-publish)
- [Publisher profile](https://clawhub.ai/user/justsosog)
- [Personal app store service endpoint](https://appstore.qinghuan.fun)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash commands, API request examples, JSON examples, and client integration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include app upload results, download URLs, update-check URLs, and platform-specific integration code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
