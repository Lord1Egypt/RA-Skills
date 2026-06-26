## Description: <br>
一键读取 20+ 平台聊天，生成智能纪要（摘要、决策、行动项、风险、多维分析、AI 建议）。Auto-read 20+ platforms, generate smart minutes with summaries, decisions, actions, risks, multi-dimensional analysis, and AI suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaomo-1225](https://clawhub.ai/user/yaomo-1225) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, and project teams use ChatMerge to summarize authorized multi-platform chat or meeting content into concise minutes, decisions, action items, risks, and follow-up guidance. It supports recurring summaries, monitoring, and optional task-tracking workflows when the user grants the needed access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad chat, meeting, and connected-tool access could expose sensitive business communications or workspace data. <br>
Mitigation: Start with pasted text or one explicit channel, use least-privilege tokens, and grant access only to workspaces and tools required for the intended summary. <br>
Risk: Scheduled summaries, monitoring, auto-created tasks, and reminders can send or modify information unexpectedly if enabled too broadly. <br>
Mitigation: Keep auto-create and auto-record disabled until deliberately needed, and verify the schedule, destination, monitoring status, retention behavior, and stop/delete controls before enabling automation. <br>


## Reference(s): <br>
- [ChatMerge Skill Page](https://clawhub.ai/yaomo-1225/chatmerge) <br>
- [Input Contract](artifact/references/input-contract.md) <br>
- [Config Schema](artifact/references/config-schema.md) <br>
- [Output Examples](artifact/references/output-examples.md) <br>
- [Quickstart](artifact/QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown by default, with optional JSON structures, configuration snippets, and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include summaries, decisions, action items, risks, follow-up questions, role-specific views, and automation configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
