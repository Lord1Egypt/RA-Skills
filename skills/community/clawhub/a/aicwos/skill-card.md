## Description:

Aicwos provides a Python-backed workflow for generating spoken-video copy, learning lecturer style profiles, retrieving knowledge-base context, and preserving series continuity with local storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallroya](https://clawhub.ai/user/smallroya)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to run copywriting workflows that combine lecturer style analysis, knowledge retrieval, behavior rules, and saved series progress. It is intended for agents that need structured CLI guidance and local persistence for spoken-video script generation and revision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports broad persistent write and delete authority, with path and remote-sync handling that may overwrite or remove files outside the intended workspace.

Mitigation: Install and run the skill only in a dedicated workspace with non-sensitive content, review the resolved data directory before write/delete actions, and keep backups of any workspace that contains important drafts or profiles.

Risk: The scan guidance warns against untrusted cloud knowledge URLs and imported lecturer packages.

Mitigation: Use only trusted knowledge-sync endpoints and lecturer packages, and inspect imported content before allowing it to affect generated copy or local persisted state.

Risk: The skill automatically persists and deletes copywriting work, lecturer samples, profiles, knowledge documents, and series state.

Mitigation: Treat generated actions as durable changes, review CLI commands before execution, and avoid relying on the workflow for temporary drafting unless persistence is intended.

## Reference(s):

- [Profile Format](references/profile-format.md)
- [Script Styles](references/script-styles.md)
- [Copywriting Workflow](references/workflow-copywriting.md)
- [Knowledge Workflow](references/workflow-knowledge.md)
- [Lecturer Workflow](references/workflow-lecturer.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents to use local Python CLIs that read and write SQLite-backed workspace files for profiles, knowledge documents, and generated series copy.]

## Skill Version(s):

1.10.5 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
