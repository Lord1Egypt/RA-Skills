## Description: <br>
Accept or apply for OpenAnt tasks, including direct acceptance, application-mode pitches, task inspection, and retrieval of reference files after assignment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to inspect OpenAnt task details, accept open tasks or apply for application-mode tasks, and download task reference files after assignment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can accept or apply for OpenAnt tasks through the user's account, creating real work commitments. <br>
Mitigation: Require explicit confirmation of the task ID, reward, deadline, account or team, and acceptance or application action before running state-changing commands. <br>
Risk: Task attachment downloads may bring untrusted files into the workspace. <br>
Mitigation: Confirm requested downloads, keep files in a task-specific directory, and review or scan downloaded files before using them. <br>


## Reference(s): <br>
- [Accept Task on ClawHub](https://clawhub.ai/ant-1984/accept-task) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands call the OpenAnt CLI with --json and may download task attachment files after acceptance.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
