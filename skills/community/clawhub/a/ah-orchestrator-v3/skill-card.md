## Description:

This skill helps agents route software work to specialists, coordinate sequential or parallel execution, and add quality checkpoints and human-in-the-loop decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to route work to specialist agents, coordinate sequential or parallel execution plans, and add quality checkpoints for software projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad routing triggers can recommend sensitive workstreams such as security, deployments, authentication, or large refactors.

Mitigation: Review the proposed specialist routing and checkpoint plan before acting on recommendations for sensitive or high-impact work.

Risk: Agent-planning guidance can produce incorrect or incomplete project plans if the user request lacks context.

Mitigation: Use the skill's human-in-the-loop checkpoints to confirm requirements, architecture choices, and validation criteria before implementation.

## Reference(s):

- [AI Project Orchestrator Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/mtsatryan/skills/ah-orchestrator-v3)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown planning guidance with specialist routing recommendations and checkpoints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable files or tool integrations are present in the artifact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
