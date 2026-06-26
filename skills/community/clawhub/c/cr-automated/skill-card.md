## Description: <br>
CR Automated helps agents perform structured code review for pull requests and local changes, including CI status checks, code quality review, security inspection, performance analysis, and maintainability feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review pull requests or code changes, check CI failures, and produce prioritized review feedback with concrete remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review verdict is suspicious because the skill can guide nested review execution with broad local access and approval bypass. <br>
Mitigation: Use the documented non-yolo mode where available, review commands before execution, and run the skill in a constrained workspace with only the repositories and credentials needed for the review. <br>
Risk: The skill may fetch PR metadata, CI logs, and code diffs that can include sensitive project information. <br>
Mitigation: Use it only in repositories where the agent is authorized to inspect PR data, and avoid exposing secrets or proprietary diffs to fallback reviewers unless approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/cr-automated) <br>
- [Detailed review criteria](reference.md) <br>
- [Review examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review report with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CI status summaries, prioritized findings, suggested fixes, and notes for reviewers.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
