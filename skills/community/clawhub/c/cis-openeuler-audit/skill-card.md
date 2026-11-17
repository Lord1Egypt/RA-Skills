## Description:

Audits OpenEuler systems against the corresponding RHEL CIS Benchmark mapping and produces a compliance difference report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x008](https://clawhub.ai/user/0x008)

### License/Terms of Use:

MIT-0

## Use Case:

System administrators and security engineers use this skill to collect OpenEuler host baselines, map them to RHEL CIS Benchmark expectations, and generate Markdown compliance reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The baseline collection workflow uses privileged host-audit commands and can expose sensitive system details.

Mitigation: Run it only on systems you administer, review commands before execution, and store generated baselines and reports in private, access-controlled directories.

Risk: Generated compliance findings may be incomplete or misleading when an OpenEuler check has no direct RHEL CIS equivalent.

Mitigation: Review manual or unavailable mappings before relying on the report for compliance decisions.

## Reference(s):

- [OpenEuler to RHEL Version Matrix](references/version-matrix.md)
- [CIS RHEL Benchmark to OpenEuler Check Mapping](references/cis-rhel-benchmark-mapping.md)
- [ClawHub Skill Page](https://clawhub.ai/0x008/skills/cis-openeuler-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown compliance reports with supporting shell-command and script guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include pass, fail, and manual-review findings derived from collected baseline files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
