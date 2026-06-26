## Description: <br>
Orchestrates structured multi-agent debates with configurable roles, rounds, local archiving, and multi-voter scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[updatedb](https://clawhub.ai/user/updatedb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team facilitators use this skill to run structured debates in chat, configure participant roles and rounds, archive arguments, and collect votes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debate state, archives, logs, votes, and optional defaults are stored locally. <br>
Mitigation: Avoid confidential debate content unless local retention is acceptable, and clean up ~/.openclaw/debate-arena or configured state/archive paths when retention is no longer needed. <br>
Risk: Saved defaults can persist participant and account settings. <br>
Mitigation: Review settings before running debate conf, and remove default-config.json when defaults should no longer be reused. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/updatedb/debate-arena) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with chat commands and Node.js API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces debate orchestration instructions and local state-management guidance for agents.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
