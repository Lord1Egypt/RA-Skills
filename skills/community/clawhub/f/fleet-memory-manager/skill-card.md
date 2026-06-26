## Description: <br>
Upgrade your agent's memory from basic notes to a 3-layer production system with nightly consolidation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vswarm-ai](https://clawhub.ai/user/vswarm-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up persistent, layered memory for AI agents across sessions. It provides templates and setup guidance for long-term memory, daily operational notes, user preferences, heartbeat checks, and nightly consolidation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files can accumulate personal or sensitive context and may be reused in shared or automated contexts. <br>
Mitigation: Use the skill only in a trusted private workspace, keep MEMORY.md out of group or shared sessions, and require explicit opt-in before loading USER.md outside private sessions. <br>
Risk: Markdown memory files may be used to store secrets or other data that should not persist in agent-readable files. <br>
Mitigation: Do not store credentials, tokens, private keys, or other secrets in MEMORY.md, USER.md, daily notes, or heartbeat configuration. <br>
Risk: Nightly consolidation can promote inaccurate, stale, or overly personal observations into long-term memory. <br>
Mitigation: Review consolidation output before it writes long-term memories, keep MEMORY.md curated, and prune stale or unnecessary personal details. <br>
Risk: Heartbeat checks for email, calendar, and weather can broaden the agent's access to personal services. <br>
Mitigation: Disable those checks unless they are intentionally configured, scoped, and useful for the deployment. <br>


## Reference(s): <br>
- [Fleet Memory Manager on ClawHub](https://clawhub.ai/vswarm-ai/fleet-memory-manager) <br>
- [Publisher profile](https://clawhub.ai/user/vswarm-ai) <br>
- [Bot Fleet Playbook](https://github.com/sentien-labs/bot-fleet-playbook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown templates, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates workspace memory files and recommends cron and heartbeat configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
