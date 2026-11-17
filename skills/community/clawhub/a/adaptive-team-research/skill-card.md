## Description:

Adaptive Team Research coordinates a multi-agent software project review, selects a collaboration mode, and produces structured findings, consensus, and action plans with cost estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe-rq](https://clawhub.ai/user/joe-rq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering leads, and product teams use this skill to run multi-perspective reviews of software projects across product, design, and engineering concerns. It is intended for analysis and planning rather than direct code modification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may spawn several review agents and read the target project, which can increase review cost and expose more project content to the agent session.

Mitigation: Confirm the selected collaboration mode before execution and restrict the project scope or files available to the agent when needed.

Risk: The skill writes a review canvas under the target project's reviews directory.

Mitigation: Run it in a workspace where creating a review artifact is acceptable, or explicitly request a no-write workflow before starting.

Risk: The artifact primarily uses Chinese prompts and output structure, which may not match teams that require English deliverables.

Mitigation: Request English output before running the workflow when English review artifacts are required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joe-rq/skills/adaptive-team-research)
- [Mode Selection Guide](artifact/references/mode-selection.md)
- [Round Protocols](artifact/references/round-protocols.md)
- [Round 1 Role Prompts](artifact/references/role-prompts-r1.md)
- [Round 2 Role Prompts](artifact/references/role-prompts-r2.md)
- [Review Canvas Template](artifact/assets/canvas-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Files]

**Output Format:** [Markdown review canvas and concise Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a bounded review canvas under a project reviews directory and summarizes mode choice, consensus, disagreements, priority actions, costs, and critic insights.]

## Skill Version(s):

1.3.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
