## Description:

Orchestrator helps agents analyze software project requests, route work to specialist agents, plan sequential or parallel execution, and add quality checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to decompose software project requests, select specialist agents, coordinate sequential or parallel workstreams, and add review checkpoints before major decisions or broad changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad routing and parallel-workflow suggestions may lead an agent to share sensitive project context with more specialist agents or sessions than needed.

Mitigation: Review proposed agent choices and limit shared context before approving routing, parallel sessions, or large changes.

Risk: Generated execution plans may be incomplete or may recommend an unsuitable specialist for a specific project.

Mitigation: Use the skill's checkpoint and self-review steps to confirm agent selection, dependencies, risks, and success criteria before proceeding.

## Reference(s):

- [AI Project Orchestrator V4 code examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown plans, routing analyses, checklists, checkpoint prompts, and session command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning and coordination guidance; it does not include executable code in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
