## Description: <br>
Agent Retro helps an agent run a daily retrospective by reading a target day's session history, summarizing successes, mistakes, improvement points, user profile, and agent profile, then updating memory and configuration files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tangc](https://clawhub.ai/user/Tangc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent operators and developers use this skill to review a specific day's OpenClaw agent sessions, capture lessons learned, and update memory and behavior files. It is intended for retrospective analysis when a user asks the agent to review recent performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private local OpenClaw session history. <br>
Mitigation: Run it only for an explicit date and agent ID, and limit access to workspaces where reviewing those sessions is appropriate. <br>
Risk: The skill can change long-lived memory and agent instruction files such as USER.md, SOUL.md, AGENTS.md, and MEMORY.md. <br>
Mitigation: Ask for a dry run or diff first, then manually approve changes before allowing persistent updates. <br>


## Reference(s): <br>
- [Agent Retro on ClawHub](https://clawhub.ai/Tangc/agent-retro) <br>
- [Publisher profile: Tangc](https://clawhub.ai/user/Tangc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration] <br>
**Output Format:** [Markdown summaries, persistent memory files, configuration edits, and a concise retrospective report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local session history and writes daily memory, lock, and core configuration files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
