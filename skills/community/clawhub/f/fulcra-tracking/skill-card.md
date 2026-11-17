## Description:

Allows the user to record custom data annotations and agent visibility metrics, and generates simple HTML dashboards for visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fulcra](https://clawhub.ai/user/fulcra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to define Fulcra custom data schemas, record annotations and agent visibility metrics through the Fulcra CLI, and create lightweight HTML previews or route larger dashboards to Fulcra dashboard workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run an external Fulcra CLI for authentication and data changes.

Mitigation: Pin or pre-approve a specific fulcra-api version before use, and require user approval before authentication or data-modifying commands.

Risk: Agent visibility and personalization flows can log agent activity, memory, or chat-history-derived context.

Mitigation: Require explicit approval before logging agent activity or using memory and chat history for personalization.

Risk: The skill includes record deletion workflows that can remove Fulcra data.

Mitigation: Require explicit confirmation of the data type and record ID before deletion, then re-record corrected data only after user approval.

## Reference(s):

- [Fulcra Tracking CLI Reference](references/fulcra-tracking-cli.md)
- [Fulcra High-Impact Use Cases](references/fulcra-tracking-usecases.md)
- [Fulcra CLI Documentation](https://raw.githubusercontent.com/fulcradynamics/agent-skills/main/skills/fulcra-onboarding/references/fulcra-cli.md)
- [Fulcra Agent Skills Repository](https://github.com/fulcradynamics/agent-skills)
- [ClawHub Skill Page](https://clawhub.ai/fulcra/skills/fulcra-tracking)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional single-file HTML/CSS/JS preview code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Fulcra CLI commands for authentication, schema creation, record creation, data retrieval, and record deletion.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
