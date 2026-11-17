## Description:

Audit DVC (Data Version Control) pipelines for reproducibility, storage efficiency, and tracking correctness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and ML engineers use this skill to inspect DVC projects for pipeline reproducibility, data tracking correctness, remote storage readiness, parameter hygiene, and operational issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit output can include remediation commands that modify DVC remotes, data synchronization state, cache contents, or dependency pins.

Mitigation: Review proposed commands and configuration changes before execution, especially commands that push or pull data, clean caches, rewrite remotes, or change pinned dependencies.

Risk: The skill inspects local DVC project files and may surface sensitive paths, remote names, or configuration details in its report.

Mitigation: Run it only in projects intended for review and check generated reports before sharing them outside the project team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/dvc-pipeline-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with findings, scores, dependency notes, and remediation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DVC command suggestions that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
