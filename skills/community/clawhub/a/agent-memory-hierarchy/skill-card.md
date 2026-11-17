## Description:

Structures an OpenClaw agent's memory into hot, warm, and cold layers using concise prose, YAML facts, lookup indexes, project files, and daily logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kimmi2ue](https://clawhub.ai/user/kimmi2ue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to reorganize OpenClaw memory files, reduce context-window token usage, and make facts easier for agents to retrieve. It is suited for migrations from prose-only memory into structured fact stores, lookup indexes, project notes, and cold session logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can centralize sensitive personal, health, account, system, and credential-location information into persistent plaintext files.

Mitigation: Review before installing, opt in only to necessary sensitive categories, minimize stored data, and exclude raw secrets, tokens, passwords, private keys, recovery codes, and exact credential paths.

Risk: Structured lookup indexes and fact stores can make private information easier to retrieve or expose if memory files are shared or committed.

Mitigation: Keep generated memory files private, review them before sharing or committing, and store only non-secret pointers when referencing sensitive systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kimmi2ue/skills/agent-memory-hierarchy)
- [facts-yaml-template.md](artifact/references/facts-yaml-template.md)
- [lookup-index-template.md](artifact/references/lookup-index-template.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with YAML and Markdown templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to create or reorganize persistent plaintext memory files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
