## Description: <br>
Provides Google Tasks API helpers for listing task lists and creating, updating, completing, and deleting tasks after OAuth 2.0 authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibluewind](https://clawhub.ai/user/ibluewind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent manage Google Tasks for an authorized Google account, including task list lookup and task creation, updates, completion, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, create, modify, complete, and delete Google Tasks after OAuth authorization. <br>
Mitigation: Install only for accounts where this access is acceptable, and revoke the OAuth grant or delete ~/.google-tasks-token.pickle when access is no longer needed. <br>
Risk: Local OAuth credential and token files grant access to the selected Google account's Tasks data. <br>
Mitigation: Keep ~/.google-credentials.json and ~/.google-tasks-token.pickle private, and do not use token pickle files from untrusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ibluewind/andrew-google-tasks) <br>
- [Google Tasks OAuth scope](https://www.googleapis.com/auth/tasks) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with Python examples, shell commands, and Google Tasks API operation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or mutate Google Tasks after OAuth authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
