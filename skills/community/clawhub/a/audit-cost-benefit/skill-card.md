## Description:

Runs a five-step cost-benefit audit workflow covering cost collection, benefit measurement, comparative analysis, sensitivity simulation, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rc17777](https://clawhub.ai/user/rc17777)

### License/Terms of Use:

MIT-0

## Use Case:

Audit teams and workflow operators use this skill to evaluate project or activity costs and benefits, compare results, simulate sensitivity scenarios, and produce a cost-benefit analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow declares external engine and helper skill dependencies that are not bundled in the artifact.

Mitigation: Review pipeline_engine.py v3.0, audit_workflow.py, audit_router.py, and referenced helper skills before using the workflow with sensitive audit data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rc17777/skills/audit-cost-benefit)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/workflow.yaml](artifact/workflow.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with bash command examples and workflow-generated audit report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on pipeline_engine.py v3.0, audit_workflow.py, audit_router.py, and referenced helper skills.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
