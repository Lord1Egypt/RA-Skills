## Description:

Provides configuration backup, drift detection, and golden config validation for Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS network environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network operations engineers use this skill to audit device configuration state, compare running and startup configurations, validate golden baselines, and plan remediation for drift or compliance findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive device configurations may be exported over plaintext TFTP or FTP.

Mitigation: Prefer SCP or local encrypted storage for configuration archives, and use TFTP or FTP only on isolated management networks with explicit risk acceptance.

Risk: Rollback, config replace, save, and archival procedures can modify production network device state.

Mitigation: Require operator authorization, maintenance-window confirmation, and human review before executing any write operation.

Risk: Drift remediation guidance may be incorrect if the baseline, device role, or change authorization context is wrong.

Mitigation: Validate golden baselines, check change tickets, and re-run read-only collection and comparison steps after remediation.

## Reference(s):

- [Configuration Management CLI Reference](references/cli-reference.md)
- [Drift Detection Methodology](references/drift-detection.md)
- [Config Management Skill Page](https://clawhub.ai/vahagn-madatyan/skills/config-management)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command blocks and structured report guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read-only assessment steps and human-reviewed write-operation guidance for archival, rollback, config replace, and save operations.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
