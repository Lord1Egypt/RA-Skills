## Description:

Universal multi-agent workflow orchestration using Claude Code Agent Teams for running team workflows, creating agent teams, and coordinating parallel work across specialized teammates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieyer](https://clawhub.ai/user/sieyer)

### License/Terms of Use:


## Use Case:

Developers and Claude Code users use this skill to plan and coordinate five-agent workflows across software, content, data, strategy, research, and custom domains. It helps a lead agent confirm scope, assign specialized teammate roles, manage handoffs, and synthesize final deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a setup step that enables Claude Code Agent Teams globally.

Mitigation: Install it only when Agent Teams are intentionally needed and the user is comfortable enabling the experimental global setting.

Risk: Multi-agent workflows can increase cost and scope compared with a single-agent session.

Mitigation: Confirm objective, constraints, budget, and definition of done before spawning teammates.

Risk: Sensitive user inputs may be shared with spawned teammates during handoffs.

Mitigation: Avoid sharing sensitive inputs with teammates unless that sharing is intended for the task.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sieyer/skills/claude-agent-team-workflows-0-1-0)
- [Domain Presets](reference/domain-presets.md)
- [Pipeline Patterns](reference/patterns.md)
- [Prompt Templates](reference/prompt-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with workflow specs, task lists, prompt templates, handoff messages, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require enabling Claude Code experimental Agent Teams and confirming cost, scope, and sensitive-input sharing before spawning teammates.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta version 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
