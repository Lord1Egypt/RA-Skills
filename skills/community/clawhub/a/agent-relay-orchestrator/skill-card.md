## Description: <br>
Multi-worker orchestration for Claude Code with Notion visibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theagentacademy](https://clawhub.ai/user/theagentacademy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to start and operate a local relay for spawning, messaging, suspending, resuming, and monitoring multiple Claude Code worker sessions with Notion-backed visibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local relay can control persistent Claude Code worker sessions through an HTTP API. <br>
Mitigation: Keep the service bound to localhost, restrict machine access, and review worker actions before relying on results. <br>
Risk: Operational data may be sent to Notion and optionally Telegram. <br>
Mitigation: Protect the Notion token, disable Telegram unless needed, and avoid sending secrets through worker messages. <br>
Risk: Persistent sessions can retain sensitive context across restarts. <br>
Mitigation: Periodically inspect stored sessions and purge worker state when the retained context is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/theagentacademy/agent-relay-orchestrator) <br>
- [Agent Relay Orchestrator Homepage](https://github.com/TheAgentAcademy/agent-relay-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Assumes a local relay service, Node.js, Claude Code, and Notion credentials are configured before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
