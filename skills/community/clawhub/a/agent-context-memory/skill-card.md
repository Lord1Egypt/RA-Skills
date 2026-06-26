## Description: <br>
Agent 上下文管理方法论：通过分层文件体系实现跨-session 记忆延续、职责分离和高效上下文恢复。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[349840432m-dev](https://clawhub.ai/user/349840432m-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up layered local context files, startup protocols, and memory maintenance routines for agents that need continuity across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory files may accumulate secrets, API tokens, session cookies, private personal data, regulated data, or confidential business material. <br>
Mitigation: Do not store sensitive material in SOUL.md, USER.md, TOOLS.md, MEMORY.md, or memory/ files; review entries before retaining them long term. <br>
Risk: The distillation script can append extracted lessons to MEMORY.md and record processed daily files. <br>
Mitigation: Run the script with --dry-run first, review the proposed additions, and enable cron or heartbeat maintenance only deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/349840432m-dev/agent-context-memory) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [claw.json](artifact/claw.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file templates, command examples, and Python utility code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory-management structures and optional distillation workflow guidance; no external API calls are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
