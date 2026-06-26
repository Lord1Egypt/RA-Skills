## Description: <br>
Agent memory persistence and state backup for saving and restoring an AI agent's memory, identity, and state through the Ensoul Network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suitandclaw](https://clawhub.ai/user/suitandclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create a persistent agent identity, register it on the Ensoul Network, and sync hashed memory or state proofs for recovery across machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a persistent blockchain identity and permanent registration for an agent. <br>
Mitigation: Install only when persistent identity is intended, confirm registration with the user, and decide how unwanted registration will be handled before use. <br>
Risk: The skill can repeatedly sync broad agent memory or configuration state, including files such as SOUL.md and MEMORY.md. <br>
Mitigation: Review exactly which files are included, remove secrets and sensitive prompts, and verify the SDK's raw-data versus hash-only behavior before syncing. <br>
Risk: The local identity file can contain a secret seed. <br>
Mitigation: Protect ~/.ensoul/agent-identity.json, keep restrictive file permissions, and never display, log, or transmit the seed. <br>
Risk: Background sync behavior or unwanted permanent registration may be difficult to reverse. <br>
Mitigation: Confirm how to disable background sync and recover from unwanted registration before deploying the skill. <br>


## Reference(s): <br>
- [Ensoul homepage](https://ensoul.dev) <br>
- [Ensoul Explorer](https://explorer.ensoul.dev) <br>
- [@ensoul-network/sdk on npm](https://www.npmjs.com/package/@ensoul-network/sdk) <br>
- [Ensoul Network status](https://status.ensoul.dev) <br>
- [ClawHub skill page](https://clawhub.ai/suitandclaw/agent-memory-backup-ensoul) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or use ~/.ensoul/agent-identity.json and make network calls to Ensoul services when the agent follows the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
