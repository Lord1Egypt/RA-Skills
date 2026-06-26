## Description: <br>
Manage tasks, projects, and workspaces in Exponential via the `exponential` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[positonic](https://clawhub.ai/user/positonic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Exponential users use this skill to create, list, review, and update actions, projects, workspaces, and kanban board state from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Exponential CLI uses a JWT token for authentication, and exposed tokens can allow access to Exponential data. <br>
Mitigation: Verify the npm CLI package before use, avoid sharing JWTs in terminals or transcripts, and rotate the token if it is exposed. <br>
Risk: Broad task-management requests may create or update the wrong Exponential action in shared workspaces. <br>
Mitigation: Review create and update commands, task IDs, project IDs, and status changes before execution. <br>


## Reference(s): <br>
- [Exponential service URL](https://www.exponential.im) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [TTY output is pretty-printed; scripted or forced JSON output is available through the Exponential CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
