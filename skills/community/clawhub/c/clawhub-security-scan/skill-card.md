## Description:

Pre-publish security scan for ClawHub skills - Scans code for patterns that might get flagged as suspicious and gives fixing suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyiyuleyuli-cloud](https://clawhub.ai/user/yuyiyuleyuli-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to scan ClawHub skill folders before release, review suspicious code patterns, and receive practical remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan.py and precheck.py commands perform a paid SkillPay network charge before the scan or checklist runs.

Mitigation: Use the skill only when the per-call billing is acceptable, trust in the SkillPay endpoint is established, and the required user ID and API key are intentionally provided.

Risk: The security evidence reports a scan-root isolation flaw that can allow a crafted folder to make the scanner read files outside the intended scan root.

Mitigation: Avoid scanning untrusted folders until symlink handling is fixed; prefer trusted directories and sandboxed execution with limited filesystem access.

Risk: The server security verdict is suspicious because of the paid network charge and scan-root isolation concern.

Mitigation: Review the skill before installing and pin use to the reviewed release version and source fingerprint.

## Reference(s):

- [ClawHub Security Scan release page](https://clawhub.ai/yuyiyuleyuli-cloud/skills/clawhub-security-scan)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Terminal text with optional JSON scan results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner exits with a non-zero status when high-risk findings are detected.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
