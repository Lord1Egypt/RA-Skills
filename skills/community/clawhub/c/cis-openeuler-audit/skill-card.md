## Description: <br>
Audits OpenEuler systems against corresponding RHEL CIS Benchmark mappings and generates compliance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x008](https://clawhub.ai/user/0x008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers and system administrators use this skill to collect OpenEuler baseline data, compare it with RHEL CIS Benchmark mappings, and produce Markdown compliance reports for authorized hosts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated baselines and reports may include sensitive local security configuration, including sudo policy, user and account details, SSH settings, firewall state, audit rules, and limited shadow-derived indicators. <br>
Mitigation: Run the skill only on OpenEuler systems the operator is authorized to audit, store generated baseline and report directories with restrictive permissions, and limit sharing to approved reviewers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0x008/cis-openeuler-audit) <br>
- [OpenEuler to RHEL version matrix](references/version-matrix.md) <br>
- [CIS RHEL Benchmark to OpenEuler mapping](references/cis-rhel-benchmark-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown audit reports with shell command guidance and baseline file summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped baseline directories and reports; the documented workflow is audit-only and does not modify target system configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
