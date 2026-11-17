## Description:

Shared family grocery list for multiple members to add, remove, and view items organized by store, with admin-managed access and optional web checks for store addresses and item availability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adeydas](https://clawhub.ai/user/adeydas)

### License/Terms of Use:

MIT-0

## Use Case:

External family members use this skill to maintain a shared grocery list, organize items by store, manage family access, and view change history without using it for purchases or meal planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can write grocery data files to a user-chosen local path.

Mitigation: Use only a dedicated, non-sensitive shared folder and review the chosen path before setup.

Risk: Shared-file access controls are weak, so family members with filesystem access may be able to read or modify membership, list, and history files directly.

Mitigation: Do not rely on this skill for strong access control; manage filesystem permissions and review membership and history files regularly.

Risk: User-provided paths containing shell metacharacters can create unsafe setup behavior.

Mitigation: Avoid paths with shell metacharacters and review setup commands before execution.

## Reference(s):

- [Family Grocery List on ClawHub](https://clawhub.ai/adeydas/skills/family-grocery)
- [List Operations](artifact/lists.md)
- [Store Management](artifact/stores.md)
- [User Management](artifact/user-management.md)
- [Data File Templates](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with occasional shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include grocery list entries, store and user management guidance, setup commands, and local shared-file updates.]

## Skill Version(s):

1.0.0 (source: frontmatter, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
