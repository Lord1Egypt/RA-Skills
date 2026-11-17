## Description:

Agent Guild helps trusted local AI assistants share durable memory and hand off selected tasks without automatically loading unrelated work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dqsjqian](https://clawhub.ai/user/dqsjqian)

### License/Terms of Use:

MIT

## Use Case:

People using multiple trusted AI assistants with local file access can keep shared preferences and long-term memory, list pending tasks, and resume only the task they select.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared local memory and task files may expose sensitive information to assistants with filesystem access.

Mitigation: Use only with trusted assistants, keep secrets out of the guild, and do not treat private directory names as access controls.

Risk: Adopting or linking existing files can change the scope of shared access.

Mitigation: Review the dry-run output and choose only the intended scope before adopting or linking files.

Risk: Automatic updates change installed skill code, and permanent history cleanup can remove the final recovery copy.

Mitigation: Keep updates in check or off mode unless wanted; review exact cleanup plans and require explicit approval for irreversible deletion.

## Reference(s):

- [Agent Guild on ClawHub](https://clawhub.ai/dqsjqian/skills/agent-guild)
- [Project homepage listed in skill metadata](https://github.com/dqsjqian/agent-guild)
- [Security guidance](artifact/references/SECURITY.md)
- [Protocol specification](artifact/references/SPEC.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Text and Markdown with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task lists show metadata before a user selects a task; handoffs may reference local files and attachments.]

## Skill Version(s):

4.1.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
