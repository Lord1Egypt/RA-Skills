## Description:

Manage Craft documents through the craft CLI, including listing, searching, creating, updating, deleting, and exporting documents in JSON, table, or markdown formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerveband](https://clawhub.ai/user/nerveband)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to operate on Craft documents from a command line workflow, including retrieval, search, document creation, updates, deletion, and export. It is suited to LLM-assisted document workflows where machine-readable JSON or markdown output is useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release exposes real-looking Craft access URLs.

Mitigation: Do not use the embedded Craft URLs; replace them with protected user-owned configuration before installing or running the skill.

Risk: The skill documents powerful document mutation commands, including create, update, and delete operations.

Mitigation: Confirm the active Craft space and target document ID before any create, update, or delete action.

Risk: A local CLI binary is expected before use.

Mitigation: Prefer a user-local, verified CLI install and review the release carefully before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nerveband/skills/craft-cli)
- [Publisher profile](https://clawhub.ai/user/nerveband)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Markdown, Code]

**Output Format:** [Markdown with inline shell commands and CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The craft CLI can emit JSON, table, or markdown output depending on command flags.]

## Skill Version(s):

1.6.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
