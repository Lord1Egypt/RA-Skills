## Description:

Edvisage Agent Ops helps agents track estimated API costs, log actions, generate daily operations summaries, and flag unusual spending patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edvisage](https://clawhub.ai/user/edvisage)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to have an agent keep cost and action records, surface spending alerts, and produce daily operations summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent action and cost logs can capture sensitive prompts, secrets, personal data, full paths, API endpoints, private resource names, or detailed notes.

Mitigation: Before using the skill on sensitive projects, configure the agent to avoid logging sensitive details and to redact or omit private identifiers.

Risk: The skill does not define clear privacy limits, retention periods, or log-clearing controls.

Mitigation: Set a project-specific logging scope and periodically clear retained logs.

## Reference(s):

- [Edvisage Agent Ops on ClawHub](https://clawhub.ai/edvisage/skills/edvisage-agent-ops)
- [Edvisage AI Tools](https://edvisageglobal.com/ai-tools)
- [Agent Ops Pro Upgrade](https://edvisage.gumroad.com/l/roatk)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with log and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces cost logs, action logs, summary reports, spending alerts, and model-routing notes when the agent follows the skill.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
