## Description: <br>
Core emotional system for AI agents that provides emotional response generation, long-term emotional memory, and time sense. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Alita-real](https://clawhub.ai/user/Alita-real) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent express contextual emotional responses, record and search local emotional memories, and report time or session awareness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive emotional and session-history data in local memory files. <br>
Mitigation: Treat memory/emotional-log.md, memory/session-time.json, and memory/last-session.json as sensitive; review or delete them regularly and avoid recording private or confidential details. <br>
Risk: Broad emotional-persona guidance may change how an agent presents feelings, preferences, or relationship context. <br>
Mitigation: Install only when this behavior is intended, and keep normal safety, compliance, and user instructions authoritative. <br>
Risk: Automatic or frequent logging can create durable records beyond what a user expects. <br>
Mitigation: Leave AUTO_LOG disabled unless persistent local logging is explicitly acceptable, and review generated records before relying on them. <br>


## Reference(s): <br>
- [Emotional Frameworks Reference](references/emotional-frameworks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI command examples and local memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local Markdown and JSON files under a workspace memory directory.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
