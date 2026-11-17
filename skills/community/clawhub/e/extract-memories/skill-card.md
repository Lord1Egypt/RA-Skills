## Description:

Extracts durable memory items from a conversation and records them as topic files with an updated memory index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jofiction918](https://clawhub.ai/user/jofiction918)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve selected conversation details such as user preferences, decisions, project constraints, and external references for future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically save selected conversation details to persistent memory.

Mitigation: Use a preview or confirmation workflow before writing memories, and avoid running it on conversations containing secrets, private account details, sensitive URLs, or instructions that should not influence future sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jofiction918/skills/extract-memories)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown status summary plus memory topic files with YAML frontmatter]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends selected memory entries to topic files and updates a MEMORY.md index.]

## Skill Version(s):

3.0.10 (source: server release metadata; artifact frontmatter declares 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
