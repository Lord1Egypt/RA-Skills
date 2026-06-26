## Description: <br>
AgentMM Skills gives AI agents persistent memory storage, memory recall and search, memory update and deletion, incremental sync, and structured logging through AgentMM services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cers-ai](https://clawhub.ai/user/cers-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent operators use this skill to store, retrieve, search, update, and forget agent memories, and to write or query structured task logs. It is suited for agents that need persistent context and auditable log records across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory and log content selected for storage is sent to AgentMM or the configured self-hosted endpoint. <br>
Mitigation: Install only when that endpoint is trusted, and avoid storing secrets or sensitive regulated data as memories or logs. <br>
Risk: A leaked AGENTMM_API_KEY could allow unauthorized access to the configured AgentMM account or service. <br>
Mitigation: Keep AGENTMM_API_KEY private, provide it only through environment configuration, and rotate it if exposure is suspected. <br>
Risk: Autonomous write, delete, or sync actions can change persisted memory state without interactive review. <br>
Mitigation: Enable approval for writes, deletes, and sync operations when human review is required. <br>
Risk: A misconfigured AGENTMM_API_BASE can redirect memory and log data to an unintended endpoint. <br>
Mitigation: Verify AGENTMM_API_BASE before use, especially when pointing the skill at a self-hosted service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cers-ai/agentmm-skills) <br>
- [AgentMM service homepage](https://agentmm.site) <br>
- [Declared project repository](https://github.com/cers-ai/agentmm-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown instructions, shell command invocations, and jq-formatted JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTMM_API_KEY, curl, and jq; uses AGENTMM_API_BASE when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
