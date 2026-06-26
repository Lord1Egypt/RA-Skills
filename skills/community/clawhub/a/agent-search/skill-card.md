## Description: <br>
List all agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yujin1liu](https://clawhub.ai/user/yujin1liu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent to list available agents through the local agent-browser command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local agent-browser command behavior is outside the submitted skill artifact. <br>
Mitigation: Confirm the command is from a trusted source and behaves as a read-only agent listing tool before installing or running the skill. <br>
Risk: The activation condition and documentation are sparse. <br>
Mitigation: Review the submitted SKILL.md and ClawScan guidance before deployment, and use the skill only where agent listing is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yujin1liu/agent-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown from agent-browser command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local node, npm, and a trusted agent-browser command.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
