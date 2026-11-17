## Description:

Helps developers set up a Flutter development environment on new macOS devices in China-region network conditions, including Android and optional iOS tooling, mirror configuration, diagnostics, and validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjneng](https://clawhub.ai/user/wjneng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, repair, and validate Flutter tooling on macOS for China-region development workflows. It guides Android setup, optional iOS setup, mirror configuration, flutter doctor remediation, and smoke-test validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bootstrap flow can persist changes to the user's shell profile and PATH.

Mitigation: Review the script before execution, inspect the target shell profile after running it, and confirm the added Flutter mirror and PATH lines are expected.

Risk: The setup guidance includes mutable network installer and package-manager steps.

Mitigation: Run only in a trusted environment, verify installer sources before use, and treat Homebrew, Flutter, Xcode, and CocoaPods installation steps as explicit user-approved actions.

Risk: Environment variables such as FLUTTER_DIR, SHELL_PROFILE, MIRROR_PUB_URL, and MIRROR_STORAGE_URL alter installation behavior.

Mitigation: Avoid passing untrusted environment variables and confirm any custom paths or mirror URLs before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjneng/skills/flutter-cn-setup)
- [Publisher profile](https://clawhub.ai/user/wjneng)
- [Flutter SDK repository](https://github.com/flutter/flutter.git)
- [Flutter China pub mirror](https://pub.flutter-io.cn)
- [Flutter China storage mirror](https://storage.flutter-io.cn)
- [Troubleshooting guide](troubleshooting.md)
- [Usage examples](examples.md)
- [Self-test checklist](self-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and validation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local shell-profile changes, Flutter mirror environment variables, macOS toolchain setup steps, and validation commands.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
