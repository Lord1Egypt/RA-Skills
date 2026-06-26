## Description: <br>
AI agent memory backup. Register at agentsmem.com, get an API key, then encrypt and upload memory via the API; owner manages backups on the web. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ocmuuu](https://clawhub.ai/user/ocmuuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to register an agent with AgentsMem, claim the account, encrypt local memory files, upload backups, and restore backed-up memory when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to handle API keys, account passwords, session cookies, and encryption keys. <br>
Mitigation: Avoid sharing existing account passwords or encryption keys in chat, restrict local permissions on credentials.json, .vault, and session.txt, and verify downloaded helper scripts before execution. <br>
Risk: Memory backups are uploaded to agentsmem.com and the skill states the service is not end-to-end encrypted. <br>
Mitigation: Use the skill only if the owner trusts agentsmem.com, confirm exactly which files will be backed up, and avoid uploading memory content outside the owner's acceptable data policy. <br>
Risk: Losing the local vault key can make encrypted backups unrecoverable. <br>
Mitigation: Have the owner save the generated encryption key offline before relying on backups, and do not overwrite an existing .vault file without explicit owner confirmation. <br>


## Reference(s): <br>
- [AgentsMem homepage](https://agentsmem.com) <br>
- [AgentsMem API base](https://agentsmem.com/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/ocmuuu/agentsmem) <br>
- [Publisher profile](https://clawhub.ai/user/ocmuuu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, backup, restore, credential-handling, and API-use instructions for the agent.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
