## Description:

Controls the Eagle digital asset management application through CLI commands for searching, organizing, tagging, and managing local library items, folders, tags, and tag groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roaycl](https://clawhub.ai/user/roaycl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to operate a local Eagle library through the Eagle API, including finding assets, updating metadata, managing folders, and managing tags. It is suited for workflows where an agent should assist with digital asset organization while the user confirms mutating operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can be pointed at an arbitrary HTTP endpoint through EAGLE_SERVER_URL or --server, which may expose private Eagle library metadata, local paths, URLs, annotations, or asset content.

Mitigation: Use the default local Eagle server unless the destination is fully trusted, and avoid overriding the server URL for normal library operations.

Risk: Mutating commands can rename or merge tags, move items and folders, delete tag groups, or move items to trash.

Mitigation: Ask for a preview of affected items and confirm changes before running mutating commands, especially tag merges, folder moves, trash operations, and tag-group deletion.

## Reference(s):

- [App Tools](references/app-tools.md)
- [Item Tools](references/item-tools.md)
- [Folder Tools](references/folder-tools.md)
- [Tag Tools](references/tag-tools.md)
- [Tag Group Tools](references/tag-group-tools.md)
- [AI Search Tools](references/ai-search-tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Eagle library metadata such as item IDs, tags, folders, local paths, source URLs, annotations, and asset details returned by the local Eagle API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
