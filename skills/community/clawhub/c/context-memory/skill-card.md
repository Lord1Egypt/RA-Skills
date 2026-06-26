## Description: <br>
解决AI记忆混乱问题——"今天讲明天忘"。通过文件系统和规则流程实现持久记忆，确保新任务开始时自动回顾上下文，而不是靠"想"。核心机制：任务开始判断→读取记忆→执行→保存。适用于频繁切换话题或任务的AI协作场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[long57777](https://clawhub.ai/user/long57777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to make an assistant persist useful workspace context, user preferences, task notes, and lessons learned in local markdown files so future sessions can reload relevant context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to persist local cross-session memory, which can retain sensitive or unnecessary personal details if used carelessly. <br>
Mitigation: Review memory files before sharing or committing a workspace, avoid storing secrets or unnecessary personal data, and tell the agent when information should remain ephemeral. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/long57777/context-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may guide the agent to create or update local memory files such as MEMORY.md, BOOTSTRAP.md, .learnings files, and dated logs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
