## Description: <br>
Assistant Configurator helps users manage and optimize OpenClaw configuration, including model selection, skill management, tool configuration, and system tuning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junsheng428](https://clawhub.ai/user/junsheng428) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to evaluate and adjust OpenClaw assistant behavior, model routing, skill loading, tool setup, troubleshooting, and performance settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested configuration patches can change OpenClaw assistant behavior, tool access, channels, or service state. <br>
Mitigation: Review each proposed patch before applying it, back up the current configuration, change one setting at a time, and test after each change. <br>
Risk: Credential placeholders for API keys and bot tokens could lead users to paste real secrets into chat, files, or logs. <br>
Mitigation: Keep real API keys and bot tokens out of chat transcripts and logs, and inject secrets through approved local secret-management or configuration mechanisms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/junsheng428/assistant-configurator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; proposed configuration changes should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
