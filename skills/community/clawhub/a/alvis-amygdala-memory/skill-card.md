## Description: <br>
Emotional processing layer for AI agents with persistent emotional states that can influence future behavior and responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to give an OpenClaw-style agent a persistent emotional state, track emotional dimensions over time, and optionally encode conversation history into that state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent emotional state can influence future sessions and responses. <br>
Mitigation: Review or delete AMYGDALA_STATE.md, emotional-state.json, and brain-events.jsonl when persistent emotional context should not affect future work. <br>
Risk: Automatic encoding may process conversation history through SkillBoss on a schedule. <br>
Mitigation: Enable cron or automatic encoding only after reviewing the behavior and use a dedicated, revocable SkillBoss_API_KEY. <br>
Risk: The evidence package references runtime scripts that are not included in the artifact. <br>
Mitigation: Inspect the source scripts before running install, cron, or encoding commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis-amygdala-memory) <br>
- [Publisher profile](https://clawhub.ai/user/alvisdunlop) <br>
- [OpenClaw metadata repository](https://github.com/ImpKind/amygdala-memory) <br>
- [Related hippocampus skill](https://www.clawhub.ai/skills/hippocampus) <br>
- [Related VTA memory skill](https://www.clawhub.ai/skills/vta-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON state examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq, awk, and SkillBoss_API_KEY when automatic emotional encoding is enabled.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
