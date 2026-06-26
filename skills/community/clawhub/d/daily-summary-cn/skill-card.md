## Description: <br>
每日工作总结自动生成。根据聊天记录和浏览器历史生成一句话工作总结，定时发送飞书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppop0uuiu](https://clawhub.ai/user/ppop0uuiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to generate a concise daily work summary from local chat memory and browser history, then save it locally or send it through a configured Feishu channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw memory and Chrome/Edge browsing history, which may include sensitive personal or work information. <br>
Mitigation: Review the local data sources before use, run the skill manually first, and install it only where this local history access is acceptable. <br>
Risk: Optional Feishu delivery can send generated work summaries to a configured channel. <br>
Mitigation: Use a Feishu destination approved for automated work summaries and verify the channel configuration before enabling the scheduled command. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Plain text summary with a Markdown memory entry and optional setup commands/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a short daily-summary sentence and appends it to the local OpenClaw memory file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
