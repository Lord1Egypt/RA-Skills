## Description: <br>
Claw Taming guides an OpenClaw agent through user profiling, persona setup, memory structure, skill and channel planning, and heartbeat checks intended to reduce behavior drift. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejianjun000](https://clawhub.ai/user/xiejianjun000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and agent builders use this skill to onboard and tune an agent into a persistent persona with local profile, memory, and self-check files. It is most relevant when an agent needs consistent voice, structured memory, and routine drift or memory-pollution checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to create persistent persona, user profile, memory, and heartbeat files that may contain sensitive personal context. <br>
Mitigation: Review USER.md, SECRET.md, SOUL.md, HEARTBEAT.md, and .memory after creation; leave sensitive fields blank unless needed and do not store passwords or tokens. <br>
Risk: Skill expansion and channel integration guidance could lead an agent to add capabilities or connect channels beyond the user's intended scope. <br>
Mitigation: Manually approve any extra skills or channel integrations before installation or activation. <br>
Risk: Persona and memory templates can preserve incorrect, stale, or overly personal information if they are not maintained. <br>
Mitigation: Use the included heartbeat and memory-pollution checks to identify duplicate, contradictory, outdated, or persona-conflicting memory and request user confirmation before correction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejianjun000/claw-taming) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [HEARTBEAT_TEMPLATE.md](artifact/templates/HEARTBEAT_TEMPLATE.md) <br>
- [MEMORY_TEMPLATE.md](artifact/templates/MEMORY_TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance and Markdown file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill prompts the agent to create or maintain local persona, user profile, memory, and heartbeat review files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
