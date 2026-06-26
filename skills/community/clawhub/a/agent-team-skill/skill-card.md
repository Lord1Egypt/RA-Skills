## Description: <br>
Manage AI agent team members with roles, skills, and task delegation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realqiyan](https://clawhub.ai/user/realqiyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain local team-member records, identify relevant expertise, set a single team leader, and support task delegation in OpenClaw-based multi-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local team records may influence leader-agent behavior if they contain inaccurate, stale, or instruction-like content. <br>
Mitigation: Keep ~/.agent-team/team.json factual and non-sensitive, and review team fields before enabling the OpenClaw plugin. <br>
Risk: The reset command clears the skill's local team data file. <br>
Mitigation: Back up or inspect the configured team data file before running reset, especially when using a custom data path. <br>
Risk: Automatic context injection may continue after the user no longer wants team data applied. <br>
Mitigation: Disable the plugin or reset the team file when team context should no longer guide the agent. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/realqiyan/agent-team-skill) <br>
- [Project Homepage](https://github.com/realqiyan/agent-team-skill) <br>
- [OpenClaw Plugin Installation Guide](https://github.com/realqiyan/agent-team-skill/blob/master/integrations/openclaw/agent-team/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON-backed local state, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and OpenClaw plugin installation; stores team data in a local JSON file by default.] <br>

## Skill Version(s): <br>
2.1.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
