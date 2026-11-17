## Description:

Turn a vague feature idea into an approved design brief that records intent, decisions with rationale and cost-if-wrong, scope boundaries, exact interfaces, and constraints for downstream planning and execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to turn an undeveloped feature idea into a decision-focused Markdown design brief before implementation or task planning. It helps clarify intent, scope, interfaces, constraints, precedents, alternatives, and open questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads nearby project context and writes project-scoped design brief files.

Mitigation: Run it only in the intended workspace and review the generated brief content before approval or downstream handoff.

Risk: Broad brainstorming phrases can activate the workflow and create or update .claude/design-briefs entries.

Mitigation: Use an explicit /design-brief request when activation should be intentional, and check the target brief path before keeping changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dennisrongo/skills/design-brief)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown design brief with concise conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a project-scoped .claude/design-briefs/<slug>.md file; does not implement code.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
