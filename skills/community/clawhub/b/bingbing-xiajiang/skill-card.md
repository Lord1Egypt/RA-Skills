## Description: <br>
蜂兵虾将 is a Chinese-language multi-agent skill for cross-industry hotspot monitoring, content strategy, trend insight, workflow recording, and adaptive memory-assisted execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[e2e5g](https://clawhub.ai/user/e2e5g) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Content teams, operators, and individual creators use this skill to monitor industry topics, rank useful signals, turn trends into publishing plans, inspect personal or workflow status, and generate reusable workflow records. It is designed for Chinese-language workflows that combine multi-agent prompts, local memory, and JavaScript demonstration utilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist long-lived user profile, goal, value, and behavior data in its memory system. <br>
Mitigation: Review the memory directory and retention behavior before deployment, and avoid entering sensitive personal or business data unless persistent profiling is acceptable. <br>
Risk: Adaptive confirmation reduction could reduce human review for high-impact tasks. <br>
Mitigation: Keep explicit human confirmation enabled for consequential decisions and review generated recommendations before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/e2e5g/bingbing-xiajiang) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Agent prompts](AGENT_PROMPTS.md) <br>
- [Complete workflow design](references/workflow-design.md) <br>
- [Module data flow](references/data-flow.md) <br>
- [Complete usage manual](docs/AI协作操作系统_完整使用说明书.md) <br>
- [Deployment guide](docs/集中部署指南.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured text with optional JavaScript examples, shell commands, and JSON-like workflow or memory data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include hotspot reports, content plans, trend and status analysis, workflow templates, memory summaries, and execution recommendations.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata; artifact package.json declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
