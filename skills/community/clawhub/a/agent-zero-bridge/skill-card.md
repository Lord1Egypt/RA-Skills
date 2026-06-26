## Description: <br>
Delegate complex coding, research, or autonomous tasks to Agent Zero framework. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DOWingard](https://clawhub.ai/user/DOWingard) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to delegate complex coding, research, long-running build, test, and infrastructure tasks from Clawdbot to Agent Zero while allowing Agent Zero to report progress or request input through Clawdbot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent Zero can use token-backed access to call back into Clawdbot and attached files can expose local content. <br>
Mitigation: Install only when bidirectional Agent Zero access is needed, use a dedicated low-privilege token, review each file before using --attach, and avoid sending secrets or regulated data. <br>
Risk: Binding the Clawdbot gateway on public or shared networks can expose the bridge beyond the intended local workflow. <br>
Mitigation: Prefer localhost or a private Docker network, and avoid 0.0.0.0 unless the network boundary and token controls have been reviewed. <br>
Risk: Persisted Agent Zero context can carry information between unrelated tasks. <br>
Mitigation: Reset Agent Zero context between unrelated tasks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DOWingard/agent-zero-bridge) <br>
- [Agent Zero](https://github.com/frdel/agent-zero) <br>
- [Clawdbot](https://github.com/clawdbot/clawdbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI text with inline shell commands, JSON examples, configuration snippets, and generated task files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can send prompts and attachments to Agent Zero, persist or reset conversation context, invoke Clawdbot from Agent Zero, and create Markdown task breakdown files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
