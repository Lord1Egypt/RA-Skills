## Description: <br>
Agent Memory gives AI agents persistent local memory with tiered storage, correction learning, self-reflection, multi-agent sharing, and decay rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ironmanc2014](https://clawhub.ai/user/ironmanc2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to set up local persistent memory so an agent can remember explicit preferences, corrections, project patterns, and shared multi-agent knowledge over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-term local memory may retain user preferences, corrections, and work context beyond the current session. <br>
Mitigation: Review ~/agent-memory periodically, avoid storing sensitive personal or business data, and use the documented forget or wipe workflow when memory should be removed. <br>
Risk: Shared multi-agent memory files can spread overly broad or stale patterns across agents. <br>
Mitigation: Keep shared files narrowly scoped, prefer project or agent-specific entries when appropriate, and review conflicts before promoting patterns. <br>
Risk: Casual phrases could be encoded as approval patterns in workflows where approval has high impact. <br>
Mitigation: Require explicit confirmation for high-impact actions and do not treat ambiguous conversational signals as standing authorization. <br>


## Reference(s): <br>
- [Agent Memory release page](https://clawhub.ai/ironmanc2014/agent-memory-architect) <br>
- [Memory Architecture](references/architecture.md) <br>
- [Multi-Agent Memory](references/multi-agent.md) <br>
- [Security Boundaries](references/security.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and maintains local files under ~/agent-memory when the bootstrap script or setup instructions are used.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
