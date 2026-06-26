## Description: <br>
Helps developers in China set up and validate a Flutter development environment on new macOS machines, including Android/iOS toolchains, mirror configuration, diagnostics, and acceptance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjneng](https://clawhub.ai/user/wjneng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to bootstrap or repair a Flutter environment for macOS development in China. It guides mirror configuration, Flutter SDK setup, Android/iOS toolchain readiness, troubleshooting, and validation with repeatable shell scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bootstrap script makes lasting local configuration changes, including shell profile edits, Flutter cache setup, and creation of a sample project. <br>
Mitigation: Review the scripts before execution and back up the configured shell profile if rollback may be needed. <br>
Risk: The setup workflow downloads tools and source code through Homebrew, GitHub, Flutter mirrors, and related development tooling. <br>
Mitigation: Run only in an environment where these network downloads are expected and acceptable for Flutter development setup. <br>
Risk: iOS setup steps can require administrator prompts for Xcode configuration. <br>
Mitigation: Use the Android-only path when iOS development is not needed, and review administrator commands before approving them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjneng/flutter-cn-setup) <br>
- [Flutter SDK repository](https://github.com/flutter/flutter.git) <br>
- [Flutter China package mirror](https://pub.flutter-io.cn) <br>
- [Flutter China storage mirror](https://storage.flutter-io.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PASS/WARN/FAIL validation results and next-step remediation commands.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
