## Description:

Identify, categorize, and prioritize technical debt across a codebase, including TODOs, complexity hotspots, dependency age, test coverage gaps, and code duplication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to inspect a codebase for technical debt and create an actionable backlog of prioritized maintenance work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect source files, dependency manifests, and git history to build a technical-debt report.

Mitigation: Run it only in repositories where the agent is permitted to read code and history, and review generated reports before sharing them outside the team.

Risk: Prioritization guidance can be incomplete if the available repository signals do not reflect current business impact or operational risk.

Mitigation: Validate high-priority recommendations with maintainers and product owners before turning them into sprint commitments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/cm-tech-debt-tracker)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with inline shell commands and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes debt categories, priority scoring, estimated effort, business impact, and sprint planning guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
