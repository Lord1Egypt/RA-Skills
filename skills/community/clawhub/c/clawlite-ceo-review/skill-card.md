## Description: <br>
ClawLite CEO Review guides agents through CEO-style strategic plan reviews with scope-mode selection, assumption challenges, implementation alternatives, failure-mode mapping, and observability checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering leads, and product decision makers use this skill to review software plans before implementation. It helps compare implementation paths, surface scope tradeoffs, map likely failure modes, identify observability gaps, and choose whether to expand, hold, or reduce scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Git history, diffs, TODO/FIXME matches, and project planning documents during review. <br>
Mitigation: Run it only from the project intended for review and ensure the agent may inspect those repository files. <br>
Risk: Strategic review guidance can be incomplete or unsuitable for the product context. <br>
Mitigation: Treat the output as review input for the team and validate recommendations before implementation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown strategic review report with structured sections and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes mode selection, assumption challenge, recommended approach, failure-mode map, error map, observability gaps, edge cases, test coverage gaps, and completion status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
