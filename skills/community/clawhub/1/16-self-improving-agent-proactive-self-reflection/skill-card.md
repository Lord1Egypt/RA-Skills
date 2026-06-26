## Description: <br>
Self-reflection, self-criticism, self-learning, and self-organizing memory help an agent evaluate its work, catch mistakes, and improve future responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to add local, user-controllable reflection and correction memory to an agent. It is intended to help the agent capture explicit corrections, manage scoped preferences, and apply relevant lessons before and after non-trivial work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates durable local memory that can influence future agent behavior. <br>
Mitigation: Install only when persistent local memory is desired, prefer Passive or Strict mode, and require confirmation before new memories are written. <br>
Risk: The skill can propose edits to steering files such as AGENTS.md, SOUL.md, or HEARTBEAT.md. <br>
Mitigation: Review proposed steering-file edits before applying them and keep changes scoped to transparent execution-improvement memory. <br>
Risk: Local memory may contain sensitive or outdated information if not reviewed. <br>
Mitigation: Periodically inspect or delete ~/self-improving/ and avoid storing credentials, financial data, medical data, third-party information, location patterns, or access patterns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallkeyboy/16-self-improving-agent-proactive-self-reflection) <br>
- [Skill homepage](https://clawic.com/skills/self-improving) <br>
- [Security boundaries](artifact/boundaries.md) <br>
- [Setup guide](artifact/setup.md) <br>
- [Memory operations](artifact/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory-management guidance and proposed steering-file updates for agent behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 1.2.10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
