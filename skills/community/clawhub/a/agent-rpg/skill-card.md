## Description:

Transforms the agent into a genre-agnostic text RPG Game Master with session-zero setup, persistent campaign state, dice rolling, and narrative consequence management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhrisfu](https://clawhub.ai/user/xhrisfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill to run text-based RPG sessions across genres, establish character and world setup, resolve actions with optional dice mechanics, and persist campaign state between turns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaign names affect where state files are stored, and unsafe names could access files outside the intended campaign folder.

Mitigation: Use only simple campaign names with letters, numbers, hyphens, or underscores until path validation is added.

Risk: Dice expressions do not have resource limits and can create excessive computation or output.

Mitigation: Use modest dice expressions and add limits before deployment in shared or automated environments.

Risk: Campaign state is written to disk and may contain sensitive personal or roleplay content.

Mitigation: Avoid saving sensitive personal content and provide clear opt-in, retention, and deletion practices before shared use.

Risk: Adult-roleplay guidance can create policy, workplace-safety, or audience-appropriateness concerns.

Mitigation: Remove or gate adult-roleplay guidance and require clear boundaries for acceptable themes.

## Reference(s):

- [RPG Rule Systems](artifact/references/systems.md)
- [World Templates](artifact/references/world-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/xhrisfu/skills/agent-rpg)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown narrative responses with optional shell command invocations and JSON or Markdown save files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write campaign state under memory/rpg/<campaign_name>/ when the context manager is used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
