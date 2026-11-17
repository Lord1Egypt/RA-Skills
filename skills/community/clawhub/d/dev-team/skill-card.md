## Description:

Orchestrates a multi-agent OpenClaw dev or agency team with shared memory, role handoffs, setup guidance, and optional multi-session routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realm1lf](https://clawhub.ai/user/realm1lf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agency operators, and solo founders use this skill to set up and coordinate role-based OpenClaw teams for customer or project work. It guides shared team memory, customer context, portfolio tracking, role templates, and task handoffs across participating agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared team folder can persist customer notes, task handoffs, and project status that may contain sensitive information.

Mitigation: Choose DEV_TEAM_ROOT deliberately, keep it outside sensitive repositories unless intended, and avoid storing real passwords, API keys, or other secrets in shared Markdown files.

Risk: Multi-agent routing, external channels, and scheduled work can broaden which agents act on project context.

Mitigation: Enable routing, channels, scheduled work, sandbox access, and tool permissions only for the agents and workflows that need them.

## Reference(s):

- [Dev Team Skill](SKILL.md)
- [OpenClaw x dev_team - guided team setup](references/OPENCLAW_TEAM_SETUP_GUIDE.md)
- [dev_team - first-time setup](references/SKILL-SETUP.md)
- [OpenClaw layout x dev_team](references/OPENCLAW_LAYOUT.md)
- [Role templates](references/ROLE_TEMPLATES.md)
- [board.json portfolio index schema](references/BOARD_SCHEMA.md)
- [Customer context template](references/CUSTOMER_CONTEXT.template.md)
- [Structure map](references/ORG_CHART_EXAMPLE.md)
- [OpenClaw multi-agent routing](https://docs.openclaw.ai/concepts/multi-agent)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [OpenClaw sandboxing](https://docs.openclaw.ai/gateway/sandboxing)
- [ClawHub skill format](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)
- [awesome-openclaw-usecases multi-agent team reference](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/multi-agent-team.md)
- [OpenClaw Showcase](https://openclaw.ai/showcase)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown guidance with file templates, JSON schema notes, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for creating and maintaining shared team folders and handoff files; no binaries or secrets are installed by the skill.]

## Skill Version(s):

1.0.1 (source: frontmatter, release evidence, _meta.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
