## Description: <br>
Meta-agent skill for orchestrating complex tasks through autonomous sub-agents by decomposing work, spawning specialized agents, coordinating file-based communication, and consolidating results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to break complex work into parallel sub-agent tasks, define per-agent workspaces and handoffs, monitor completion, and merge the resulting deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous multi-agent delegation can grant spawned agents broad file, command, and third-party API capabilities. <br>
Mitigation: Use a dedicated workspace, review generated sub-agent instructions before dispatch, and set explicit limits on tools, paths, runtime, and agent count. <br>
Risk: Sub-agents may send sensitive task data to a third-party AI service when SKILLBOSS_API_KEY is provided. <br>
Mitigation: Provide the API key and sensitive inputs only when third-party processing by SkillBoss is acceptable for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abel-agent-orchestrator) <br>
- [File-Based Communication Protocol](references/communication-protocol.md) <br>
- [Sub-Agent Templates](references/sub-agent-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks, JSON snippets, file paths, and task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce generated SKILL.md content, inbox/outbox workspace layouts, status.json conventions, and final consolidation summaries; AI-backed sub-agents require SKILLBOSS_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
