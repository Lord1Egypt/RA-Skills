## Description: <br>
Double-Check-It Skill helps agents verify deliverables against user requirements and execution plans while recording task memory and review lessons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webray1983](https://clawhub.ai/user/webray1983) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to add plan confirmation, delivery verification, user-triggered double checks, and local task memory workflows to ClawHub/OpenClaw-style agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent local records of conversations, task details, and inferred lessons. <br>
Mitigation: Install only when persistent local memory is intended, and define where memory is stored, reviewed, and deleted before use. <br>
Risk: Automatic recording or idle reflection may capture sensitive, personal, credential-related, or business-confidential task details. <br>
Mitigation: Disable or avoid automatic recording and idle reflection for sensitive work, and review memory files before retaining or sharing them. <br>
Risk: The bundled helper script writes memory data to a fixed local workspace path unless changed. <br>
Mitigation: Review and adjust the memory directory configuration before running the script in a new environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/webray1983/double-check-skill) <br>
- [Publisher profile](https://clawhub.ai/user/webray1983) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [memory.sh](artifact/scripts/memory.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and a Bash helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent local Markdown and JSON memory files under the configured memory directory when helper commands are used.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
