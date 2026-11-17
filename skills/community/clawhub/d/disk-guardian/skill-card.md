## Description:

Run S.M.A.R.T. diagnostics on all drives, parse health indicators, maintain a history log, and flag drives showing early failure patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and system operators use this skill to check macOS and Linux disk health, generate drive health reports, rank drives by failure risk, and review S.M.A.R.T. indicators before taking backup or replacement action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional sudo mode can execute a PATH-selected smartctl binary with elevated privileges.

Mitigation: Use non-sudo mode when possible, and only run --sudo after verifying smartctl resolves to a trusted system binary.

Risk: History logging can store drive identifiers such as model and serial number under the local Disk Guardian data directory.

Mitigation: Use --data-dir to control where history is stored, limit access to that directory, and avoid recording history when device identifiers should not be retained.

## Reference(s):

- [SMART Attributes Reference](references/smart-attributes.md)
- [ClawHub skill page](https://clawhub.ai/newageinvestments25-byte/skills/disk-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports, JSON scan data, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write optional local history records containing drive model and serial identifiers when history logging is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
