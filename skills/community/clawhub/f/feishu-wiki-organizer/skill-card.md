## Description:

飞书知识库整理专家 helps agents classify and organize Feishu wiki content without merging, deleting, or editing source documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgugeng](https://clawhub.ai/user/lgugeng)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and knowledge-base maintainers use this skill to plan Feishu wiki folder structures, classify scattered root documents, and prepare or execute approved document moves. It is intended for single-wiki cleanup and multi-wiki organization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reorganize Feishu wiki content, so incorrect plans or approvals could move documents into the wrong locations.

Mitigation: Require a dry-run plan with specific target knowledge bases and explicit approval for each move batch before executing changes.

Risk: The release security summary flags ambiguous hourly background-check behavior that could continue accessing or logging wiki data after the session.

Mitigation: Treat automatic checks as disabled unless personally configured, and verify or remove any cron entry plus local .kb_organizer logs or status files when finished.

Risk: Cross-library moves and moves involving nodes with children can have broader effects than simple leaf-document reclassification.

Mitigation: Require separate approval for cross-library moves and for moving documents that have child nodes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lgugeng/skills/feishu-wiki-organizer)
- [Source skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown plans, previews, checklists, and inline code or command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before move batches and separate approval for higher-risk wiki moves.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
