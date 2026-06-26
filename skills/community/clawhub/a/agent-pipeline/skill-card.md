## Description: <br>
Manages a code-task workflow by coordinating research, coding, review, security audit, testing, and commit stages with board and planner updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Curbob](https://clawhub.ai/user/Curbob) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to run code changes through a structured pipeline with role-specific research, implementation, review, security, test, and commit responsibilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks agents to broadly share an auth profile and always post status updates to a board service without enough scoping or user control. <br>
Mitigation: Use only in a trusted development environment, replace blanket auth-profile copying with per-role or temporary credentials, and confirm the board endpoint and update behavior before running the workflow. <br>
Risk: The workflow includes branch creation, commit, and push behavior that can affect a repository. <br>
Mitigation: Confirm the target repository, branch name, planner target, and push behavior before allowing the commit stage to proceed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown workflow instructions with inline commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes prescribed stage order, role responsibilities, board logging, planner updates, branch naming, and commit guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
