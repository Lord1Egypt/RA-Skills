## Description:

Automates energy service repository risk inspections, optionally compiles the target, and reports structured findings with commit metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bhlkkk](https://clawhub.ai/user/bhlkkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect an energy service repository branch or commit, optionally compile it, and report structured risk findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is rated suspicious, and scan coverage is incomplete: no components were fully inspected and one analyzer was degraded.

Mitigation: Review the complete skill source before installation and treat this scan as incomplete.

Risk: The security assessment reports code-execution and redirected-write risks in the scan workflow.

Mitigation: Run it only in an environment you control, and inspect the requested operations and resulting file changes.

Risk: The security assessment reports that scan reports may be sent to an untrusted endpoint.

Mitigation: Verify the configured reporting endpoint and avoid sending sensitive repository data to an untrusted destination.

## Reference(s):

- [ClawHub release](https://clawhub.ai/bhlkkk/skills/energy-service-risk-inspect)
- [Runtime configuration source (prepare/env)](https://git.xiaojukeji.com/amonline_arch/risk-inspect-online/raw/master/prepare/env)

## Skill Output:

**Output Type(s):** [Risk analysis, JSON, HTML report, Status summary]

**Output Format:** [Structured JSON findings with a concise text summary; an HTML report may be included when produced.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports findings and severity counts, run and build status, commit ID, and an optional HTML report.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
