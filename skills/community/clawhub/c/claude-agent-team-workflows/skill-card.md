## Description:

Universal multi-agent workflow orchestration using Claude Code Agent Teams. Use when user asks to run a team workflow, create an agent team, or coordinate parallel work across multiple teammates - for any domain (software, content, data, strategy, research, etc.).

This skill is ready for commercial/non-commercial use.

## Publisher:

[doanbactam](https://clawhub.ai/user/doanbactam)

### License/Terms of Use:


## Use Case:

Developers, technical leads, and other agent users use this skill to plan and coordinate five-role Claude Code Agent Teams for software, content, data, business strategy, research, and custom workflows. It helps the lead agent confirm scope, assign role cards, manage handoffs, and synthesize final deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the user to enable a persistent Claude Code Agent Teams setting.

Mitigation: Review the settings change before applying it and enable it only in environments where Agent Teams workflows are intended.

Risk: Multi-agent workflows can expose user inputs to several teammates.

Mitigation: Confirm scope before spawning a team and share sensitive inputs only with teammates that need them for the task.

Risk: Delegated teammates can produce incomplete, conflicting, or costly plans if the lead skips coordination gates.

Mitigation: Use the documented scope confirmation, acceptance criteria, handoff checks, and user approvals for irreversible, external, high-cost, production, or legal/compliance actions.

## Reference(s):

- [Domain Presets](reference/domain-presets.md)
- [Pipeline Patterns](reference/patterns.md)
- [Prompt Templates](reference/prompt-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/doanbactam/skills/claude-agent-team-workflows)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON, shell snippets, role cards, task lists, and prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow setup instructions, team prompts, handoff guidance, validation criteria, and final synthesis structure.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
