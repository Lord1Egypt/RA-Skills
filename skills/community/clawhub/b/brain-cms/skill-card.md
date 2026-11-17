## Description:

Brain CMS sets up a neuroscience-inspired memory system for OpenClaw agents with semantic schemas, a topic router, a LanceDB vector store, and local sleep-cycle scripts for memory consolidation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrey401](https://clawhub.ai/user/harrey401)

### License/Terms of Use:


## Use Case:

Developers and external OpenClaw users use this skill to install and operate persistent agent memory that can load relevant schemas, search semantic memory, and consolidate daily logs into long-term memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify long-term OpenClaw memory and AGENTS.md.

Mitigation: Install only in workspaces where persistent memory changes are acceptable, keep backups or rollback options, and review generated REM updates before relying on them.

Risk: The installer uses unpinned Python dependencies and shell execution.

Mitigation: Review the installer before running it, pin dependencies in controlled environments, and install from trusted package indexes.

Risk: Daily logs and schemas may contain sensitive information that later becomes searchable or consolidated.

Mitigation: Avoid storing secrets in logs, schemas, or anchors, and review memory files before sharing or publishing a workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrey401/skills/brain-cms)
- [Publisher profile](https://clawhub.ai/user/harrey401)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands and Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs local memory files and scripts, writes vector-store metadata, and may append consolidated facts to memory schemas.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
