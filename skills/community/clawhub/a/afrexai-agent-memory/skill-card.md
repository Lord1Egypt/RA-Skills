## Description:

Complete zero-dependency memory system for AI agents using file-based architecture, daily notes, long-term curation, context management, heartbeat integration, and memory hygiene.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to set up and maintain a local, markdown-based memory system for AI agents. It helps agents manage active context, long-term memory, daily notes, topic files, archives, and session handoffs without external services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory files may persist private user, project, or business context in local markdown.

Mitigation: Protect the memory directory, exclude it from sync and source control when needed, and avoid storing regulated personal data or sensitive business details.

Risk: Secrets or credentials could be written into memory files if users ignore the storage rules.

Mitigation: Store secrets in a dedicated secrets manager and record only safe references to where credentials are managed.

Risk: Shared or group contexts may expose private long-term memory if loaded indiscriminately.

Mitigation: Load only active context and daily notes in shared settings, and avoid loading MEMORY.md where private context could be exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1kalin/skills/afrexai-agent-memory)
- [Publisher Profile](https://clawhub.ai/user/1kalin)
- [Context Packs](https://afrexai-cto.github.io/context-packs/)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline file templates, command examples, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file-structure guidance, memory templates, operating protocols, maintenance schedules, migration steps, and natural-language agent commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
