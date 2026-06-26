## Description: <br>
生成飞书 AI 助手团队工作日报，收集团队成员当天工作内容，整理为日报文件并发送到飞书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tilly266](https://clawhub.ai/user/Tilly266) <br>

### License/Terms of Use: <br>


## Use Case: <br>
团队运营人员和使用 OpenClaw/飞书的 AI 助手团队可用该技能汇总当天多个 agent 的用户消息，生成可保存并发送到飞书的工作日报。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read multiple agents' private session logs and summarize user messages into a team report. <br>
Mitigation: Install only where team-wide reporting from agent session logs is intended and authorized, and confirm which agents are included. <br>
Risk: The skill can automatically send summarized user messages to Feishu. <br>
Mitigation: Confirm the Feishu chat recipient, reader access, redaction expectations, and whether a human preview and approval step is required before scheduled sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tilly266/feishu-ai-dailyreport) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files] <br>
**Output Format:** [Markdown daily report with Feishu message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Date-stamped daily report using Beijing time (UTC+8).] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
