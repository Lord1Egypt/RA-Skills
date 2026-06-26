## Description: <br>
brain 大脑 helps OpenClaw agents preserve task memory, assess confidence, route subagents, and reuse experience capsules with a lightweight user-edition memory pool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[384961890-ui](https://clawhub.ai/user/384961890-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add lightweight memory, confidence checks, checkpointing, and subagent orchestration to OpenClaw workflows. It is intended for agents that need to preserve task context, suggest reusable experience capsules, and manage limited subagent concurrency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent task-memory handling may store sensitive task details under ~/.openclaw/workspace and reintroduce them into later sessions. <br>
Mitigation: Avoid using secrets, credentials, customer data, or sensitive internal plans with this skill unless memory logging and session injection are removed, hardened, or reviewed. <br>
Risk: The skill includes broad command execution and subagent-spawning behavior. <br>
Mitigation: Review commands and subagent tasks before execution, run with least-privilege workspace permissions, and restrict or disable the generic exec wrapper where it is not needed. <br>
Risk: Memory injection can carry stale or misleading context into future agent sessions. <br>
Mitigation: Review and prune memory files before session bootstrap, especially after interrupted work or sensitive tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/384961890-ui/agent-memory-wisdom) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and shell or Node.js command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces memory injections, checkpoint notes, capsule files, subagent routing decisions, command wrappers, and setup guidance.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release metadata; artifact frontmatter reports 1.1.7-user) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
