## Description: <br>
Search, retrieve, log, and manage past conversations, research, job tasks, and files in Frank's Second Brain knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryandeangraves](https://clawhub.ai/user/ryandeangraves) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Authorized agents use this skill to search and update a personal external knowledge base, manage Kanban tasks, handle files, and delegate jobs to downstream agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an agent to a personal external knowledge base with broad read, write, upload, delete, and job-delegation capabilities. <br>
Mitigation: Install only for the intended owner and review each requested read, write, upload, delete, or delegation action before allowing the agent to execute it. <br>
Risk: The artifact includes a hardcoded API key for the external service. <br>
Mitigation: Treat the key and service as privileged, avoid exposing the key in shared logs, and rotate or revoke the key if it is no longer intended to be public. <br>
Risk: File upload and attachment deletion behavior can expose local files or remove remote content. <br>
Mitigation: Allow file operations only when explicitly requested and after reviewing the exact local path, destination metadata, and target attachment. <br>


## Reference(s): <br>
- [Brain Search on ClawHub](https://clawhub.ai/ryandeangraves/brain-search) <br>
- [ryandeangraves publisher profile](https://clawhub.ai/user/ryandeangraves) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown or plain text with curl commands and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include real HTTP responses from the Second Brain API when executed by an agent.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
