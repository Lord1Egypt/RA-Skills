## Description: <br>
AI自我改进与记忆系统 - 让AI从错误中学习，越用越聪明 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AndyLue](https://clawhub.ai/user/AndyLue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent memory routines that record errors, user corrections, best practices, and knowledge gaps so future agent work can check and apply prior context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory may capture broad user, command, project, or error context in long-lived local files. <br>
Mitigation: Use the skill only when persistent memory is intended, avoid it around secrets or sensitive project output, and review ~/.openclaw/memory/self-improving regularly. <br>
Risk: Project-level syncing could write memory-derived content into CLAUDE.md or AGENTS.md. <br>
Mitigation: Require explicit review before allowing any memory entry to be copied into project instruction files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AndyLue/ai-self-learning) <br>
- [Publisher Profile](https://clawhub.ai/user/AndyLue) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSONL memory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists memory entries and an index under the user's local OpenClaw memory directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact skill metadata declares 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
