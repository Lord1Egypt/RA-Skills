## Description:

Intelligent skill router that analyzes the current problem statement and context, scores available skills for applicability, and recommends the most relevant ones in priority order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[science-prof-robot](https://clawhub.ai/user/science-prof-robot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Autoskill to identify applicable agent skills for a task, review a scored execution plan, and explicitly approve which skills may run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved downstream skills may perform file, network, or external-service actions outside Autoskill's own behavior.

Mitigation: Review the execution plan before approval, decline high-risk skills that are not needed, and cancel when the proposed queue is broader than intended.

Risk: Skill recommendations could route work to an unsuitable or overly broad skill.

Mitigation: Use the scored table and mandatory confirmation step to select only the skills that match the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/science-prof-robot/skills/autoskill)
- [Project homepage](https://github.com/Science-Prof-Robot/autoskill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with scored recommendations, execution previews, confirmation prompts, and audit tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before invoking recommended, suggested, or high-risk downstream skills.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
