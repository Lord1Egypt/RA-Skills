## Description:

Estimates development effort in hours from requirements and project source code using task breakdowns, complexity factors, and technology-stack baselines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlykan](https://clawhub.ai/user/wlykan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering leads use this skill during sprint planning or backlog refinement to estimate frontend, backend, or full-stack implementation effort from requirements and repository code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may inspect project requirements and source files to estimate effort.

Mitigation: Run it only in repositories and workspaces whose contents the agent is allowed to inspect.

Risk: The skill instructions and default report format are Chinese-language.

Mitigation: Ask the agent to adapt the final report language when the team needs another language.

Risk: Effort estimates can mislead planning when requirements, acceptance criteria, or code analysis are incomplete.

Mitigation: Review the task breakdown, assumptions, buffer, risks, and dependencies before using estimates for planning.

## Reference(s):

- [Complexity Factors](references/complexity-factors.md)
- [Tech Stack Baseline](references/tech-stack-baseline.md)
- [ClawHub Skill Page](https://clawhub.ai/wlykan/skills/estimate-effort)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown effort-estimation report with tables, risk notes, and optimization suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a 3-year developer baseline and requires task-level factor breakdowns before giving effort numbers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
