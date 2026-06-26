## Description: <br>
Agent Memory Patterns provides implementation guidance for persistent agent memory using daily logs, curated long-term memory, grep-based search, queued external content review, scheduled maintenance, and heartbeat checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Byron-McKeeby](https://clawhub.ai/user/Byron-McKeeby) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to design workspace-based memory systems for long-running agents, including daily notes, long-term curated memory, searchable logs, external-content review queues, scheduled maintenance, and memory health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example scripts write persistent local memory files that may accumulate secrets, sensitive personal data, or stale context. <br>
Mitigation: Review paths and content before use, avoid storing secrets or sensitive personal data, and periodically prune or archive stale memories. <br>
Risk: External content queued into memory may be inaccurate or untrusted before review. <br>
Mitigation: Use the pending-memory review steps to verify source reliability, consistency with existing memory, value, and classification before promoting content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Byron-McKeeby/agent-memory-patterns) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only examples for local workspace memory files and maintenance schedules.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
