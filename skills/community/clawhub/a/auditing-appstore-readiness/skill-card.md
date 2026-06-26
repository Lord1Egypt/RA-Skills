## Description: <br>
Audit an iOS app repo (Swift/Xcode or React Native/Expo) for App Store compliance and release readiness; output a pass/warn/fail report and publish checklist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to audit native iOS, React Native, or Expo repositories before App Store or TestFlight submission. It produces static readiness findings, remediation guidance, and a publish checklist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional build, archive, dependency install, Expo, signing, or patch steps can execute project code or create artifacts. <br>
Mitigation: Run the default read-only audit first, and review any optional mutating or build command before approving it. <br>


## Reference(s): <br>
- [Audit App Store Readiness on ClawHub](https://clawhub.ai/tristanmanchester/auditing-appstore-readiness) <br>
- [Expo-specific checks](references/expo.md) <br>
- [Manual checklist](references/manual-checklist.md) <br>
- [Native iOS checks](references/native-ios.md) <br>
- [Permissions to Info.plist usage strings](references/permissions-map.md) <br>
- [React Native iOS checks](references/react-native.md) <br>
- [App Store Readiness Report template](references/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with optional JSON output and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes PASS/WARN/FAIL findings, evidence, remediation steps, and a publish checklist.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
