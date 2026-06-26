## Description: <br>
深度思考协议为 AI 助手提供系统性思考框架，用于复杂问题、多角度分析、深入推理和高价值决策。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hejng](https://clawhub.ai/user/hejng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other agent users apply this skill when they want an AI assistant to reason through complex technical, strategic, design, debugging, or multi-stakeholder questions with explicit hypothesis testing, validation, and synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or confidential context could appear in visible reasoning or in an optional local thinking report. <br>
Mitigation: Avoid using the skill with secrets, private personal data, confidential business plans, or production credentials unless that exposure is acceptable. <br>
Risk: Suggested shell, web, memory, or file access could act on sensitive user context if followed without review. <br>
Mitigation: Keep external access and command execution under explicit user control and review suggested actions before running them. <br>


## Reference(s): <br>
- [深度思考协议 - 示例](references/examples.md) <br>
- [深度思考协议 - 快速参考](references/quick-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code] <br>
**Output Format:** [Markdown guidance with optional interactive shell-script output and JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate a local thinking report when the optional checklist script is run and the user chooses to save it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
