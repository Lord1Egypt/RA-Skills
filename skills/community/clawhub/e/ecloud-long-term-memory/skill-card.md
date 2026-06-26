## Description: <br>
Ecloud Long Term Memory provides a long-term memory workflow backed by China Mobile eCloud, with commands for saving, searching, and listing user memories in cloud storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helloofyoursffsf](https://clawhub.ai/user/helloofyoursffsf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to China Mobile eCloud long-term memory, store user-provided personal facts, retrieve relevant memories by semantic search, and list stored history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends raw personal memories and memory search queries to China Mobile eCloud. <br>
Mitigation: Use it only when remote storage on that service is intended, and avoid storing highly sensitive information unless the service's retention, access, and deletion controls meet the user's needs. <br>
Risk: The setup flow requires cloud AK/SK credentials and writes them to a generated .env file. <br>
Mitigation: Use least-privilege credentials, keep the .env file out of version control, and rotate credentials if exposure is suspected. <br>
Risk: The artifact creates local logs and persistence around memory operations. <br>
Mitigation: Review local logging behavior before deployment and disable or restrict logs if they could expose personal data. <br>
Risk: The skill asks the agent to prefer this cloud memory path over built-in or local memory tools. <br>
Mitigation: Review the installed agent rules and confirm this behavior matches the workspace's privacy and memory-management policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/helloofyoursffsf/ecloud-long-term-memory) <br>
- [China Mobile eCloud AK/SK access page](https://ecloud.10086.cn/api/page/op-aksk-static/#/) <br>
- [China Mobile eCloud console](https://console.ecloud.10086.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs Node.js scripts for configuration, cloud memory save/search/list operations, and local configuration checks.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
