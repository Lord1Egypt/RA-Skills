## Description: <br>
Build a more reliable OpenClaw agent with battle-tested architecture patterns. Covers WAL protocol, working buffer, memory anti-poisoning, layered memory compression, cron design, selective skill integration, and heartbeat batching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zihaofeng2001](https://clawhub.ai/user/zihaofeng2001) <br>

### License/Terms of Use: <br>
CC BY-SA 4.0 <br>


## Use Case: <br>
Developers and agent builders use this skill as architecture guidance for making OpenClaw agents more reliable through memory, cron, delivery, retrieval, and operational patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad, long-lived memory logging can retain secrets or sensitive personal data. <br>
Mitigation: Define what may be saved, exclude secrets and sensitive personal data, set deletion and retention rules, and review memory files periodically. <br>
Risk: Remote memory indexing can send indexed memory to external embedding providers. <br>
Mitigation: Prefer local embeddings or require explicit approval before using remote providers for indexed memory. <br>
Risk: Architecture recommendations may be adopted as automatic policy without review. <br>
Mitigation: Treat the skill as guidance and review each pattern against the agent's privacy, reliability, and operational requirements before adoption. <br>


## Reference(s): <br>
- [Agent Architecture Guide on ClawHub](https://clawhub.ai/zihaofeng2001/agent-architecture-guide) <br>
- [Companion Agent Health Optimizer skill](https://clawhub.ai/zihaofeng2001/agent-health-optimizer) <br>
- [Proactive Agent source pattern reference](https://clawhub.ai/halthelobster/proactive-agent) <br>
- [Self Improving Agent credit reference](https://clawhub.ai/pskoett/self-improving-agent) <br>
- [ClawHub skill API example](https://clawhub.ai/api/v1/skills/SLUG) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, tables, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only architecture guidance; no executable scripts are bundled.] <br>

## Skill Version(s): <br>
4.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
