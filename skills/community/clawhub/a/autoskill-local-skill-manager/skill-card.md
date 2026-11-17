## Description:

AutoSkill Local Skill Manager helps agents detect reusable session knowledge, search for similar skills, and draft approved local skill creations, merges, or improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drjzhou](https://clawhub.ai/user/drjzhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain personal, team, or workspace skill libraries by identifying reusable behavior, comparing similar skills, and preparing proposed skill files or diffs for review. It is designed for local skill management workflows where durable changes require explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose durable changes to local agent instructions and skill files.

Mitigation: Review every proposed SKILL.md file or diff and approve only intended changes before writes.

Risk: The skill may use unpinned external discovery commands such as npx skills find.

Mitigation: Pin or avoid npx skills commands for sensitive workflows and approve the exact query and destination before external discovery.

Risk: External discovery can expose private task context if queries contain sensitive details.

Mitigation: Keep external discovery disabled for private work unless the query is reviewed and sanitized.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/drjzhou/skills/autoskill-local-skill-manager)
- [Source Repository Link From Artifact README](https://github.com/ECNU-ICALK/autoskill-skill)
- [Original Project Link From Artifact README](https://github.com/ECNU-ICALK/AutoSkill)
- [skills.sh](https://skills.sh/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with proposed SKILL.md content, diffs, commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before creating, updating, deleting, importing, installing, enabling, or materially rewriting skill files.]

## Skill Version(s):

0.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
