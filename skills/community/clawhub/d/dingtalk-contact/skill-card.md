## Description: <br>
Dingtalk Contact helps agents query DingTalk address book data, including users, departments, employee details, department membership, organizational paths, and employee counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[breath57](https://clawhub.ai/user/breath57) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, administrators, and support operators use this skill to find DingTalk users and departments, retrieve contact details, inspect department membership, and summarize organization directory information when they are authorized to access it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores DingTalk app credentials and cached tokens in a local configuration file. <br>
Mitigation: Use a least-privilege DingTalk app, restrict file access, prefer secure secret storage where available, and rotate credentials if the local config or tokens may have been exposed. <br>
Risk: The skill can access broad employee directory data, including user details, department membership, and organization counts. <br>
Mitigation: Install it only for authorized DingTalk administrators or trusted operators, restrict who can invoke it, and avoid bulk member queries unless they are approved. <br>
Risk: The skill runs shell-based workflows that call external DingTalk APIs. <br>
Mitigation: Review commands before execution and confirm that each query matches the operator's approved directory-access purpose. <br>


## Reference(s): <br>
- [Dingtalk Contact API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/breath57/dingtalk-contact) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and DingTalk API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or summarize DingTalk directory API results; credentials and tokens should be masked in user-facing output.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
