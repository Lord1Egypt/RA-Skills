## Description:

Coordinates consulting deliverable projects through a file-based multi-agent workflow for research, framework development, execution, review, iteration, and final delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lorwaleroy](https://clawhub.ai/user/lorwaleroy)

### License/Terms of Use:

MIT-0

## Use Case:

Consulting teams and agent operators use this skill to coordinate Chinese-language, multi-agent consulting projects that move from parallel research into structured review and final delivery. It is most useful when shared files, handoff documents, human approval gates, forbidden-term checks, and version snapshots are needed across several agents or platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks agents to preserve project lessons and research copies outside the active project, which can expose consulting context beyond the intended workspace.

Mitigation: Keep retrospectives and research copies inside the project unless the user explicitly approves export to global OpenClaw memory or Obsidian.

Risk: Project initialization accepts project names and project types that may be unsafe if they come from untrusted sources.

Mitigation: Use trusted project inputs or constrain init-project.sh input handling before accepting untrusted project names or types.

Risk: The skill relies on shared filesystem storage for project coordination, which is not appropriate for highly confidential project data without additional controls.

Mitigation: Confirm the shared project path is approved for the data involved and avoid using this workflow for highly confidential projects unless access controls are established.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lorwaleroy/skills/consulting-agent-pipeline)
- [Agent Card Spec](references/agent-card-spec.md)
- [Forbidden Terms Spec](references/forbidden-terms-spec.md)
- [Handoff Spec](references/handoff-spec.md)
- [State Lifecycle](references/state-lifecycle.md)
- [Version Control Spec](references/version-control-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown templates, YAML configuration, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project folders, handoff documents, validation reports, forbidden-term scan results, and version snapshots through a shared file workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
