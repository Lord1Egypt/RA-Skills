## Description:

Family OS helps an AI agent initialize and maintain a private local household workspace for plans, projects, decisions, reminders, records, and long-term family workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[living-hi](https://clawhub.ai/user/living-hi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their AI agents use this skill to create and operate a local household knowledge base for family logistics, finance, health, education, legal/admin records, decisions, and recurring reviews. It is intended for private workspace management, not for storing household data inside the skill package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a persistent local household database containing highly sensitive family, financial, health, legal, and administrative information.

Mitigation: Use a private workspace path, keep the data local unless the user explicitly requests otherwise, and restrict filesystem permissions so other local users cannot read the workspace.

Risk: Auto-update behavior may record sensitive details before the user has reviewed them if configured too broadly.

Mitigation: Keep aREDACTED-SECRET enabled and review updates involving identity documents, medical details, account credentials, exact addresses, legal disputes, large asset details, or child-identifying information.

Risk: Initialization with archive-existing can move legacy material inside the selected workspace.

Mitigation: Confirm the intended workspace path before initialization and inspect the generated archive before migrating summaries back into active files.

## Reference(s):

- [Privacy Model](references/privacy-model.md)
- [Workspace Structure](references/workspace-structure.md)
- [Update Rules](references/update-rules.md)
- [Workflows](references/workflows.md)
- [Household Development Path Framework](references/development-path-framework.md)
- [Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, YAML configuration, shell command output, and concise agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates a private local workspace; can initialize templates, write configuration, report workspace status, and archive existing workspace material when requested.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
