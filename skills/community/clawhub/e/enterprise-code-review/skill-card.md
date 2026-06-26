## Description: <br>
Runs a standardized code review workflow that checks code quality, security, maintainability, and performance, then produces a structured review report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobbhchen](https://clawhub.ai/user/bobbhchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review files, pull requests, or commit history for technical quality, security risks, maintainability, and performance issues. It returns prioritized findings with locations and suggested fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect proprietary code or secrets when they are included in the requested review target. <br>
Mitigation: Provide a clear review scope and avoid supplying secrets unless they are intentionally part of the code-review context. <br>
Risk: Review findings can be incomplete or misleading if the supplied diff, file set, or commit range is incomplete. <br>
Mitigation: Give the agent the complete target to review and have a human reviewer validate findings before applying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bobbhchen/enterprise-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown structured review report with issue table, rating, strengths, and summary recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a clear review target such as files, a branch, a commit, or a pull request URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
