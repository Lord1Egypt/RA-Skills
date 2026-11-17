## Description:

A2A Manager helps Coordinator and Orchestrator agents create agents, manage Discord categories, channels, and roles, bind agents to channels, coordinate agent-to-agent work, maintain A2A_MAP.md, spawn or dispose specialist sub-agents, and manage Notion-backed task workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nyrosveil](https://clawhub.ai/user/nyrosveil)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to manage OpenClaw multi-agent workspace state, Discord coordination metadata, temporary specialist agents, and Notion task workflows from command-line helper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts can mutate local OpenClaw workspace state, including creating, editing, deleting, versioning, and rolling back agent files and A2A map content.

Mitigation: Review commands before execution, run only in intended OpenClaw workspaces, and add explicit confirmations and path validation before destructive actions.

Risk: Task board operations can send task titles, descriptions, status, tags, and identifiers to Notion.

Mitigation: Use a dedicated Notion workspace or database, restrict the Notion API token, and avoid sensitive task data unless external Notion storage is acceptable.

Risk: Untrusted agent names, specialist IDs, or rollback IDs may affect unintended files because the security scan reports unsafe path handling.

Mitigation: Accept only trusted identifiers, validate names against an allowlist, and normalize paths before creating, deleting, or restoring files.

## Reference(s):

- [A2A_MAP template](references/A2A_MAP.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local OpenClaw workspace files, Discord configuration JSON, specialist records, action logs, and Notion task data when scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
