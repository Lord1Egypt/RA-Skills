## Description:

Creates and manages persistent multi-agent teams with standardized configs and team structures for progressive memory and private skill sets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[201983290498](https://clawhub.ai/user/201983290498)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create, load, and coordinate persistent Claude Code multi-agent teams with role-specific configuration, memory, progress tracking, and private skill directories. It is intended for projects that need repeatable team setup and controlled agent handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent role configuration and team files can alter future child-agent behavior.

Mitigation: Review generated .claude/agents and .claude/teams files before loading the team, and rerun the included validator after structure changes.

Risk: Stored role memory is reinjected into generated system prompts and may carry sensitive or stale content forward.

Mitigation: Do not store secrets or sensitive user content in memory.md, and inspect generated prompts before agent instantiation.

Risk: Unvalidated team or role names could lead to unintended paths or broken team loading.

Mitigation: Use strict team and role names without path separators and confirm that role names match their .claude/agents frontmatter.

## Reference(s):

- [Agent Crew Skill](artifact/SKILL.md)
- [Data Contracts](artifact/data_contracts.md)
- [Harness Rules](artifact/harness_rules.md)
- [Prompt Generator Script](artifact/scripts/generate_prompts.py)
- [Team Validator Script](artifact/scripts/validate_team.sh)
- [ClawHub Skill Page](https://clawhub.ai/201983290498/skills/agent-crew)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, and generated configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update persistent .claude/agents and .claude/teams files; the prompt generator emits markdown system prompts assembled from role configuration, memory, and skill summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
