## Description:

Audit an iOS app repo (Swift/Xcode or React Native/Expo) for App Store compliance and release readiness; output a pass/warn/fail report and publish checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to audit native iOS, React Native, or Expo repositories before App Store or TestFlight submission. It helps identify compliance gaps, build-readiness issues, privacy checklist items, and recommended remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit script reads local repository metadata and filenames.

Mitigation: Run it only on repositories you are comfortable auditing locally and review the generated report before sharing it.

Risk: Optional commands can write files or download tooling.

Mitigation: Start with the default read-only command, keep JSON output to a simple repo-local filename such as audit.json, and avoid optional npx Expo commands unless the package source is trusted or pinned.

Risk: Automated checks cannot fully verify App Store metadata, privacy labels, export compliance, rights, payments, and regional obligations.

Mitigation: Use the manual checklist before submission and have the release owner confirm unresolved legal, privacy, and store-listing items.

## Reference(s):

- [Expo-specific checks](artifact/references/expo.md)
- [Manual checklist](artifact/references/manual-checklist.md)
- [Native iOS checks](artifact/references/native-ios.md)
- [Permissions to Info.plist usage strings](artifact/references/permissions-map.md)
- [React Native iOS checks](artifact/references/react-native.md)
- [App Store Readiness Report template](artifact/references/report-template.md)
- [ClawHub skill page](https://clawhub.ai/tristanmanchester/skills/auditing-appstore-readiness)
- [Publisher profile](https://clawhub.ai/user/tristanmanchester)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown readiness report with optional JSON audit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include PASS/WARN/FAIL checks, evidence, remediation steps, and a publish checklist.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
