## Description: <br>
Logs and organizes learnings, errors, and feature requests for continuous improvement, integrating with OpenClaw workspace for knowledge management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PEDROHENRIQUE202525](https://clawhub.ai/user/PEDROHENRIQUE202525) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, failures, missing capabilities, and recurring best practices as structured Markdown notes that can be reviewed or promoted into project memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs may preserve conversation-derived information across future sessions. <br>
Mitigation: Restrict where the skill may write and avoid logging secrets, raw transcripts, or sensitive user data. <br>
Risk: Promoted notes could introduce incorrect, unsafe, or overly broad guidance into agent memory files. <br>
Mitigation: Require review and approval before promoting entries into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md, or Copilot instructions. <br>
Risk: Optional hooks or external setup steps may execute repository-provided scripts. <br>
Mitigation: Review external repositories and hook scripts before enabling them. <br>


## Reference(s): <br>
- [Agente Conhecimento on ClawHub](https://clawhub.ai/PEDROHENRIQUE202525/agente-conhecimento) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured learning, error, and feature-request entries intended for persistent review; avoid recording secrets or raw transcripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
