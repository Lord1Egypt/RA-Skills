## Description: <br>
Creates new OpenClaw agents through a guided confirmation flow, then registers them with the CLI and initializes workspace Markdown documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangyangupday](https://clawhub.ai/user/yangyangupday) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using OpenClaw use this skill to create and initialize a new agent after confirming the agent name, purpose, model, workspace path, and final summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates directories, writes Markdown files, modifies OpenClaw agent configuration, and appends a persistent history record. <br>
Mitigation: Review the final summary before confirming and choose a workspace that does not contain unrelated sensitive files. <br>
Risk: Agent descriptions and setup details can be written to the local history file. <br>
Mitigation: Do not put secrets or sensitive personal data in the agent description or setup responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangyangupday/skills/agent-add) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with shell command execution and file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates OpenClaw agent workspace documents, updates agent configuration, and appends a local history record after user confirmation.] <br>

## Skill Version(s): <br>
1.4.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
