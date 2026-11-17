## Description:

Manage and mutate a Notion-based agency dispatch board through slash commands and natural-language task operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[automatelab](https://clawhub.ai/user/automatelab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent teams use this skill to create, discuss, approve, launch, and close work in a Notion task board while keeping kickoff briefs bounded and linked to local project guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can be launched from mutable Notion task content.

Mitigation: Install only for trusted Notion workspaces, review task descriptions before `/agency-os run --go`, and require explicit confirmation for writes inferred from natural language.

Risk: The skill uses a Notion integration token and refers to local `.env` credential storage.

Mitigation: Use a least-privilege Notion token, share it only with the required Tasks database, and remove `.env` from broad read or grep guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/automatelab/skills/agency-os)
- [Notion public template](https://www.notion.so/35dd01a02a8081dea01cd8d42617f0c8)
- [General guidance template](artifact/references/general-guidance.md)
- [Task page template](artifact/references/task-page-template.md)
- [Corpus template](artifact/references/corpus-template.md)
- [Configuration template](artifact/references/config-template.json)
- [Notion pointers template](artifact/references/notion-pointers.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with clickable links, slash commands, JSON configuration, and generated sidecar files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can mutate Notion task state, write local pointer/configuration files, and write a task queue sidecar after successful Notion API refresh.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
