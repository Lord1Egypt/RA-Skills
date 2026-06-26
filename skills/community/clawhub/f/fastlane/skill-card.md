## Description: <br>
iOS/macOS app automation - builds, signing, TestFlight, App Store via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexissan](https://clawhub.ai/user/alexissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to get Fastlane CLI guidance for iOS and macOS build, signing, TestFlight, App Store submission, testing, screenshots, and metadata workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes Fastlane workflows that can upload builds, change testers, submit apps for review, automatically release apps, or reset signing assets. <br>
Mitigation: Require explicit user confirmation before uploads, tester changes, certificate resets, App Store submission, automatic release, or force actions; prefer listing or validation commands before state-changing commands. <br>
Risk: The skill handles Apple credentials, App Store Connect API keys, and signing repository secrets. <br>
Mitigation: Use least-privileged App Store Connect API keys, store secrets in CI secret managers, avoid placing secrets in chat or shell history, and use read-only signing sync in CI. <br>


## Reference(s): <br>
- [ClawHub Fastlane release](https://clawhub.ai/alexissan/fastlane) <br>
- [App Store Connect API keys](https://appstoreconnect.apple.com/access/api) <br>
- [Apple ID account management](https://appleid.apple.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Fastlane CLI commands, environment variable guidance, and release workflow recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
