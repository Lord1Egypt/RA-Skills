## Description:

Clawhub Memory Tiers helps OpenClaw agents maintain concise L0/L1 workspace memory so each activation starts with current state, recent context, active tasks, and blockers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dirtyrootsstudio](https://clawhub.ai/user/dirtyrootsstudio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing OpenClaw agents use this skill to add and maintain concise workspace memory files that reduce startup context reconstruction and support multi-agent status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent workspace memory may retain secrets, sensitive personal data, or operational details if users place them in L0.md or L1.md.

Mitigation: Keep memory files scoped to operational context, avoid storing secrets or sensitive personal data, and review the files before sharing or publishing a workspace.

Risk: Shared or stale memory files can mislead agents, cause task collisions, or preserve resolved blockers as active state.

Mitigation: Give each agent its own L0.md and L1.md, keep L0 to four current lines, cap L1 to recent context, and remove resolved blockers during each end-of-run update.

Risk: Editing SOUL.md changes how the agent reads and writes persistent context.

Mitigation: Review the SOUL.md additions before installation and confirm the agent is expected to maintain persistent workspace memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dirtyrootsstudio/skills/clawhub-memory-tiers)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with L0.md, L1.md, and SOUL.md snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace memory templates and operating guidance; no code, network calls, or external APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
