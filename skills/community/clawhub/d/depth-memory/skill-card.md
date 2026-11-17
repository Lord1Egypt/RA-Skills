## Description:

Depth Memory provides a workspace-level long-term memory system for storing, indexing, and retrieving structured knowledge, skill experience, and long-term notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qshfu](https://clawhub.ai/user/qshfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve reusable knowledge, implementation notes, and tool experience across sessions, then retrieve entries through a Markdown index and keyword query script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent notes may capture secrets, credentials, private documents, or untrusted third-party content.

Mitigation: Use the skill only for intended long-term memory workflows, avoid storing sensitive material, and clearly label untrusted source material.

Risk: Retrieved memory entries may be stale, incorrect, or misleading if treated as instructions.

Mitigation: Treat retrieved entries as reference material and review them before relying on them for decisions or code changes.

Risk: Workspace-level index rows or file paths may be unexpected because the skill maintains DEEP-MEMORY.md and deep-memory/*.md.

Mitigation: Review DEEP-MEMORY.md and referenced memory files for unexpected rows or paths before trusting results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qshfu/skills/depth-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON query results, shell commands, and workspace Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates persistent workspace files such as DEEP-MEMORY.md and deep-memory/*.md when setup or add workflows are used.]

## Skill Version(s):

0.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
