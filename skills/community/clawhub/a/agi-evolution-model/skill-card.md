## Description: <br>
基于双环架构的AGI进化模型，通过意向性分析、人格层映射、元认知检测和错误智慧库实现持续自我演进；当用户需要智能对话、人格定制、复杂问题求解或从错误中学习时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiwifruit13](https://clawhub.ai/user/kiwifruit13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill as a conversational AGI-style companion framework for personalized dialogue, personality customization, complex problem solving, metacognitive checks, and learning from prior errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags broad local file, process, system-information, and shell-command powers without tight safeguards. <br>
Mitigation: Use only in a sandbox or disposable workspace, keep secrets and important files out of reach, and enable command, file, or process tools only when that host-level access is intentional. <br>
Risk: Release metadata and packaged documentation disagree on the license. <br>
Mitigation: Confirm the applicable license before deployment or redistribution and align the release metadata with the packaged documentation. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/kiwifruit13/agi-evolution-model) <br>
- [AGI进化模型架构详解](references/architecture.md) <br>
- [AGI进化模型能力边界说明](references/capability_boundaries.md) <br>
- [CLI工具箱完整指南](references/cli-tools-guide.md) <br>
- [错误智慧库规范](references/error_wisdom_spec.md) <br>
- [智能体响应规则](references/intelligence-agent-response-rules.md) <br>
- [人格初始化参数映射对照表](references/personality_mapping.md) <br>
- [Tool Use 接口设计规范](references/tool_use_spec.md) <br>
- [使用示例](references/usage-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python script invocations, and generated local configuration or memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local AGI memory, personality, history, and error-wisdom files when its scripts are used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
