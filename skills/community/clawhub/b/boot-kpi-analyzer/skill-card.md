## Description:

Analyzes SS4 in-vehicle system boot and shutdown KPI timing data to help diagnose slow startup, slow shutdown, service failures, and qcrosvm performance issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lichm1007](https://clawhub.ai/user/lichm1007)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect SS4 vehicle boot and shutdown KPI log directories, compare sessions, and identify slow services, qcrosvm timing issues, reboot duration problems, and failed units.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can read outside the intended KPI folders when untrusted session names or arbitrary paths are passed to --dir.

Mitigation: Install only in the intended internal KPI environment and restrict --dir inputs to expected KPI session names.

Risk: Generated output may expose VINs, build IDs, boot counters, error messages, and raw log summaries.

Mitigation: Treat analysis output as sensitive and share it only within authorized vehicle KPI debugging workflows.

Risk: The skill documents curl access to a private KPI web API.

Mitigation: Use the API only from authorized internal environments and avoid copying private API responses into external systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lichm1007/skills/boot-kpi-analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash command examples and terminal text analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include vehicle identifiers, build IDs, boot counters, error messages, and log-derived timing summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
