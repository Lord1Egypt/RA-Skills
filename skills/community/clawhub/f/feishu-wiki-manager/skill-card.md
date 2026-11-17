## Description:

Feishu Wiki Manager helps agents browse, search, create, move, and rename nodes in Feishu or Lark knowledge spaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[young-joey](https://clawhub.ai/user/young-joey)

### License/Terms of Use:

MIT-0

## Use Case:

Knowledge-base maintainers, operators, and developers use this skill to navigate Feishu Wiki spaces, search wiki content, and organize node structures through confirmed create, move, and rename operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Create, move, and rename actions can reorganize the wrong wiki space or node when targets are ambiguous.

Mitigation: Confirm the target space, node list, and proposed change summary with the user before approving structural edits.

Risk: Batch operations can hit Feishu API rate limits or apply too many structural changes at once.

Mitigation: Run batch operations serially, keep each batch to 10 nodes or fewer, and wait at least 1 second between API calls.

Risk: The skill does not implement wiki content edits or permission changes despite broad wiki-management wording.

Mitigation: Route content edits to the Feishu document workflow and permission changes to a permission-specific workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/young-joey/skills/feishu-wiki-manager)
- [Feishu Wiki structure templates](references/wiki-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown-formatted text with structured lists and Feishu Wiki tool action requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before create, move, or rename operations; batch operations are serial and limited to 10 nodes per run.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
