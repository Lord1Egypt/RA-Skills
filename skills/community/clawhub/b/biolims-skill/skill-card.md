## Description:

Call Bio-LIMS system APIs to manage orders, sample receiving, sequencing QC, reports, and experiment templates through guided API and shell-command workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biolims](https://clawhub.ai/user/biolims)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and lab operations users use this skill to query and update Bio-LIMS orders, sample receiving records, sequencing QC data, reports, and experiment templates from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive patient, sample, order, QC, and report data when run with real Bio-LIMS credentials.

Mitigation: Install only in a controlled Bio-LIMS environment, require HTTPS, and restrict access through role checks and mandatory authentication.

Risk: Broad command and server interfaces can change orders, sample receiving records, templates, QC data, or workflow state.

Mitigation: Gate destructive or workflow-changing commands behind explicit human confirmation and appropriate Bio-LIMS permissions.

Risk: Diagnostic scripts or shared token caches may expose secrets or active sessions.

Mitigation: Remove or protect diagnostic scripts that print secrets, avoid shared temporary token caches, and bind local services to loopback only.

## Reference(s):

- [Bio-LIMS API Reference](references/api.md)
- [Sample Receive API Reference](references/api-sample-receive.md)
- [Experiment Template API Reference](references/api-experiment-template.md)
- [Experiment Center API Reference](references/experiment-api.md)
- [Sequencing QC API Reference](references/qc-api.md)
- [Report Workflow Reference](references/report-workflow.md)
- [Order Field Mapping Quick Reference](references/field-mapping-quick-reference.md)
- [Sample Receive Field Mapping Quick Reference](references/field-mapping-sample-receive-quick-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Bio-LIMS API payload examples, command invocations, and summarized API responses.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-03-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
