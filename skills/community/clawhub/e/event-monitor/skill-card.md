## Description:

Predicts CPU spikes using Random Forest regressor, monitors system resources, saves metrics, and generates Excel reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ningtoba](https://clawhub.ai/user/ningtoba)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to collect local CPU and memory process metrics, predict potential CPU spikes, persist alerts, and generate system usage reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records host and running-process telemetry to local files, including monitoring.db and system_report.xlsx, without documented retention or deletion controls.

Mitigation: Install only in environments approved for local process telemetry, review the generated files, and apply local data-retention and deletion procedures.

Risk: The install metadata understates the skill's file-write behavior.

Mitigation: Confirm file-write permissions and storage paths before deployment, and prefer a release that explicitly declares generated database and report files.

Risk: Runtime dependencies are listed without pinned versions.

Mitigation: Review and pin dependencies in the deployment environment before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ningtoba/skills/event-monitor)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Terminal text plus local SQLite and XLSX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes monitoring.db, system_report.xlsx, and CPU alert records when prediction is enabled.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
