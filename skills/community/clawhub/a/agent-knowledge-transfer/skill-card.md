## Description: <br>
Complete knowledge transfer protocol for transforming process-only agents into proper agents with full identity, skills, memory, and context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefanferreira](https://clawhub.ai/user/stefanferreira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to prepare or migrate OpenClaw agents by transferring identity, user context, system knowledge, memory, skills documentation, and required tool access before activation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy private user context and memory into persistent agent workspaces. <br>
Mitigation: Review and redact USER.md, MEMORY.md, AGENTS.md, TOOLS.md, HEARTBEAT.md, and memory logs before transfer. <br>
Risk: Bulk transfer can give multiple agents the same context without each agent being approved to receive it. <br>
Mitigation: Avoid --all unless every target agent is approved for the same context. <br>
Risk: Transferred tool access can exceed what a target agent needs. <br>
Mitigation: Restrict each agent's tools to the minimum needed for its role. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stefanferreira/agent-knowledge-transfer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, and checklist examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes procedural checklists, verification questions, and example workspace file structures.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
