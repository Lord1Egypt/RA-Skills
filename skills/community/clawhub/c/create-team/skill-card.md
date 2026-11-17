## Description:

Builds a runnable Claude Code Agent Teams skill package that produces a lead-operator SKILL.md playbook, runtime subagent definitions, 8-section role specs, and optional hooks for reusable multi-agent teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-team authors use this skill to create runnable Claude Code Agent Teams packages with coordinated roles, task dependencies, disjoint file ownership, install instructions, and teardown guidance. It is intended for cases where a reusable multi-agent team should run end-to-end rather than only producing static role documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated team packages can add agent definitions or hooks under .claude locations, changing how future Claude Code sessions run.

Mitigation: Prefer project-scoped .claude/agents installation unless reusable user-wide agents are intended, and review generated tool allowlists and hook commands before enabling them.

Risk: Multi-agent teams can overwrite each other's work when role ownership overlaps or can leave runtime resources behind when teardown is skipped.

Mitigation: Run the included checklist, require disjoint Owned Paths for every role, and complete the documented shutdown sequence before TeamDelete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/create-team)
- [Templates](references/templates.md)
- [Virtual Team Skill Checklist](references/checklist.md)
- [Claude Code Subagents Documentation](https://code.claude.com/docs/en/sub-agents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown skill files with inline command examples and optional shell hook scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a skill package structure containing SKILL.md, agents/<role>.md files, references/<role>.md specs, references/member.md, and optional hooks/ files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
