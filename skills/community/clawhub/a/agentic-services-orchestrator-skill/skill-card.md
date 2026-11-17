## Description:

Coordinate schema-driven workflows across configurable domains using workflow definitions, adapters, active tracks, artifact versions, approval/risk triage, event logs, validation, and recovery actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[completetech](https://clawhub.ai/user/completetech)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to route multi-stage agentic service workflows, preserve project state, coordinate specialist handoffs, validate approvals, and recover from missing or conflicting workflow information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflow or document artifacts may contain incorrect routing, approval, or handoff guidance if source facts are missing or stale.

Mitigation: Review generated documents before sharing and keep approval, blocker, and artifact-version fields current.

Risk: The optional PDF and PNG rendering path uses local Python dependencies and writes user-selected artifact files.

Mitigation: Run rendering in a constrained environment and avoid optional PNG generation unless the image and PDF dependencies are acceptable.

Risk: CompleteTech-branded output may be inappropriate for users who do not want third-party branding in generated PDFs.

Mitigation: Install only if CompleteTech-branded PDF output is acceptable for the intended workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/completetech/skills/agentic-services-orchestrator-skill)
- [Homepage](https://github.com/CompleteTech-LLC/agentic-services-orchestrator-skill)
- [Workflow Definition Schema](references/workflow-definition-schema.yaml)
- [CompleteTech Services Workflow](references/completetech-services-workflow.yaml)
- [Hiring Pipeline Workflow](references/hiring-pipeline-workflow.yaml)
- [CompleteTech Agentic Services Orchestration Architecture](references/orchestration-architecture.md)
- [Full Workflow Generation Variables](references/full-workflow-variables.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with YAML project_state snippets and optional shell commands for PDF or PNG rendering]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write user-selected PDF, PNG, or Markdown artifact paths only when the bundled renderer is explicitly run.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
