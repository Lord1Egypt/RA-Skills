## Description: <br>
Configuration backup, drift detection, and golden config validation across Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers and operations teams use this skill to collect device configurations, compare running and saved state, detect drift against golden baselines, validate compliance patterns, and plan remediation for Cisco, Juniper, and Arista environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some procedures can modify network device state, including configuration archival, rollback, and configuration replacement. <br>
Mitigation: Run write operations only with explicit authorization, appropriate privileges, and a maintenance window; use the skill's read-only assessment steps when change approval is not in place. <br>
Risk: Incorrect drift interpretation or remediation commands could disrupt routing, switching, security, or management-plane behavior. <br>
Mitigation: Review diffs by section, confirm change-ticket context and device vendor syntax, and validate against a current backup or golden baseline before applying remediation. <br>


## Reference(s): <br>
- [Configuration Management CLI Reference](references/cli-reference.md) <br>
- [Drift Detection Methodology](references/drift-detection.md) <br>
- [Config Management ClawHub Release](https://clawhub.ai/vahagn-madatyan/config-management) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, tables, and report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes read-only assessment guidance and explicitly marked write-operation guidance for archival, rollback, and configuration replacement.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
