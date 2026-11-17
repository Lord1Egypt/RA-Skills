## Description:

iOS/macOS app automation - builds, signing, TestFlight, App Store via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexissan](https://clawhub.ai/user/alexissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to plan and generate Fastlane CLI commands for iOS and macOS builds, code signing, TestFlight distribution, App Store submission, testing, screenshots, and related App Store Connect workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged installation commands can alter the host Ruby environment or require elevated permissions.

Mitigation: Prefer `brew install fastlane` or a pinned Bundler setup; require explicit user approval before using `sudo gem install fastlane -NV`.

Risk: Release commands can submit an app for review, enable automatic release, or skip preview checks.

Mitigation: Require explicit confirmation before commands using `--submit_for_review`, `--automatic_release`, or `--force`; review generated metadata and upload targets first.

Risk: Signing commands can create, renew, or remove certificates and provisioning profiles.

Mitigation: Use `--readonly` for CI and require explicit approval before `match nuke`, `--force`, or other commands that change signing assets.

## Reference(s):

- [ClawHub Fastlane skill page](https://clawhub.ai/alexissan/skills/fastlane)
- [App Store Connect API keys](https://appstoreconnect.apple.com/access/api)
- [Apple ID app-specific passwords](https://appleid.apple.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that install Fastlane, authenticate to App Store Connect, upload builds, submit apps, or modify signing assets; commands should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
