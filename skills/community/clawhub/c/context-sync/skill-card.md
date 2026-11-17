## Description:

Helps agents search, read, create, update, move, copy, delete, and bulk-sync local files, notes, and context in Aicoo workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xisen-w](https://clawhub.ai/user/xisen-w)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep an Aicoo workspace current by browsing existing notes, searching context, uploading local project files, and managing folders, notes, snapshots, shared folders, identity files, and deletes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can use the configured Aicoo API key to create, edit, move, copy, search, and delete workspace content.

Mitigation: Require an explicit preview and user confirmation before syncs, deletes, shared-folder writes, or memory/self policy changes.

Risk: Local files may contain secrets, private repositories, or other sensitive content that should not be uploaded.

Mitigation: Ask for the exact file list and destination before upload, and exclude secrets and private repositories by default.

Risk: Shared-folder and identity-file updates can affect other users or alter how the shared agent represents the user.

Mitigation: Limit these operations to intended folders and require confirmation for shared-folder writes and memory/self changes.

## Reference(s):

- [Context Sync ClawHub Page](https://clawhub.ai/xisen-w/skills/context-sync)
- [Context Sync API Reference](reference/API.md)
- [Example: Sync a Project Directory](examples/sync-project.md)
- [Aicoo API Base URL](https://www.aicoo.io/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AICOO_API_KEY bearer authentication and can guide file sync, folder, note, snapshot, memory, shared-folder, and delete operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
