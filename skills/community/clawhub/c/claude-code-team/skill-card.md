## Description: <br>
Claude Code Team mode automatically assigns team tasks, detects the active model platform, selects role-specific models across Bailian, Volcengine, or OpenAI, and starts teams for project-related requests while answering everyday questions directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to coordinate multi-agent teams for software development, architecture, testing, operations, documentation, and custom role-based project work. It is intended for project tasks that benefit from multiple specialized agents and model routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can auto-launch multiple agents for broad project prompts, which can create unexpected tool activity and model/API cost. <br>
Mitigation: Require explicit confirmation before spawning agents and monitor model usage during team-mode runs. <br>
Risk: The skill persists team and agent memory, which can retain sensitive task context if users include secrets or regulated data. <br>
Mitigation: Avoid sending secrets or regulated data and inspect or clear generated memory files after use. <br>
Risk: The security verdict is suspicious because broad team-mode automation and retention controls are not clearly constrained. <br>
Mitigation: Review the skill before deployment, restrict it to intended project workflows, and keep human oversight on generated plans and changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidme6/claude-code-team) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Team configuration](artifact/teams.json) <br>
- [Platform auto-detect notes](artifact/PLATFORM_AUTO_DETECT.md) <br>
- [Gateway fix notes](artifact/GATEWAY_FIX.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with optional code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May spawn multiple agents, summarize their results, and persist task memory when used in a compatible OpenClaw environment.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
