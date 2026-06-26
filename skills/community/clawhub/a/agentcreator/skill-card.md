## Description: <br>
Agent Creator guides an agent through generating independent OpenClaw agent workspaces with core and optional files, review gates, Git initialization, and TEAM.md registration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovesunshine0](https://clawhub.ai/user/lovesunshine0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create new domain-specific agents with standardized Markdown files, optional configuration templates, validation steps, and registration metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and register new agents by writing to the OpenClaw workspace and TEAM.md. <br>
Mitigation: Review generated files and require explicit user confirmation before deployment. <br>
Risk: The OPENCLAWS_AUTO_CONFIRM setting can bypass review gates. <br>
Mitigation: Keep OPENCLAWS_AUTO_CONFIRM unset outside controlled testing. <br>
Risk: The skill may persist learned failure patterns or memory-like summaries. <br>
Mitigation: Require persistence behavior to be visible, opt-in, and easy to clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lovesunshine0/agentcreator) <br>
- [Publisher profile](https://clawhub.ai/user/lovesunshine0) <br>
- [Artifact: SKILL.md](artifact/SKILL.md) <br>
- [Artifact: SKILL_METADATA.md](artifact/ext/SKILL_METADATA.md) <br>
- [Artifact: SKILL_DYNAMIC_FILES.md](artifact/ext/SKILL_DYNAMIC_FILES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, inline shell command plans, and configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create workspace files, Git metadata, TEAM.md entries, pending-confirmation files, and summarized failure-pattern records when executed by an agent with the required permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
