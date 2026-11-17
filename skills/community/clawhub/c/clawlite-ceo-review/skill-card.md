## Description:

ClawLite CEO Review is a strategic planning reviewer that challenges assumptions, compares implementation approaches, maps failure modes, and produces observability and edge-case review guidance before implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering leads, and product decision-makers use this skill to review plans before coding, choose a review posture, challenge assumptions, compare alternatives, and surface failure modes, tests, and observability gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read local repository history, diffs, TODOs, and design documents to build planning context.

Mitigation: Use it only in repositories where reviewing those local files is acceptable, especially when sensitive material may be present.

Risk: Strategic review output may contain incorrect or misleading recommendations.

Mitigation: Have a human reviewer validate assumptions, proposed scope changes, failure-mode mappings, and observability recommendations before acting on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown review report with inline shell commands and structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect local repository history, diffs, TODOs, and design documents when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
