## Description: <br>
智能模型路由 - 根据任务是否需要工具调用自动选择模型。需要工具(搜索/浏览器/文件/天气/股票等)使用百炼付费模型，纯聊天使用OpenRouter免费模型。V3.1.0新增route_by_tool_required()函数。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cmz666666](https://clawhub.ai/user/cmz666666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to reduce token usage and model spend by routing tasks, recommending leaner context bundles, optimizing heartbeat intervals, and tracking budget usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is broader than a simple model router and can write persistent OpenClaw workspace state or agent-guidance files. <br>
Mitigation: Review generated AGENTS and HEARTBEAT files before adopting them, and avoid running overwrite-style helper commands casually. <br>
Risk: Local usage metadata may be stored under ~/.openclaw/workspace/memory. <br>
Mitigation: Use the skill only where local budget and usage state is acceptable, and review workspace memory files according to local data-handling policy. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/cmz666666/cmz-token-optimizer) <br>
- [ClawDIS homepage](https://github.com/Asif2BD/OpenClaw-Token-Optimizer) <br>
- [README](artifact/README.md) <br>
- [Security documentation](artifact/SECURITY.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-style script outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some helper flows can generate local agent guidance files or store local usage metadata under the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
